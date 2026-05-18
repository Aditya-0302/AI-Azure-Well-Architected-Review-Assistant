import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { riskFindings } from "@/data/platform";

export function RiskTable() {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Finding</TableHead>
          <TableHead>Pillar</TableHead>
          <TableHead>Severity</TableHead>
          <TableHead>Owner</TableHead>
          <TableHead>Status</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {riskFindings.map((finding) => (
          <TableRow key={finding.title}>
            <TableCell className="max-w-[360px] font-medium">{finding.title}</TableCell>
            <TableCell>{finding.pillar}</TableCell>
            <TableCell>
              <Badge variant={finding.severity === "High" ? "critical" : "warning"}>{finding.severity}</Badge>
            </TableCell>
            <TableCell>{finding.owner}</TableCell>
            <TableCell className="text-muted-foreground">{finding.status}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

