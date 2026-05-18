const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

export type ApiError = {
  code: string;
  message: string;
  correlation_id?: string;
  details?: Record<string, unknown>;
};

export async function apiRequest<TResponse>(
  path: string,
  init: RequestInit = {}
): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init.headers
    }
  });

  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as ApiError | null;
    throw new Error(body?.message ?? `API request failed with ${response.status}`);
  }

  return (await response.json()) as TResponse;
}

export type ArchitectureEvaluationPayload = {
  project_id?: string;
  architecture_version_id?: string;
  workload_name: string;
  workload_description: string;
  business_criticality: string;
  environment: string;
  regions: string[];
  azure_services: string[];
  compliance_requirements: string[];
  architecture_summary: string;
  requested_pillars: string[];
};

export function evaluateArchitecture(payload: ArchitectureEvaluationPayload) {
  return apiRequest("/reviews/evaluate", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

