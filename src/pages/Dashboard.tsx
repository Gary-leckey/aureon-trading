import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown, DollarSign, Activity } from "lucide-react";
import Navbar from "@/components/Navbar";

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 pt-24 pb-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Trading Dashboard</h1>
          <p className="text-muted-foreground">Monitor your portfolio and market opportunities</p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-card shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Balance</CardTitle>
              <DollarSign className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">$124,450.00</div>
              <p className="text-xs text-success flex items-center gap-1 mt-1">
                <TrendingUp className="h-3 w-3" />
                +12.5% from last month
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Portfolio Value</CardTitle>
              <Activity className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">$98,250.00</div>
              <p className="text-xs text-success flex items-center gap-1 mt-1">
                <TrendingUp className="h-3 w-3" />
                +8.3% today
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Active Trades</CardTitle>
              <Activity className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <p className="text-xs text-muted-foreground mt-1">
                8 winning positions
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Today's P&L</CardTitle>
              <TrendingUp className="h-4 w-4 text-success" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-success">+$2,450.00</div>
              <p className="text-xs text-success flex items-center gap-1 mt-1">
                +2.5% profit
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chart Area */}
          <Card className="lg:col-span-2 bg-card shadow-card">
            <CardHeader>
              <CardTitle>Market Chart</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80 flex items-center justify-center border border-border rounded-lg bg-muted/20">
                <p className="text-muted-foreground">Chart visualization coming soon</p>
              </div>
            </CardContent>
          </Card>

          {/* Watchlist */}
          <Card className="bg-card shadow-card">
            <CardHeader>
              <CardTitle>Watchlist</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {[
                { symbol: "BTC/USD", price: "43,250", change: "+2.45%", positive: true },
                { symbol: "ETH/USD", price: "2,285", change: "+1.82%", positive: true },
                { symbol: "EUR/USD", price: "1.0875", change: "-0.23%", positive: false },
                { symbol: "XAU/USD", price: "2,036", change: "+0.89%", positive: true },
              ].map((asset) => (
                <div key={asset.symbol} className="flex items-center justify-between p-3 rounded-lg bg-muted/20 hover:bg-muted/40 transition-colors cursor-pointer">
                  <div>
                    <p className="font-semibold">{asset.symbol}</p>
                    <p className="text-sm text-muted-foreground">${asset.price}</p>
                  </div>
                  <div className={`font-semibold ${asset.positive ? "text-success" : "text-destructive"}`}>
                    {asset.change}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Recent Trades */}
          <Card className="lg:col-span-3 bg-card shadow-card">
            <CardHeader>
              <CardTitle>Recent Trades</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[
                  { symbol: "BTC/USD", type: "BUY", amount: "$5,000", time: "2 mins ago", status: "success" },
                  { symbol: "ETH/USD", type: "SELL", amount: "$2,500", time: "15 mins ago", status: "success" },
                  { symbol: "EUR/USD", type: "BUY", amount: "$10,000", time: "1 hour ago", status: "success" },
                ].map((trade, idx) => (
                  <div key={idx} className="flex items-center justify-between p-4 rounded-lg bg-muted/20 hover:bg-muted/40 transition-colors">
                    <div className="flex items-center gap-4">
                      <div className={`px-3 py-1 rounded-md text-xs font-semibold ${
                        trade.type === "BUY" ? "bg-success/20 text-success" : "bg-destructive/20 text-destructive"
                      }`}>
                        {trade.type}
                      </div>
                      <div>
                        <p className="font-semibold">{trade.symbol}</p>
                        <p className="text-sm text-muted-foreground">{trade.time}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold">{trade.amount}</p>
                      <p className="text-xs text-success">Completed</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
