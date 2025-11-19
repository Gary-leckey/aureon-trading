import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

// Helper function to create HMAC signature
async function createSignature(secret: string, message: string): Promise<string> {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secret);
  const messageData = encoder.encode(message);
  
  const key = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  
  const signature = await crypto.subtle.sign('HMAC', key, messageData);
  return Array.from(new Uint8Array(signature))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    console.log('[fetch-binance-portfolio] Fetching live Binance portfolio');

    const apiKey = Deno.env.get('BINANCE_API_KEY')?.trim();
    const apiSecret = Deno.env.get('BINANCE_API_SECRET')?.trim();

    if (!apiKey || !apiSecret) {
      throw new Error('Binance API credentials not configured');
    }

    console.log('[fetch-binance-portfolio] API Key length:', apiKey.length);
    console.log('[fetch-binance-portfolio] API Key prefix:', apiKey.substring(0, 8) + '...');

    // First, test with a simple unauthenticated endpoint to check connectivity
    console.log('[fetch-binance-portfolio] Testing Binance connectivity...');
    const pingResponse = await fetch('https://api.binance.com/api/v3/ping');
    if (!pingResponse.ok) {
      throw new Error(`Cannot reach Binance API: ${pingResponse.status}`);
    }
    console.log('[fetch-binance-portfolio] Binance API is reachable');

    // Test authenticated endpoint with API key restrictions check
    const timestamp = Date.now();
    const recvWindow = 60000; // 60 seconds
    
    // Try api key check endpoint first (less restrictive)
    console.log('[fetch-binance-portfolio] Testing API key validity...');
    const apiKeyCheckUrl = `https://api.binance.com/api/v3/account/status?timestamp=${timestamp}&recvWindow=${recvWindow}`;
    const checkSignature = await createSignature(apiSecret, `timestamp=${timestamp}&recvWindow=${recvWindow}`);
    
    const checkResponse = await fetch(`${apiKeyCheckUrl}&signature=${checkSignature}`, {
      method: 'GET',
      headers: {
        'X-MBX-APIKEY': apiKey,
      },
    });

    if (!checkResponse.ok) {
      const errorText = await checkResponse.text();
      console.error('[fetch-binance-portfolio] API key check failed:', errorText);
      let errorJson;
      try {
        errorJson = JSON.parse(errorText);
      } catch (e) {
        throw new Error(`Binance API error: ${checkResponse.status}`);
      }
      
      // Provide specific error guidance
      if (errorJson.code === -2015) {
        throw new Error('Binance API key has IP restrictions enabled. Please go to Binance API Management and set "IP access restrictions" to "Unrestricted (Less Secure)" or whitelist Lovable Cloud IPs');
      } else if (errorJson.code === -2014) {
        throw new Error('Binance API key invalid format or signature mismatch. Please regenerate your API keys');
      } else if (errorJson.code === -1022) {
        throw new Error('Binance API signature invalid. Please check your API secret is correct');
      }
      
      throw new Error(`Binance API error: ${errorJson.msg || errorJson.code || checkResponse.status}`);
    }

    console.log('[fetch-binance-portfolio] API key is valid, fetching account data...');

    // Now fetch the actual account information
    const queryString = `timestamp=${timestamp}&recvWindow=${recvWindow}`;
    const signature = await createSignature(apiSecret, queryString);
    const accountUrl = `https://api.binance.com/api/v3/account?${queryString}&signature=${signature}`;

    const response = await fetch(accountUrl, {
      method: 'GET',
      headers: {
        'X-MBX-APIKEY': apiKey,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('[fetch-binance-portfolio] Binance API error response:', errorText);
      console.error('[fetch-binance-portfolio] Status:', response.status);
      
      let errorMessage = `Binance API error: ${response.status}`;
      try {
        const errorJson = JSON.parse(errorText);
        errorMessage = `Binance API error: ${errorJson.msg || errorJson.code || response.status}`;
        console.error('[fetch-binance-portfolio] Parsed error:', errorJson);
      } catch (e) {
        console.error('[fetch-binance-portfolio] Could not parse error response');
      }
      
      throw new Error(errorMessage);
    }

    const accountData = await response.json();
    console.log('[fetch-binance-portfolio] Account data received');

    // Filter balances to only non-zero amounts
    const balances = accountData.balances
      .filter((balance: any) => parseFloat(balance.free) > 0 || parseFloat(balance.locked) > 0)
      .map((balance: any) => ({
        asset: balance.asset,
        free: parseFloat(balance.free),
        locked: parseFloat(balance.locked),
        total: parseFloat(balance.free) + parseFloat(balance.locked),
      }));

    // Fetch current prices for all assets
    const tickerResponse = await fetch('https://api.binance.com/api/v3/ticker/price');
    const tickers = await tickerResponse.json();
    
    // Create price map
    const priceMap = new Map();
    tickers.forEach((ticker: any) => {
      priceMap.set(ticker.symbol, parseFloat(ticker.price));
    });

    // Calculate USDT values
    const enrichedBalances = balances.map((balance: any) => {
      let usdtValue = 0;
      
      if (balance.asset === 'USDT') {
        usdtValue = balance.total;
      } else {
        const usdtSymbol = `${balance.asset}USDT`;
        const btcSymbol = `${balance.asset}BTC`;
        
        if (priceMap.has(usdtSymbol)) {
          usdtValue = balance.total * priceMap.get(usdtSymbol);
        } else if (priceMap.has(btcSymbol)) {
          const btcPrice = priceMap.get('BTCUSDT') || 0;
          const assetBtcPrice = priceMap.get(btcSymbol) || 0;
          usdtValue = balance.total * assetBtcPrice * btcPrice;
        }
      }

      return {
        ...balance,
        usdtValue,
        price: priceMap.get(`${balance.asset}USDT`) || 0,
      };
    });

    // Sort by USDT value descending
    enrichedBalances.sort((a: any, b: any) => b.usdtValue - a.usdtValue);

    // Calculate totals
    const totalUSDT = enrichedBalances.reduce((sum: number, b: any) => sum + b.usdtValue, 0);
    const totalBTC = totalUSDT / (priceMap.get('BTCUSDT') || 1);

    const portfolio = {
      balances: enrichedBalances,
      totalUSDT,
      totalBTC,
      accountType: accountData.accountType,
      canTrade: accountData.canTrade,
      canWithdraw: accountData.canWithdraw,
      canDeposit: accountData.canDeposit,
      updateTime: accountData.updateTime,
      fetchedAt: new Date().toISOString(),
    };

    console.log('[fetch-binance-portfolio] Portfolio calculated, total USDT:', totalUSDT);

    return new Response(
      JSON.stringify(portfolio),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );

  } catch (error) {
    console.error('[fetch-binance-portfolio] Error:', error);
    return new Response(
      JSON.stringify({
        error: error instanceof Error ? error.message : 'Unknown error',
        details: 'Failed to fetch Binance portfolio',
      }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});
