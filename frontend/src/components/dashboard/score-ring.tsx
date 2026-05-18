import { cn, formatPercent } from "@/lib/utils";

export function ScoreRing({
  score,
  label,
  className
}: {
  score: number;
  label: string;
  className?: string;
}) {
  return (
    <div className={cn("flex items-center gap-4", className)}>
      <div
        className="grid h-20 w-20 shrink-0 place-items-center rounded-full"
        style={{
          background: `conic-gradient(hsl(var(--primary)) ${score * 3.6}deg, hsl(var(--muted)) 0deg)`
        }}
      >
        <div className="grid h-16 w-16 place-items-center rounded-full bg-card">
          <span className="text-lg font-semibold">{score}</span>
        </div>
      </div>
      <div className="min-w-0">
        <p className="text-sm font-semibold">{label}</p>
        <p className="text-sm text-muted-foreground">{formatPercent(score)} aligned</p>
      </div>
    </div>
  );
}

