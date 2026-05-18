import {
  Activity,
  BarChart3,
  Bot,
  FileText,
  Gauge,
  LayoutDashboard,
  ShieldCheck,
  UploadCloud
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import type { Route } from "next";

type NavigationItem = {
  title: string;
  href: Route;
  icon: LucideIcon;
};

export const navigationItems: NavigationItem[] = [
  { title: "Dashboard", href: "/", icon: LayoutDashboard },
  { title: "Upload", href: "/upload", icon: UploadCloud },
  { title: "AI Chat", href: "/chat", icon: Bot },
  { title: "Reports", href: "/reports", icon: FileText },
  { title: "Analytics", href: "/analytics", icon: BarChart3 },
  { title: "Scoring", href: "/scoring", icon: Gauge }
];

export const pillarScores = [
  { pillar: "Security", key: "security", score: 84, maturity: 4, delta: 7, status: "Managed" },
  { pillar: "Reliability", key: "reliability", score: 76, maturity: 3, delta: 4, status: "Defined" },
  { pillar: "Cost Optimization", key: "cost", score: 69, maturity: 3, delta: -3, status: "Defined" },
  { pillar: "Performance Efficiency", key: "performance", score: 81, maturity: 4, delta: 5, status: "Managed" },
  { pillar: "Operational Excellence", key: "operations", score: 73, maturity: 3, delta: 6, status: "Defined" }
];

export const executiveMetrics = [
  { label: "Architecture score", value: "77", unit: "/100", change: "+5.2", tone: "success" },
  { label: "Open high risks", value: "8", unit: "", change: "-3", tone: "success" },
  { label: "Reviews completed", value: "42", unit: "", change: "+11", tone: "success" },
  { label: "Projected savings", value: "$318K", unit: "", change: "+18%", tone: "warning" }
];

export const riskFindings = [
  {
    title: "Private endpoint coverage is incomplete for data services",
    pillar: "Security",
    severity: "High",
    owner: "Platform Security",
    status: "In review"
  },
  {
    title: "RTO target is not backed by regional failover evidence",
    pillar: "Reliability",
    severity: "High",
    owner: "Cloud Architecture",
    status: "Action needed"
  },
  {
    title: "Nonproduction workloads run premium SKUs continuously",
    pillar: "Cost",
    severity: "Medium",
    owner: "FinOps",
    status: "Planned"
  },
  {
    title: "Load testing does not cover peak claims intake windows",
    pillar: "Performance",
    severity: "Medium",
    owner: "SRE",
    status: "Planned"
  }
];

export const scoreTrend = [
  { month: "Jan", Security: 72, Reliability: 66, Cost: 61, Performance: 70, Operations: 64 },
  { month: "Feb", Security: 74, Reliability: 68, Cost: 63, Performance: 72, Operations: 66 },
  { month: "Mar", Security: 77, Reliability: 70, Cost: 65, Performance: 75, Operations: 68 },
  { month: "Apr", Security: 80, Reliability: 73, Cost: 68, Performance: 78, Operations: 71 },
  { month: "May", Security: 84, Reliability: 76, Cost: 69, Performance: 81, Operations: 73 }
];

export const reviewVolume = [
  { week: "W1", completed: 8, findings: 29 },
  { week: "W2", completed: 11, findings: 34 },
  { week: "W3", completed: 9, findings: 22 },
  { week: "W4", completed: 14, findings: 38 },
  { week: "W5", completed: 12, findings: 31 }
];

export const uploadedDocuments = [
  { name: "enterprise-claims-architecture.pdf", type: "Architecture", status: "Indexed", chunks: 128 },
  { name: "landing-zone-policy.md", type: "Policy", status: "Indexed", chunks: 42 },
  { name: "network-topology.drawio", type: "Diagram", status: "Queued", chunks: 0 },
  { name: "cost-export-q2.csv", type: "FinOps", status: "Processing", chunks: 18 }
];

export const chatMessages = [
  {
    role: "assistant",
    content:
      "The current review shows the strongest evidence in Security and Performance. Reliability needs regional failover proof before the score should be treated as final.",
    citation: "Review run 2026.05"
  },
  {
    role: "user",
    content: "What should we remediate first for the claims platform?",
    citation: null
  },
  {
    role: "assistant",
    content:
      "Prioritize private endpoint gaps and failover validation. Those two changes reduce breach exposure and outage risk without forcing a broad redesign.",
    citation: "Security finding 1, Reliability finding 2"
  }
];

export const reports = [
  { name: "Executive WAF Summary", type: "PDF", audience: "CIO", status: "Approved", generated: "May 18, 2026" },
  { name: "Technical Remediation Plan", type: "PDF", audience: "Architecture Review Board", status: "Draft", generated: "May 18, 2026" },
  { name: "Security Findings Export", type: "JSON", audience: "Security Engineering", status: "Approved", generated: "May 17, 2026" },
  { name: "FinOps Opportunity Register", type: "CSV", audience: "Finance", status: "Approved", generated: "May 16, 2026" }
];

export const roadmapItems = [
  { sequence: 1, title: "Close public data-plane exposure", pillar: "Security", effort: "M", impact: "Critical" },
  { sequence: 2, title: "Run regional failover exercise", pillar: "Reliability", effort: "L", impact: "High" },
  { sequence: 3, title: "Apply nonproduction schedules", pillar: "Cost", effort: "S", impact: "Medium" },
  { sequence: 4, title: "Expand peak load test coverage", pillar: "Performance", effort: "M", impact: "Medium" },
  { sequence: 5, title: "Standardize alert ownership", pillar: "Operations", effort: "S", impact: "Medium" }
];

export const architectureNodes = [
  { label: "Front Door", tone: "azure", x: "8%", y: "40%" },
  { label: "API Management", tone: "primary", x: "28%", y: "30%" },
  { label: "App Service", tone: "success", x: "48%", y: "22%" },
  { label: "Azure SQL", tone: "warning", x: "70%", y: "30%" },
  { label: "Key Vault", tone: "critical", x: "48%", y: "60%" },
  { label: "Monitor", tone: "primary", x: "72%", y: "66%" }
];

export const activeReview = {
  name: "Enterprise Claims Platform",
  owner: "Cloud Architecture Board",
  environment: "Production",
  status: "Reviewer approval",
  model: "GPT-4o",
  icon: ShieldCheck
};
