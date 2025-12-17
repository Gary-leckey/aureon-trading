import { Suspense, lazy } from "react";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "@/components/theme-provider";

const TradeDashboard = lazy(() => import("./pages/TradeDashboard"));
const Auth = lazy(() => import("./pages/Auth"));
const Settings = lazy(() => import("./pages/Settings"));
const Terms = lazy(() => import("./pages/Terms"));
const Privacy = lazy(() => import("./pages/Privacy"));
const NotFound = lazy(() => import("./pages/NotFound"));

const queryClient = new QueryClient();

const App = () => {
  return (
    <ThemeProvider defaultTheme="dark">
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Suspense
              fallback={
                <div className="min-h-screen bg-background flex items-center justify-center">
                  <div className="flex flex-col items-center gap-4">
                    <div className="h-10 w-10 rounded-full border-2 border-primary border-t-transparent animate-spin" />
                    <p className="text-sm text-muted-foreground">Loading…</p>
                  </div>
                </div>
              }
            >
              <Routes>
                {/* Main Dashboard */}
                <Route path="/" element={<TradeDashboard />} />

                {/* Auth & Settings */}
                <Route path="/auth" element={<Auth />} />
                <Route path="/settings" element={<Settings />} />

                {/* Legal */}
                <Route path="/terms" element={<Terms />} />
                <Route path="/privacy" element={<Privacy />} />

                {/* Redirects for old routes */}
                <Route path="/war-room" element={<Navigate to="/" replace />} />
                <Route path="/systems" element={<Navigate to="/" replace />} />
                <Route path="/quantum" element={<Navigate to="/" replace />} />
                <Route path="/prism" element={<Navigate to="/" replace />} />
                <Route path="/rainbow" element={<Navigate to="/" replace />} />
                <Route path="/earth" element={<Navigate to="/" replace />} />
                <Route path="/analytics" element={<Navigate to="/" replace />} />
                <Route path="/portfolio" element={<Navigate to="/" replace />} />
                <Route path="/backtest" element={<Navigate to="/" replace />} />

                <Route path="*" element={<NotFound />} />
              </Routes>
            </Suspense>
          </BrowserRouter>
        </TooltipProvider>
      </QueryClientProvider>
    </ThemeProvider>
  );
};

export default App;
