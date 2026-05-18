import { ReportLibrary } from "@/components/reports/report-library";

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold">Review Reports</h2>
        <p className="mt-1 text-sm text-muted-foreground">Executive summaries, technical findings, exports, and remediation roadmaps.</p>
      </div>
      <ReportLibrary />
    </div>
  );
}

