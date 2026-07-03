"""Evaluation protocol helpers for paper-facing experiment claims."""

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

__all__ = [
    "ClaimTableManifest",
    "ClaimTableRow",
    "NumericAuditIssue",
    "NumericAuditReport",
    "ProvenanceIssue",
    "ProvenanceValidationReport",
    "RegistryIssue",
    "RegistryValidationReport",
    "audit_registry_numbers",
    "build_main_costmatched_claims",
    "build_stack_boundary_claims",
    "build_trigger_repair_claims",
    "format_registry_report",
    "format_numeric_audit_report",
    "format_provenance_report",
    "read_registry_rows",
    "render_claims_latex_table",
    "render_claims_markdown_table",
    "repeat_summary_row",
    "summarize_repeats",
    "validate_current_provenance",
    "validate_evidence_registry",
    "write_claim_table_assets",
]
