import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.4";
import { createHmac } from "node:crypto";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

function isPrintableAscii(s: string) {
  // allow common API key charset; disallow whitespace/control chars
  if (!s) return false;
  if (/[\s\x00-\x1F\x7F]/.test(s)) return false;
  return /^[\x21-\x7E]+$/.test(s);
}

function maskKey(key: string) {
  const trimmed = key.trim();
  if (trimmed.length <= 8) return "****";
  return `${trimmed.slice(0, 4)}****${trimmed.slice(-4)}`;
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return new Response(JSON.stringify({ error: "Missing authorization" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY")!;
    const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

    // Verify user
    const anonSupabase = createClient(supabaseUrl, supabaseAnonKey);
    const token = authHeader.replace("Bearer ", "");
    const {
      data: { user },
      error: authError,
    } = await anonSupabase.auth.getUser(token);

    if (authError || !user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    const { data: session, error: sessionError } = await supabase
      .from("aureon_user_sessions")
      .select("binance_api_key_encrypted, binance_api_secret_encrypted, binance_iv")
      .eq("user_id", user.id)
      .single();

    if (sessionError || !session) {
      return new Response(JSON.stringify({ error: "No session found" }), {
        status: 404,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (!session.binance_api_key_encrypted || !session.binance_api_secret_encrypted || !session.binance_iv) {
      return new Response(JSON.stringify({ error: "No Binance credentials configured" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const decodeIvFromB64 = (ivB64: string) => Uint8Array.from(atob(ivB64), (c) => c.charCodeAt(0));
    const iv = decodeIvFromB64(session.binance_iv);

    // Match the working function: primary key is the unified padded key.
    // Also attempt MASTER_ENCRYPTION_KEY for backwards compatibility.
    const primaryKeyString = "aureon-default-key-32chars!!";
    const fallbackKeyString = Deno.env.get("MASTER_ENCRYPTION_KEY") || "";

    const encoder = new TextEncoder();
    const keyBytes1 = encoder.encode(primaryKeyString.padEnd(32, "0").slice(0, 32));
    const keyBytes2 = encoder.encode(fallbackKeyString.padEnd(32, "0").slice(0, 32));

    const cryptoKey1 = await crypto.subtle.importKey("raw", keyBytes1, { name: "AES-GCM" }, false, ["decrypt"]);
    const cryptoKey2 = fallbackKeyString
      ? await crypto.subtle.importKey("raw", keyBytes2, { name: "AES-GCM" }, false, ["decrypt"])
      : null;

    async function decryptWithKey(encrypted: string, key: CryptoKey): Promise<string> {
      const encryptedBytes = Uint8Array.from(atob(encrypted), (c) => c.charCodeAt(0));
      const decrypted = await crypto.subtle.decrypt({ name: "AES-GCM", iv: iv as unknown as BufferSource }, key, encryptedBytes);
      return new TextDecoder().decode(decrypted);
    }

    async function decryptCredential(encrypted: string): Promise<string> {
      // 1) Try primary AES-GCM key
      try {
        return await decryptWithKey(encrypted, cryptoKey1);
      } catch {
        // 2) Try fallback key if configured
        if (cryptoKey2) {
          try {
            return await decryptWithKey(encrypted, cryptoKey2);
          } catch {
            // continue
          }
        }

        // 3) Legacy: stored as base64 of plaintext
        try {
          return atob(encrypted);
        } catch {
          throw new Error("Credential decryption failed");
        }
      }
    }

    let apiKey = (await decryptCredential(session.binance_api_key_encrypted)).trim();
    let apiSecret = (await decryptCredential(session.binance_api_secret_encrypted)).trim();

    // Validate decrypted output before using in headers
    if (!isPrintableAscii(apiKey) || apiKey.length < 16) {
      console.error("[fetch-open-positions] Decrypted Binance API key invalid", {
        userId: user.id,
        apiKeyMasked: maskKey(apiKey),
        apiKeyLen: apiKey.length,
      });
      return new Response(
        JSON.stringify({
          error: "Binance credentials invalid. Please re-save your Binance API Key/Secret in Settings.",
        }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (!isPrintableAscii(apiSecret) || apiSecret.length < 16) {
      console.error("[fetch-open-positions] Decrypted Binance API secret invalid", {
        userId: user.id,
        apiSecretLen: apiSecret.length,
      });
      return new Response(
        JSON.stringify({
          error: "Binance credentials invalid. Please re-save your Binance API Key/Secret in Settings.",
        }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Fetch account info from Binance
    const timestamp = Date.now();
    const queryString = `timestamp=${timestamp}`;
    const signature = createHmac("sha256", apiSecret).update(queryString).digest("hex");

    const accountRes = await fetch(`https://api.binance.com/api/v3/account?${queryString}&signature=${signature}`, {
      headers: { "X-MBX-APIKEY": apiKey },
    });

    if (!accountRes.ok) {
      const errText = await accountRes.text();
      console.error("Binance account error:", errText);
      return new Response(JSON.stringify({ error: "Failed to fetch Binance account" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const accountData = await accountRes.json();
    const balances = accountData.balances || [];

    const spotPositions = balances
      .filter((b: any) => {
        const free = parseFloat(b.free || "0");
        const locked = parseFloat(b.locked || "0");
        return free > 0 || locked > 0;
      })
      .map((b: any) => ({
        asset: b.asset,
        free: parseFloat(b.free || "0"),
        locked: parseFloat(b.locked || "0"),
        total: parseFloat(b.free || "0") + parseFloat(b.locked || "0"),
      }));

    const pricesRes = await fetch("https://api.binance.com/api/v3/ticker/price");
    const allPrices = pricesRes.ok ? await pricesRes.json() : [];
    const priceMap: Record<string, number> = {};
    for (const p of allPrices) priceMap[p.symbol] = parseFloat(p.price);

    const enrichedPositions = spotPositions.map((pos: any) => {
      let usdValue = 0;
      if (pos.asset === "USDT" || pos.asset === "USDC" || pos.asset === "BUSD") {
        usdValue = pos.total;
      } else {
        const usdtPair = `${pos.asset}USDT`;
        const btcPair = `${pos.asset}BTC`;
        if (priceMap[usdtPair]) usdValue = pos.total * priceMap[usdtPair];
        else if (priceMap[btcPair] && priceMap["BTCUSDT"]) usdValue = pos.total * priceMap[btcPair] * priceMap["BTCUSDT"];
      }
      return { ...pos, usdValue };
    });

    enrichedPositions.sort((a: any, b: any) => b.usdValue - a.usdValue);
    const totalUsdValue = enrichedPositions.reduce((sum: number, p: any) => sum + p.usdValue, 0);

    return new Response(
      JSON.stringify({
        success: true,
        positions: enrichedPositions,
        totalUsdValue,
        positionCount: enrichedPositions.length,
      }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error: any) {
    console.error("fetch-open-positions error:", error);
    return new Response(JSON.stringify({ error: error?.message || String(error) }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
