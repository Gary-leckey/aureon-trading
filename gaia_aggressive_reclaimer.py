#!/usr/bin/env python3
"""
🔥⚡ GAIA AGGRESSIVE RECLAIMER ⚡🔥
NO GATES. NO WAITING. JUST TAKE.

Based on the WORKING rotations from this chat:
- Buy SOL → Wait → Sell SOL → Buy BTC → Wait → Sell BTC → Repeat
- Any profit = TAKE IT
- Deploy ALL cash immediately
"""

import sys, os
os.environ['PYTHONUNBUFFERED'] = '1'

import time
import math
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.getcwd())

# Sacred Constants
PHI = (1 + math.sqrt(5)) / 2
SCHUMANN = 7.83

class AggressiveReclaimer:
    def __init__(self):
        print("🔥" * 40)
        print("   GAIA AGGRESSIVE RECLAIMER - TAKE EVERYTHING")
        print("🔥" * 40)
        
        from binance_client import BinanceClient
        from alpaca_client import AlpacaClient
        from kraken_client import KrakenClient
        
        self.binance = BinanceClient()
        self.alpaca = AlpacaClient()
        self.kraken = KrakenClient()
        
        self.trades = 0
        self.profit = 0.0
        
        # Track our entry prices PER ASSET
        self.entries = {}
        
        print("✅ BINANCE | ALPACA | KRAKEN - ALL CONNECTED")
        print()
        
    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}", flush=True)

    # ═══════════════════════════════════════════════════════════════
    # BINANCE - FAST EXECUTION
    # ═══════════════════════════════════════════════════════════════
    
    def binance_scan_and_trade(self):
        """Scan Binance positions - take any profit - deploy all cash"""
        try:
            # Check what we hold
            for asset in ['SOL', 'BTC', 'ETH', 'AVAX', 'DOGE', 'XRP']:
                bal = self.binance.get_free_balance(asset)
                if bal < 0.00001:
                    continue
                
                pair = f'{asset}USDC'
                t = self.binance.get_ticker_price(pair)
                if not t:
                    continue
                    
                price = float(t.get('price', 0))
                value = bal * price
                
                if value < 1:
                    continue
                
                # Get entry - if none, set it NOW
                key = f'bin_{asset}'
                if key not in self.entries:
                    self.entries[key] = price
                    self.log(f"📍 BINANCE {asset}: Entry set @ ${price:.4f}")
                    continue
                
                entry = self.entries[key]
                pnl_pct = (price - entry) / entry * 100
                
                # ANY PROFIT = SELL
                if pnl_pct > 0.01:  # Just 0.01% profit threshold
                    self.log(f"🔥 BINANCE SELL {asset}: ${value:.2f} ({pnl_pct:+.2f}%)")
                    
                    result = self.binance.place_market_order(pair, 'SELL', quantity=bal * 0.999)
                    
                    if result and ('orderId' in result or result.get('status') == 'FILLED'):
                        profit_usd = value * (pnl_pct / 100)
                        self.profit += profit_usd
                        self.trades += 1
                        self.log(f"   ✅ SOLD! +${profit_usd:.4f}")
                        
                        # Remove entry so we reset on next buy
                        del self.entries[key]
                        
                        time.sleep(0.3)
                        
                        # Immediately buy next best
                        self._binance_buy_best()
                    else:
                        self.log(f"   ⚠️ Sell failed: {result}")
                        
            # Deploy any idle USDC
            usdc = self.binance.get_free_balance('USDC')
            if usdc > 2:
                self._binance_buy_best()
                
        except Exception as e:
            self.log(f"⚠️ Binance error: {e}")
    
    def _binance_buy_best(self):
        """Buy the best momentum asset on Binance"""
        usdc = self.binance.get_free_balance('USDC')
        if usdc < 2:
            return
            
        # Find best momentum
        pairs = ['SOLUSDC', 'BTCUSDC', 'ETHUSDC', 'AVAXUSDC', 'DOGEUSDC']
        best_pair, best_mom = None, -999
        
        for pair in pairs:
            try:
                t = self.binance.get_24h_ticker(pair)
                mom = float(t.get('priceChangePercent', 0))
                if mom > best_mom:
                    best_pair, best_mom = pair, mom
            except:
                pass
        
        if best_pair:
            asset = best_pair.replace('USDC', '')
            self.log(f"📥 BINANCE BUY {asset}: ${usdc:.2f} ({best_mom:+.1f}%)")
            
            result = self.binance.place_market_order(best_pair, 'BUY', quote_qty=usdc * 0.98)
            
            if result and ('orderId' in result or result.get('status') == 'FILLED'):
                # Record entry price
                t = self.binance.get_ticker_price(best_pair)
                price = float(t.get('price', 0))
                self.entries[f'bin_{asset}'] = price
                self.log(f"   ✅ BOUGHT @ ${price:.4f}")
            else:
                self.log(f"   ⚠️ Buy failed: {result}")

    # ═══════════════════════════════════════════════════════════════
    # ALPACA - FAST EXECUTION
    # ═══════════════════════════════════════════════════════════════
    
    def alpaca_scan_and_trade(self):
        """Scan Alpaca - take profits - deploy cash"""
        try:
            positions = self.alpaca.get_positions()
            
            for pos in positions:
                sym = pos.get('symbol', '')
                qty = float(pos.get('qty', 0))
                entry = float(pos.get('avg_entry_price', 0))
                current = float(pos.get('current_price', 0))
                value = float(pos.get('market_value', 0))
                
                if value < 0.5:
                    continue
                
                pnl_pct = (current - entry) / entry * 100 if entry > 0 else 0
                
                # ANY PROFIT = SELL
                if pnl_pct > 0.01:
                    asset = sym.replace('USD', '').replace('/', '')
                    self.log(f"🔥 ALPACA SELL {asset}: ${value:.2f} ({pnl_pct:+.2f}%)")
                    
                    result = self.alpaca.place_order(sym, qty, 'sell', 'market', 'ioc')
                    
                    if result and result.get('status') in ['filled', 'accepted', 'new']:
                        profit_usd = value * (pnl_pct / 100)
                        self.profit += profit_usd
                        self.trades += 1
                        self.log(f"   ✅ SOLD! +${profit_usd:.4f}")
                        
                        time.sleep(0.5)
                        self._alpaca_buy_best()
                    else:
                        self.log(f"   ⚠️ Sell failed: {result}")
            
            # Deploy cash
            acc = self.alpaca.get_account()
            cash = float(acc.get('cash', 0))
            if cash > 2:
                self._alpaca_buy_best()
                
        except Exception as e:
            self.log(f"⚠️ Alpaca error: {e}")
    
    def _alpaca_buy_best(self):
        """Buy best on Alpaca"""
        try:
            acc = self.alpaca.get_account()
            cash = float(acc.get('cash', 0))
            if cash < 2:
                return
            
            # Use Binance momentum data
            pairs = ['SOLUSDC', 'BTCUSDC', 'ETHUSDC']
            best_asset, best_mom = None, -999
            
            for pair in pairs:
                try:
                    t = self.binance.get_24h_ticker(pair)
                    mom = float(t.get('priceChangePercent', 0))
                    if mom > best_mom:
                        best_asset = pair.replace('USDC', '')
                        best_mom = mom
                except:
                    pass
            
            if best_asset:
                alpaca_sym = f'{best_asset}/USD'
                self.log(f"📥 ALPACA BUY {best_asset}: ${cash:.2f} ({best_mom:+.1f}%)")
                
                # Get price and calc qty
                try:
                    quotes = self.alpaca.get_latest_crypto_quotes([alpaca_sym])
                    price = float(quotes[alpaca_sym].get('ap', 0))
                    qty = (cash * 0.95) / price
                    
                    result = self.alpaca.place_order(alpaca_sym, qty, 'buy', 'market', 'ioc')
                    if result:
                        self.log(f"   ✅ BOUGHT")
                except Exception as e:
                    self.log(f"   ⚠️ Buy error: {e}")
                    
        except Exception as e:
            self.log(f"⚠️ Alpaca buy error: {e}")

    # ═══════════════════════════════════════════════════════════════
    # KRAKEN - FAST EXECUTION
    # ═══════════════════════════════════════════════════════════════
    
    def kraken_scan_and_trade(self):
        """Scan Kraken - take profits - deploy USD"""
        try:
            acct = self.kraken.account()
            usd_bal = 0
            
            for bal in acct.get('balances', []):
                asset = bal.get('asset', '')
                free = float(bal.get('free', 0))
                
                if free <= 0:
                    continue
                
                # Track USD
                if asset in ['USD', 'USDC', 'ZUSD']:
                    usd_bal += free
                    continue
                
                if asset in ['USDT', 'EUR', 'ZEUR']:
                    continue
                
                # It's a crypto - check value
                pair = f'{asset}USD'
                try:
                    ticker = self.kraken.get_ticker(pair)
                    price = float(ticker.get('price', 0))
                except:
                    continue
                
                value = free * price
                if value < 1:
                    continue
                
                # Get entry
                key = f'krk_{asset}'
                if key not in self.entries:
                    self.entries[key] = price
                    self.log(f"📍 KRAKEN {asset}: Entry set @ ${price:.4f}")
                    continue
                
                entry = self.entries[key]
                pnl_pct = (price - entry) / entry * 100
                
                # ANY PROFIT = SELL
                if pnl_pct > 0.01:
                    self.log(f"🔥 KRAKEN SELL {asset}: ${value:.2f} ({pnl_pct:+.2f}%)")
                    
                    result = self.kraken.place_market_order(pair, 'sell', quantity=free * 0.999)
                    
                    # Check for ANY success indicator
                    if result and (result.get('txid') or result.get('status') == 'FILLED' or 
                                   result.get('orderId') or 'dryRun' in result):
                        profit_usd = value * (pnl_pct / 100)
                        self.profit += profit_usd
                        self.trades += 1
                        self.log(f"   ✅ SOLD! +${profit_usd:.4f}")
                        
                        del self.entries[key]
                        time.sleep(0.3)
                        self._kraken_buy_best()
                    else:
                        self.log(f"   ⚠️ Sell failed: {result}")
            
            # Deploy USD
            if usd_bal > 2:
                self._kraken_buy_best()
                
        except Exception as e:
            self.log(f"⚠️ Kraken error: {e}")
    
    def _kraken_buy_best(self):
        """Buy best on Kraken"""
        try:
            acct = self.kraken.account()
            usd = sum(float(b.get('free', 0)) for b in acct.get('balances', []) 
                     if b.get('asset') in ['USD', 'USDC', 'ZUSD'])
            
            if usd < 2:
                return
            
            # Use Binance momentum
            pairs = ['SOLUSDC', 'BTCUSDC', 'ETHUSDC']
            best_asset, best_mom = None, -999
            
            for pair in pairs:
                try:
                    t = self.binance.get_24h_ticker(pair)
                    mom = float(t.get('priceChangePercent', 0))
                    if mom > best_mom:
                        best_asset = pair.replace('USDC', '')
                        best_mom = mom
                except:
                    pass
            
            if best_asset:
                kraken_pair = f'{best_asset}USD'
                self.log(f"📥 KRAKEN BUY {best_asset}: ${usd:.2f} ({best_mom:+.1f}%)")
                
                result = self.kraken.place_market_order(kraken_pair, 'buy', quote_qty=usd * 0.95)
                
                if result and (result.get('txid') or 'dryRun' in result):
                    ticker = self.kraken.get_ticker(kraken_pair)
                    price = float(ticker.get('price', 0))
                    self.entries[f'krk_{best_asset}'] = price
                    self.log(f"   ✅ BOUGHT @ ${price:.4f}")
                else:
                    self.log(f"   ⚠️ Buy failed: {result}")
                    
        except Exception as e:
            self.log(f"⚠️ Kraken buy error: {e}")

    # ═══════════════════════════════════════════════════════════════
    # MAIN LOOP - PARALLEL AGGRESSIVE SCANNING
    # ═══════════════════════════════════════════════════════════════
    
    def run_cycle(self):
        """Run one aggressive cycle across all platforms"""
        with ThreadPoolExecutor(max_workers=3) as ex:
            ex.submit(self.binance_scan_and_trade)
            ex.submit(self.alpaca_scan_and_trade)
            ex.submit(self.kraken_scan_and_trade)
    
    def print_status(self):
        """Quick status"""
        self.log(f"═══ TRADES: {self.trades} | PROFIT: ${self.profit:.4f} | ENTRIES: {len(self.entries)} ═══")
    
    def run(self):
        """RUN FOREVER - TAKE EVERYTHING"""
        print()
        print("⚡ AGGRESSIVE MODE: 0.01% profit threshold")
        print("⚡ NO GATES - Just profits")
        print("⚡ Parallel scanning all 3 platforms")
        print()
        
        cycle = 0
        while True:
            try:
                self.run_cycle()
                cycle += 1
                
                if cycle % 5 == 0:
                    self.print_status()
                
                time.sleep(1)  # Fast cycle
                
            except KeyboardInterrupt:
                print()
                self.log("🛑 STOPPED")
                self.print_status()
                break
            except Exception as e:
                self.log(f"ERROR: {e}")
                time.sleep(2)


if __name__ == "__main__":
    r = AggressiveReclaimer()
    r.run()
