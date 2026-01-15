"""
On-chain Whale Tracker - Real Integration

Monitors on-chain transfers for large movements (exchange deposits/withdrawals)
using Etherscan, Covalent, and Alchemy providers with fallback chain.

Publishes `whale.onchain.detected` for transfers >= threshold.
"""
from __future__ import annotations

import logging
import time
import threading
from typing import Any, Dict, List, Optional, Set
from collections import deque

from aureon_thought_bus import get_thought_bus, Thought

logger = logging.getLogger(__name__)

# Try to import onchain providers
try:
    from onchain_providers import (
        get_provider_manager, 
        TransferEvent, 
        TransferDirection,
        KNOWN_EXCHANGE_ADDRESSES,
        EXCHANGE_ADDRESS_TO_NAME
    )
    PROVIDERS_AVAILABLE = True
except ImportError:
    PROVIDERS_AVAILABLE = False
    logger.warning("onchain_providers not available; falling back to stub mode")


class WhaleOnchainTracker:
    def __init__(
        self, 
        watch_addresses: Optional[List[str]] = None, 
        threshold_usd: float = 100_000.0,
        poll_interval_seconds: float = 60.0,
        eth_price_usd: float = 3000.0  # Fallback ETH price if no oracle
    ):
        self.thought_bus = get_thought_bus()
        self.watch_addresses: Set[str] = set(watch_addresses or [])
        self.threshold_usd = float(threshold_usd)
        self.poll_interval = poll_interval_seconds
        self.eth_price_usd = eth_price_usd
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._seen_txs: deque = deque(maxlen=1000)  # Track recent txs to avoid duplicates
        
        # Add known exchange addresses to watchlist
        if PROVIDERS_AVAILABLE:
            for addr in KNOWN_EXCHANGE_ADDRESSES.keys():
                self.watch_addresses.add(addr.lower())
            logger.info(f"Added {len(KNOWN_EXCHANGE_ADDRESSES)} exchange addresses to watchlist")

    def start(self):
        """Start background polling thread"""
        if not PROVIDERS_AVAILABLE:
            logger.warning("On-chain providers not available; tracker running in stub mode")
            return
        
        if self._running:
            logger.debug("WhaleOnchainTracker already running")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._polling_loop, daemon=True)
        self._thread.start()
        logger.info(f'WhaleOnchainTracker started; watching {len(self.watch_addresses)} addresses, threshold=${self.threshold_usd:,.0f}')
    
    def stop(self):
        """Stop polling thread"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("WhaleOnchainTracker stopped")
    
    def _polling_loop(self):
        """Background polling for new transfers"""
        provider_manager = get_provider_manager()
        
        while self._running:
            try:
                # Poll each watched address
                for address in list(self.watch_addresses)[:10]:  # Limit to 10 to avoid rate limits
                    if not self._running:
                        break
                    
                    try:
                        transfers = provider_manager.get_recent_transfers(address, limit=20)
                        for event in transfers:
                            self._process_transfer(event, provider_manager)
                    except Exception as e:
                        logger.debug(f"Error polling {address}: {e}")
                        continue
                
                # Sleep between poll cycles
                time.sleep(self.poll_interval)
                
            except Exception as e:
                logger.error(f"Polling loop error: {e}", exc_info=True)
                time.sleep(10)
    
    def _process_transfer(self, event: TransferEvent, provider_manager):
        """Process single transfer event"""
        # Skip if already seen
        if event.tx_hash in self._seen_txs:
            return
        self._seen_txs.append(event.tx_hash)
        
        # Classify transfer direction
        provider_manager.classify_transfer(event)
        
        # Estimate USD value if not set
        if event.amount_usd == 0.0:
            if event.token_symbol == 'ETH':
                event.amount_usd = event.amount * self.eth_price_usd
            # TODO: Add price oracle lookup for other tokens
        
        # Check threshold
        if event.amount_usd < self.threshold_usd:
            return
        
        # Publish to thought bus
        payload = {
            'tx_hash': event.tx_hash,
            'block_number': event.block_number,
            'timestamp': event.timestamp,
            'from': event.from_address,
            'to': event.to_address,
            'amount': event.amount,
            'amount_usd': event.amount_usd,
            'symbol': event.token_symbol,
            'token_address': event.token_address,
            'direction': event.direction.value,
            'exchange_name': event.exchange_name,
            'detected_at': time.time()
        }
        
        th = Thought(source='whale_onchain_tracker', topic='whale.onchain.detected', payload=payload)
        try:
            self.thought_bus.publish(th)
            logger.info(f"🐋 Large {event.direction.value}: {event.token_symbol} ${event.amount_usd:,.0f} | {event.exchange_name or 'Unknown'} | {event.tx_hash[:10]}...")
        except Exception as e:
            logger.debug(f'Failed to publish whale.onchain.detected: {e}')
    
    def simulate_transfer(self, symbol: str, tx_hash: str, from_addr: str, to_addr: str, amount_usd: float) -> None:
        """Simulate detection of a large transfer (for tests)"""
        payload = {
            'symbol': symbol,
            'tx_hash': tx_hash,
            'from': from_addr,
            'to': to_addr,
            'amount_usd': float(amount_usd),
            'detected_at': time.time(),
            'direction': 'simulated',
            'exchange_name': None
        }
        if amount_usd >= self.threshold_usd:
            th = Thought(source='whale_onchain_tracker', topic='whale.onchain.detected', payload=payload)
            try:
                self.thought_bus.publish(th)
            except Exception:
                logger.debug('Failed to publish whale.onchain.detected')
            logger.info('Simulated large on-chain transfer detected: %s %s', symbol, amount_usd)


# Default instance
_default_onchain: Optional[WhaleOnchainTracker] = None
try:
    _default_onchain = WhaleOnchainTracker()
    _default_onchain.start()  # Auto-start background polling
except Exception as e:
    logger.debug(f"Failed to initialize default WhaleOnchainTracker: {e}")
    _default_onchain = None


def get_onchain_tracker() -> Optional[WhaleOnchainTracker]:
    """Get singleton instance"""
    return _default_onchain
