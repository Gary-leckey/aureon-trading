# ⚡ UNIFIED TRADE EXECUTOR - Execution Hub
# Stage 3: Queen → Trade Executor → Multi-Exchange Orchestration
import os
import json
import time
import logging
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)

@dataclass
class TradeGatingConfig:
    """Safety guardrails for trade execution"""
    min_score: float = 0.618
    min_coherence: float = 0.618
    min_lambda: float = 0.618
    max_position_pct: float = 0.05
    max_daily_trades: int = 50
    max_daily_loss_pct: float = 0.05
    allowed_exchanges: list = None
    
    def __post_init__(self):
        if self.allowed_exchanges is None:
            self.allowed_exchanges = ["kraken", "binance", "alpaca", "capital"]

@dataclass
class ExecutionRequest:
    """Standardized trade request"""
    symbol: str
    side: str
    quantity: float
    price: float
    confidence: float
    coherence: float
    lambda_val: float
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

@dataclass
class ExecutionResult:
    """Execution outcome"""
    success: bool
    symbol: str
    side: str
    executed_qty: float
    executed_price: float
    pnl: float
    error: Optional[str] = None
    order_id: Optional[str] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class UnifiedTradeExecutor:
    """Central execution hub"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.config = TradeGatingConfig()
        self.stats = {"requests": 0, "approved": 0, "rejected": 0, "pnl": 0.0}
        
    def initialize(self):
        logger.info(f"⚡ Executor: {'🧪 DRY-RUN' if self.dry_run else '💰 LIVE'}")
        
    def apply_gating_rules(self, request: ExecutionRequest) -> Tuple[bool, str]:
        if request.confidence < self.config.min_score:
            return False, "Low confidence"
        return True, "✅"
    
    def execute_trade(self, request: ExecutionRequest) -> ExecutionResult:
        self.stats["requests"] += 1
        approved, _ = self.apply_gating_rules(request)
        if approved:
            self.stats["approved"] += 1
        else:
            self.stats["rejected"] += 1
        return ExecutionResult(success=approved, symbol=request.symbol, side=request.side, executed_qty=request.quantity, executed_price=request.price, pnl=0.0)
    
    def get_statistics(self) -> Dict:
        return self.stats

class QueenExecutorBridge:
    def __init__(self, executor):
        self.executor = executor
    def wire_queen_to_executor(self):
        logger.info("🔌 Bridge wired")
