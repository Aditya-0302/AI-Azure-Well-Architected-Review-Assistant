import { ScoringMatrix } from "@/components/scoring/scoring-matrix";

export default function ScoringPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold">Architecture Scoring</h2>
        <p className="mt-1 text-sm text-muted-foreground">Pillar maturity, deterministic scoring, and finding impact.</p>
      </div>
      <ScoringMatrix />
    </div>
  );
}

