import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, TrendingUp, Wallet } from "lucide-react";
import Navbar from "@/components/Navbar";

const Portfolio = () => {
  const holdings = [
    { asset: "Bitcoin", symbol: "BTC", amount: "0.5", value: "$21,625", allocation: "35%", change: "+2.45%" },
    { asset: "Ethereum", symbol: "ETH", amount: "5.2", value: "$11,885", allocation: "19%", change: "+1.82%" },
    { asset: "Gold", symbol: "XAU", amount: "10 oz", value: "$20,358", allocation: "33%", change: "+0.89%" },
    { asset: "EUR/USD", symbol: "EUR", amount: "$5,000", value: "$5,438", allocation: "9%", change: "-0.23%" },
    { asset: "Tesla Stock", symbol: "TSLA", amount: "15", value: "$2,944", allocation: "4%", change: "+3.12%" },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <main className="container mx-auto px-4 pt-24 pb-12">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Portfolio</h1>
          <p className="text-muted-foreground">Manage and track your investment portfolio</p>
        </div>

        {/* Portfolio Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-card shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Value</CardTitle>
              <Wallet className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">$62,250.00</div>
              <p className="text-xs text-success flex items-center gap-1 mt-1">
                <TrendingUp className="h-3 w-3" />
                +$4,850 (8.45%)
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">24h Change</CardTitle>
              <TrendingUp className="h-4 w-4 text-success" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-success">+$1,245.00</div>
              <p className="text-xs text-muted-foreground mt-1">
                +2.04% today
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card shadow-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Assets</CardTitle>
              <PieChart className="h-4 w-4 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">5</div>
              <p className="text-xs text-muted-foreground mt-1">
                Across 3 categories
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Holdings */}
        <Card className="bg-card shadow-card mb-8">
          <CardHeader>
            <CardTitle>Your Holdings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {holdings.map((holding) => (
                <div key={holding.symbol} className="flex items-center justify-between p-4 rounded-lg bg-muted/20 hover:bg-muted/40 transition-colors">
                  <div className="flex items-center gap-4 flex-1">
                    <div>
                      <p className="font-bold">{holding.asset}</p>
                      <p className="text-sm text-muted-foreground">{holding.amount} {holding.symbol}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-8">
                    <div className="text-right">
                      <p className="text-sm text-muted-foreground">Value</p>
                      <p className="font-bold">{holding.value}</p>
                    </div>

                    <div className="text-right">
                      <p className="text-sm text-muted-foreground">Allocation</p>
                      <p className="font-semibold">{holding.allocation}</p>
                    </div>

                    <div className="text-right min-w-[80px]">
                      <p className="text-sm text-muted-foreground">Change</p>
                      <p className={`font-bold ${holding.change.startsWith('+') ? 'text-success' : 'text-destructive'}`}>
                        {holding.change}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Allocation Chart Placeholder */}
        <Card className="bg-card shadow-card">
          <CardHeader>
            <CardTitle>Asset Allocation</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center border border-border rounded-lg bg-muted/20">
              <p className="text-muted-foreground">Allocation chart visualization</p>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Portfolio;
