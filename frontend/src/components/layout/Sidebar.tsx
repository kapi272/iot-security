import { ChangeEvent } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Play, Square, Crosshair, Terminal, Zap } from "lucide-react";

export function Sidebar() {
  const handleAction = (action: string) => {
    console.log(`[Action Triggered] ${action}`);
  };

  return (
    <aside className="w-80 h-full border-r border-border bg-card overflow-y-auto flex flex-col pt-14">
      <div className="p-6 space-y-8 flex-1">
        
        {/* Operating Mode */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Mode Configuration</h3>
          <div className="space-y-2">
            <Label>System Mode</Label>
            <Select defaultValue="simulation" onValueChange={(v: string) => handleAction(`Mode changed to: ${v}`)}>
              <SelectTrigger>
                <SelectValue placeholder="Select operating mode" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="simulation">Simulation Mode</SelectItem>
                <SelectItem value="live">Live Mode</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <Separator />

        {/* Simulation Parameters */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Simulation Parameters</h3>
          
          <div className="space-y-2">
            <Label htmlFor="node-count">Node Count</Label>
            <Input id="node-count" type="number" defaultValue={10} onChange={(e: ChangeEvent<HTMLInputElement>) => handleAction(`Node Count changed: ${e.target.value}`)} />
          </div>

          <div className="space-y-2">
            <Label>Primary Device Type</Label>
            <Select defaultValue="camera" onValueChange={(v: string) => handleAction(`Device Type changed: ${v}`)}>
              <SelectTrigger>
                <SelectValue placeholder="Select device type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="camera">IP Camera</SelectItem>
                <SelectItem value="thermostat">Smart Thermostat</SelectItem>
                <SelectItem value="router">Home Router</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <Separator />

        {/* Network Controls */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Network Controls</h3>
          <div className="grid grid-cols-2 gap-3">
            <Button className="w-full gap-2" onClick={() => handleAction("Start Network")}>
              <Play className="w-4 h-4" /> Start
            </Button>
            <Button variant="secondary" className="w-full gap-2" onClick={() => handleAction("Stop System")}>
              <Square className="w-4 h-4" /> Stop
            </Button>
          </div>
        </div>

        <Separator />

        {/* Attack Triggers */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Attack Triggers</h3>
          <div className="space-y-3">
            <Button variant="destructive" className="w-full justify-start gap-3" onClick={() => handleAction("Attack: Reconnaissance (Nmap)")}>
              <Terminal className="w-4 h-4" /> Reconnaissance (Nmap)
            </Button>
            <Button variant="destructive" className="w-full justify-start gap-3" onClick={() => handleAction("Attack: Brute Force (Hydra)")}>
              <Crosshair className="w-4 h-4" /> Brute Force (Hydra)
            </Button>
            <Button variant="destructive" className="w-full justify-start gap-3" onClick={() => handleAction("Attack: SYN Flood (Hping3)")}>
              <Zap className="w-4 h-4" /> SYN Flood (Hping3)
            </Button>
          </div>
        </div>

      </div>
    </aside>
  );
}
