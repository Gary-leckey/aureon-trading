import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.7";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface SchedulerConfig {
  enabled: boolean;
  min_coherence_threshold: number;
  require_lhe_in_window: boolean;
  cooldown_hours: number;
  max_daily_activations: number;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    console.log('[auto-trading-scheduler] Starting scheduler check');

    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Get current scheduler config (from request or default)
    const { config } = await req.json().catch(() => ({ config: null }));
    const schedulerConfig: SchedulerConfig = config || {
      enabled: true,
      min_coherence_threshold: 0.75,
      require_lhe_in_window: true,
      cooldown_hours: 2,
      max_daily_activations: 5,
    };

    if (!schedulerConfig.enabled) {
      console.log('[auto-trading-scheduler] Scheduler is disabled');
      return new Response(JSON.stringify({ 
        action: 'none',
        reason: 'Scheduler disabled',
        schedulerEnabled: false,
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Fetch current unified field analysis
    const { data: analysisData, error: analysisError } = await supabase.functions.invoke('unified-field-analysis');
    
    if (analysisError) {
      console.error('[auto-trading-scheduler] Failed to fetch unified field analysis:', analysisError);
      throw new Error('Failed to fetch unified field analysis');
    }

    const currentHour = new Date().getHours();
    const currentWindowData = analysisData.timeline.find((h: any) => h.hour === currentHour);

    if (!currentWindowData) {
      console.log('[auto-trading-scheduler] No data for current hour');
      return new Response(JSON.stringify({ 
        action: 'none',
        reason: 'No data for current hour',
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Check if current window is optimal
    const isOptimalWindow = 
      currentWindowData.unifiedFieldCoherence >= schedulerConfig.min_coherence_threshold &&
      (!schedulerConfig.require_lhe_in_window || currentWindowData.lighthouseEvents > 0);

    // Get current trading config
    const { data: tradingConfigs } = await supabase
      .from('trading_config')
      .select('*')
      .limit(1)
      .maybeSingle();

    const currentlyEnabled = tradingConfigs?.is_enabled || false;

    // Check cooldown and daily activation limits
    const now = new Date();
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    
    // Count activations today
    const { data: activationsToday, error: activationsError } = await supabase
      .from('trading_executions')
      .select('id')
      .gte('created_at', todayStart.toISOString());

    const dailyActivations = activationsToday?.length || 0;

    // Determine action
    let action = 'none';
    let reason = '';
    let newTradingState = currentlyEnabled;

    if (isOptimalWindow && !currentlyEnabled) {
      // Check if we can activate
      if (dailyActivations >= schedulerConfig.max_daily_activations) {
        action = 'none';
        reason = `Daily activation limit reached (${dailyActivations}/${schedulerConfig.max_daily_activations})`;
      } else {
        action = 'enable';
        reason = `Optimal window detected: coherence ${(currentWindowData.unifiedFieldCoherence * 100).toFixed(0)}%, LHE: ${currentWindowData.lighthouseEvents}`;
        newTradingState = true;
      }
    } else if (!isOptimalWindow && currentlyEnabled) {
      action = 'disable';
      reason = `Low coherence: ${(currentWindowData.unifiedFieldCoherence * 100).toFixed(0)}% (threshold: ${(schedulerConfig.min_coherence_threshold * 100).toFixed(0)}%)`;
      newTradingState = false;
    } else if (isOptimalWindow && currentlyEnabled) {
      action = 'none';
      reason = `Trading already active in optimal window`;
    } else {
      action = 'none';
      reason = `Trading already paused in non-optimal window`;
    }

    // Execute action if needed
    if (action !== 'none' && tradingConfigs) {
      const { error: updateError } = await supabase
        .from('trading_config')
        .update({ 
          is_enabled: newTradingState,
          updated_at: new Date().toISOString(),
        })
        .eq('id', tradingConfigs.id);

      if (updateError) {
        console.error('[auto-trading-scheduler] Failed to update trading config:', updateError);
        throw updateError;
      }

      // Log to scheduler history
      await supabase
        .from('scheduler_history')
        .insert({
          action,
          reason,
          coherence_at_action: currentWindowData.unifiedFieldCoherence,
          lighthouse_events_count: currentWindowData.lighthouseEvents,
          trading_enabled_before: currentlyEnabled,
          trading_enabled_after: newTradingState,
          daily_activations: dailyActivations,
          metadata: {
            hour: currentHour,
            threshold: schedulerConfig.min_coherence_threshold,
            require_lhe: schedulerConfig.require_lhe_in_window,
          },
        });

      console.log(`[auto-trading-scheduler] ${action.toUpperCase()} trading: ${reason}`);
    }

    // Prepare response
    const response = {
      timestamp: new Date().toISOString(),
      action,
      reason,
      schedulerEnabled: schedulerConfig.enabled,
      currentState: {
        hour: currentHour,
        coherence: currentWindowData.unifiedFieldCoherence,
        lighthouseEvents: currentWindowData.lighthouseEvents,
        isOptimal: isOptimalWindow,
        tradingEnabled: newTradingState,
      },
      statistics: {
        dailyActivations,
        maxDailyActivations: schedulerConfig.max_daily_activations,
        avgCoherence: analysisData.statistics.avgUnifiedCoherence,
        totalOptimalHours: analysisData.statistics.totalOptimalHours,
      },
      nextOptimalWindows: analysisData.recurringPatterns.slice(0, 3),
    };

    console.log('[auto-trading-scheduler] Check complete:', action);

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });

  } catch (error) {
    console.error('[auto-trading-scheduler] Error:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    return new Response(
      JSON.stringify({ error: errorMessage }),
      { 
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});
