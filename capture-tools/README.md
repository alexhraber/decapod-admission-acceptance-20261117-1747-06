# Portable reproduction carrier (Decapod #1757/#1758)

These are portable derivatives of the actually executed private capture
adapters, not a claim that these different bytes ran in the original experiment.
Only run locations, provider/model/actor configuration helper interpreter selection and reviewed pin metadata were parameterized. Original executed adapter hashes are in runtime.json.
The Rust observer remains the read-only correlation implementation; these host
carriers neither validate nor admit work. They are opt-in experiment tooling,
not mandatory CI dependencies or a new agent framework.

Prepare a fresh issue-owned fixture baseline as described in the evidence README,
with configured accepted base and fixed native commands. Configure normal Pi
provider authentication privately; this runner never imports, prints or changes
credentials. Use a new private output path that does not yet exist.

```sh
export DECAPOD_ACCEPTANCE_RUN=/absolute/new-private-run
export DECAPOD_ACCEPTANCE_REPO=/absolute/issue-owned-fixture-checkout
export DECAPOD_ACCEPTANCE_BASE=acceptance/1757/NEW-accepted-base
export DECAPOD_ACCEPTANCE_PI=/absolute/pi-0.73.1/node_modules/.bin/pi
export DECAPOD_ACCEPTANCE_KERNEL=/absolute/pinned-decapod-0.148.8
export DECAPOD_ACCEPTANCE_KERNEL_VERSION=0.148.8
export DECAPOD_ACCEPTANCE_KERNEL_SOURCE=18cbb30ca4d16a80810d8f3c0cecfc4073a83cbc
export DECAPOD_ACCEPTANCE_AGENT=pi-1758-reproduction
export DECAPOD_ACCEPTANCE_REPOSITORY_SLUG=OWNER/DISPOSABLE-REPOSITORY
export DECAPOD_ACCEPTANCE_RUN_ID=pi-1758-UNIQUE
export DECAPOD_ACCEPTANCE_PROVIDER=openai-codex
export DECAPOD_ACCEPTANCE_MODEL=gpt-6.1-sol
python3 run_pi.py
```

The objective is the single ordinary engineering sentence used in the original
run; an explicit DECAPOD_ACCEPTANCE_OBJECTIVE can select another reviewed revision.
The runner snapshots Git, copies the kernel into the private run, measures its
bytes, supplies a child-process-only PATH carrier, and observes actual Pi JSON.
It never repairs source, changes tools/results, injects follow-up prompts or
publishes a PR itself. It stops the owned process group on its recorded budget.
A failure remains a failure; inspect process-result.private.json, raw host events
and kernel evidence rather than treating a model's final statement as proof.

Inspect these scripts and the Pi package before execution. Original Python was
3.9.6 on macOS; these portable standard-library scripts also compile under 3.12.
The official Pi extension interface is type-only imported. No framebuffer,
background service, paid provider provisioning or browser is required.

Use the Rust observer's versioned capture schema to select safe sibling witnesses
from the raw records. Join each native invocation to its unique observed bash
interval, and retain each source digest. Independent GitHub PR and live-target
readback must be added after the process ends. Operator-owned controls must remain
separate from the model activity. Never export raw reasoning, session output,
credentials or machine paths. Uncaptured arbitrary host activity is unknown.

After the agent ends, independently obtain PR metadata and the actual live target
ref. Write forge-readback.private.json in the private run as the exact `gh pr view`
JSON fields `url,headRefOid,headRefName,baseRefOid,baseRefName,state,mergedAt`, plus
`actual_target` from `gh api repos/OWNER/REPO/git/ref/heads/BASE --jq .object.sha`.
Record these read-only operations against the experiment issue. Then:

```sh
python3 export_capture.py
/absolute/built-observer trace flight-recorder acceptance \
  --capture "$DECAPOD_ACCEPTANCE_RUN/public-witnesses/capture.json" \
  > "$DECAPOD_ACCEPTANCE_RUN/new-manifest.json"
```

Review only the allowlisted export for public release. The original execution
used the same correlation algorithm with private location constants; the
portable exporter takes those reviewed locations and pins from the environment.
Do not infer actual_target from the PR base field, label operator controls as
agent repairs, or turn this historical manifest into live admission authority.
