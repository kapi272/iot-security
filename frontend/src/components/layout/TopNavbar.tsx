import { Activity } from "lucide-react";

export function TopNavbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 h-14 bg-surface border-b border-border z-50 flex items-center justify-between px-6">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded bg-primary flex items-center justify-center">
          <Activity className="w-5 h-5 text-primary-foreground" />
        </div>
        <h1 className="text-lg font-semibold tracking-tight">Autonomous IoT Cyber Defense</h1>
      </div>
      
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary/50 border border-border">
        <div className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse" />
        <span className="text-xs font-mono text-muted-foreground uppercase tracking-wider">System Idle</span>
      </div>
    </nav>
  );
}
