import Navbar from "@/components/Navbar";
import { ExchangeCredentialsManager } from "@/components/ExchangeCredentialsManager";
import { TradingConfigPanel } from "@/components/TradingConfigPanel";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Bell, Key, Settings as SettingsIcon } from "lucide-react";

const Settings = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="pt-20 px-4 pb-8">
        <div className="container mx-auto space-y-6">
          <div className="flex items-center gap-3 mb-6">
            <SettingsIcon className="h-8 w-8 text-primary" />
            <h1 className="text-3xl font-bold text-foreground">Settings</h1>
          </div>
          
          <Card className="bg-card border-border">
            <CardContent className="pt-6">
              <Tabs defaultValue="trading" className="w-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="trading" className="flex items-center gap-2">
                    <SettingsIcon className="h-4 w-4" />
                    Trading
                  </TabsTrigger>
                  <TabsTrigger value="credentials" className="flex items-center gap-2">
                    <Key className="h-4 w-4" />
                    API Credentials
                  </TabsTrigger>
                  <TabsTrigger value="alerts" className="flex items-center gap-2">
                    <Bell className="h-4 w-4" />
                    Alerts
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="trading" className="mt-6">
                  <TradingConfigPanel />
                </TabsContent>
                
                <TabsContent value="credentials" className="mt-6">
                  <ExchangeCredentialsManager />
                </TabsContent>
                
                <TabsContent value="alerts" className="mt-6">
                  <Card className="bg-muted/30 border-dashed">
                    <CardContent className="py-12 text-center">
                      <Bell className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                      <h3 className="text-lg font-medium text-foreground mb-2">
                        Alert Settings
                      </h3>
                      <p className="text-muted-foreground max-w-md mx-auto">
                        Configure price alerts, coherence thresholds, and notification preferences. 
                        This feature is currently in development.
                      </p>
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Settings;
