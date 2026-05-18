import { UploadCenter } from "@/components/upload/upload-center";

export default function UploadPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold">Upload Center</h2>
        <p className="mt-1 text-sm text-muted-foreground">Evidence ingestion, chunking, embeddings, and Azure AI Search indexing.</p>
      </div>
      <UploadCenter />
    </div>
  );
}

