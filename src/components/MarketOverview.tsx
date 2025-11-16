import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown } from "lucide-react";

const marketData = [
  { name: "BTC/USD", price: "43,250.00", change: "+2.45%", positive: true },
  { name: "ETH/USD", price: "2,285.50", change: "+1.82%", positive: true },
  { name: "EUR/USD", price: "1.0875", change: "-0.23%", positive: false },
  { name: "GBP/USD", price: "1.2654", change: "+0.45%", positive: true },
  { name: "XAU/USD", price: "2,035.80", change: "+0.89%", positive: true },
  { name: "S&P 500", price: "4,568.23", change: "-0.12%", positive: false },
];

const MarketOverview = () => {
  return (
    <section className="py-24 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">Live Market Data</h2>
          <p className="text-muted-foreground text-lg">Real-time prices from global markets</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {marketData.map((market) => (
            <Card key={market.name} className="bg-card shadow-card hover:shadow-glow transition-all duration-300 cursor-pointer">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg flex items-center justify-between">
                  <span>{market.name}</span>
                  {market.positive ? (
                    <TrendingUp className="h-5 w-5 text-success" />
                  ) : (
                    <TrendingDown className="h-5 w-5 text-destructive" />
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-end justify-between">
                  <div>
                    <p className="text-3xl font-bold">${market.price}</p>
                  </div>
                  <div className={`text-lg font-semibold ${market.positive ? "text-success" : "text-destructive"}`}>
                    {market.change}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default MarketOverview;
