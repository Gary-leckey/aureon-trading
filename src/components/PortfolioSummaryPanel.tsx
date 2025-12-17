import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useUserBalances } from '@/hooks/useUserBalances';
import { Wallet, RefreshCw } from 'lucide-react';
import { formatDistanceToNowStrict } from 'date-fns';

export function PortfolioSummaryPanel() {
  const { totalEquityUsd, connectedExchanges, isLoading, error, lastUpdated, refresh, getConsolidatedAssets } = useUserBalances(true, 30000);
  const assets = getConsolidatedAssets().slice(0, 6);

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          <Wallet className="h-4 w-4 text-primary" />
          Portfolio
          <Button
            variant="ghost"
            size="icon"
            className="ml-auto"
            onClick={() => refresh()}
            disabled={isLoading}
            aria-label="Refresh portfolio"
          >
            <RefreshCw className={isLoading ? 'h-4 w-4 animate-spin' : 'h-4 w-4'} />
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {error ? (
          <div className="text-sm text-destructive">{error}</div>
        ) : (
          <>
            <div className="flex items-baseline justify-between">
              <div>
                <div className="text-2xl font-bold">
                  ${totalEquityUsd.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                </div>
                <div className="text-xs text-muted-foreground">
                  {connectedExchanges.length} exchange(s) connected
                  {lastUpdated ? ` • updated ${formatDistanceToNowStrict(lastUpdated)} ago` : ''}
                </div>
              </div>
            </div>

            {assets.length === 0 ? (
              <div className="text-sm text-muted-foreground">
                {isLoading ? 'Loading balances…' : 'No assets found (or exchanges not configured).'}
              </div>
            ) : (
              <div className="space-y-2">
                {assets.map((a) => (
                  <div key={a.asset} className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-foreground">{a.asset}</span>
                      <span className="text-xs text-muted-foreground">({a.exchanges.length})</span>
                    </div>
                    <div className="font-mono text-foreground">
                      ${a.usdValue.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}
