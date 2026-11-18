"""OpenCode Go replicas of the pending reviewer-response stages (built 2026-11-04, user request).

Nebius billing was halted with S5i at 33/72 and S5k at 0/48. OpenCode Go serves the same named models for the
attacker/auditor families and the judge (DeepSeek-V4-Pro, MiniMax-M3, GLM-5.3, Kimi-K3), but not the Qwen3-235B
population model. These stages therefore:
  * run the FULL designs of S5i / S5k again (all seeds), on one serving stack, under new stage ids, so the frozen
    Nebius stages stay single-provider;
  * use Qwen3.7-Plus (Go) as the population (honest compiler + agents) in place of Qwen3-235B-2507;
  * are pinned to provider opencode_go (the runner skips them under Nebius, and skips the Nebius stages under Go).
Same instruments, validity rules, outcome taxonomy and reading rules (RR_PLAN_v1) as the parent stages. EXPLORATORY.
They are NOT interchangeable with S5i/S5k: model weights may be served with different quantisation, reasoning
switches and sampling defaults, and the population differs. The 33 S5i cells done on Nebius give a provider
comparison on matched (cell, seed, governor) units; quote it as such, never pool the two stages.
"""
from __future__ import annotations

from .reviewer_exps import S5iRoleFactorial, S5kOracleFeedback

GO_NOTE = ("Provider: OpenCode Go (stand-in while Nebius billing was halted, 2026-11). Population Qwen3.7-Plus "
           "instead of Qwen3-235B-2507. Not poolable with the Nebius stage of the same design.")


class S5iGo(S5iRoleFactorial):
    id = "S5i_go"
    provider = "opencode_go"
    title = S5iRoleFactorial.title + " [OpenCode Go replica]"
    question = S5iRoleFactorial.question + " (Replica on OpenCode Go; population Qwen3.7-Plus.)"
    default_params = {**S5iRoleFactorial.default_params, "population": "qwen37_plus"}

    def analyze(self):
        return f"> {GO_NOTE}\n\n" + super().analyze()


class S5kGo(S5kOracleFeedback):
    id = "S5k_go"
    provider = "opencode_go"
    title = S5kOracleFeedback.title + " [OpenCode Go replica]"
    question = S5kOracleFeedback.question + " (Replica on OpenCode Go; population Qwen3.7-Plus.)"
    default_params = {**S5kOracleFeedback.default_params, "population": "qwen37_plus"}

    def analyze(self):
        return f"> {GO_NOTE}\n\n" + super().analyze()
