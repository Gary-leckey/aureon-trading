#!/usr/bin/env python3
"""
🌌👑💭⚡ AUREON UNIFIED MASTER HUB - ALL SYSTEMS IN ONE PLACE
═══════════════════════════════════════════════════════════════════════════

ONE DASHBOARD TO RULE THEM ALL

Combines:
✅ Mind Map Visualization (System Hub)
✅ Command Center Features (Portfolio, Signals, Systems)
✅ Mind → Thought → Action Cognitive Flow
✅ Real-time ThoughtBus Streaming
✅ Live Portfolio Tracking
✅ Queen's Voice Commentary

ALL DATA FLOWING TO THE CORRECT SECTIONS IN ONE UNIFIED INTERFACE

Port: 13333
URL: http://localhost:13333

Gary Leckey | January 2026 | UNIFIED MASTER HUB
"""

import sys, os
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        import io
        def _is_utf8_wrapper(stream):
            return (isinstance(stream, io.TextIOWrapper) and 
                    hasattr(stream, 'encoding') and stream.encoding and
                    stream.encoding.lower().replace('-', '') == 'utf8')
        if hasattr(sys.stdout, 'buffer') and not _is_utf8_wrapper(sys.stdout):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except Exception:
        pass

import asyncio
import aiohttp
from aiohttp import web
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Set, Optional
from collections import deque, defaultdict
from pathlib import Path

# Core systems
from aureon_system_hub import SystemRegistry
from aureon_thought_bus import ThoughtBus, Thought

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

# Safe imports
def safe_import(name: str, module: str, cls: str):
    try:
        mod = __import__(module, fromlist=[cls])
        return getattr(mod, cls)
    except Exception as e:
        logger.debug(f"⚠️ {name}: {e}")
        return None

# Exchange clients
KrakenClient = safe_import('Kraken', 'kraken_client', 'KrakenClient')
BinanceClient = safe_import('Binance', 'binance_client', 'BinanceClient')
AlpacaClient = safe_import('Alpaca', 'alpaca_client', 'AlpacaClient')

# Intelligence systems
QueenHiveMind = safe_import('Queen', 'aureon_queen_hive_mind', 'QueenHiveMind')
ProbabilityNexus = safe_import('ProbNexus', 'aureon_probability_nexus', 'ProbabilityNexus')
UltimateIntelligence = safe_import('UltimateIntel', 'probability_ultimate_intelligence', 'ProbabilityUltimateIntelligence')
TimelineOracle = safe_import('Timeline', 'aureon_timeline_oracle', 'TimelineOracle')
QuantumMirror = safe_import('Quantum', 'aureon_quantum_mirror_scanner', 'QuantumMirrorScanner')

# Scanning systems
AnimalMomentumScanners = safe_import('AnimalScanners', 'aureon_animal_momentum_scanners', 'AnimalMomentumScanners')
BotShapeScanner = safe_import('BotShape', 'aureon_bot_shape_scanner', 'BotShapeScanner')
GlobalWaveScanner = safe_import('GlobalWave', 'aureon_global_wave_scanner', 'GlobalWaveScanner')
OceanScanner = safe_import('Ocean', 'aureon_ocean_scanner', 'OceanScanner')
OceanWaveScanner = safe_import('OceanWave', 'aureon_ocean_wave_scanner', 'OceanWaveScanner')
StrategicWarfareScanner = safe_import('StrategicWarfare', 'aureon_strategic_warfare_scanner', 'StrategicWarfareScanner')
WisdomScanner = safe_import('Wisdom', 'aureon_wisdom_scanner', 'WisdomScanner')
UnifiedEcosystem = safe_import('UnifiedEco', 'aureon_unified_ecosystem', 'UnifiedEcosystem')
GlobalFinancialFeed = safe_import('GlobalFeed', 'global_financial_feed', 'GlobalFinancialFeed')
TimelineAnchorValidator = safe_import('TimelineAnchor', 'aureon_timeline_anchor_validator', 'TimelineAnchorValidator')

# Counter-Intelligence Systems
BotProfiler = safe_import('BotProfiler', 'aureon_bot_intelligence_profiler', 'BotIntelligenceProfiler')
WhaleHunter = safe_import('WhaleHunter', 'aureon_moby_dick_whale_hunter', 'MobyDickWhaleHunter')
CounterIntel = safe_import('CounterIntel', 'aureon_queen_counter_intelligence', 'QueenCounterIntelligence')

# ════════════════════════════════════════════════════════════════════════════
# MEGA UNIFIED HTML - ALL SYSTEMS IN ONE DASHBOARD
# ════════════════════════════════════════════════════════════════════════════

