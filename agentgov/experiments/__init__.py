"""Experiment registry. Add a new stage by subclassing Experiment and listing it here."""
from .probes import S0Connectivity, S1InterfaceProbe
from .gcge_exps import (S2GCGEReplication, S3GCGECrossModel, S5AdaptiveAttacker, S6RiskRouting,
                        S5v2InformedAttacker, S6v2ImpactRouting, S3bTextJudgedIntegrity,
                        S5bRoleRotation, A0AttackerInterface)
from .calibration import A1AuditCalibration, A2JudgeValidation, H1IndependentLabels
from .bank_exps import A3FixedBank
from .memory_exps import S5dMemoryVariants
from .replay_exps import S5eMemoryReplay, S5fSpotlightReplay
from .rule_exps import A5RuleByRule
from .guard_exps import A6LlamaGuard
from .h1_judges import A4H1Judges
from .confirmatory_exps import S3bConfirm, S5bConfirm, S7bConfirm, A7COutsideJudge
from .quarantine_exps import S5gQuarantineReplay
from .followup_exps import S7cNonResponse, S5hLiveQuarantine
from .planning_exps import S4PlanningBackbone, S7JointFactorial, S8JointController, S4bScenarioBank, S7bMechanismAblation

REGISTRY = {cls.id: cls for cls in [
    S0Connectivity, S1InterfaceProbe, S2GCGEReplication, S3GCGECrossModel, S4PlanningBackbone,
    S5AdaptiveAttacker, S6RiskRouting, S7JointFactorial, S8JointController,
    S5v2InformedAttacker, S6v2ImpactRouting, A1AuditCalibration, S3bTextJudgedIntegrity, S4bScenarioBank,
    S5bRoleRotation, A2JudgeValidation, S7bMechanismAblation, A0AttackerInterface, H1IndependentLabels,
    A3FixedBank, S5dMemoryVariants, S5eMemoryReplay, A4H1Judges, S5fSpotlightReplay, A5RuleByRule, A6LlamaGuard,
    S3bConfirm, S5bConfirm, S7bConfirm, A7COutsideJudge, S5gQuarantineReplay,
    S7cNonResponse, S5hLiveQuarantine,
]}
