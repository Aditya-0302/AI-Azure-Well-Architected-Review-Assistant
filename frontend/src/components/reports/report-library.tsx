import { Download, FileJson, FileText, MoreHorizontal } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { reports, roadmapItems } from "@/data/platform";

export function ReportLibrary() {
  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_360px]">
      <Card>
        <CardHeader>
          <CardTitle>Review Reports</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Report</TableHead>
                <TableHead>Audience</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Generated</TableHead>
                <TableHead className="w-20">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {reports.map((report) => {
                const Icon = report.type === "JSON" ? FileJson : FileText;
                return (
                  <TableRow key={report.name}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Icon className="h-4 w-4 text-primary" />
                        <div>
                          <p className="font-medium">{report.name}</p>
                          <p className="text-xs text-muted-foreground">{report.type}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>{report.audience}</TableCell>
                    <TableCell>
                      <Badge variant={report.status === "Approved" ? "success" : "warning"}>{report.status}</Badge>
                    </TableCell>
                    <TableCell>{report.generated}</TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <Button size="icon" variant="ghost" aria-label="Download report">
                          <Download className="h-4 w-4" />
                        </Button>
                        <Button size="icon" variant="ghost" aria-label="More actions">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Improvement Roadmap</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {roadmapItems.map((item) => (
            <div key={item.sequence} className="rounded-md border p-3">
              <div className="flex items-start gap-3">
                <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-primary/10 text-sm font-semibold text-primary">
                  {item.sequence}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-semibold">{item.title}</p>
                  <p className="mt-1 text-xs text-muted-foreground">{item.pillar} · Effort {item.effort}</p>
                </div>
                <Badge variant={item.impact === "Critical" ? "critical" : item.impact === "High" ? "warning" : "secondary"}>
                  {item.impact}
                </Badge>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}

