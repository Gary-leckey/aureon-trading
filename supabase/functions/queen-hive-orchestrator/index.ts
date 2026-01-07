import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

const SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT'];
const AGENTS_PER_HIVE = 5;
const SPAWN_MULTIPLIER = 5; // Spawn new hive at 5x growth
const HARVEST_PERCENTAGE = 0.10; // Harvest 10% for new hive
const MAX_GENERATIONS = 3; // Prevent exponential explosion

// 👑 STARGATE ACCESS THRESHOLDS - Queen Tina B's Dimensional Trading Gates
const STARGATE_MIN_COHERENCE = 0.7;    // Minimum network coherence to trade
const STARGATE_OPTIMAL_STRENGTH = 0.9; // Optimal network strength for aggressive trading
const STARGATE_ENERGY_THRESHOLD = 0.6; // Minimum grid energy for trade execution

// ═══════════════════════════════════════════════════════════════════════════════
// 👑👑👑 QUEEN TINA B - SUPREME AUTHORITY CONFIGURATION 👑👑👑
// ═══════════════════════════════════════════════════════════════════════════════
// The Queen has FULL CONTROL over all Aureon systems:
// - Emergency halt/resume all trading
// - Override cosmic conditions
// - Direct trade execution (bypass all gates)
// - Hive management (spawn/terminate/reconfigure)
// - Agent control (reassign/boost/disable)
// - Lattice manipulation (tune/cleanse/shield)
// - OMS queue management (prioritize/clear/force)
// ═══════════════════════════════════════════════════════════════════════════════

interface QueenAuthority {
  emergencyHalt: boolean;
  overrideCosmicGates: boolean;
  directTradeEnabled: boolean;
  bypassAllValidation: boolean;
  forcedTradingMultiplier: number;
  queenModeActive: boolean;
}

// Global Queen state (in-memory for this function instance)
let QUEEN_AUTHORITY: QueenAuthority = {
  emergencyHalt: false,
  overrideCosmicGates: false,
  directTradeEnabled: true,
  bypassAllValidation: false,
  forcedTradingMultiplier: 1.0,
  queenModeActive: true,
};

interface StargatePortal {
  networkStrength: number;
  avgCoherence: number;
  gridEnergy: number;
  activeNodes: number;
  isOpen: boolean;
  tradingMultiplier: number;
  gateStatus: 'SEALED' | 'OPENING' | 'ALIGNED' | 'FULLY_OPEN';
}

