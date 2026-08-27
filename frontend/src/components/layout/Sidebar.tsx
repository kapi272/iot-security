import { type ChangeEvent, useState } from "react";
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

const API_BASE = "http://127.0.0.1:8000/api";

export function Sidebar() {
  const [mode, setMode] = useState<string>("simulation");
  const [nodeCount, setNodeCount] = useState<number>(10);
  const [deviceType, setDeviceType] = useState<string>("camera");
  const [loading, setLoading] = useState<boolean>(false);

  const startNetwork = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/network/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode, node_count: nodeCount, device_type: deviceType })
      });
      const data = await res.json();
      console.log(data);
    } catch (e) {
      console.error("Failed to start network:", e);
    }
    setLoading(false);
  };

  const stopSystem = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/system/stop`, {
        method: "POST",
      });
      const data = await res.json();
      console.log(data);
    } catch (e) {
      console.error("Failed to stop system:", e);
    }
    setLoading(false);
  };

  const triggerAttack = async (attackType: string) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/attacks/trigger`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attack_type: attackType })
      });
      const data = await res.json();
      console.log(data);
    } catch (e) {
      console.error(`Failed to trigger attack ${attackType}:`, e);
    }
    setLoading(false);
  };

  return (
    <aside className="w-80 h-full border-r border-border bg-card overflow-y-auto flex flex-col pt-14">
      <div className="p-6 space-y-8 flex-1">
        
        {/* Operating Mode */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Mode Configuration</h3>
          <div className="space-y-2">
            <Label>System Mode</Label>
            <Select value={mode} onValueChange={setMode} disabled={loading}>
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
            <Input 
              id="node-count" 
              type="number" 
              value={nodeCount} 
              onChange={(e: ChangeEvent<HTMLInputElement>) => setNodeCount(parseInt(e.target.value) || 0)} 
              disabled={loading}
            />
          </div>

          <div className="space-y-2">
            <Label>Primary Device Type</Label>
            <Select value={deviceType} onValueChange={setDeviceType} disabled={loading}>
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
            <Button className="w-full gap-2" onClick={startNetwork} disabled={loading}>
              <Play className="w-4 h-4" /> Start
            </Button>
            <Button variant="secondary" className="w-full gap-2" onClick={stopSystem} disabled={loading}>
              <Square className="w-4 h-4" /> Stop
            </Button>
          </div>
        </div>

        <Separator />

        {/* Attack Triggers */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Attack Triggers</h3>
          <div className="space-y-3">
            <Button variant="destructive" className="w-full justify-start gap-3" onClick={() => triggerAttack("reconnaissance")} disabled={loading}>
              <Terminal className="w-4 h-4" /> Reconnaissance (Nmap)
            </Button>
            <Button variant="destructive" className="w-full justify-start gap-3" onClick={() => triggerAttack("bruteforce")} disabled={loading}>
              <Crosshair className="w-4 h-4" /> Brute Force (Hydra)
            </Button>
            <Button variant="destructive" className="w-full justify-start gap-3" onClick={() => triggerAttack("synflood")} disabled={loading}>
              <Zap className="w-4 h-4" /> SYN Flood (Hping3)
            </Button>
          </div>
        </div>

      </div>
    </aside>
  );
}
