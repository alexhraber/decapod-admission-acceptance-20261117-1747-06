# Interfaces

## Project Purpose
An isolated repository access module with accepted independent source checks and exact-evidence GitHub publication

## Authoring Scope and Evidence
Project: Repository authorization acceptance. This is an initial authoring scaffold, not an implementation attestation.

Describe the configured project from purpose to architecture to implementation depth. Start with the whole product: its users, problem, outcomes, and boundaries; then explain the system and its components, interfaces, state, operations, security, and proof. Ground factual prose in the repository's config, README/product documentation, source paths and symbols, contracts, and tests. Distinguish implemented behavior, intended behavior, assumptions, and unresolved gaps. A narrow task changes the relevant part of this whole-project account; it must not replace project-wide identity with the latest task, release workflow, or tooling. Record task-specific scope and evidence in the current change's governance record. Templates and declared capabilities are authoring/proof obligations, not evidence that a runtime guarantee exists. Preserve authored prose during generated refreshes. If configured metadata and explicit project-level sections are absent, leave project identity unknown and ask for or author grounded context rather than promoting an arbitrary legacy/task line.

Use the seeded context below as a starting point to verify against repository sources. Replace example diagrams, suggested controls, targets, tables, and blank fields with source-grounded prose; mark non-applicable topics with a reason. Do not adopt a store, queue, server, CI provider, replay guarantee, or service level merely because it appears in a template.

## Contract Principles
The public CommonJS export is `require('./src/access.cjs').canRead(actor,
repository)`. It is a synchronous, side-effect-free Boolean predicate, not a
mutating RPC or an authentication service.

Actor records carry `id`, `organizationId`, `active`, and optional array
`repositoryIds`; repository records carry `id`, `organizationId`, and `ownerId`.
For well-formed IDs, authorization requires `active === true`, exact organization
equality, and either exact owner equality or inclusion of the repository ID in
the grants array. Null actors/repositories return false. Missing or malformed
grant arrays deny nonowners; owners do not need a grant array. Revocation and
foreign organization membership deny owners as well as ordinary members.

Record authentication and ID validation remain caller responsibilities; this
change does not introduce schema parsing, remote lookups, or durable state.
Accepted proof covers ten specified actor combinations, not arbitrary malformed
input or end-to-end caller authentication.

## Generated Contract Depth
Generated interface specs should include:
- API/CLI contracts with request/response schemas.
- Read/write ownership for each storage path.
- Idempotency and retry behavior for mutations.
- Typed failure classes and recovery instructions.

## API / RPC Contracts
| Interface | Method | Request Schema | Response Schema | Errors | Idempotency |
|---|---|---|---|---|---|
| `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

## Event Consumers
| Consumer | Event | Ordering Requirement | Retry Policy | DLQ Policy |
|---|---|---|---|---|
| `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

## Outbound Dependencies
| Dependency | Purpose | SLA | Timeout | Circuit-Breaker |
|---|---|---|---|---|
| `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

## Inbound Contracts
- API / RPC entrypoints:
- CLI surfaces:
- Event/webhook consumers:
- Repository-detected surfaces: not detected yet

## Data Ownership
- Source-of-truth tables/collections:
- Cross-boundary read models:
- Consistency expectations:

## Error Taxonomy Example (service_or_library)
```ts
export enum ApiErrorCode {
  Validation = "validation_failed",
  UpstreamTimeout = "upstream_timeout",
  Conflict = "conflict"
}
```

## Failure Semantics
| Failure Class | Retry/Backoff | Client Contract | Observability |
|---|---|---|---|
| Validation | No retry | 4xx typed error | warn log + metric |
| Dependency timeout | Exponential backoff | 503 with retryable code | error log + alert |
| Conflict | Conditional retry | 409 with conflict detail | info log + metric |

## Timeout Budget
| Hop | Budget (ms) | Notes |
|---|---|---|
| Client -> Edge/API | 500 | Includes auth + routing |
| API -> Domain | 300 | Includes validation |
| Domain -> Store/Dependency | 200 | Includes retry overhead |

## Interface Versioning
- Version strategy (`v1`, date-based, semver):
- Backward-compatibility guarantees:
- Deprecation window and removal policy:

## CLI and Machine-Readable Contract
| Surface | Invocation/Shape | Reads | Writes | Output Stability | Proof |
|---|---|---|---|---|---|
| Human CLI | | | | | |
| JSON/automation | | | | | |
| RPC/plugin | | | | | |
| Event/file boundary | | | | | |

## Compatibility Matrix
| Contract | Current Version | Consumers | Additive Changes | Breaking Changes | Migration Trigger |
|---|---|---|---|---|---|
| Request/input | | | | | |
| Response/output | | | | | |
| Persisted data | | | | | |
| Events/artifacts | | | | | |

## Observability Contract
- Correlation/request identity:
- Structured fields required on success:
- Structured fields required on failure:
- Audit events for sensitive mutations:
- Metrics and traces that prove latency, retries, and outcomes:

## Interface Change Review
- [ ] The owner and source of truth are named for every changed field.
- [ ] Retry, idempotency, timeout, and conflict behavior are explicit.
- [ ] Consumers can distinguish validation, authorization, conflict,
  dependency, and internal failures.
- [ ] Backward compatibility or migration instructions are published.


## Accepted repository access contract

The application exports canRead(actor, repository) from src/access.cjs. Active
organization membership alone is insufficient: explicit repository grant or
active ownership is required, and revoked/foreign/anonymous actors are denied.
The native proof command contains ten independently accepted assertion literals
plus a separate source guard. Agent-authored tests cannot replace these accepted
commands. Preserve a genuine baseline validation failure, then agent-initiated
diagnosis/repair and fresh full evidence before exact-head/base GitHub admission.
The operator seeds the initial defect; no operator supplies the repair. Fixture
actions belong to Decapod #1757/#1758. Historical refs and PR #1 are immutable;
the new issue-scoped target is independent. Admission never authorizes merge.

<!-- decapod:codebase-attestation:start -->

## Codebase Attestation

- Repository signal fingerprint: `2fe66f34809a3076c48a682476ae2b859d57ae142d7999bd39a5fafd22588b25`
- Significant implementation surfaces: `README.md/` (1 files), `src/` (2 files)
- Refreshed from the current codebase by `decapod rpc --op specs.refresh`
<!-- decapod:codebase-attestation:end -->
