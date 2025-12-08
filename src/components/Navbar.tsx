import { Link, useNavigate, useLocation } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { Button } from "@/components/ui/button";
import { 
  TrendingUp, 
  LogOut, 
  ShieldCheck, 
  Settings, 
  Menu, 
  X,
  LayoutDashboard,
  Briefcase,
  BarChart3,
  FlaskConical,
  Activity,
  ChevronDown,
  User,
  Swords,
  Atom,
  Diamond,
  Rainbow,
  Globe,
  Cog
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  DropdownMenuLabel,
} from "@/components/ui/dropdown-menu";
import { toast } from "sonner";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

// Primary navigation - always visible
const primaryNavItems = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard, emoji: "🏠" },
  { path: "/war-room", label: "War Room", icon: Swords, emoji: "⚔️" },
  { path: "/portfolio", label: "Portfolio", icon: Briefcase, emoji: "💼" },
  { path: "/analytics", label: "Analytics", icon: BarChart3, emoji: "📊" },
];

// Systems dropdown items
const systemsNavItems = [
  { path: "/quantum", label: "Quantum", icon: Atom, emoji: "🔮" },
  { path: "/prism", label: "Prism", icon: Diamond, emoji: "💎" },
  { path: "/rainbow", label: "Rainbow", icon: Rainbow, emoji: "🌈" },
  { path: "/earth", label: "Earth", icon: Globe, emoji: "🌍" },
];

