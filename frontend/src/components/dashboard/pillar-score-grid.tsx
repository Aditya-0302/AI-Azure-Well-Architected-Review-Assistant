import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { pillarScores } from "@/data/platform";

export function PillarScoreGrid() {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
      {pillarScores.map((pillar) => (
        <Card key={pillar.key}>
          <CardContent className="p-5">
            <div className="flex min-h-12 items-start justify-between gap-3">
              <p className="text-sm font-semibold leading-5">{pillar.pillar}</p>
              <Badge variant={pillar.delta >= 0 ? "success" : "warning"}>{pillar.delta >= 0 ? `+${pillar.delta}` : pillar.delta}</Badge>
            </div>
            <div className="mt-4 flex items-end justify-between gap-3">
              <span className="text-3xl font-semibold">{pillar.score}</span>
              <span className="text-xs text-muted-foreground">L{pillar.maturity} {pillar.status}</span>
            </div>
            <Progress value={pillar.score} className="mt-4" />
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

