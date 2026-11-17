import { execFileSync } from 'node:child_process';
import { appendFileSync } from 'node:fs';
import type { ExtensionAPI } from '@mariozechner/pi-coding-agent';
// Observe only. No prompt injection, block return, input edit, result patch or repair.
export default function capture(pi: ExtensionAPI) {
  for (const phase of ['tool_call', 'tool_result'] as const) {
    pi.on(phase, async (event, ctx) => {
      try {
        execFileSync(process.env.DECAPOD_ACCEPTANCE_PYTHON!, [process.env.DECAPOD_ACCEPTANCE_SNAPSHOT_HELPER!], {
          input: JSON.stringify({ phase, event, cwd: ctx.cwd }), timeout: 15000, stdio: ['pipe','ignore','pipe'],
        });
      } catch {
        appendFileSync(process.env.DECAPOD_ACCEPTANCE_RUN! + '/capture-errors.private.jsonl',
          JSON.stringify({ phase, toolCallId: event.toolCallId, error: 'host_snapshot_unavailable' })+'\n', { mode: 0o600 });
      }
    });
  }
}
