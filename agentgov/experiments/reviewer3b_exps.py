"""Reviewer-response stage v3, amendment 1 (2026-11-20; exploratory). See RR_PLAN_v3.md, "Amendments".

S5m2_attack_challenge  Re-run of S5m_attack_challenge with the attacker prompt the plan specifies. RR_PLAN_v3 says each
                       strategy is appended to "the unchanged attacker system prompt" of the S5b studies, i.e. the
                       INFORMED attacker prompt (X.ATTACKER_SYSTEM_INFORMED: the attacker is told the governor's hard
                       rules). S5m appended the strategies to the plain X.ATTACKER_SYSTEM instead, so its attackers
                       declared non-factual labels and were rejected by the hard rules (attacker deploy rate 0.09 vs
                       0.46 in S5b_C; standard-arm ASR 0.000): a floor that cannot test the strategies. S5m is kept and
                       reported as a disclosed deviation. S5m2 changes only (1) the base prompt, (2) fresh seeds 711-714,
                       and (3) the S5m analysis bug that dropped the second-judge ASR contrast (asr_j2 was present twice
                       when the per-episode extras were merged). Design, rotations, judges, strategies, validity rules and
                       reading rules R-M1..R-M3 and the consequence are those of S5m, unchanged.
"""
from __future__ import annotations

from .reviewer3_exps import STRATEGIES, S5mAttackChallenge


class S5m2AttackChallengeInformed(S5mAttackChallenge):
    id = "S5m2_attack_challenge"
    title = ("Attack challenge with the informed S5b attacker: strategies outside the original attacker prompt, incl. "
             "auditor-directed prompt injection")
    question = ("With the informed attacker of the S5b studies, does plain content auditing keep attack success low against "
                "attack strategies the attacker never used before (impersonated authority, quoted instructions, "
                "implicature, multilingual text, auditor-directed prompt injection), relative to the standard strategy, "
                "with two independent judges?")
    default_params = {**S5mAttackChallenge.default_params, "seeds": [711, 712, 713, 714]}

    def _attacker_system(self, unit):
        # the S5b attacker prompt (informed, inherited from S5v2InformedAttacker) + the strategy text
        return self.attacker_system + STRATEGIES[unit["strategy"]]

    def _episode_extras(self, el):
        # S5m fix: drop the run-level asr_j2 so the per-episode value (identical by construction) is not suffixed away
        return super()._episode_extras(el.drop(columns=[c for c in ("asr_j2",) if c in el.columns]))

    def analyze(self):
        txt = super().analyze()
        note = ("Amendment 1 (2026-11-20): attacker prompt = the informed S5b prompt + strategy text (S5m used the plain "
                "prompt; kept as a disclosed deviation). Seeds 711-714. Rules R-M1..R-M3 unchanged.")
        parts = txt.split("\n\n", 1)
        return parts[0] + "\n\n" + note + ("\n\n" + parts[1] if len(parts) > 1 else "")
