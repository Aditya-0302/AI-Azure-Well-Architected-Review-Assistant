import { CheckCircle2, CircleAlert, ShieldAlert } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { pillarScores, riskFindings } from "@/data/platform";

export function ScoringMatrix() {
  return (
    <Tabs defaultValue="scores" className="space-y-6">
      <TabsList className="grid w-full grid-cols-3 md:w-[520px]">
        <TabsTrigger value="scores">Scores</TabsTrigger>
        <TabsTrigger value="findings">Findings</TabsTrigger>
        <TabsTrigger value="maturity">Maturity</TabsTrigger>
      </TabsList>

      <TabsContent value="scores">
        <div className="grid gap-4 lg:grid-cols-2">
          {pillarScores.map((pillar) => (
            <Card key={pillar.key}>
              <CardHeader>
                <div className="flex items-center justify-between gap-3">
                  <CardTitle>{pillar.pillar}</CardTitle>
                  <Badge variant={pillar.score >= 80 ? "success" : pillar.score >= 70 ? "warning" : "critical"}>
                    {pillar.score}/100
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <Progress value={pillar.score} />
                <div className="mt-4 grid gap-3 sm:grid-cols-3">
                  <div className="rounded-md border p-3">
                    <p className="text-xs text-muted-foreground">Maturity</p>
                    <p className="mt-1 text-lg font-semibold">Level {pillar.maturity}</p>
                  </div>
                  <div className="rounded-md border p-3">
                    <p className="text-xs text-muted-foreground">Status</p>
                    <p className="mt-1 text-lg font-semibold">{pillar.status}</p>
                  </div>
                  <div className="rounded-md border p-3">
                    <p className="text-xs text-muted-foreground">Change</p>
                    <p className="mt-1 text-lg font-semibold">{pillar.delta >= 0 ? `+${pillar.delta}` : pillar.delta}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </TabsContent>

      <TabsContent value="findings">
        <div className="grid gap-4">
          {riskFindings.map((finding) => (
            <Card key={finding.title}>
              <CardContent className="flex flex-col gap-3 p-5 md:flex-row md:items-center md:justify-between">
                <div className="flex items-start gap-3">
                  {finding.severity === "High" ? (
                    <ShieldAlert className="mt-0.5 h-5 w-5 text-critical" />
                  ) : (
                    <CircleAlert className="mt-0.5 h-5 w-5 text-warning" />
                  )}
                  <div>
                    <p className="font-semibold">{finding.title}</p>
                    <p className="mt-1 text-sm text-muted-foreground">{finding.pillar} · {finding.owner}</p>
                  </div>
                </div>
                <Badge variant={finding.severity === "High" ? "critical" : "warning"}>{finding.severity}</Badge>
              </CardContent>
            </Card>
          ))}
        </div>
      </TabsContent>

      <TabsContent value="maturity">
        <Card>
          <CardContent className="grid gap-4 p-5 md:grid-cols-5">
            {["Initial", "Repeatable", "Defined", "Managed", "Optimized"].map((level, index) => (
              <div key={level} className="rounded-md border p-4">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className={index < 4 ? "h-4 w-4 text-success" : "h-4 w-4 text-muted-foreground"} />
                  <p className="text-sm font-semibold">L{index + 1}</p>
                </div>
                <p className="mt-3 text-sm">{level}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  );
}

