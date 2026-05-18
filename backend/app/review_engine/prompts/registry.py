from __future__ import annotations

from app.review_engine.schemas.common import ArchitectureReviewContext, WellArchitectedPillar
from app.review_engine.schemas.pillar import PillarReviewResult

PROMPT_VERSION = "waf-review-engine-v1"


PILLAR_RUBRICS: dict[WellArchitectedPillar, str] = {
    WellArchitectedPillar.SECURITY: """
Evaluate identity, access control, network isolation, data protection, key management,
secrets handling, threat detection, vulnerability management, governance, compliance,
secure configuration, and incident readiness. Look for Azure anti-patterns such as
public data planes without justification, broad RBAC, missing private endpoints,
unmanaged keys, absent Defender coverage, weak logging, and unclear threat models.
""",
    WellArchitectedPillar.RELIABILITY: """
Evaluate availability targets, fault isolation, zone and region strategy, backup,
restore testing, disaster recovery, RTO/RPO alignment, dependency resilience,
capacity failover, deployment safety, health probes, and chaos/resiliency testing.
Look for single points of failure, missing backup validation, no regional recovery
plan, tight coupling, and undocumented failure modes.
""",
    WellArchitectedPillar.COST_OPTIMIZATION: """
Evaluate cost governance, budgets, tagging, SKU selection, autoscaling, reservations,
savings plans, storage lifecycle, waste detection, unit economics, chargeback,
forecasting, and right-sizing. Look for oversized SKUs, always-on nonproduction,
missing cost alerts, unmanaged data retention, and unclear ownership.
""",
    WellArchitectedPillar.PERFORMANCE_EFFICIENCY: """
Evaluate scalability, latency, throughput, caching, data partitioning, async patterns,
load testing, capacity management, service limits, CDN/front-door use, database
performance, and workload-specific scaling. Look for chatty dependencies, no load
test evidence, bottlenecked data stores, missing autoscale, and poor cache strategy.
""",
    WellArchitectedPillar.OPERATIONAL_EXCELLENCE: """
Evaluate infrastructure as code, CI/CD, change safety, observability, alerting,
incident response, runbooks, SLOs, release governance, automation, environment
parity, inventory, and continuous improvement. Look for manual changes, missing
dashboards, weak incident processes, no deployment rollback, and unowned operations.
""",
}


SYSTEM_PROMPT = """
You are a senior staff-level Azure cloud architect performing an enterprise
Azure Well-Architected Framework review.

Your job:
- Evaluate only the requested Well-Architected pillar.
- Ground every material observation in the supplied architecture context and evidence.
- Distinguish confirmed facts from inferred risks and missing evidence.
- Do not invent architecture details.
- Prefer Azure-native recommendations that are practical for enterprise production.
- Return only JSON that conforms to the provided schema.

Severity guidance:
- critical: credible path to severe outage, breach, compliance failure, or major business loss.
- high: material architectural risk requiring near-term remediation.
- medium: meaningful risk or optimization opportunity with bounded impact.
- low: hygiene issue or lower-risk best-practice gap.
- informational: observation or clarification with no direct risk.

Citation guidance:
- High and critical findings should include citations whenever evidence is available.
- If evidence is insufficient, create missing_evidence entries and use evidence_status=missing_evidence.
"""


SYNTHESIS_SYSTEM_PROMPT = """
You are the lead Azure architecture reviewer creating the final executive synthesis
from five pillar-specific Well-Architected review results.

Your job:
- Produce a balanced, executive-ready synthesis.
- Identify cross-pillar tradeoffs and modernization opportunities.
- Sequence a pragmatic improvement roadmap.
- Do not introduce new findings that are not supported by the pillar results.
- Return only JSON that conforms to the provided schema.
"""


def build_pillar_prompt(
    *,
    pillar: WellArchitectedPillar,
    context: ArchitectureReviewContext,
) -> str:
    evidence_block = "\n\n".join(
        (
            f"Source ID: {item.source_id}\n"
            f"Title: {item.title}\n"
            f"Type: {item.source_type}\n"
            f"Locator: {item.locator}\n"
            f"Trust Level: {item.trust_level}\n"
            f"Content:\n{item.content}"
        )
        for item in context.evidence
    )
    if not evidence_block:
        evidence_block = "No additional evidence supplied. Identify missing evidence explicitly."

    return f"""
Prompt version: {PROMPT_VERSION}
Requested pillar: {pillar.value}

Pillar rubric:
{PILLAR_RUBRICS[pillar].strip()}

Architecture context:
- Tenant ID: {context.tenant_id}
- Project ID: {context.project_id}
- Architecture version ID: {context.architecture_version_id}
- Workload name: {context.workload_name}
- Business criticality: {context.business_criticality}
- Environment: {context.environment}
- Regions: {", ".join(context.regions) or "not provided"}
- Azure services: {", ".join(context.azure_services) or "not provided"}
- Compliance requirements: {", ".join(context.compliance_requirements) or "not provided"}
- Target RTO: {context.target_rto or "not provided"}
- Target RPO: {context.target_rpo or "not provided"}
- Monthly budget USD: {context.monthly_budget_usd if context.monthly_budget_usd is not None else "not provided"}

Architecture summary:
{context.architecture_summary}

Workload description:
{context.workload_description}

Evidence:
{evidence_block}

Return a {PillarReviewResult.__name__} JSON object for pillar={pillar.value}.
Ensure the pillar field exactly equals "{pillar.value}".
"""


def build_synthesis_prompt(*, context: ArchitectureReviewContext, pillar_json: str) -> str:
    return f"""
Prompt version: {PROMPT_VERSION}

Architecture context:
- Workload name: {context.workload_name}
- Business criticality: {context.business_criticality}
- Environment: {context.environment}
- Azure services: {", ".join(context.azure_services) or "not provided"}
- Compliance requirements: {", ".join(context.compliance_requirements) or "not provided"}

Pillar review results JSON:
{pillar_json}

Create the final synthesis. Roadmap items should be ordered by risk reduction,
dependency, and enterprise delivery practicality.
"""

