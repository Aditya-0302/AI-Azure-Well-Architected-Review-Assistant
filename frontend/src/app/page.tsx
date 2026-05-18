import { Activity, ArrowRight, ShieldCheck } from "lucide-react";

import { ArchitectureMap } from "@/components/dashboard/architecture-map";
import { MetricStrip } from "@/components/dashboard/metric-strip";
import { PillarScoreGrid } from "@/components/dashboard/pillar-score-grid";
import { RiskTable } from "@/components/dashboard/risk-table";
import { ScoreRing } from "@/components/dashboard/score-ring";
import { ScoreTrendChart } from "@/components/dashboard/score-trend-chart";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { activeReview } from "@/data/platform";

export default function DashboardPage() {
  const ActiveIcon = activeReview.icon;

  return (
    <div className="space-y-6">
      <section className="grid gap-4 xl:grid-cols-[1.4fr_0.8fr]">
        <div className="rounded-lg border bg-card p-5 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div className="flex items-start gap-4">
              <div className="flex h-11 w-11 items-center justify-center rounded-md bg-primary text-primary-foreground">
                <ActiveIcon className="h-5 w-5" />
              </div>
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-xl font-semibold">{activeReview.name}</h2>
                  <Badge variant="secondary">{activeReview.environment}</Badge>
                  <Badge variant="outline">{activeReview.model}</Badge>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{activeReview.owner} · {activeReview.status}</p>
              </div>
            </div>
            <Button>
              Continue review
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
        <div className="rounded-lg border bg-card p-5 shadow-sm">
          <ScoreRing score={77} label="Overall maturity" />
        </div>
      </section>

      <MetricStrip />
      <PillarScoreGrid />

      <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between gap-3">
              <div>
                <CardTitle>Architecture Score Trend</CardTitle>
                <CardDescription>Security, reliability, and operations trajectory</CardDescription>
              </div>
              <Activity className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardHeader>
          <CardContent>
            <ScoreTrendChart />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between gap-3">
              <div>
                <CardTitle>Architecture Map</CardTitle>
                <CardDescription>Service topology and policy overlay</CardDescription>
              </div>
              <ShieldCheck className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardHeader>
          <CardContent>
            <ArchitectureMap />
          </CardContent>
        </Card>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Priority Findings</CardTitle>
          <CardDescription>Open risks requiring reviewer attention</CardDescription>
        </CardHeader>
        <CardContent>
          <RiskTable />
        </CardContent>
      </Card>
    </div>
  );
}

