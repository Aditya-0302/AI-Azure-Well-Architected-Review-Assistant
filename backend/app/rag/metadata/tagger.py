from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import PurePosixPath


class MetadataTagger:
    PILLAR_TERMS = {
        "security": [
            "identity",
            "entra",
            "key vault",
            "private endpoint",
            "defender",
            "encryption",
            "rbac",
            "firewall",
            "zero trust",
        ],
        "reliability": [
            "availability",
            "zone",
            "region",
            "backup",
            "disaster recovery",
            "rto",
            "rpo",
            "failover",
            "resiliency",
        ],
        "performance_efficiency": [
            "latency",
            "throughput",
            "autoscale",
            "cache",
            "cdn",
            "load test",
            "capacity",
        ],
        "cost_optimization": [
            "cost",
            "budget",
            "reservation",
            "savings plan",
            "sku",
            "rightsize",
            "tagging",
        ],
        "operational_excellence": [
            "monitor",
            "alert",
            "logging",
            "deployment",
            "devops",
            "runbook",
            "incident",
            "iac",
        ],
    }

    AZURE_SERVICE_PATTERNS = {
        "azure_openai": r"\b(azure openai|openai)\b",
        "azure_ai_search": r"\b(azure ai search|cognitive search|azure search)\b",
        "azure_blob_storage": r"\b(blob storage|storage account|azure storage)\b",
        "azure_key_vault": r"\b(key vault)\b",
        "azure_kubernetes_service": r"\b(aks|kubernetes service)\b",
        "azure_container_apps": r"\b(container apps)\b",
        "azure_functions": r"\b(azure functions|function app)\b",
        "azure_sql": r"\b(azure sql|sql database)\b",
        "cosmos_db": r"\b(cosmos db|cosmosdb)\b",
        "app_service": r"\b(app service|web app)\b",
        "api_management": r"\b(api management|apim)\b",
        "front_door": r"\b(front door)\b",
        "application_gateway": r"\b(application gateway|app gateway)\b",
        "virtual_network": r"\b(vnet|virtual network)\b",
        "service_bus": r"\b(service bus)\b",
        "event_grid": r"\b(event grid)\b",
        "azure_monitor": r"\b(azure monitor|application insights|log analytics)\b",
    }

    def build_document_metadata(
        self,
        *,
        tenant_id: str,
        blob_name: str,
        file_name: str,
        content_type: str | None,
        document_type: str,
        sensitivity_label: str,
        source_uri: str | None,
        project_id: str | None,
        architecture_version_id: str | None,
        extra_metadata: dict[str, str],
        text: str,
    ) -> dict[str, object]:
        extension = PurePosixPath(file_name).suffix.lower().lstrip(".")
        lowered = text.lower()
        pillars = [
            pillar
            for pillar, terms in self.PILLAR_TERMS.items()
            if any(term in lowered for term in terms)
        ]
        services = [
            service
            for service, pattern in self.AZURE_SERVICE_PATTERNS.items()
            if re.search(pattern, lowered)
        ]

        return {
            "tenant_id": tenant_id,
            "project_id": project_id,
            "architecture_version_id": architecture_version_id,
            "blob_name": blob_name,
            "file_name": file_name,
            "content_type": content_type,
            "file_extension": extension,
            "document_type": document_type,
            "sensitivity_label": sensitivity_label,
            "source_uri": source_uri,
            "pillars": pillars,
            "azure_services": services,
            "ingested_at": datetime.now(UTC).isoformat(),
            **extra_metadata,
        }

