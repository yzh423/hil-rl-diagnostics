"""Evaluation protocol helpers for paper-facing experiment claims."""

from .attention_diagnostics import (
    AttentionTraceSource,
    build_attention_trace_profile,
    collect_attention_trace_rows,
    finite_numeric_values,
    rows_for_strategy,
    write_profile_csv,
)
from .claim_tables import (
    ClaimTableManifest,
    ClaimTableRow,
    build_main_costmatched_claims,
    build_stack_boundary_claims,
    build_trigger_repair_claims,
    read_registry_rows,
    render_claims_latex_table,
    render_claims_markdown_table,
    write_claim_table_assets,
)
from .protocol import repeat_summary_row, summarize_repeats
from .registry_validation import (
    RegistryIssue,
    RegistryValidationReport,
    format_registry_report,
    validate_evidence_registry,
)
from .registry_numeric_audit import (
    NumericAuditIssue,
    NumericAuditReport,
    audit_registry_numbers,
    format_numeric_audit_report,
)
from .provenance_validation import (
    ProvenanceIssue,
    ProvenanceValidationReport,
    format_provenance_report,
    validate_current_provenance,
)
from .document_links import (
    DocumentLinkIssue,
    DocumentLinkReport,
    find_local_markdown_link_issues,
    format_document_link_report,
)
from .protocol_diagnostics import (
    build_derived_metric_rows,
    build_failure_taxonomy_rows,
    build_protocol_gate_matrix,
    read_csv_rows as read_protocol_diagnostic_csv_rows,
    render_latex_table,
    write_csv_rows,
)

__all__ = [
    "ClaimTableManifest",
    "ClaimTableRow",
    "AttentionTraceSource",
    "DocumentLinkIssue",
    "DocumentLinkReport",
    "NumericAuditIssue",
    "NumericAuditReport",
    "ProvenanceIssue",
    "ProvenanceValidationReport",
    "RegistryIssue",
    "RegistryValidationReport",
    "audit_registry_numbers",
    "build_attention_trace_profile",
    "build_derived_metric_rows",
    "build_failure_taxonomy_rows",
    "build_main_costmatched_claims",
    "build_protocol_gate_matrix",
    "build_stack_boundary_claims",
    "build_trigger_repair_claims",
    "collect_attention_trace_rows",
    "find_local_markdown_link_issues",
    "finite_numeric_values",
    "format_document_link_report",
    "format_registry_report",
    "format_numeric_audit_report",
    "format_provenance_report",
    "read_registry_rows",
    "read_protocol_diagnostic_csv_rows",
    "render_claims_latex_table",
    "render_claims_markdown_table",
    "render_latex_table",
    "repeat_summary_row",
    "rows_for_strategy",
    "summarize_repeats",
    "validate_current_provenance",
    "validate_evidence_registry",
    "write_claim_table_assets",
    "write_csv_rows",
    "write_profile_csv",
]
