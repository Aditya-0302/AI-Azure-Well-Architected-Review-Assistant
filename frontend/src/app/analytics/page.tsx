import { AnalyticsOverview } from "@/components/analytics/analytics-overview";

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold">Analytics</h2>
        <p className="mt-1 text-sm text-muted-foreground">Review throughput, risk distribution, AI usage, and FinOps impact.</p>
      </div>
      <AnalyticsOverview />
    </div>
  );
}

