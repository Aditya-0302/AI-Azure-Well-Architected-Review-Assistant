import { architectureNodes } from "@/data/platform";
import { cn } from "@/lib/utils";

const toneClasses: Record<string, string> = {
  azure: "border-azure/40 bg-azure/10 text-azure",
  primary: "border-primary/40 bg-primary/10 text-primary",
  success: "border-success/40 bg-success/10 text-success",
  warning: "border-warning/40 bg-warning/10 text-warning",
  critical: "border-critical/40 bg-critical/10 text-critical"
};

export function ArchitectureMap() {
  return (
    <div className="relative h-[320px] overflow-hidden rounded-lg border bg-card enterprise-grid">
      <div className="absolute left-[15%] top-[47%] h-px w-[60%] bg-border" />
      <div className="absolute left-[55%] top-[35%] h-[35%] w-px bg-border" />
      {architectureNodes.map((node) => (
        <div
          key={node.label}
          className={cn(
            "absolute flex h-11 min-w-28 items-center justify-center rounded-md border px-3 text-xs font-semibold shadow-sm",
            toneClasses[node.tone]
          )}
          style={{ left: node.x, top: node.y }}
        >
          {node.label}
        </div>
      ))}
      <div className="absolute bottom-4 left-4 right-4 grid grid-cols-3 gap-2 text-xs text-muted-foreground">
        <div className="rounded-md border bg-background/80 p-2">6 services mapped</div>
        <div className="rounded-md border bg-background/80 p-2">2 evidence gaps</div>
        <div className="rounded-md border bg-background/80 p-2">3 policy overlays</div>
      </div>
    </div>
  );
}