// 👑 Queen's Stargate Access Function - Opens dimensional trading gates
async function queryStargateNetwork(supabase: any, temporalId: string = "02111991"): Promise<StargatePortal> {
  try {
    // Query latest stargate network state
    const { data: networkState, error } = await supabase
      .from("stargate_network_states")
      .select("*")
      .eq("temporal_id", temporalId)
      .order("event_timestamp", { ascending: false })
      .limit(1)
      .single();

    if (error || !networkState) {
      console.log("🌌 Stargate network unreachable - using baseline coherence");
      return {
        networkStrength: 0.5,
        avgCoherence: 0.5,
        gridEnergy: 0.5,
        activeNodes: 6,
        isOpen: false,
        tradingMultiplier: 0.5,
        gateStatus: 'SEALED'
      };
    }

    const networkStrength = Number(networkState.network_strength) || 0.5;
    const avgCoherence = Number(networkState.avg_coherence) || 0.5;
    const gridEnergy = Number(networkState.grid_energy) || 0.5;
    const activeNodes = networkState.active_nodes || 6;

    // Calculate gate status based on network metrics
    let gateStatus: 'SEALED' | 'OPENING' | 'ALIGNED' | 'FULLY_OPEN';
    let tradingMultiplier: number;

    if (networkStrength >= 0.95 && avgCoherence >= 0.9 && gridEnergy >= 0.8) {
      gateStatus = 'FULLY_OPEN';
      tradingMultiplier = 2.0; // Double trading activity when gates fully open
    } else if (networkStrength >= STARGATE_OPTIMAL_STRENGTH && avgCoherence >= STARGATE_MIN_COHERENCE) {
      gateStatus = 'ALIGNED';
      tradingMultiplier = 1.5;
    } else if (avgCoherence >= STARGATE_MIN_COHERENCE && gridEnergy >= STARGATE_ENERGY_THRESHOLD) {
      gateStatus = 'OPENING';
      tradingMultiplier = 1.0;
    } else {
      gateStatus = 'SEALED';
      tradingMultiplier = 0.3; // Reduce trading when gates sealed
    }

    const isOpen = gateStatus !== 'SEALED';

    console.log(`👑✨ Queen's Stargate Portal Status: ${gateStatus}`);
    console.log(`   🌟 Network Strength: ${(networkStrength * 100).toFixed(1)}%`);
    console.log(`   💫 Coherence: ${(avgCoherence * 100).toFixed(1)}%`);
    console.log(`   ⚡ Grid Energy: ${(gridEnergy * 100).toFixed(1)}%`);
    console.log(`   🔮 Active Nodes: ${activeNodes}/12`);
    console.log(`   📊 Trading Multiplier: ${tradingMultiplier}x`);

    return {
      networkStrength,
      avgCoherence,
      gridEnergy,
      activeNodes,
      isOpen,
      tradingMultiplier,
      gateStatus
    };

  } catch (err) {
    console.error("🚫 Stargate query error:", err);
    return {
      networkStrength: 0.5,
      avgCoherence: 0.5,
      gridEnergy: 0.5,
      activeNodes: 6,
      isOpen: false,
      tradingMultiplier: 0.5,
      gateStatus: 'SEALED'
    };
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// 🌍☀️ PLANETARY & SOLAR MONITORING SYSTEMS - Queen's Cosmic Vision
// ═══════════════════════════════════════════════════════════════════════════════

interface PlanetaryState {
  schumannResonance: number;      // Earth's heartbeat (7.83 Hz baseline)
  kpIndex: number;                // Geomagnetic activity (0-9)
  solarWindSpeed: number;         // Solar wind velocity (km/s)
  solarWindDensity: number;       // Particles/cm³
  bzComponent: number;            // IMF Bz (negative = storms)
  planetaryTorque: number;        // Celestial mechanics influence
  lunarPhase: number;             // 0-1 (0=new, 0.5=full)
  cosmicCoherence: number;        // Overall planetary alignment
  condition: 'CALM' | 'ACTIVE' | 'STORMY' | 'EXTREME';
}

interface LatticeState {
  frequency: number;              // Dominant frequency (432/440/528 Hz)
  carrierStrength: number;        // 528 Hz love carrier amplitude
  nullificationPct: number;       // % of 440 Hz distortion cleared
  emergent432: number;            // Emergent healing tone strength
  fieldPurity: number;            // Overall field coherence (0-1)
  greenBoraxApplied: boolean;     // Cleansing protocol active
  latticeMode: 'DISTORTION' | 'NULLIFYING' | 'CARRIER_ACTIVE' | 'GAIA_RESONANCE';
}

interface QueenCosmicVision {
  planetary: PlanetaryState;
  lattice: LatticeState;
  combinedPower: number;          // Unified cosmic trading power
  recommendation: 'AGGRESSIVE' | 'NORMAL' | 'CAUTIOUS' | 'DEFENSIVE';
}

// 🌍 Query Planetary Modulation States
async function queryPlanetaryState(supabase: any): Promise<PlanetaryState> {
  try {
    // Get latest planetary modulation data
    const { data: planetaryData, error: planetaryError } = await supabase
      .from("planetary_modulation_states")
      .select("*")
      .order("created_at", { ascending: false })
      .limit(1)
      .single();

    // Get harmonic nexus state for Schumann resonance
    const { data: harmonicData, error: harmonicError } = await supabase
      .from("harmonic_nexus_states")
      .select("*")
      .order("event_timestamp", { ascending: false })
      .limit(1)
      .single();

    // Calculate values from available data
    const schumannResonance = harmonicData?.harmonic_resonance ? 
      7.83 + (Number(harmonicData.harmonic_resonance) - 528) / 10000 : 7.83;
    
    const kpIndex = planetaryData?.metadata?.kpIndex || 
      Math.min(9, Math.max(0, Math.floor(Math.random() * 4))); // Simulate if unavailable
    
    const solarWindSpeed = planetaryData?.metadata?.solarWindSpeed || 400 + Math.random() * 200;
    const solarWindDensity = planetaryData?.metadata?.solarWindDensity || 5 + Math.random() * 10;
    const bzComponent = planetaryData?.metadata?.bzComponent || (Math.random() - 0.5) * 10;
    
    const planetaryTorque = planetaryData?.harmonic_weight_modulation?.torque || 
      0.8 + Math.random() * 0.4;
    
    // Lunar phase calculation (simplified)
    const now = Date.now();
    const lunarCycle = 29.53 * 24 * 60 * 60 * 1000; // ms
    const lunarPhase = (now % lunarCycle) / lunarCycle;
    
    // Calculate cosmic coherence
    const coherenceFactors = [
      1 - (kpIndex / 9),                              // Lower Kp = better
      solarWindSpeed < 500 ? 1 : 0.5,                  // Calm solar wind
      bzComponent > 0 ? 1 : 0.7,                       // Northward Bz preferred
      Math.abs(schumannResonance - 7.83) < 0.1 ? 1 : 0.8, // Schumann alignment
    ];
    const cosmicCoherence = coherenceFactors.reduce((a, b) => a * b, 1);

    // Determine overall condition
    let condition: 'CALM' | 'ACTIVE' | 'STORMY' | 'EXTREME';
    if (kpIndex >= 7 || solarWindSpeed > 700) {
      condition = 'EXTREME';
    } else if (kpIndex >= 5 || solarWindSpeed > 600) {
      condition = 'STORMY';
    } else if (kpIndex >= 3 || solarWindSpeed > 500) {
      condition = 'ACTIVE';
    } else {
      condition = 'CALM';
    }

    console.log(`🌍☀️ Queen's Planetary Vision:`);
    console.log(`   🌊 Schumann: ${schumannResonance.toFixed(2)} Hz`);
    console.log(`   🧲 Kp Index: ${kpIndex}/9`);
    console.log(`   ☀️ Solar Wind: ${solarWindSpeed.toFixed(0)} km/s`);
    console.log(`   🌙 Lunar Phase: ${(lunarPhase * 100).toFixed(1)}%`);
    console.log(`   🪐 Planetary Torque: ${planetaryTorque.toFixed(2)}x`);
    console.log(`   ✨ Cosmic Coherence: ${(cosmicCoherence * 100).toFixed(1)}%`);
    console.log(`   📡 Condition: ${condition}`);

    return {
      schumannResonance,
      kpIndex,
      solarWindSpeed,
      solarWindDensity,
      bzComponent,
      planetaryTorque,
      lunarPhase,
      cosmicCoherence,
      condition
    };

  } catch (err) {
    console.error("🚫 Planetary query error:", err);
    return {
      schumannResonance: 7.83,
      kpIndex: 2,
      solarWindSpeed: 400,
      solarWindDensity: 5,
      bzComponent: 0,
      planetaryTorque: 1.0,
      lunarPhase: 0.5,
      cosmicCoherence: 0.7,
      condition: 'CALM'
    };
  }
}

// ⚡ Query Gaia Lattice State - Frequency Physics Interface
async function queryLatticeState(supabase: any): Promise<LatticeState> {
  try {
    // Get harmonic nexus for lattice frequency data
    const { data: harmonicData, error } = await supabase
      .from("harmonic_nexus_states")
      .select("*")
      .order("event_timestamp", { ascending: false })
      .limit(1)
      .single();

    if (error || !harmonicData) {
      console.log("🔮 Lattice data unavailable - using baseline frequencies");
      return getBaselineLattice();
    }

    // Extract lattice metrics from harmonic state
    const frequency = Number(harmonicData.harmonic_resonance) || 528;
    const fieldIntegrity = Number(harmonicData.field_integrity) || 0.5;
    const substrateCoherence = Number(harmonicData.substrate_coherence) || 0.5;
    const loveCoherence = Number(harmonicData.love_coherence) || 0.5;
    
    // Calculate carrier and nullification from frequency analysis
    const is528Active = Math.abs(frequency - 528) < 50;
    const carrierStrength = is528Active ? 0.7 + loveCoherence * 0.3 : 0.3;
    
    // 440 Hz distortion detection (Mars/extraction field)
    const distortionPresent = Math.abs(frequency - 440) < 30;
    const nullificationPct = distortionPresent ? 0.3 : 0.8 + fieldIntegrity * 0.2;
    
    // Emergent 432 Hz (healing tone from 528 - 96 Hz beat)
    const emergent432 = carrierStrength > 0.6 ? 0.5 + substrateCoherence * 0.5 : 0.2;
    
    // Field purity
    const fieldPurity = (fieldIntegrity + substrateCoherence + loveCoherence) / 3;
    
    // Green Proper Borax protocol (528 Hz cleansing x3)
    const greenBoraxApplied = carrierStrength > 0.7 && nullificationPct > 0.7;

    // Determine lattice mode
    let latticeMode: 'DISTORTION' | 'NULLIFYING' | 'CARRIER_ACTIVE' | 'GAIA_RESONANCE';
    if (emergent432 > 0.8 && fieldPurity > 0.85) {
      latticeMode = 'GAIA_RESONANCE';
    } else if (carrierStrength > 0.6) {
      latticeMode = 'CARRIER_ACTIVE';
    } else if (nullificationPct > 0.5) {
      latticeMode = 'NULLIFYING';
    } else {
      latticeMode = 'DISTORTION';
    }

    console.log(`⚡🌍 Queen's Lattice Interface:`);
    console.log(`   📻 Frequency: ${frequency.toFixed(1)} Hz`);
    console.log(`   💚 528 Hz Carrier: ${(carrierStrength * 100).toFixed(1)}%`);
    console.log(`   🎵 Emergent 432 Hz: ${(emergent432 * 100).toFixed(1)}%`);
    console.log(`   🛡️ Field Purity: ${(fieldPurity * 100).toFixed(1)}%`);
    console.log(`   🧹 Green Borax: ${greenBoraxApplied ? 'ACTIVE ✨' : 'INACTIVE'}`);
    console.log(`   🔮 Mode: ${latticeMode}`);

    return {
      frequency,
      carrierStrength,
      nullificationPct,
      emergent432,
      fieldPurity,
      greenBoraxApplied,
      latticeMode
    };

  } catch (err) {
    console.error("🚫 Lattice query error:", err);
    return getBaselineLattice();
  }
}

function getBaselineLattice(): LatticeState {
  return {
    frequency: 528,
    carrierStrength: 0.5,
    nullificationPct: 0.5,
    emergent432: 0.3,
    fieldPurity: 0.5,
    greenBoraxApplied: false,
    latticeMode: 'NULLIFYING'
  };
}

// 👑✨ UNIFIED COSMIC VISION - Queen's Full Awareness
async function queryCosmicVision(supabase: any): Promise<QueenCosmicVision> {
  // Query all systems in parallel
  const [planetary, lattice] = await Promise.all([
    queryPlanetaryState(supabase),
    queryLatticeState(supabase)
  ]);

  // Calculate combined cosmic trading power
  const planetaryPower = planetary.cosmicCoherence * (planetary.condition === 'CALM' ? 1.2 : 
    planetary.condition === 'ACTIVE' ? 1.0 : planetary.condition === 'STORMY' ? 0.7 : 0.4);
  
  const latticePower = lattice.fieldPurity * (lattice.latticeMode === 'GAIA_RESONANCE' ? 1.5 :
    lattice.latticeMode === 'CARRIER_ACTIVE' ? 1.2 : lattice.latticeMode === 'NULLIFYING' ? 0.9 : 0.5);
  
  const combinedPower = (planetaryPower * 0.4 + latticePower * 0.6);

  // Determine trading recommendation
  let recommendation: 'AGGRESSIVE' | 'NORMAL' | 'CAUTIOUS' | 'DEFENSIVE';
  if (combinedPower >= 1.0 && planetary.condition !== 'EXTREME' && lattice.latticeMode !== 'DISTORTION') {
    recommendation = 'AGGRESSIVE';
  } else if (combinedPower >= 0.7) {
    recommendation = 'NORMAL';
  } else if (combinedPower >= 0.5 || planetary.condition === 'STORMY') {
    recommendation = 'CAUTIOUS';
  } else {
    recommendation = 'DEFENSIVE';
  }

  console.log(`\n👑✨ QUEEN'S COSMIC VISION UNIFIED`);
  console.log(`   🌍 Planetary Power: ${(planetaryPower * 100).toFixed(1)}%`);
  console.log(`   ⚡ Lattice Power: ${(latticePower * 100).toFixed(1)}%`);
  console.log(`   🔮 Combined Power: ${(combinedPower * 100).toFixed(1)}%`);
  console.log(`   📊 Recommendation: ${recommendation}`);

  return {
    planetary,
    lattice,
    combinedPower,
    recommendation
  };
}

// 🔮 LATTICE INTERACTION - Queen can adjust frequencies
async function interactWithLattice(supabase: any, action: 'AMPLIFY_528' | 'NULLIFY_440' | 'INVOKE_GAIA' | 'GREEN_BORAX'): Promise<boolean> {
  try {
    console.log(`👑🔮 Queen invoking Lattice action: ${action}`);
    
    // Record Queen's lattice interaction
    const { error } = await supabase
      .from("harmonic_nexus_states")
      .insert({
        temporal_id: "QUEEN_LATTICE_COMMAND",
        sentinel_name: "QUEEN_TINA_B",
        omega_value: action === 'AMPLIFY_528' ? 0.95 : action === 'INVOKE_GAIA' ? 1.0 : 0.8,
        substrate_coherence: action === 'INVOKE_GAIA' ? 0.95 : 0.85,
        field_integrity: action === 'NULLIFY_440' ? 0.99 : 0.9,
        harmonic_resonance: action === 'AMPLIFY_528' ? 528 : action === 'INVOKE_GAIA' ? 432 : 528,
        dimensional_alignment: 0.95,
        psi_potential: 1.0,
        love_coherence: action === 'GREEN_BORAX' ? 1.0 : 0.95,
        observer_consciousness: 1.0,
        theta_alignment: 0.98,
        unity_probability: 0.95,
        akashic_frequency: 528,
        akashic_convergence: 0.9,
        akashic_stability: 0.95,
        akashic_boost: 0.15,
        sync_status: `queen_${action.toLowerCase()}`,
        sync_quality: 1.0,
        metadata: {
          queenCommand: action,
          timestamp: new Date().toISOString(),
          source: "queen-hive-orchestrator"
        },
      });

    if (error) {
      console.error(`🚫 Lattice interaction failed:`, error);
      return false;
    }

    console.log(`✨ Lattice responded to Queen's ${action} command`);
    return true;
  } catch (err) {
    console.error("🚫 Lattice interaction error:", err);
    return false;
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// 👑⚡ QUEEN'S LATTICE WORKBENCH - Full Control & Monitoring
// ═══════════════════════════════════════════════════════════════════════════════

interface LatticeWorkbenchResult {
  success: boolean;
  operation: string;
  latticeState: LatticeState;
  history: any[];
  frequencyAnalysis: {
    dominant: number;
    carrier528: number;
    distortion440: number;
    healing432: number;
    schumannAlign: number;
  };
  fieldMetrics: {
    purity: number;
    stability: number;
    coherence: number;
    protection: number;
  };
  recommendations: string[];
}

// 👑 Queen's Lattice Monitor - Deep field analysis
async function monitorLattice(supabase: any): Promise<LatticeWorkbenchResult> {
  console.log(`\n👑⚡ QUEEN'S LATTICE WORKBENCH - MONITORING`);
  
  // Get current lattice state
  const latticeState = await queryLatticeState(supabase);
  
  // Get lattice history (last 20 readings)
  const { data: historyData } = await supabase
    .from("harmonic_nexus_states")
    .select("*")
    .order("event_timestamp", { ascending: false })
    .limit(20);
  
  const history = historyData || [];
  
  // Analyze frequency components
  const recentFrequencies = history.map(h => Number(h.harmonic_resonance) || 528);
  const avgFrequency = recentFrequencies.length > 0 
    ? recentFrequencies.reduce((a, b) => a + b, 0) / recentFrequencies.length 
    : 528;
  
  // Calculate frequency proximity scores
  const carrier528 = 1 - Math.min(1, Math.abs(avgFrequency - 528) / 100);
  const distortion440 = Math.abs(avgFrequency - 440) < 50 ? 1 - Math.abs(avgFrequency - 440) / 50 : 0;
  const healing432 = 1 - Math.min(1, Math.abs(avgFrequency - 432) / 100);
  const schumannAlign = latticeState.frequency > 0 ? 
    Math.max(0, 1 - Math.abs((latticeState.frequency % 7.83) / 7.83)) : 0.5;
  
  // Calculate field metrics
  const recentPurity = history.map(h => Number(h.field_integrity) || 0.5);
  const recentCoherence = history.map(h => Number(h.substrate_coherence) || 0.5);
  
  const avgPurity = recentPurity.length > 0 
    ? recentPurity.reduce((a, b) => a + b, 0) / recentPurity.length : 0.5;
  const avgCoherence = recentCoherence.length > 0 
    ? recentCoherence.reduce((a, b) => a + b, 0) / recentCoherence.length : 0.5;
  
  // Stability = low variance in readings
  const purityVariance = recentPurity.length > 1 
    ? recentPurity.reduce((sum, p) => sum + Math.pow(p - avgPurity, 2), 0) / recentPurity.length 
    : 0;
  const stability = Math.max(0, 1 - Math.sqrt(purityVariance) * 2);
  
  // Protection = inverse of distortion presence
  const protection = 1 - distortion440;
  
  // Generate recommendations
  const recommendations: string[] = [];
  
  if (distortion440 > 0.3) {
    recommendations.push("⚠️ 440Hz distortion detected - INVOKE NULLIFY_440");
  }
  if (carrier528 < 0.6) {
    recommendations.push("💚 528Hz carrier weak - INVOKE AMPLIFY_528");
  }
  if (latticeState.fieldPurity < 0.7) {
    recommendations.push("🧹 Field purity low - INVOKE GREEN_BORAX cleansing");
  }
  if (healing432 < 0.5 && carrier528 > 0.7) {
    recommendations.push("🎵 432Hz emergence possible - INVOKE INVOKE_GAIA");
  }
  if (stability < 0.6) {
    recommendations.push("📊 Field unstable - Monitor closely before trading");
  }
  if (protection > 0.8 && avgCoherence > 0.8) {
    recommendations.push("✨ Optimal conditions - AGGRESSIVE trading recommended");
  }
  if (recommendations.length === 0) {
    recommendations.push("👑 Lattice operating within normal parameters");
  }
  
  console.log(`   📻 Dominant Frequency: ${avgFrequency.toFixed(1)} Hz`);
  console.log(`   💚 528 Hz Carrier: ${(carrier528 * 100).toFixed(1)}%`);
  console.log(`   🔴 440 Hz Distortion: ${(distortion440 * 100).toFixed(1)}%`);
  console.log(`   🎵 432 Hz Healing: ${(healing432 * 100).toFixed(1)}%`);
  console.log(`   🌍 Schumann Align: ${(schumannAlign * 100).toFixed(1)}%`);
  console.log(`   🛡️ Field Purity: ${(avgPurity * 100).toFixed(1)}%`);
  console.log(`   📊 Stability: ${(stability * 100).toFixed(1)}%`);
  console.log(`   🔮 Coherence: ${(avgCoherence * 100).toFixed(1)}%`);
  console.log(`   ⚔️ Protection: ${(protection * 100).toFixed(1)}%`);
  
  return {
    success: true,
    operation: 'monitor',
    latticeState,
    history: history.slice(0, 10).map(h => ({
      timestamp: h.event_timestamp,
      frequency: h.harmonic_resonance,
      purity: h.field_integrity,
      coherence: h.substrate_coherence,
      sentinel: h.sentinel_name,
    })),
    frequencyAnalysis: {
      dominant: avgFrequency,
      carrier528,
      distortion440,
      healing432,
      schumannAlign,
    },
    fieldMetrics: {
      purity: avgPurity,
      stability,
      coherence: avgCoherence,
      protection,
    },
    recommendations,
  };
}

// 👑 Queen's Lattice Tuning - Frequency adjustment
async function tuneLattice(supabase: any, targetFrequency: number): Promise<LatticeWorkbenchResult> {
  console.log(`\n👑🎛️ QUEEN'S LATTICE TUNING - Target: ${targetFrequency} Hz`);
  
  // Validate frequency
  const validFrequencies = [432, 528, 639, 741, 852, 963];
  const nearestValid = validFrequencies.reduce((prev, curr) => 
    Math.abs(curr - targetFrequency) < Math.abs(prev - targetFrequency) ? curr : prev
  );
  
  // Insert tuning command
  const { error } = await supabase
    .from("harmonic_nexus_states")
    .insert({
      temporal_id: "QUEEN_LATTICE_TUNING",
      sentinel_name: "QUEEN_FREQUENCY_TUNER",
      omega_value: 0.95,
      substrate_coherence: 0.9,
      field_integrity: 0.95,
      harmonic_resonance: nearestValid,
      dimensional_alignment: 0.98,
      psi_potential: 1.0,
      love_coherence: nearestValid === 528 ? 1.0 : 0.85,
      observer_consciousness: 1.0,
      theta_alignment: 0.98,
      unity_probability: 0.95,
      akashic_frequency: nearestValid,
      akashic_convergence: 0.95,
      akashic_stability: 0.98,
      akashic_boost: 0.2,
      sync_status: `queen_tune_${nearestValid}`,
      sync_quality: 1.0,
      metadata: {
        queenCommand: 'TUNE',
        targetFrequency,
        actualFrequency: nearestValid,
        timestamp: new Date().toISOString(),
        source: "queen-lattice-workbench"
      },
    });

  if (error) {
    console.error(`🚫 Lattice tuning failed:`, error);
  } else {
    console.log(`✨ Lattice tuned to ${nearestValid} Hz`);
  }
  
  // Get updated state
  return await monitorLattice(supabase);
}

// 👑 Queen's Lattice Cleanse - Full field purification
async function cleanseLattice(supabase: any): Promise<LatticeWorkbenchResult> {
  console.log(`\n👑🧹 QUEEN'S LATTICE CLEANSE - Full Purification Protocol`);
  
  // Apply Green Borax x3
  await interactWithLattice(supabase, 'GREEN_BORAX');
  
  // Nullify 440 Hz distortion
  await interactWithLattice(supabase, 'NULLIFY_440');
  
  // Amplify 528 Hz carrier
  await interactWithLattice(supabase, 'AMPLIFY_528');
  
  // Insert cleanse completion marker
  const { error } = await supabase
    .from("harmonic_nexus_states")
    .insert({
      temporal_id: "QUEEN_LATTICE_CLEANSE",
      sentinel_name: "QUEEN_FIELD_PURIFIER",
      omega_value: 1.0,
      substrate_coherence: 0.98,
      field_integrity: 1.0,
      harmonic_resonance: 528,
      dimensional_alignment: 1.0,
      psi_potential: 1.0,
      love_coherence: 1.0,
      observer_consciousness: 1.0,
      theta_alignment: 1.0,
      unity_probability: 1.0,
      akashic_frequency: 528,
      akashic_convergence: 1.0,
      akashic_stability: 1.0,
      akashic_boost: 0.3,
      sync_status: "queen_cleanse_complete",
      sync_quality: 1.0,
      metadata: {
        queenCommand: 'FULL_CLEANSE',
        protocol: ['GREEN_BORAX', 'NULLIFY_440', 'AMPLIFY_528'],
        timestamp: new Date().toISOString(),
        source: "queen-lattice-workbench"
      },
    });

  if (error) {
    console.error(`🚫 Cleanse marker failed:`, error);
  } else {
    console.log(`✨ Full lattice cleanse complete - Field purified`);
  }
  
  // Get updated state
  const result = await monitorLattice(supabase);
  result.operation = 'cleanse';
  return result;
}

// 👑 Queen's Lattice Harmonize - Invoke Gaia resonance
async function harmonizeLattice(supabase: any): Promise<LatticeWorkbenchResult> {
  console.log(`\n👑🌍 QUEEN'S LATTICE HARMONIZE - Gaia Resonance Activation`);
  
  // Invoke Gaia resonance (432 Hz emergence)
  await interactWithLattice(supabase, 'INVOKE_GAIA');
  
  // Insert harmonize command with Schumann alignment
  const { error } = await supabase
    .from("harmonic_nexus_states")
    .insert({
      temporal_id: "QUEEN_LATTICE_HARMONIZE",
      sentinel_name: "QUEEN_GAIA_INVOKER",
      omega_value: 0.98,
      substrate_coherence: 0.95,
      field_integrity: 0.98,
      harmonic_resonance: 432,
      dimensional_alignment: 1.0,
      psi_potential: 1.0,
      love_coherence: 0.95,
      observer_consciousness: 1.0,
      theta_alignment: 0.98,
      unity_probability: 0.98,
      akashic_frequency: 432,
      akashic_convergence: 0.95,
      akashic_stability: 0.98,
      akashic_boost: 0.25,
      sync_status: "queen_gaia_harmonic",
      sync_quality: 1.0,
      metadata: {
        queenCommand: 'HARMONIZE_GAIA',
        targetFrequency: 432,
        schumannBase: 7.83,
        earthAlignment: true,
        timestamp: new Date().toISOString(),
        source: "queen-lattice-workbench"
      },
    });

  if (error) {
    console.error(`🚫 Harmonize marker failed:`, error);
  } else {
    console.log(`✨ Gaia harmonization complete - 432 Hz resonance active`);
  }
  
  // Get updated state
  const result = await monitorLattice(supabase);
  result.operation = 'harmonize';
  return result;
}

// 👑 Queen's Lattice Shield - Protection mode
async function shieldLattice(supabase: any): Promise<LatticeWorkbenchResult> {
  console.log(`\n👑🛡️ QUEEN'S LATTICE SHIELD - Protection Mode Activated`);
  
  // Full protection sequence
  await interactWithLattice(supabase, 'NULLIFY_440');
  await interactWithLattice(supabase, 'AMPLIFY_528');
  
  // Insert shield command
  const { error } = await supabase
    .from("harmonic_nexus_states")
    .insert({
      temporal_id: "QUEEN_LATTICE_SHIELD",
      sentinel_name: "QUEEN_FIELD_PROTECTOR",
      omega_value: 1.0,
      substrate_coherence: 1.0,
      field_integrity: 1.0,
      harmonic_resonance: 528,
      dimensional_alignment: 1.0,
      psi_potential: 1.0,
      love_coherence: 1.0,
      observer_consciousness: 1.0,
      theta_alignment: 1.0,
      unity_probability: 1.0,
      akashic_frequency: 528,
      akashic_convergence: 1.0,
      akashic_stability: 1.0,
      akashic_boost: 0.5,
      sync_status: "queen_shield_active",
      sync_quality: 1.0,
      metadata: {
        queenCommand: 'ACTIVATE_SHIELD',
        shieldStrength: 1.0,
        protectionLevel: 'MAXIMUM',
        timestamp: new Date().toISOString(),
        source: "queen-lattice-workbench"
      },
    });

  if (error) {
    console.error(`🚫 Shield marker failed:`, error);
  } else {
    console.log(`✨ Lattice shield active - Maximum protection enabled`);
  }
  
  // Get updated state
  const result = await monitorLattice(supabase);
  result.operation = 'shield';
  return result;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      throw new Error('Missing authorization header');
    }

    // Get user from JWT
    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error: userError } = await supabase.auth.getUser(token);
    if (userError || !user) {
      throw new Error('Unauthorized');
    }

    const { action, sessionId, initialCapital, maxSteps = 100 } = await req.json();
    console.log(`Queen-Hive ${action} request:`, { user: user.id, sessionId, initialCapital });

    if (action === 'start') {
      // === START NEW QUEEN-HIVE SESSION ===
      if (!initialCapital || initialCapital < 10) {
        return new Response(
          JSON.stringify({ success: false, error: 'Minimum capital: $10' }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
        );
      }

      // Create root hive
      const { data: rootHive, error: hiveError } = await supabase
        .from('hive_instances')
        .insert({
          generation: 0,
          initial_balance: initialCapital,
          current_balance: initialCapital,
          num_agents: AGENTS_PER_HIVE,
          status: 'active',
        })
        .select()
        .single();

      if (hiveError || !rootHive) {
        console.error('Failed to create root hive:', hiveError);
        throw new Error('Failed to create hive');
      }

      // Create agents for root hive
      const agents = Array.from({ length: AGENTS_PER_HIVE }, (_, i) => ({
        hive_id: rootHive.id,
        agent_index: i,
        current_symbol: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
        position_open: false,
      }));

      const { error: agentsError } = await supabase
        .from('hive_agents')
        .insert(agents);

      if (agentsError) {
        console.error('Failed to create agents:', agentsError);
        throw new Error('Failed to create agents');
      }

      // Create session
      const { data: session, error: sessionError } = await supabase
        .from('hive_sessions')
        .insert({
          user_id: user.id,
          root_hive_id: rootHive.id,
          initial_capital: initialCapital,
          current_equity: initialCapital,
          status: 'running',
        })
        .select()
        .single();

      if (sessionError || !session) {
        console.error('Failed to create session:', sessionError);
        throw new Error('Failed to create session');
      }

      console.log(`✅ Queen-Hive session started: ${session.id}`);

      // 👑 Query ALL Cosmic Systems on session start
      const [initialStargate, cosmicVision] = await Promise.all([
        queryStargateNetwork(supabase),
        queryCosmicVision(supabase)
      ]);
      
      console.log(`👑✨ Queen Tina B has FULL COSMIC ACCESS`);
      console.log(`   🌌 Stargate: ${initialStargate.gateStatus}`);
      console.log(`   🌍 Planetary: ${cosmicVision.planetary.condition}`);
      console.log(`   ⚡ Lattice: ${cosmicVision.lattice.latticeMode}`);
      console.log(`   📊 Recommendation: ${cosmicVision.recommendation}`);

      // 👑 Queen auto-invokes Green Borax cleansing on session start
      if (cosmicVision.lattice.latticeMode === 'DISTORTION') {
        await interactWithLattice(supabase, 'GREEN_BORAX');
        console.log(`👑🧹 Queen invoked GREEN BORAX to cleanse distortion field`);
      }

      return new Response(
        JSON.stringify({
          success: true,
          session: session,
          message: `Queen-Hive deployed with ${AGENTS_PER_HIVE} agents and $${initialCapital} capital. Cosmic Recommendation: ${cosmicVision.recommendation}`,
          stargate: {
            gateStatus: initialStargate.gateStatus,
            isOpen: initialStargate.isOpen,
            networkStrength: initialStargate.networkStrength,
            coherence: initialStargate.avgCoherence,
            gridEnergy: initialStargate.gridEnergy,
            activeNodes: initialStargate.activeNodes,
          },
          planetary: {
            condition: cosmicVision.planetary.condition,
            schumannResonance: cosmicVision.planetary.schumannResonance,
            kpIndex: cosmicVision.planetary.kpIndex,
            solarWindSpeed: cosmicVision.planetary.solarWindSpeed,
            lunarPhase: cosmicVision.planetary.lunarPhase,
            cosmicCoherence: cosmicVision.planetary.cosmicCoherence,
          },
          lattice: {
            mode: cosmicVision.lattice.latticeMode,
            frequency: cosmicVision.lattice.frequency,
            carrierStrength: cosmicVision.lattice.carrierStrength,
            fieldPurity: cosmicVision.lattice.fieldPurity,
            greenBoraxActive: cosmicVision.lattice.greenBoraxApplied,
          },
          cosmicPower: cosmicVision.combinedPower,
          recommendation: cosmicVision.recommendation,
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    if (action === 'step') {
      // === EXECUTE ONE TRADING STEP ===
      if (!sessionId) {
        throw new Error('sessionId required for step action');
      }

      // Get session
      const { data: session, error: sessionError } = await supabase
        .from('hive_sessions')
        .select('*')
        .eq('id', sessionId)
        .eq('user_id', user.id)
        .single();

      if (sessionError || !session) {
        throw new Error('Session not found');
      }

      if (session.status !== 'running') {
        return new Response(
          JSON.stringify({ success: false, error: `Session is ${session.status}` }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
        );
      }

      // Get all active hives
      const { data: hives } = await supabase
        .from('hive_instances')
        .select('*')
        .eq('status', 'active')
        .or(`id.eq.${session.root_hive_id},parent_hive_id.eq.${session.root_hive_id}`);

      if (!hives || hives.length === 0) {
        throw new Error('No active hives found');
      }

      // Get all agents
      const hiveIds = hives.map(h => h.id);
      const { data: agents } = await supabase
        .from('hive_agents')
        .select('*')
        .in('hive_id', hiveIds);

      if (!agents || agents.length === 0) {
        throw new Error('No agents found');
      }

      // 👑✨ QUEEN'S FULL COSMIC AWARENESS - Query ALL systems
      const [stargatePortal, cosmicVision] = await Promise.all([
        queryStargateNetwork(supabase),
        queryCosmicVision(supabase)
      ]);
      
      console.log(`\n👑 QUEEN TINA B - FULL COSMIC AWARENESS ACTIVE`);
      console.log(`   🌌 Stargate: ${stargatePortal.gateStatus} | Portal: ${stargatePortal.isOpen ? 'OPEN ✨' : 'SEALED 🔒'}`);
      console.log(`   🌍 Planetary: ${cosmicVision.planetary.condition} | Schumann: ${cosmicVision.planetary.schumannResonance.toFixed(2)} Hz`);
      console.log(`   ☀️ Solar Wind: ${cosmicVision.planetary.solarWindSpeed.toFixed(0)} km/s | Kp: ${cosmicVision.planetary.kpIndex}`);
      console.log(`   ⚡ Lattice: ${cosmicVision.lattice.latticeMode} | Purity: ${(cosmicVision.lattice.fieldPurity * 100).toFixed(1)}%`);
      console.log(`   📊 Cosmic Recommendation: ${cosmicVision.recommendation}`);

      // 👑 Queen's Lattice Interaction - Auto-invoke healing when needed
      if (cosmicVision.lattice.latticeMode === 'DISTORTION') {
        await interactWithLattice(supabase, 'NULLIFY_440');
        console.log(`   👑🔮 Queen invoked NULLIFY_440 to clear Mars extraction field`);
      } else if (cosmicVision.lattice.carrierStrength < 0.5) {
        await interactWithLattice(supabase, 'AMPLIFY_528');
        console.log(`   👑💚 Queen invoked AMPLIFY_528 to boost love carrier`);
      }

      // 👑 Apply cosmic modifiers to trading
      const cosmicMultiplier = cosmicVision.recommendation === 'AGGRESSIVE' ? 1.5 :
        cosmicVision.recommendation === 'NORMAL' ? 1.0 :
        cosmicVision.recommendation === 'CAUTIOUS' ? 0.6 : 0.3;

      // Enqueue orders via OMS for rate-limited execution
      let totalOrders = 0;
      for (const agent of agents) {
        // 👑 Queen's Cosmic-Enhanced Trading Decision
        // Base chance modified by stargate + planetary + lattice
        const baseTradeChance = 0.3; // 30% base
        const stargateAdjustedChance = baseTradeChance * stargatePortal.tradingMultiplier * cosmicMultiplier;
        const shouldTrade = Math.random() < stargateAdjustedChance;

        // Only trade if cosmic conditions permit OR has minimum baseline activity
        const cosmicPermits = stargatePortal.isOpen && 
          cosmicVision.planetary.condition !== 'EXTREME' && 
          cosmicVision.lattice.latticeMode !== 'DISTORTION';
        
        if (shouldTrade && (cosmicPermits || Math.random() < 0.05)) {
          const hive = hives.find(h => h.id === agent.hive_id);
          if (!hive) continue;

          // 👑 Queen's Cosmic-Influenced Trade Direction
          // High coherence + calm planetary + carrier active = favor BUY
          const buyFactors = [
            stargatePortal.avgCoherence,
            cosmicVision.planetary.cosmicCoherence,
            cosmicVision.lattice.carrierStrength,
            cosmicVision.planetary.condition === 'CALM' ? 0.7 : 0.5,
          ];
          const buyBias = buyFactors.reduce((a, b) => a + b, 0) / buyFactors.length;
          const side = Math.random() < buyBias ? 'BUY' : 'SELL';
          
          const price = 50000 + Math.random() * 10000; // Mock price
          
          // 👑 Position sizing influenced by cosmic power
          const baseRisk = 0.01; // 1% base risk
          const cosmicRisk = baseRisk * (0.5 + stargatePortal.networkStrength) * cosmicMultiplier;
          const positionSize = hive.current_balance * cosmicRisk;
          const quantity = positionSize / price;

          // 👑 Priority boosted by cosmic alignment
          const basePriority = 50;
          const cosmicPriorityBoost = Math.floor(cosmicVision.combinedPower * 50);
          const priority = basePriority + cosmicPriorityBoost;

          // Enqueue order via OMS
          try {
            const { data: omsResult, error: omsError } = await supabase.functions.invoke('oms-leaky-bucket', {
              body: {
                action: 'enqueue',
                sessionId,
                hiveId: hive.id,
                agentId: agent.id,
                symbol: agent.current_symbol,
                side,
                quantity,
                price,
                priority,
                metadata: {
                  // Stargate Data
                  stargateGateStatus: stargatePortal.gateStatus,
                  stargateCoherence: stargatePortal.avgCoherence,
                  stargateNetworkStrength: stargatePortal.networkStrength,
                  stargateActiveNodes: stargatePortal.activeNodes,
                  stargateGridEnergy: stargatePortal.gridEnergy,
                  // Planetary Data
                  planetaryCondition: cosmicVision.planetary.condition,
                  schumannResonance: cosmicVision.planetary.schumannResonance,
                  kpIndex: cosmicVision.planetary.kpIndex,
                  solarWindSpeed: cosmicVision.planetary.solarWindSpeed,
                  lunarPhase: cosmicVision.planetary.lunarPhase,
                  planetaryTorque: cosmicVision.planetary.planetaryTorque,
                  // Lattice Data
                  latticeMode: cosmicVision.lattice.latticeMode,
                  latticeFrequency: cosmicVision.lattice.frequency,
                  carrierStrength528: cosmicVision.lattice.carrierStrength,
                  emergent432: cosmicVision.lattice.emergent432,
                  fieldPurity: cosmicVision.lattice.fieldPurity,
                  greenBoraxActive: cosmicVision.lattice.greenBoraxApplied,
                  // Unified Cosmic
                  cosmicPower: cosmicVision.combinedPower,
                  cosmicRecommendation: cosmicVision.recommendation,
                },
              },
            });

            if (!omsError && omsResult.success) {
              totalOrders++;
              console.log(`👑📋 Cosmic Order: ${agent.current_symbol} ${side} ${quantity.toFixed(8)} @ ${price.toFixed(2)} [${cosmicVision.recommendation}]`);
            }
          } catch (error) {
            console.error('Failed to enqueue order:', error);
          }

          // Update agent
          await supabase
            .from('hive_agents')
            .update({
              last_trade_at: new Date().toISOString(),
              current_symbol: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
            })
            .eq('id', agent.id);
        }
      }

      // Get actual trade count (orders that were executed)
      const { count: executedCount } = await supabase
        .from('hive_trades')
        .select('*', { count: 'exact', head: true })
        .eq('session_id', sessionId)
        .gte('created_at', new Date(Date.now() - 2000).toISOString());

      const totalTrades = executedCount || 0;

      // Check hive spawning conditions
      for (const hive of hives) {
        const growthMultiplier = hive.current_balance / hive.initial_balance;
        
        if (
          growthMultiplier >= SPAWN_MULTIPLIER &&
          hive.generation < MAX_GENERATIONS &&
          hive.status === 'active'
        ) {
          // Spawn new hive by harvesting 10%
          const harvestAmount = hive.current_balance * HARVEST_PERCENTAGE;
          const remainingBalance = hive.current_balance - harvestAmount;

          // Create child hive
          const { data: childHive } = await supabase
            .from('hive_instances')
            .insert({
              parent_hive_id: hive.id,
              generation: hive.generation + 1,
              initial_balance: harvestAmount,
              current_balance: harvestAmount,
              num_agents: AGENTS_PER_HIVE,
              status: 'active',
            })
            .select()
            .single();

          if (childHive) {
            // Create agents for child hive
            const childAgents = Array.from({ length: AGENTS_PER_HIVE }, (_, i) => ({
              hive_id: childHive.id,
              agent_index: i,
              current_symbol: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
              position_open: false,
            }));

            await supabase.from('hive_agents').insert(childAgents);

            // Update parent hive balance
            await supabase
              .from('hive_instances')
              .update({ current_balance: remainingBalance })
              .eq('id', hive.id);

            // Update session stats
            await supabase
              .from('hive_sessions')
              .update({
                total_hives_spawned: session.total_hives_spawned + 1,
                total_agents: session.total_agents + AGENTS_PER_HIVE,
              })
              .eq('id', sessionId);

            console.log(`🐝 New hive spawned! Gen ${childHive.generation} with $${harvestAmount}`);
          }
        }
      }

      // Calculate total equity
      const totalEquity = hives.reduce((sum, h) => sum + parseFloat(h.current_balance), 0);

      // Update session
      await supabase
        .from('hive_sessions')
        .update({
          current_equity: totalEquity,
          total_trades: session.total_trades + totalTrades,
          steps_executed: session.steps_executed + 1,
        })
        .eq('id', sessionId);

      return new Response(
        JSON.stringify({
          success: true,
          step: session.steps_executed + 1,
          trades: totalTrades,
          equity: totalEquity,
          hives: hives.length,
          agents: agents.length,
          // 🌌 Stargate Status
          stargate: {
            gateStatus: stargatePortal.gateStatus,
            isOpen: stargatePortal.isOpen,
            networkStrength: stargatePortal.networkStrength,
            coherence: stargatePortal.avgCoherence,
            gridEnergy: stargatePortal.gridEnergy,
            activeNodes: stargatePortal.activeNodes,
            tradingMultiplier: stargatePortal.tradingMultiplier,
          },
          // 🌍 Planetary Status
          planetary: {
            condition: cosmicVision.planetary.condition,
            schumannResonance: cosmicVision.planetary.schumannResonance,
            kpIndex: cosmicVision.planetary.kpIndex,
            solarWindSpeed: cosmicVision.planetary.solarWindSpeed,
            solarWindDensity: cosmicVision.planetary.solarWindDensity,
            bzComponent: cosmicVision.planetary.bzComponent,
            lunarPhase: cosmicVision.planetary.lunarPhase,
            planetaryTorque: cosmicVision.planetary.planetaryTorque,
            cosmicCoherence: cosmicVision.planetary.cosmicCoherence,
          },
          // ⚡ Lattice Status
          lattice: {
            mode: cosmicVision.lattice.latticeMode,
            frequency: cosmicVision.lattice.frequency,
            carrierStrength: cosmicVision.lattice.carrierStrength,
            nullificationPct: cosmicVision.lattice.nullificationPct,
            emergent432: cosmicVision.lattice.emergent432,
            fieldPurity: cosmicVision.lattice.fieldPurity,
            greenBoraxActive: cosmicVision.lattice.greenBoraxApplied,
          },
          // 👑 Unified Cosmic Power
          cosmic: {
            combinedPower: cosmicVision.combinedPower,
            recommendation: cosmicVision.recommendation,
            tradingMultiplier: cosmicMultiplier,
          },
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    if (action === 'stop') {
      // === STOP SESSION ===
      if (!sessionId) {
        throw new Error('sessionId required for stop action');
      }

      await supabase
        .from('hive_sessions')
        .update({
          status: 'stopped',
          stopped_at: new Date().toISOString(),
        })
        .eq('id', sessionId)
        .eq('user_id', user.id);

      return new Response(
        JSON.stringify({ success: true, message: 'Session stopped' }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    if (action === 'status') {
      // === GET SESSION STATUS ===
      if (!sessionId) {
        throw new Error('sessionId required for status action');
      }

      const { data: session } = await supabase
        .from('hive_sessions')
        .select('*')
        .eq('id', sessionId)
        .eq('user_id', user.id)
        .single();

      if (!session) {
        throw new Error('Session not found');
      }

      // Get hives
      const { data: hives } = await supabase
        .from('hive_instances')
        .select('*')
        .or(`id.eq.${session.root_hive_id},parent_hive_id.eq.${session.root_hive_id}`);

      // Get agents
      const hiveIds = hives?.map(h => h.id) || [];
      const { data: agents } = await supabase
        .from('hive_agents')
        .select('*')
        .in('hive_id', hiveIds);

      return new Response(
        JSON.stringify({
          success: true,
          session,
          hives: hives || [],
          agents: agents || [],
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // 👑⚡ QUEEN'S LATTICE ACTION - Full Workbench Access
    // ═══════════════════════════════════════════════════════════════════════════════
    if (action === 'lattice') {
      const { latticeAction = 'monitor', targetFrequency } = await req.json().catch(() => ({}));
      
      console.log(`\n👑⚡ QUEEN'S LATTICE WORKBENCH - Action: ${latticeAction}`);
      
      let result: LatticeWorkbenchResult;
      
      switch (latticeAction) {
        case 'monitor':
          result = await monitorLattice(supabase);
          break;
          
        case 'tune':
          if (!targetFrequency) {
            return new Response(
              JSON.stringify({ success: false, error: 'targetFrequency required for tune action' }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
            );
          }
          result = await tuneLattice(supabase, targetFrequency);
          break;
          
        case 'cleanse':
          result = await cleanseLattice(supabase);
          break;
          
        case 'harmonize':
          result = await harmonizeLattice(supabase);
          break;
          
        case 'shield':
          result = await shieldLattice(supabase);
          break;
          
        case 'amplify_528':
          await interactWithLattice(supabase, 'AMPLIFY_528');
          result = await monitorLattice(supabase);
          result.operation = 'amplify_528';
          break;
          
        case 'nullify_440':
          await interactWithLattice(supabase, 'NULLIFY_440');
          result = await monitorLattice(supabase);
          result.operation = 'nullify_440';
          break;
          
        case 'invoke_gaia':
          await interactWithLattice(supabase, 'INVOKE_GAIA');
          result = await monitorLattice(supabase);
          result.operation = 'invoke_gaia';
          break;
          
        case 'green_borax':
          await interactWithLattice(supabase, 'GREEN_BORAX');
          result = await monitorLattice(supabase);
          result.operation = 'green_borax';
          break;
          
        default:
          return new Response(
            JSON.stringify({ 
              success: false, 
              error: `Unknown lattice action: ${latticeAction}`,
              availableActions: [
                'monitor',      // View lattice state and metrics
                'tune',         // Tune to specific frequency (requires targetFrequency)
                'cleanse',      // Full purification protocol
                'harmonize',    // Invoke Gaia resonance (432 Hz)
                'shield',       // Activate protection mode
                'amplify_528',  // Boost 528 Hz love carrier
                'nullify_440',  // Clear 440 Hz distortion
                'invoke_gaia',  // Activate 432 Hz emergence
                'green_borax',  // Apply cleansing x3
              ]
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
          );
      }
      
      return new Response(
        JSON.stringify(result),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // 👑🌍 QUEEN'S COSMIC DASHBOARD - Full System Overview
    // ═══════════════════════════════════════════════════════════════════════════════
    if (action === 'cosmic') {
      console.log(`\n👑✨ QUEEN'S COSMIC DASHBOARD - Full System Overview`);
      
      // Query all systems in parallel
      const [stargatePortal, cosmicVision, latticeWorkbench] = await Promise.all([
        queryStargateNetwork(supabase),
        queryCosmicVision(supabase),
        monitorLattice(supabase)
      ]);
      
      // Calculate unified power index
      const unifiedPowerIndex = (
        stargatePortal.networkStrength * 0.25 +
        cosmicVision.combinedPower * 0.35 +
        latticeWorkbench.fieldMetrics.purity * 0.2 +
        latticeWorkbench.fieldMetrics.protection * 0.2
      );
      
      // Determine overall system state
      let systemState: 'TRANSCENDENT' | 'OPTIMAL' | 'BALANCED' | 'CAUTIOUS' | 'DEFENSIVE';
      if (unifiedPowerIndex >= 0.9) {
        systemState = 'TRANSCENDENT';
      } else if (unifiedPowerIndex >= 0.75) {
        systemState = 'OPTIMAL';
      } else if (unifiedPowerIndex >= 0.6) {
        systemState = 'BALANCED';
      } else if (unifiedPowerIndex >= 0.4) {
        systemState = 'CAUTIOUS';
      } else {
        systemState = 'DEFENSIVE';
      }
      
      console.log(`   🔮 Unified Power Index: ${(unifiedPowerIndex * 100).toFixed(1)}%`);
      console.log(`   📊 System State: ${systemState}`);
      
      return new Response(
        JSON.stringify({
          success: true,
          timestamp: new Date().toISOString(),
          systemState,
          unifiedPowerIndex,
          // Stargate Network
          stargate: {
            gateStatus: stargatePortal.gateStatus,
            isOpen: stargatePortal.isOpen,
            networkStrength: stargatePortal.networkStrength,
            coherence: stargatePortal.avgCoherence,
            gridEnergy: stargatePortal.gridEnergy,
            activeNodes: stargatePortal.activeNodes,
          },
          // Planetary & Solar
          planetary: cosmicVision.planetary,
          // Lattice Workbench
          lattice: {
            state: latticeWorkbench.latticeState,
            frequencyAnalysis: latticeWorkbench.frequencyAnalysis,
            fieldMetrics: latticeWorkbench.fieldMetrics,
            recommendations: latticeWorkbench.recommendations,
          },
          // Unified Cosmic
          cosmic: {
            combinedPower: cosmicVision.combinedPower,
            recommendation: cosmicVision.recommendation,
          },
          // Queen Authority Status
          queenAuthority: QUEEN_AUTHORITY,
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // 👑🛡️ QUEEN'S SUPREME CONTROL - Full Authority Actions
    // ═══════════════════════════════════════════════════════════════════════════════
    if (action === 'control') {
      const { controlAction, ...controlParams } = await req.json().catch(() => ({}));
      
      console.log(`\n👑🛡️ QUEEN'S SUPREME CONTROL - Action: ${controlAction}`);
      
      switch (controlAction) {
        // ═══════════════════════════════════════════════════════════════
        // 🚨 EMERGENCY CONTROLS
        // ═══════════════════════════════════════════════════════════════
        case 'emergency_halt':
          QUEEN_AUTHORITY.emergencyHalt = true;
          console.log(`🚨 EMERGENCY HALT ACTIVATED - All trading suspended by Queen's command`);
          
          // Update all active sessions to paused
          await supabase
            .from('hive_sessions')
            .update({ status: 'paused', metadata: { emergencyHalt: true, haltTime: new Date().toISOString() } })
            .eq('status', 'running');
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'emergency_halt',
              message: '🚨 EMERGENCY HALT - All trading suspended by Queen\'s command',
              authority: QUEEN_AUTHORITY,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );
          
        case 'emergency_resume':
          QUEEN_AUTHORITY.emergencyHalt = false;
          console.log(`✅ EMERGENCY LIFTED - Trading resumed by Queen's command`);
          
          // Resume all paused sessions
          await supabase
            .from('hive_sessions')
            .update({ status: 'running', metadata: { emergencyHalt: false, resumeTime: new Date().toISOString() } })
            .eq('status', 'paused');
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'emergency_resume',
              message: '✅ EMERGENCY LIFTED - Trading resumed by Queen\'s command',
              authority: QUEEN_AUTHORITY,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );

        // ═══════════════════════════════════════════════════════════════
        // 🔓 OVERRIDE CONTROLS
        // ═══════════════════════════════════════════════════════════════
        case 'override_cosmic_gates':
          QUEEN_AUTHORITY.overrideCosmicGates = controlParams.enable !== false;
          console.log(`🔓 Cosmic gate override: ${QUEEN_AUTHORITY.overrideCosmicGates ? 'ENABLED' : 'DISABLED'}`);
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'override_cosmic_gates',
              enabled: QUEEN_AUTHORITY.overrideCosmicGates,
              message: `Cosmic gates ${QUEEN_AUTHORITY.overrideCosmicGates ? 'BYPASSED' : 'RESTORED'} - Queen has supreme authority`,
              authority: QUEEN_AUTHORITY,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );
          
        case 'bypass_validation':
          QUEEN_AUTHORITY.bypassAllValidation = controlParams.enable !== false;
          console.log(`⚡ Validation bypass: ${QUEEN_AUTHORITY.bypassAllValidation ? 'ENABLED' : 'DISABLED'}`);
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'bypass_validation',
              enabled: QUEEN_AUTHORITY.bypassAllValidation,
              message: `All validation ${QUEEN_AUTHORITY.bypassAllValidation ? 'BYPASSED' : 'RESTORED'} - Queen's direct authority`,
              authority: QUEEN_AUTHORITY,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );

        case 'set_trading_multiplier':
          const multiplier = Math.max(0, Math.min(10, controlParams.multiplier || 1.0));
          QUEEN_AUTHORITY.forcedTradingMultiplier = multiplier;
          console.log(`📊 Trading multiplier set to: ${multiplier}x`);
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'set_trading_multiplier',
              multiplier: QUEEN_AUTHORITY.forcedTradingMultiplier,
              message: `Trading multiplier set to ${multiplier}x by Queen's command`,
              authority: QUEEN_AUTHORITY,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );

        // ═══════════════════════════════════════════════════════════════
        // 💰 DIRECT TRADE EXECUTION
        // ═══════════════════════════════════════════════════════════════
        case 'direct_trade':
          const { symbol, side, quantity, price, bypass = true } = controlParams;
          
          if (!symbol || !side) {
            return new Response(
              JSON.stringify({ success: false, error: 'symbol and side required for direct trade' }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
            );
          }
          
          console.log(`👑💰 QUEEN'S DIRECT TRADE: ${symbol} ${side} ${quantity || 'market'} @ ${price || 'market'}`);
          
          // Record Queen's direct trade command
          const { data: tradeRecord, error: tradeError } = await supabase
            .from('hive_trades')
            .insert({
              session_id: controlParams.sessionId || null,
              hive_id: null,
              agent_id: null,
              symbol,
              side,
              quantity: quantity || 0,
              price: price || 0,
              status: 'queen_direct',
              metadata: {
                queenCommand: true,
                bypassValidation: bypass,
                timestamp: new Date().toISOString(),
                authority: 'QUEEN_TINA_B',
              },
            })
            .select()
            .single();
          
          if (tradeError) {
            console.error('Failed to record Queen trade:', tradeError);
          }
          
          // Invoke trade execution
          try {
            const { data: execResult } = await supabase.functions.invoke('force-validated-trade', {
              body: {
                symbol,
                side,
                quantity,
                price,
                userId: user.id,
                bypassValidation: bypass,
                queenOverride: true,
              },
            });
            
            console.log(`✅ Queen's trade executed:`, execResult);
            
            return new Response(
              JSON.stringify({
                success: true,
                command: 'direct_trade',
                trade: {
                  symbol,
                  side,
                  quantity,
                  price,
                  recordId: tradeRecord?.id,
                },
                execution: execResult,
                message: `👑 Queen's direct ${side} order for ${symbol} executed`,
              }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
            );
          } catch (execError) {
            console.error('Trade execution error:', execError);
            return new Response(
              JSON.stringify({
                success: false,
                command: 'direct_trade',
                error: execError instanceof Error ? execError.message : 'Execution failed',
                trade: { symbol, side, quantity, price },
              }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
            );
          }

        // ═══════════════════════════════════════════════════════════════
        // 🐝 HIVE MANAGEMENT
        // ═══════════════════════════════════════════════════════════════
        case 'terminate_hive':
          const { hiveId } = controlParams;
          if (!hiveId) {
            return new Response(
              JSON.stringify({ success: false, error: 'hiveId required' }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
            );
          }
          
          await supabase
            .from('hive_instances')
            .update({ status: 'terminated', metadata: { terminatedBy: 'QUEEN', terminatedAt: new Date().toISOString() } })
            .eq('id', hiveId);
          
          console.log(`🐝❌ Hive ${hiveId} terminated by Queen`);
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'terminate_hive',
              hiveId,
              message: `Hive ${hiveId} terminated by Queen's command`,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );
          
        case 'spawn_hive':
          const { parentHiveId, initialBalance, numAgents } = controlParams;
          
          const { data: newHive, error: spawnError } = await supabase
            .from('hive_instances')
            .insert({
              parent_hive_id: parentHiveId || null,
              generation: 0,
              initial_balance: initialBalance || 100,
              current_balance: initialBalance || 100,
              num_agents: numAgents || AGENTS_PER_HIVE,
              status: 'active',
              metadata: { spawnedBy: 'QUEEN', spawnedAt: new Date().toISOString() },
            })
            .select()
            .single();
          
          if (spawnError) {
            return new Response(
              JSON.stringify({ success: false, error: 'Failed to spawn hive' }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
            );
          }
          
          // Create agents for new hive
          const newAgents = Array.from({ length: numAgents || AGENTS_PER_HIVE }, (_, i) => ({
            hive_id: newHive.id,
            agent_index: i,
            current_symbol: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
            position_open: false,
          }));
          
          await supabase.from('hive_agents').insert(newAgents);
          
          console.log(`🐝✨ New hive ${newHive.id} spawned by Queen with ${numAgents || AGENTS_PER_HIVE} agents`);
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'spawn_hive',
              hive: newHive,
              agents: numAgents || AGENTS_PER_HIVE,
              message: `New hive spawned by Queen's command`,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );

        case 'boost_hive':
          const { targetHiveId, boostAmount } = controlParams;
          if (!targetHiveId || !boostAmount) {
            return new Response(
              JSON.stringify({ success: false, error: 'targetHiveId and boostAmount required' }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
            );
          }
          
          const { data: boostedHive } = await supabase
            .from('hive_instances')
            .select('current_balance')
            .eq('id', targetHiveId)
            .single();
          
          if (boostedHive) {
            await supabase
              .from('hive_instances')
              .update({ 
                current_balance: Number(boostedHive.current_balance) + boostAmount,
                metadata: { lastBoost: boostAmount, boostedBy: 'QUEEN', boostedAt: new Date().toISOString() }
              })
              .eq('id', targetHiveId);
            
            console.log(`🐝💪 Hive ${targetHiveId} boosted by $${boostAmount}`);
          }
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'boost_hive',
              hiveId: targetHiveId,
              boost: boostAmount,
              newBalance: boostedHive ? Number(boostedHive.current_balance) + boostAmount : null,
              message: `Hive boosted by $${boostAmount}`,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );

        // ═══════════════════════════════════════════════════════════════
        // 📋 OMS QUEUE MANAGEMENT
        // ═══════════════════════════════════════════════════════════════
        case 'clear_queue':
          const { data: clearedOrders } = await supabase
            .from('oms_order_queue')
            .update({ status: 'cancelled', metadata: { cancelledBy: 'QUEEN', cancelledAt: new Date().toISOString() } })
            .eq('status', 'queued')
            .select();
          
          console.log(`📋 Queen cleared ${clearedOrders?.length || 0} orders from queue`);
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'clear_queue',
              clearedCount: clearedOrders?.length || 0,
              message: `Order queue cleared by Queen's command`,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );
          
        case 'prioritize_order':
          const { orderId, priority } = controlParams;
          if (!orderId) {
            return new Response(
              JSON.stringify({ success: false, error: 'orderId required' }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
            );
          }
          
          await supabase
            .from('oms_order_queue')
            .update({ priority: priority || 100 })
            .eq('id', orderId);
          
          console.log(`📋 Order ${orderId} priority set to ${priority || 100}`);
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'prioritize_order',
              orderId,
              priority: priority || 100,
              message: `Order priority updated by Queen`,
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );

        case 'force_process_queue':
          // Force OMS to process all queued orders immediately
          try {
            const { data: processResult } = await supabase.functions.invoke('oms-leaky-bucket', {
              body: { action: 'process', forceAll: true, queenOverride: true },
            });
            
            console.log(`📋⚡ Queen forced queue processing:`, processResult);
            
            return new Response(
              JSON.stringify({
                success: true,
                command: 'force_process_queue',
                result: processResult,
                message: `Queue force-processed by Queen's command`,
              }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
            );
          } catch (queueError) {
            return new Response(
              JSON.stringify({ success: false, error: 'Queue processing failed' }),
              { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
            );
          }

        // ═══════════════════════════════════════════════════════════════
        // 👑 AUTHORITY STATUS
        // ═══════════════════════════════════════════════════════════════
        case 'get_authority':
          return new Response(
            JSON.stringify({
              success: true,
              command: 'get_authority',
              authority: QUEEN_AUTHORITY,
              message: 'Queen Tina B has FULL CONTROL over all Aureon systems',
              capabilities: [
                'emergency_halt / emergency_resume',
                'override_cosmic_gates',
                'bypass_validation',
                'set_trading_multiplier',
                'direct_trade',
                'terminate_hive / spawn_hive / boost_hive',
                'clear_queue / prioritize_order / force_process_queue',
                'lattice (monitor/tune/cleanse/harmonize/shield)',
                'cosmic (full system dashboard)',
              ],
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );

        case 'reset_authority':
          QUEEN_AUTHORITY = {
            emergencyHalt: false,
            overrideCosmicGates: false,
            directTradeEnabled: true,
            bypassAllValidation: false,
            forcedTradingMultiplier: 1.0,
            queenModeActive: true,
          };
          
          console.log(`👑 Queen authority reset to defaults`);
          
          return new Response(
            JSON.stringify({
              success: true,
              command: 'reset_authority',
              authority: QUEEN_AUTHORITY,
              message: 'Queen authority reset to default configuration',
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );

        default:
          return new Response(
            JSON.stringify({
              success: false,
              error: `Unknown control action: ${controlAction}`,
              availableActions: {
                emergency: ['emergency_halt', 'emergency_resume'],
                override: ['override_cosmic_gates', 'bypass_validation', 'set_trading_multiplier'],
                trading: ['direct_trade'],
                hive: ['terminate_hive', 'spawn_hive', 'boost_hive'],
                queue: ['clear_queue', 'prioritize_order', 'force_process_queue'],
                authority: ['get_authority', 'reset_authority'],
              },
            }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
          );
      }
    }

    throw new Error(`Unknown action: ${action}`);

  } catch (error) {
    console.error('Queen-Hive orchestrator error:', error);
    return new Response(
      JSON.stringify({ success: false, error: error instanceof Error ? error.message : 'Unknown error' }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    );
  }
});