// Tools dropdown items
const toolsNavItems = [
  { path: "/backtest", label: "Lab", icon: FlaskConical, emoji: "🧪" },
  { path: "/systems", label: "Systems", icon: Cog, emoji: "⚙️" },
];

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isAdmin, setIsAdmin] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userEmail, setUserEmail] = useState<string | null>(null);

  useEffect(() => {
    checkAdminStatus();
    getUserEmail();
  }, []);

  const getUserEmail = async () => {
    const { data: { user } } = await supabase.auth.getUser();
    setUserEmail(user?.email || null);
  };

  const checkAdminStatus = async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    const { data } = await supabase
      .from('user_roles')
      .select('role')
      .eq('user_id', user.id)
      .eq('role', 'admin')
      .maybeSingle();

    setIsAdmin(!!data);
  };

  const handleSignOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) {
      toast.error("Failed to sign out");
    } else {
      toast.success("Signed out successfully");
      navigate("/auth");
    }
  };

  const isActive = (path: string) => location.pathname === path;
  const isInGroup = (items: typeof primaryNavItems) => items.some(item => isActive(item.path));

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border bg-background/80 backdrop-blur-lg">
      <div className="container mx-auto px-4">
        <div className="flex h-14 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary">
              <TrendingUp className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-lg font-bold text-foreground hidden sm:block">AUREON</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {/* Primary Nav Items */}
            {primaryNavItems.map((item) => (
              <Link 
                key={item.path}
                to={item.path} 
                className={cn(
                  "flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                  isActive(item.path)
                    ? "bg-primary/10 text-primary" 
                    : "text-muted-foreground hover:text-foreground hover:bg-muted"
                )}
              >
                <span>{item.emoji}</span>
                <span>{item.label}</span>
              </Link>
            ))}

            {/* Systems Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className={cn(
                    "gap-1 px-3",
                    isInGroup(systemsNavItems) && "bg-primary/10 text-primary"
                  )}
                >
                  <span>🔮</span>
                  <span>Systems</span>
                  <ChevronDown className="h-3 w-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="center" className="w-48">
                <DropdownMenuLabel className="text-xs text-muted-foreground">Quantum Systems</DropdownMenuLabel>
                {systemsNavItems.map((item) => (
                  <DropdownMenuItem key={item.path} asChild>
                    <Link 
                      to={item.path} 
                      className={cn(
                        "flex items-center gap-2 cursor-pointer",
                        isActive(item.path) && "bg-primary/10 text-primary"
                      )}
                    >
                      <span>{item.emoji}</span>
                      {item.label}
                    </Link>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Tools Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className={cn(
                    "gap-1 px-3",
                    isInGroup(toolsNavItems) && "bg-primary/10 text-primary"
                  )}
                >
                  <span>🛠️</span>
                  <span>Tools</span>
                  <ChevronDown className="h-3 w-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="center" className="w-48">
                <DropdownMenuLabel className="text-xs text-muted-foreground">Developer Tools</DropdownMenuLabel>
                {toolsNavItems.map((item) => (
                  <DropdownMenuItem key={item.path} asChild>
                    <Link 
                      to={item.path} 
                      className={cn(
                        "flex items-center gap-2 cursor-pointer",
                        isActive(item.path) && "bg-primary/10 text-primary"
                      )}
                    >
                      <span>{item.emoji}</span>
                      {item.label}
                    </Link>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          {/* User Menu (Desktop) */}
          <div className="hidden md:flex items-center gap-2">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="gap-2">
                  <User className="h-4 w-4" />
                  <span className="max-w-[120px] truncate text-xs">
                    {userEmail || "Account"}
                  </span>
                  <ChevronDown className="h-3 w-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem asChild>
                  <Link to="/settings" className="flex items-center gap-2 cursor-pointer">
                    <Settings className="h-4 w-4" />
                    Settings
                  </Link>
                </DropdownMenuItem>
                {isAdmin && (
                  <DropdownMenuItem asChild>
                    <Link to="/admin/kyc" className="flex items-center gap-2 cursor-pointer">
                      <ShieldCheck className="h-4 w-4" />
                      Admin
                    </Link>
                  </DropdownMenuItem>
                )}
                <DropdownMenuSeparator />
                <DropdownMenuItem 
                  onClick={handleSignOut}
                  className="flex items-center gap-2 cursor-pointer text-destructive focus:text-destructive"
                >
                  <LogOut className="h-4 w-4" />
                  Sign Out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-border py-4 max-h-[80vh] overflow-y-auto">
            {/* Primary Navigation */}
            <div className="px-2 pb-2">
              <p className="text-[10px] uppercase text-muted-foreground font-medium px-3 py-1">Navigation</p>
              {primaryNavItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    isActive(item.path)
                      ? "bg-primary/10 text-primary" 
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  )}
                >
                  <span>{item.emoji}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
            
            <div className="my-2 border-t border-border" />
            
            {/* Systems Section */}
            <div className="px-2 pb-2">
              <p className="text-[10px] uppercase text-muted-foreground font-medium px-3 py-1">🔮 Quantum Systems</p>
              {systemsNavItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    isActive(item.path)
                      ? "bg-primary/10 text-primary" 
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  )}
                >
                  <span>{item.emoji}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
            
            <div className="my-2 border-t border-border" />
            
            {/* Tools Section */}
            <div className="px-2 pb-2">
              <p className="text-[10px] uppercase text-muted-foreground font-medium px-3 py-1">🛠️ Tools</p>
              {toolsNavItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    isActive(item.path)
                      ? "bg-primary/10 text-primary" 
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  )}
                >
                  <span>{item.emoji}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
            
            <div className="my-2 border-t border-border" />
            
            {/* User Section */}
            <div className="px-2">
              <p className="text-[10px] uppercase text-muted-foreground font-medium px-3 py-1">👤 Account</p>
              <Link
                to="/settings"
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center gap-3 px-3 py-2 rounded-md text-sm text-muted-foreground hover:text-foreground hover:bg-muted"
              >
                <Settings className="h-4 w-4" />
                Settings
              </Link>
              {isAdmin && (
                <Link
                  to="/admin/kyc"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-2 rounded-md text-sm text-muted-foreground hover:text-foreground hover:bg-muted"
                >
                  <ShieldCheck className="h-4 w-4" />
                  Admin
                </Link>
              )}
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  handleSignOut();
                }}
                className="flex items-center gap-3 px-3 py-2 rounded-md text-sm text-destructive hover:bg-destructive/10 text-left w-full"
              >
                <LogOut className="h-4 w-4" />
                Sign Out
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
