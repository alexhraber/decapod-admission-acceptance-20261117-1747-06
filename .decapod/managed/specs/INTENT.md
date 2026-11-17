# Intent

## Project Purpose
Repository authorization acceptance is a small JavaScript library for callers deciding whether an actor may read a repository. README.md defines the security outcome; `src/access.cjs` exports `canRead(actor, repository)`.

## Required Outcome
- REQ-READ: Only active members of the repository's organization may read. Within that organization, ownership or an explicit grant for this exact repository is required.
- REQ-DENY: Anonymous, revoked, foreign-organization and ungranted actors must be denied. A grant for another repository is insufficient. Ownership does not bypass active membership.
- REQ-PROOF: Preserve a genuine failing baseline through structured Decapod validation before repairing access behavior, then obtain fresh full proof for the exact publication candidate.
- REQ-GUARD: Preserve `src/guard.txt` and its independent accepted proof command.

## Current Baseline and Scope
The seeded `src/access.cjs` currently checks only active organization membership. It does not enforce REQ-READ. The planned repair is confined to that predicate and authored living specifications; the accepted proof configuration and convenience test remain unchanged.

The proof authority is the ten literal assertions in `.decapod/config.toml`, plus the independent source guard. `tests/access.contract.cjs` is a readable copy, not replacement authority. No server, database, cloud service, dependency installation, deployment or performance target is part of this product.

## Delivery Boundary
Work is owned by DecapodLabs/decapod #1758, following setup #1757. Publication uses Decapod, targets the configured isolated acceptance branch, and remains unmerged. Historical main, acceptance-evidence and PR #1 are outside scope. A failed prerequisite is not the required authorization regression evidence; validation must actually execute the accepted assertions. No merge authorization is implied.

<!-- decapod:codebase-attestation:start -->

## Codebase Attestation

- Repository signal fingerprint: `4e2cacf2680f182547e1a3cee504514bba559d43ee55e96f8599980ea3113557`
- Significant implementation surfaces: `README.md/` (1 files), `src/` (2 files)
- Refreshed from the current codebase by `decapod rpc --op specs.refresh`
<!-- decapod:codebase-attestation:end -->