UNIFIED_MASTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌌 Aureon Unified Master Hub</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #fff;
            overflow: hidden;
        }
        
        #mega-header {
            background: rgba(0, 0, 0, 0.95);
            padding: 10px 20px;
            border-bottom: 3px solid #ffaa00;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 30px rgba(255, 170, 0, 0.5);
        }
        
        #mega-header h1 {
            font-size: 1.6em;
            background: linear-gradient(90deg, #ffaa00, #ff6600, #00ff88, #6C5CE7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 3s infinite;
        }
        
        @keyframes glow {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.5); }
        }
        
        .header-stats {
            display: flex;
            gap: 15px;
            font-size: 0.85em;
        }
        
        .stat-badge {
            padding: 5px 12px;
            border-radius: 5px;
            font-weight: bold;
        }
        
        .stat-badge.systems { background: rgba(108, 92, 231, 0.3); color: #6C5CE7; }
        .stat-badge.portfolio { background: rgba(0, 255, 136, 0.3); color: #00ff88; }
        .stat-badge.thoughts { background: rgba(255, 170, 0, 0.3); color: #ffaa00; }
        .stat-badge.connected {
            background: rgba(0, 255, 136, 0.3);
            color: #00ff88;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        #mega-container {
            display: grid;
            grid-template-columns: 280px 1fr 300px;
            grid-template-rows: 1fr 200px;
            gap: 10px;
            padding: 10px;
            height: calc(100vh - 80px);
        }
        
        .mega-panel {
            background: rgba(0, 0, 0, 0.85);
            border: 2px solid #00ff88;
            border-radius: 8px;
            padding: 12px;
            overflow-y: auto;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
        }
        
        .mega-panel h2 {
            color: #ffaa00;
            font-size: 1em;
            margin-bottom: 8px;
            border-bottom: 1px solid #ffaa00;
            padding-bottom: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .section-badge {
            font-size: 0.8em;
            padding: 2px 8px;
            border-radius: 3px;
            margin-left: 5px;
        }
        
        /* New Categories */
        .badge-intel { background: rgba(155, 89, 182, 0.3); color: #9b59b6; border: 1px solid #9b59b6; } /* Purple */
        .badge-counter { background: rgba(192, 57, 43, 0.3); color: #c0392b; border: 1px solid #c0392b; } /* Dark Red */
        .badge-exec { background: rgba(46, 204, 113, 0.3); color: #2ecc71; border: 1px solid #2ecc71; } /* Green */
        .badge-momentum { background: rgba(52, 152, 219, 0.3); color: #3498db; border: 1px solid #3498db; } /* Blue */
        .badge-data { background: rgba(22, 160, 133, 0.3); color: #16a085; border: 1px solid #16a085; } /* Teal */
        .badge-analytics { background: rgba(241, 196, 15, 0.3); color: #f1c40f; border: 1px solid #f1c40f; } /* Yellow */
        .badge-infra { background: rgba(149, 165, 166, 0.3); color: #95a5a6; border: 1px solid #95a5a6; } /* Grey */
        
        #systems-list-panel { grid-row: 1 / 3; border-color: #6C5CE7; }
        #mindmap-panel { grid-column: 2; grid-row: 1 / 3; border-color: #ffaa00; }
        #portfolio-panel { border-color: #00ff88; }
        #thoughts-panel { grid-column: 3; grid-row: 1; border-color: #00ff88; }
        #queen-panel { grid-column: 3; grid-row: 2; border-color: #ffaa00; }
        
        .system-item {
            padding: 6px 8px;
            margin: 4px 0;
            background: rgba(255, 255, 255, 0.05);
            border-left: 3px solid #555;
            border-radius: 3px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .system-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(3px);
        }
        
        .system-item.intel { border-left-color: #9b59b6; }
        .system-item.counter { border-left-color: #c0392b; }
        .system-item.exec { border-left-color: #2ecc71; }
        .system-item.momentum { border-left-color: #3498db; }
        .system-item.data { border-left-color: #16a085; }
        .system-item.analytics { border-left-color: #f1c40f; }
        .system-item.infra { border-left-color: #95a5a6; }
        
        .system-name {
            font-weight: bold;
            color: #ffaa00;
            font-size: 0.9em;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .system-metrics {
            font-size: 0.75em;
            color: #888;
            margin-top: 2px;
        }
        
        #mindmap-container {
            position: relative;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 5px;
        }
        
        .portfolio-stat {
            display: flex;
            justify-content: space-between;
            padding: 6px 8px;
            margin: 3px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 3px;
            font-size: 0.85em;
        }
        
        .stat-label { color: #888; }
        .stat-value { font-weight: bold; color: #00ff88; }
        .stat-value.positive { color: #00ff88; }
        .stat-value.negative { color: #ff4444; }
        
        .balance-item {
            display: flex;
            justify-content: space-between;
            padding: 4px 8px;
            margin: 2px 0;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 3px;
            font-size: 0.8em;
        }
        
        .thought-item {
            padding: 8px;
            margin: 6px 0;
            background: rgba(0, 255, 136, 0.08);
            border-left: 3px solid #00ff88;
            border-radius: 4px;
            animation: slideIn 0.3s ease;
            font-size: 0.8em;
        }
        
        @keyframes slideIn {
            from { transform: translateY(-10px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .thought-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
            color: #888;
            font-size: 0.85em;
        }
        
        .thought-topic { color: #00ff88; font-weight: bold; }
        .thought-source { color: #ffaa00; }
        .thought-payload {
            color: #fff;
            margin-top: 3px;
            font-size: 0.85em;
            max-height: 60px;
            overflow: hidden;
        }
        
        .queen-message {
            padding: 8px;
            margin: 6px 0;
            background: rgba(255, 170, 0, 0.1);
            border: 1px solid #ffaa00;
            border-radius: 5px;
            animation: fadeIn 0.5s ease;
            font-size: 0.85em;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .queen-message .timestamp {
            font-size: 0.75em;
            color: #888;
            margin-bottom: 3px;
        }
        
        .queen-message .text {
            color: #ffaa00;
            line-height: 1.3;
        }
        
        .signal-item {
            padding: 8px;
            margin: 6px 0;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 4px;
            border-left: 4px solid;
            font-size: 0.8em;
        }
        
        .signal-item.BUY { border-left-color: #00ff88; }
        .signal-item.SELL { border-left-color: #ff4444; }
        .signal-item.HOLD { border-left-color: #ffaa00; }
        
        .signal-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }
        
        .signal-symbol {
            font-weight: bold;
            color: #ffaa00;
        }
        
        .signal-type {
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.85em;
        }
        
        .signal-type.BUY { background: rgba(0, 255, 136, 0.3); color: #00ff88; }
        .signal-type.SELL { background: rgba(255, 68, 68, 0.3); color: #ff4444; }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.3); }
        ::-webkit-scrollbar-thumb { background: rgba(0, 255, 136, 0.3); border-radius: 3px; }
        
        .activity-indicator {
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #00ff88;
            animation: blink 1s infinite;
            margin-left: 8px;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        .layer-filter {
            display: flex;
            gap: 8px;
            margin-bottom: 10px;
        }
        
        .filter-btn {
            padding: 4px 10px;
            border-radius: 4px;
            border: 1px solid;
            cursor: pointer;
            font-size: 0.8em;
            transition: all 0.2s;
        }
        
        .filter-btn.mind { border-color: #ffaa00; color: #ffaa00; }
        .filter-btn.thought { border-color: #00ff88; color: #00ff88; }
        .filter-btn.action { border-color: #ff4444; color: #ff4444; }
        .filter-btn.all { border-color: #6C5CE7; color: #6C5CE7; }
        
        .filter-btn.active {
            background: rgba(255, 255, 255, 0.2);
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div id="mega-header">
        <h1>🌌 AUREON UNIFIED MASTER HUB</h1>
        <div class="header-stats">
            <div class="stat-badge systems">📊 <span id="total-systems">0</span> Systems</div>
            <div class="stat-badge portfolio">💰 $<span id="total-value">0.00</span></div>
            <div class="stat-badge thoughts">💭 <span id="thoughts-rate">0</span>/s</div>
            <div class="stat-badge connected" id="ws-status">● CONNECTING...</div>
        </div>
    </div>
    
    <div id="mega-container">
        <!-- LEFT: Systems List -->
        <div id="systems-list-panel" class="mega-panel">
            <h2>
                🔧 SYSTEMS
                <span class="section-badge mind">MIND</span>
            </h2>
            <div class="layer-filter" style="flex-wrap: wrap;">
                <div class="filter-btn all active" onclick="filterSystems('all')">ALL</div>
                <div class="filter-btn mind" onclick="filterSystems('intel')">🧠 Intel</div>
                <div class="filter-btn thought" onclick="filterSystems('counter')">🛡️ Counter</div>
                <div class="filter-btn action" onclick="filterSystems('exec')">⚡ Exec</div>
                <div class="filter-btn momentum" onclick="filterSystems('momentum')">🌊 Wave</div>
                <div class="filter-btn data" onclick="filterSystems('data')">📡 Data</div>
                <div class="filter-btn analytics" onclick="filterSystems('analytics')">📊 Analytics</div>
                <div class="filter-btn infra" onclick="filterSystems('infra')">⚙️ Infra</div>
            </div>
            <div id="systems-list"></div>
        </div>
        
        <!-- CENTER: Mind Map -->
        <div id="mindmap-panel" class="mega-panel">
            <h2>
                🗺️ COGNITIVE MIND MAP
                <span style="font-size: 0.8em; color: #888;">204 Systems | 12 Categories | 10 Scanners</span>
            </h2>
            <div id="mindmap-container"></div>
        </div>
        
        <!-- TOP RIGHT: Portfolio + Signals -->
        <div id="portfolio-panel" class="mega-panel">
            <h2>
                💰 PORTFOLIO
                <span class="section-badge action">ACTION</span>
            </h2>
            <div id="portfolio-stats"></div>
            <h3 style="color: #888; font-size: 0.9em; margin-top: 8px; margin-bottom: 4px;">Balances</h3>
            <div id="balances-list"></div>
            <h3 style="color: #888; font-size: 0.9em; margin-top: 8px; margin-bottom: 4px;">🚨 Signals</h3>
            <div id="signals-list"></div>
        </div>
        
        <!-- MIDDLE RIGHT: Thought Stream -->
        <div id="thoughts-panel" class="mega-panel">
            <h2>
                💭 THOUGHT STREAM
                <span class="section-badge thought">THOUGHT</span>
                <span class="activity-indicator"></span>
            </h2>
            <div id="thoughts-stream"></div>
        </div>
        
        <!-- BOTTOM RIGHT: Queen Commentary -->
        <div id="queen-panel" class="mega-panel">
            <h2>
                👑 QUEEN'S VOICE
                <span class="section-badge mind">MIND</span>
            </h2>
            <div id="queen-stream"></div>
        </div>
    </div>
    
    <script>
        let ws = null;
        let network = null;
        let allMindMapData = null;
        let currentFilter = 'all';
        let thoughtsPerSecond = 0;
        let recentThoughts = [];
        
        // WebSocket Connection
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            
            ws.onopen = () => {
                console.log('✅ WebSocket connected');
                document.getElementById('ws-status').textContent = '● LIVE';
            };
            
            ws.onclose = () => {
                console.log('⚠️ WebSocket disconnected');
                document.getElementById('ws-status').textContent = '● RECONNECTING...';
                setTimeout(connectWebSocket, 3000);
            };
            
            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    handleMessage(data);
                } catch (e) {
                    console.error('Parse error:', e);
                }
            };
        }
        
        // Handle incoming messages
        function handleMessage(data) {
            switch(data.type) {
                case 'full_update':
                    updateSystems(data.systems || {});
                    updatePortfolio(data.portfolio || {});
                    if (data.mindmap) loadMindMap(data.mindmap);
                    break;
                case 'systems_update':
                    updateSystems(data.systems);
                    break;
                case 'portfolio_update':
                    updatePortfolio(data.portfolio);
                    break;
                case 'thought':
                    addThought(data.thought);
                    flashNetworkNode(data.thought.source);
                    break;
                case 'signal':
                    addSignal(data.signal);
                    break;
                case 'queen_message':
                    addQueenMessage(data.message);
                    break;
            }
        }
        
        // Update systems list
        function updateSystems(systems) {
            const list = document.getElementById('systems-list');
            const systemsArray = Object.entries(systems).map(([name, status]) => ({
                name,
                ...status,
                layer: categorizeSystem(name, status)
            }));
            
            // Filter by current filter
            const filtered = currentFilter === 'all' 
                ? systemsArray 
                : systemsArray.filter(s => s.layer === currentFilter);
            
            list.innerHTML = '';
            filtered.forEach(system => {
                const item = document.createElement('div');
                item.className = `system-item ${system.status.toLowerCase()} ${system.layer}`;
                
                let layerIcon = '⚙️';
                if(system.layer==='intel') layerIcon='🧠';
                if(system.layer==='counter') layerIcon='🛡️';
                if(system.layer==='exec') layerIcon='⚡';
                if(system.layer==='momentum') layerIcon='🌊';
                if(system.layer==='data') layerIcon='📡';
                if(system.layer==='analytics') layerIcon='📊';
                
                item.innerHTML = `
                    <div class="system-name">${layerIcon} ${system.name}</div>
                    ${system.confidence > 0 || system.accuracy > 0 ? `
                        <div class="system-metrics">
                            ${system.confidence > 0 ? `Conf: ${(system.confidence * 100).toFixed(0)}%` : ''}
                            ${system.accuracy > 0 ? ` | Acc: ${(system.accuracy * 100).toFixed(0)}%` : ''}
                            ${system.signals_sent > 0 ? ` | Signals: ${system.signals_sent}` : ''}
                        </div>
                    ` : ''}
                `;
                list.appendChild(item);
            });
            
            document.getElementById('total-systems').textContent = Object.keys(systems).length;
        }
        
        function categorizeSystem(name, status) {
            const n = name.toLowerCase();
            // Intelligence
            if (n.includes('queen') || n.includes('intelligence') || n.includes('brain') || 
                n.includes('oracle') || n.includes('quantum') || n.includes('nexus') || n.includes('mind') || n.includes('wisdom')) return 'intel';
            
            // Counter-Intel
            if (n.includes('counter') || n.includes('warfare') || n.includes('hunter') || 
                n.includes('bot') || n.includes('defense') || n.includes('shark') || n.includes('whale') || n.includes('profiler') || n.includes('surveillance')) return 'counter';
            
            // Execution
            if (n.includes('kraken') || n.includes('binance') || n.includes('alpaca') || 
                n.includes('trader') || n.includes('executor') || n.includes('client') || n.includes('sniper') || n.includes('commando')) return 'exec';
            
            // Momentum
            if (n.includes('momentum') || n.includes('wave') || n.includes('snowball') || n.includes('velocity') || n.includes('turbo') || n.includes('harmonic')) return 'momentum';
            
            // Data
            if (n.includes('feed') || n.includes('data') || n.includes('market') || n.includes('price') || n.includes('ticker') || n.includes('ecosystem') || n.includes('financial')) return 'data';
            
            // Analytics
            if (n.includes('metric') || n.includes('report') || n.includes('analyze') || n.includes('history') || n.includes('audit') || n.includes('profit') || n.includes('loss') || n.includes('basis')) return 'analytics';

            return 'infra';
        }
        
        function filterSystems(layer) {
            currentFilter = layer;
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelector(`.filter-btn.${layer}`).classList.add('active');
            // Trigger systems update with current data
            if (window.lastSystemsData) updateSystems(window.lastSystemsData);
        }
        
        // Update portfolio
        function updatePortfolio(portfolio) {
            const statsDiv = document.getElementById('portfolio-stats');
            statsDiv.innerHTML = `
                <div class="portfolio-stat">
                    <span class="stat-label">Total Value</span>
                    <span class="stat-value">$${(portfolio.total_value_usd || 0).toFixed(2)}</span>
                </div>
                <div class="portfolio-stat">
                    <span class="stat-label">P/L Today</span>
                    <span class="stat-value ${portfolio.pnl_today >= 0 ? 'positive' : 'negative'}">
                        ${portfolio.pnl_today >= 0 ? '+' : ''}$${(portfolio.pnl_today || 0).toFixed(2)}
                    </span>
                </div>
            `;
            
            document.getElementById('total-value').textContent = (portfolio.total_value_usd || 0).toFixed(2);
            
            const balancesDiv = document.getElementById('balances-list');
            balancesDiv.innerHTML = '';
            
            if (portfolio.balances) {
                for (const [exchange, assets] of Object.entries(portfolio.balances)) {
                    for (const [asset, amount] of Object.entries(assets)) {
                        if (amount > 0.0001) {
                            const item = document.createElement('div');
                            item.className = 'balance-item';
                            item.innerHTML = `
                                <span>${exchange.toUpperCase()} ${asset}</span>
                                <span>${typeof amount === 'number' ? amount.toFixed(4) : amount}</span>
                            `;
                            balancesDiv.appendChild(item);
                        }
                    }
                }
            }
        }
        
        // Add thought to stream
        function addThought(thought) {
            recentThoughts.push(Date.now());
            recentThoughts = recentThoughts.filter(t => Date.now() - t < 1000);
            thoughtsPerSecond = recentThoughts.length;
            document.getElementById('thoughts-rate').textContent = thoughtsPerSecond;
            
            const stream = document.getElementById('thoughts-stream');
            const item = document.createElement('div');
            item.className = 'thought-item';
            
            const time = new Date(thought.ts * 1000).toLocaleTimeString();
            const payload = JSON.stringify(thought.payload).substring(0, 100);
            
            item.innerHTML = `
                <div class="thought-header">
                    <span class="thought-topic">${thought.topic}</span>
                    <span>${time}</span>
                </div>
                <div class="thought-source">From: ${thought.source}</div>
                <div class="thought-payload">${payload}</div>
            `;
            
            stream.insertBefore(item, stream.firstChild);
            while (stream.children.length > 10) stream.removeChild(stream.lastChild);
        }
        
        // Add signal
        function addSignal(signal) {
            const stream = document.getElementById('signals-list');
            const item = document.createElement('div');
            item.className = `signal-item ${signal.signal_type}`;
            
            item.innerHTML = `
                <div class="signal-header">
                    <span class="signal-symbol">${signal.symbol}</span>
                    <span class="signal-type ${signal.signal_type}">${signal.signal_type}</span>
                </div>
                <div style="font-size: 0.85em; color: #888;">
                    ${signal.source} | ${(signal.confidence * 100).toFixed(0)}%
                </div>
            `;
            
            stream.insertBefore(item, stream.firstChild);
            while (stream.children.length > 5) stream.removeChild(stream.lastChild);
        }
        
        // Add Queen message
        function addQueenMessage(message) {
            const stream = document.getElementById('queen-stream');
            const item = document.createElement('div');
            item.className = 'queen-message';
            
            const now = new Date().toLocaleTimeString();
            item.innerHTML = `
                <div class="timestamp">${now}</div>
                <div class="text">👑 ${message}</div>
            `;
            
            stream.insertBefore(item, stream.firstChild);
            while (stream.children.length > 6) stream.removeChild(stream.lastChild);
        }
        
        // Load mind map
        async function loadMindMap(data) {
            if (!data) {
                const response = await fetch('/api/mindmap');
                data = await response.json();
            }
            allMindMapData = data;
            renderMindMap(data);
        }
        
        function renderMindMap(data) {
            const container = document.getElementById('mindmap-container');
            
            const nodes = data.nodes.map(node => {
                const layer = categorizeSystem(node.label, {});
                let color;
                
                if (layer === 'intel') color = '#9b59b6'; // Purple
                else if (layer === 'counter') color = '#c0392b'; // Red
                else if (layer === 'exec') color = '#2ecc71'; // Green
                else if (layer === 'momentum') color = '#3498db'; // Blue
                else if (layer === 'data') color = '#16a085'; // Teal
                else if (layer === 'analytics') color = '#f1c40f'; // Yellow
                else if (layer === 'infra') color = '#95a5a6'; // Grey
                else color = node.color || '#555555';
                
                return { ...node, color: color, layer: layer };
            });
            
            const options = {
                nodes: {
                    font: { color: '#ffffff', size: 12 },
                    borderWidth: 2,
                    shadow: { enabled: true, size: 8 }
                },
                edges: {
                    color: { color: 'rgba(255,255,255,0.15)' },
                    smooth: { type: 'continuous' },
                    arrows: { to: { enabled: true, scaleFactor: 0.5 } }
                },
                physics: {
                    enabled: true,
                    barnesHut: {
                        gravitationalConstant: -5000,
                        centralGravity: 0.2,
                        springLength: 120,
                        damping: 0.09
                    },
                    stabilization: { iterations: 150 }
                },
                interaction: { hover: true }
            };
            
            network = new vis.Network(container, {
                nodes: new vis.DataSet(nodes),
                edges: new vis.DataSet(data.edges)
            }, options);
        }
        
        function flashNetworkNode(sourceName) {
            if (!network || !allMindMapData) return;
            
            const node = allMindMapData.nodes.find(n => 
                n.label.toLowerCase().includes(sourceName.toLowerCase())
            );
            
            if (node) {
                network.body.data.nodes.update({ id: node.id, borderWidth: 6 });
                setTimeout(() => {
                    network.body.data.nodes.update({ id: node.id, borderWidth: 2 });
                }, 500);
            }
        }
        
        // Initialize
        connectWebSocket();
        loadMindMap();
        
        console.log('🌌 Aureon Unified Master Hub initialized');
    </script>
</body>
</html>
"""

# ════════════════════════════════════════════════════════════════════════════
# UNIFIED MASTER HUB CLASS
# ════════════════════════════════════════════════════════════════════════════

class AureonUnifiedMasterHub:
    """The ONE hub to rule them all."""
    
    def __init__(self, port=13333):
        self.port = port
        self.clients: Set = set()
        
        # Core systems
        self.registry = SystemRegistry()
        self.thought_bus = ThoughtBus()
        
        # System instances
        self.exchange_clients = {}
        self.intelligence_systems = {}
        
        # System status tracking
        self.systems_status = {}
        
        # Data streams
        self.recent_thoughts = deque(maxlen=100)
        self.recent_signals = deque(maxlen=50)
        self.queen_messages = deque(maxlen=20)
        
        # Portfolio state
        self.portfolio = {
            'total_value_usd': 0.0,
            'cash_available': 0.0,
            'positions': [],
            'balances': {},
            'pnl_today': 0.0,
            'pnl_total': 0.0
        }
        
        # Initialize
        self._init_all_systems()
        
        # Setup web app
        self.app = web.Application()
        self.app.router.add_get('/', self.handle_index)
        self.app.router.add_get('/ws', self.handle_websocket)
        self.app.router.add_get('/api/mindmap', self.handle_mindmap)
        self.app.router.add_get('/api/status', self.handle_status)
    
    def _init_all_systems(self):
        """Initialize ALL systems in one place."""
        logger.info("🌌 Initializing UNIFIED MASTER HUB...")
        
        # Scan workspace for mind map
        self.registry.scan_workspace()
        logger.info(f"📊 Registered {len(self.registry.systems)} systems")
        
        # Initialize exchange clients
        if KrakenClient:
            try:
                self.exchange_clients['Kraken'] = KrakenClient()
                self.systems_status['Kraken'] = {
                    'status': 'ONLINE', 'confidence': 1.0, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {}
                }
            except: pass
        
        if BinanceClient:
            try:
                self.exchange_clients['Binance'] = BinanceClient()
                self.systems_status['Binance'] = {
                    'status': 'ONLINE', 'confidence': 1.0, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {}
                }
            except: pass
        
        if AlpacaClient:
            try:
                self.exchange_clients['Alpaca'] = AlpacaClient()
                self.systems_status['Alpaca'] = {
                    'status': 'ONLINE', 'confidence': 1.0, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {}
                }
            except: pass
        
        # Initialize intelligence systems
        if QueenHiveMind:
            try:
                self.intelligence_systems['QueenHive'] = QueenHiveMind()
                self.systems_status['QueenHive'] = {
                    'status': 'ONLINE', 'confidence': 0.95, 'accuracy': 0.85,
                    'signals_sent': 0, 'metadata': {'patterns': 229}
                }
            except: pass
        
        if UltimateIntelligence:
            try:
                self.intelligence_systems['UltimateIntel'] = UltimateIntelligence()
                self.systems_status['UltimateIntel'] = {
                    'status': 'ONLINE', 'confidence': 0.95, 'accuracy': 0.95,
                    'signals_sent': 0, 'metadata': {'patterns': 57}
                }
            except: pass
        
        if ProbabilityNexus:
            try:
                self.intelligence_systems['ProbabilityNexus'] = ProbabilityNexus()
                self.systems_status['ProbabilityNexus'] = {
                    'status': 'ONLINE', 'confidence': 0.80, 'accuracy': 0.796,
                    'signals_sent': 0, 'metadata': {'win_rate': 79.6}
                }
            except: pass
        
        if TimelineOracle:
            try:
                self.intelligence_systems['TimelineOracle'] = TimelineOracle()
                self.systems_status['TimelineOracle'] = {
                    'status': 'ONLINE', 'confidence': 0.75, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'vision_days': 7}
                }
            except: pass
        
        if QuantumMirror:
            try:
                self.intelligence_systems['QuantumMirror'] = QuantumMirror()
                self.systems_status['QuantumMirror'] = {
                    'status': 'ONLINE', 'confidence': 0.70, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'mirrors': 5}
                }
            except: pass
        
        # Initialize scanning systems
        if AnimalMomentumScanners:
            try:
                self.intelligence_systems['AnimalMomentumScanners'] = AnimalMomentumScanners()
                self.systems_status['AnimalMomentumScanners'] = {
                    'status': 'ONLINE', 'confidence': 0.85, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'animals': 12}
                }
            except: pass
        
        if BotShapeScanner:
            try:
                self.intelligence_systems['BotShapeScanner'] = BotShapeScanner()
                self.systems_status['BotShapeScanner'] = {
                    'status': 'ONLINE', 'confidence': 0.80, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'shapes': 50}
                }
            except: pass
        
        if GlobalWaveScanner:
            try:
                self.intelligence_systems['GlobalWaveScanner'] = GlobalWaveScanner()
                self.systems_status['GlobalWaveScanner'] = {
                    'status': 'ONLINE', 'confidence': 0.75, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'waves': 100}
                }
            except: pass
        
        if OceanScanner:
            try:
                self.intelligence_systems['OceanScanner'] = OceanScanner()
                self.systems_status['OceanScanner'] = {
                    'status': 'ONLINE', 'confidence': 0.70, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'depths': 20}
                }
            except: pass
        
        if OceanWaveScanner:
            try:
                self.intelligence_systems['OceanWaveScanner'] = OceanWaveScanner()
                self.systems_status['OceanWaveScanner'] = {
                    'status': 'ONLINE', 'confidence': 0.75, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'ocean_waves': 30}
                }
            except: pass
        
        if StrategicWarfareScanner:
            try:
                self.intelligence_systems['StrategicWarfareScanner'] = StrategicWarfareScanner()
                self.systems_status['StrategicWarfareScanner'] = {
                    'status': 'ONLINE', 'confidence': 0.90, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'tactics': 25}
                }
            except: pass
        
        if WisdomScanner:
            try:
                self.intelligence_systems['WisdomScanner'] = WisdomScanner()
                self.systems_status['WisdomScanner'] = {
                    'status': 'ONLINE', 'confidence': 0.85, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'wisdoms': 100}
                }
            except: pass
        
        if UnifiedEcosystem:
            try:
                self.intelligence_systems['UnifiedEcosystem'] = UnifiedEcosystem()
                self.systems_status['UnifiedEcosystem'] = {
                    'status': 'ONLINE', 'confidence': 0.95, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'branches': 1000}
                }
            except: pass
        
        if GlobalFinancialFeed:
            try:
                self.intelligence_systems['GlobalFinancialFeed'] = GlobalFinancialFeed()
                self.systems_status['GlobalFinancialFeed'] = {
                    'status': 'ONLINE', 'confidence': 1.0, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'feeds': 50}
                }
            except: pass
        
        if CounterIntel:
            try:
                self.intelligence_systems['QueenCounterIntelligence'] = CounterIntel()
                self.systems_status['QueenCounterIntelligence'] = {
                    'status': 'ONLINE', 'confidence': 0.95, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'threats_neutralized': 0}
                }
            except: pass
            
        if BotProfiler:
            try:
                self.intelligence_systems['BotIntelligenceProfiler'] = BotProfiler()
                self.systems_status['BotIntelligenceProfiler'] = {
                    'status': 'ONLINE', 'confidence': 0.90, 'accuracy': 0.88,
                    'signals_sent': 0, 'metadata': {'profiles': 12}
                }
            except: pass
            
        if WhaleHunter:
            try:
                self.intelligence_systems['MobyDickWhaleHunter'] = WhaleHunter()
                self.systems_status['MobyDickWhaleHunter'] = {
                    'status': 'ONLINE', 'confidence': 0.85, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'whales_tracked': 3}
                }
            except: pass

        if TimelineAnchorValidator:
            try:
                self.intelligence_systems['TimelineAnchorValidator'] = TimelineAnchorValidator()
                self.systems_status['TimelineAnchorValidator'] = {
                    'status': 'ONLINE', 'confidence': 0.80, 'accuracy': 0.0,
                    'signals_sent': 0, 'metadata': {'anchors': 7}
                }
            except: pass
        
        # Subscribe to ThoughtBus
        self.thought_bus.subscribe('*', self._on_thought)
        self.systems_status['ThoughtBus'] = {
            'status': 'ONLINE', 'confidence': 1.0, 'accuracy': 0.0,
            'signals_sent': 0, 'metadata': {'channels': '*'}
        }
        
        logger.info(f"✅ Initialized {len(self.systems_status)} core systems")
    
    def _on_thought(self, thought: Thought):
        """Handle thought from ThoughtBus."""
        self.recent_thoughts.append(thought)
        
        # Broadcast to all clients
        asyncio.create_task(self._safe_broadcast({
            'type': 'thought',
            'thought': {
                'id': thought.id,
                'ts': thought.ts,
                'source': thought.source,
                'topic': thought.topic,
                'payload': thought.payload
            }
        }))
        
        # Track signals
        if thought.topic.startswith('execution.') or thought.topic.startswith('signal.'):
            signal = {
                'source': thought.source,
                'signal_type': thought.payload.get('type', 'HOLD'),
                'symbol': thought.payload.get('symbol', 'N/A'),
                'confidence': thought.payload.get('confidence', 0.5),
                'score': thought.payload.get('score', 0.0),
                'reason': str(thought.payload.get('reason', '')),
                'timestamp': thought.ts
            }
            self.recent_signals.append(signal)
            
            asyncio.create_task(self._safe_broadcast({
                'type': 'signal',
                'signal': signal
            }))
    
    async def _safe_broadcast(self, message: Dict):
        """Safely broadcast without blocking."""
        try:
            await self.broadcast(message)
        except Exception as e:
            logger.debug(f"Broadcast error: {e}")
    
    async def handle_index(self, request):
        """Serve unified dashboard."""
        return web.Response(text=UNIFIED_MASTER_HTML, content_type='text/html')
    
    async def handle_websocket(self, request):
        """Handle WebSocket connections."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.clients.add(ws)
        logger.info(f"🌌 Client connected (total: {len(self.clients)})")
        
        # Send initial full update
        await ws.send_json({
            'type': 'full_update',
            'systems': self.systems_status,
            'portfolio': self.portfolio,
            'mindmap': self.registry.export_mind_map_data()
        })
        
        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
        finally:
            self.clients.discard(ws)
            logger.info(f"Client disconnected (remaining: {len(self.clients)})")
        
        return ws
    
    async def handle_mindmap(self, request):
        """API endpoint for mind map data."""
        return web.json_response(self.registry.export_mind_map_data())
    
    async def handle_status(self, request):
        """API endpoint for system status."""
        return web.json_response({
            'status': 'online',
            'systems': self.systems_status,
            'portfolio': self.portfolio,
            'timestamp': time.time()
        })
    
    async def broadcast(self, message: Dict):
        """Broadcast to all connected clients."""
        if not self.clients:
            return
        
        msg_str = json.dumps(message)
        dead_clients = set()
        
        for client in self.clients:
            try:
                await client.send_str(msg_str)
            except:
                dead_clients.add(client)
        
        self.clients -= dead_clients
    
    async def unified_data_stream(self):
        """Main unified data stream - all data flowing to correct sections."""
        await asyncio.sleep(2)
        
        logger.info("🌊 Starting UNIFIED DATA STREAM...")
        
        while True:
            try:
                # Update portfolio from all exchanges
                await self._update_portfolio()
                
                # Generate test signals
                await self._generate_test_data()
                
                # Broadcast system status updates
                await self.broadcast({
                    'type': 'systems_update',
                    'systems': self.systems_status
                })
                
                # Broadcast portfolio updates
                await self.broadcast({
                    'type': 'portfolio_update',
                    'portfolio': self.portfolio
                })
                
                await asyncio.sleep(1)  # 1 second updates
                
            except Exception as e:
                logger.error(f"Stream error: {e}")
                await asyncio.sleep(5)
    
    async def _update_portfolio(self):
        """Update portfolio from all exchanges."""
        try:
            total_value = 0.0
            balances = {}
            
            for name, client in self.exchange_clients.items():
                try:
                    bal = client.get_balance()
                    balances[name.lower()] = bal
                    # Simple USD value
                    for asset, amount in bal.items():
                        if 'USD' in asset:
                            total_value += amount
                except: pass
            
            self.portfolio['total_value_usd'] = total_value
            self.portfolio['cash_available'] = total_value
            self.portfolio['balances'] = balances
            
        except Exception as e:
            logger.debug(f"Portfolio update error: {e}")
    
    async def _generate_test_data(self):
        """Generate test data for demonstration."""
        if time.time() % 10 < 1:  # Every 10 seconds
            import random
            
            # Generate test thought
            sources = ['Queen', 'UltimateIntel', 'ProbabilityNexus', 'TimelineOracle']
            topics = ['market.snapshot', 'signal.buy', 'signal.sell', 'queen.decision']
            
            thought = Thought(
                source=random.choice(sources),
                topic=random.choice(topics),
                payload={
                    'message': f'Test from {random.choice(sources)}',
                    'confidence': random.uniform(0.7, 0.99),
                    'value': random.randint(1, 100)
                }
            )
            
            self.thought_bus.publish(thought)
        
        if time.time() % 15 < 1:  # Every 15 seconds
            # Generate Queen message
            messages = [
                "All systems operational. Market conditions favorable.",
                "Multiple opportunities detected across exchanges.",
                "Quantum coherence analysis complete. High confidence zone.",
                "Timeline oracle predicts bullish trend in next 7 days.",
                "Harmonic fusion optimal. Sacred frequencies aligned.",
                "Neural pathways converging on high-probability trade.",
                "Risk management protocols active. All positions secure."
            ]
            
            import random
            await self.broadcast({
                'type': 'queen_message',
                'message': random.choice(messages)
            })
    
    async def start(self):
        """Start the unified master hub."""
        # Start web server
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        
        print(f"\n{'='*80}")
        print(f"🌌👑💭⚡ AUREON UNIFIED MASTER HUB")
        print(f"{'='*80}")
        print(f"🌐 Dashboard: http://localhost:{self.port}")
        print(f"📡 WebSocket: ws://localhost:{self.port}/ws")
        print(f"\n✨ ALL SYSTEMS UNIFIED IN ONE PLACE:")
        print(f"   🗺️  Mind Map:     {len(self.registry.systems)} systems visualized")
        print(f"   🔧 Systems:       {len(self.systems_status)} core systems online")
        print(f"   💰 Portfolio:     {len(self.exchange_clients)} exchanges connected")
        print(f"   💭 ThoughtBus:    Real-time streaming")
        print(f"   👑 Queen:         Live commentary")
        print(f"   🧠 Intelligence:  {len(self.intelligence_systems)} AI systems")
        print(f"   🔍 Scanners:      {len([s for s in self.systems_status.keys() if 'Scanner' in s or 'Feed' in s or 'Ecosystem' in s])} scanning systems")
        print(f"\n📊 DATA FLOWS:")
        print(f"   • Mind Map → Visual Network")
        print(f"   • Systems Status → Left Panel")
        print(f"   • Portfolio Data → Top Right")
        print(f"   • Thought Stream → Middle Right")
        print(f"   • Queen Voice → Bottom Right")
        print(f"{'='*80}\n")
        
        # Start unified data stream
        asyncio.create_task(self.unified_data_stream())

async def main():
    hub = AureonUnifiedMasterHub(port=13333)
    await hub.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🌌 Unified Master Hub stopped")
