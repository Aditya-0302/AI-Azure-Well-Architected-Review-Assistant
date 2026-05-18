"use client";

import { useMemo, useState } from "react";
import { CheckCircle2, Clock3, FileArchive, FileText, UploadCloud } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { uploadedDocuments } from "@/data/platform";

const statusVariant: Record<string, "success" | "warning" | "secondary"> = {
  Indexed: "success",
  Processing: "warning",
  Queued: "secondary"
};

export function UploadCenter() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const totalSize = useMemo(
    () => selectedFiles.reduce((sum, file) => sum + file.size, 0),
    [selectedFiles]
  );

  return (
    <div className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
      <Card>
        <CardHeader>
          <CardTitle>Upload Evidence</CardTitle>
        </CardHeader>
        <CardContent className="space-y-5">
          <label className="flex min-h-[260px] cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed bg-muted/25 p-8 text-center transition-colors hover:bg-muted/45">
            <UploadCloud className="h-10 w-10 text-primary" />
            <span className="mt-4 text-sm font-semibold">Architecture documents, policies, exports, diagrams</span>
            <span className="mt-2 text-xs text-muted-foreground">PDF, Markdown, CSV, JSON, Bicep, Terraform, Draw.io</span>
            <input
              type="file"
              className="sr-only"
              multiple
              onChange={(event) => setSelectedFiles(Array.from(event.target.files ?? []))}
            />
          </label>

          <div className="grid gap-3 sm:grid-cols-3">
            <div className="rounded-md border p-3">
              <p className="text-xs text-muted-foreground">Selected</p>
              <p className="mt-1 text-lg font-semibold">{selectedFiles.length}</p>
            </div>
            <div className="rounded-md border p-3">
              <p className="text-xs text-muted-foreground">Size</p>
              <p className="mt-1 text-lg font-semibold">{(totalSize / 1024 / 1024).toFixed(1)} MB</p>
            </div>
            <div className="rounded-md border p-3">
              <p className="text-xs text-muted-foreground">Pipeline</p>
              <p className="mt-1 text-lg font-semibold">RAG</p>
            </div>
          </div>

          <Button className="w-full" disabled={!selectedFiles.length}>
            <FileArchive className="h-4 w-4" />
            Start ingestion
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Ingestion Queue</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Document</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Chunks</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {uploadedDocuments.map((document) => (
                <TableRow key={document.name}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <FileText className="h-4 w-4 text-muted-foreground" />
                      <span className="font-medium">{document.name}</span>
                    </div>
                  </TableCell>
                  <TableCell>{document.type}</TableCell>
                  <TableCell>
                    <Badge variant={statusVariant[document.status]}>{document.status}</Badge>
                  </TableCell>
                  <TableCell>{document.chunks}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="rounded-md border p-4">
              <div className="flex items-center gap-2 text-sm font-semibold">
                <Clock3 className="h-4 w-4 text-warning" />
                Current pipeline
              </div>
              <Progress value={62} className="mt-4" />
              <p className="mt-2 text-xs text-muted-foreground">Extracting metadata and embeddings</p>
            </div>
            <div className="rounded-md border p-4">
              <div className="flex items-center gap-2 text-sm font-semibold">
                <CheckCircle2 className="h-4 w-4 text-success" />
                Search index
              </div>
              <Progress value={88} className="mt-4" />
              <p className="mt-2 text-xs text-muted-foreground">Tenant evidence coverage</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

