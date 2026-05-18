import { ArrowDownRight, ArrowUpRight } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { executiveMetrics } from "@/data/platform";

export function MetricStrip() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {executiveMetrics.map((metric) => {
        const positive = metric.change.startsWith("+") || metric.change.startsWith("-");
        const Icon = positive ? ArrowUpRight : ArrowDownRight;
        return (
          <Card key={metric.label}>
            <CardContent className="p-5">
              <div className="flex items-start justify-between gap-3">
                <p className="text-sm text-muted-foreground">{metric.label}</p>
                <Badge variant={metric.tone === "warning" ? "warning" : "success"}>
                  <Icon className="mr-1 h-3 w-3" />
                  {metric.change}
                </Badge>
              </div>
              <div className="mt-4 flex items-baseline gap-1">
                <span className="text-3xl font-semibold">{metric.value}</span>
                <span className="text-sm text-muted-foreground">{metric.unit}</span>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}

