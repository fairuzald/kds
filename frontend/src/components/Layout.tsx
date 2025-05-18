import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Activity, Database, Home } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b bg-white dark:bg-gray-950 sticky top-0 z-10">
        <div className="container flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <Activity className="h-6 w-6 text-primary" />
            <h1 className="text-xl font-bold tracking-tight">BacteriaPred</h1>
          </div>
          <nav className="flex items-center space-x-4">
            <NavItem
              to="/"
              icon={<Home className="h-4 w-4 mr-2" />}
              label="Home"
            />
            <NavItem
              to="/predict"
              icon={<Activity className="h-4 w-4 mr-2" />}
              label="Predict"
            />
            <NavItem
              to="/database"
              icon={<Database className="h-4 w-4 mr-2" />}
              label="Database"
            />
          </nav>
        </div>
      </header>
      <main className="flex-1 container py-8">
        <Outlet />
      </main>
      <footer className="border-t py-6 bg-muted/50">
        <div className="container text-center text-sm text-muted-foreground">
          &copy; {new Date().getFullYear()} BacteriaPred. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

interface NavItemProps {
  to: string;
  icon: React.ReactNode;
  label: string;
}

const NavItem = ({ to, icon, label }: NavItemProps) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      cn(
        "transition-colors flex items-center",
        isActive
          ? "text-primary font-medium"
          : "text-muted-foreground hover:text-foreground"
      )
    }
  >
    <Button variant="ghost" size="sm" className="flex items-center">
      {icon}
      {label}
    </Button>
  </NavLink>
);

export default Layout;
