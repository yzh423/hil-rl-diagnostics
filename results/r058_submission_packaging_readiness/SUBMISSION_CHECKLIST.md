# R058 Submission Checklist

Date: 2026-07-03

## Immediate Gates

| Item | Status | Next action |
|---|---|---|
| Local PDF compile | Complete for current draft | Use project-local Tectonic cache and `paper/figures/` snapshots. |
| PDF visual QA | Complete for current draft | Repeat after venue-template integration or major layout changes. |
| Public Git source tracking | Ready | Continue using the synced public repository for current source state. |
| Institutional source archive decision | Decided | Create archive only from final verified submission tag. |
| Evidence/experiment optimization route | Planned in R059 | Execute only after selecting the smallest claim-relevant next experiment. |

## Verification To Run Before Packaging Complete

```powershell
python scripts\validate_evidence_registry.py
python scripts\audit_registry_numbers.py
python scripts\generate_claim_tables.py
python scripts\generate_methodology_extension.py
python scripts\generate_stack_boundary_appendix.py
python scripts\validate_provenance_package.py
python scripts\validate_document_links.py
python -m unittest discover -s tests
```

## Additional Checks Before Final Submission

- Rerun PDF visual QA after venue-template integration or major layout changes.
- Rerun `paper/PAPER_CLAIM_AUDIT.md` if numeric, comparison, or scope claims
  change.
- Rerun `paper/CITATION_AUDIT.md` if citation contexts or bibliography entries
  change.
- Produce a final source archive from a clean Git tag only after all checks
  pass.
