import { ReviewVolumeChart } from "@/components/analytics/review-volume-chart";
import { SeverityDistribution } from "@/components/analytics/severity-distribution";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";

export function AnalyticsOverview() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {[
          ["Mean score", "77.4", "+5.2"],
          ["Review cycle", "3.1d", "-1.4d"],
          ["Token spend", formatCurrency(18420), "+9%"],
          ["Savings pipeline", formatCurrency(318000), "+18%"]
        ].map(([label, value, change]) => (
          <Card key={label}>
            <CardContent className="p-5">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm text-muted-foreground">{label}</p>
                <Badge variant="secondary">{change}</Badge>
              </div>
              <p className="mt-4 text-3xl font-semibold">{value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_0.8fr]">
        <Card>
          <CardHeader>
            <CardTitle>Review Throughput</CardTitle>
          </CardHeader>
          <CardContent>
            <ReviewVolumeChart />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Finding Severity</CardTitle>
          </CardHeader>
          <CardContent>
            <SeverityDistribution />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

