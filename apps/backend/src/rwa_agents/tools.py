from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal

from .schemas import (
    AgentFinding,
    QuantitativeValidationItem,
    RecommendedAction,
    RwaAnalysisRequest,
    ValidationFlag,
)


def analyze_data_quality(
    request: RwaAnalysisRequest,
) -> tuple[list[AgentFinding], list[ValidationFlag], list[RecommendedAction]]:
    findings: list[AgentFinding] = []
    flags: list[ValidationFlag] = []
    actions: list[RecommendedAction] = []
    input_ids = [record.asset_id for record in request.rwa_input_data]
    output_ids = {record.asset_id for record in request.rwa_output_results}

    duplicates = sorted(asset_id for asset_id, count in Counter(input_ids).items() if count > 1)
    if duplicates:
        flags.append(
            ValidationFlag(
                code="DUPLICATE_ASSET_ID",
                severity="critical",
                message=f"Duplicate asset identifiers detected: {', '.join(duplicates)}",
                source="DataAnalystAgent",
            )
        )
        actions.append(
            RecommendedAction(
                id="dq-deduplicate-assets",
                label="Resolve duplicate anonymized asset identifiers before sign-off",
                owner="Data Quality",
                priority="high",
                source_agent="DataAnalystAgent",
            )
        )

    missing_outputs = sorted(set(input_ids) - output_ids)
    if missing_outputs:
        flags.append(
            ValidationFlag(
                code="MISSING_OUTPUT",
                severity="critical",
                message=f"Missing calculated RWA output for {len(missing_outputs)} input records",
                source="DataAnalystAgent",
            )
        )

    missing_parameters = [
        record.asset_id
        for record in request.rwa_input_data
        if record.risk_weight is None and (record.pd is None or record.lgd is None)
    ]
    if missing_parameters:
        flags.append(
            ValidationFlag(
                code="MISSING_RISK_PARAMETER",
                severity="warning",
                message=f"{len(missing_parameters)} records need risk weight or PD/LGD parameters",
                source="DataAnalystAgent",
            )
        )
        actions.append(
            RecommendedAction(
                id="dq-complete-risk-parameters",
                label="Complete missing risk parameters for affected anonymized records",
                owner="Risk Data",
                priority="medium",
                source_agent="DataAnalystAgent",
            )
        )

    total_exposure = sum(record.exposure_amount for record in request.rwa_input_data)
    concentration_threshold = Decimal("0.25")
    concentrated = [
        record
        for record in request.rwa_input_data
        if total_exposure > 0 and record.exposure_amount / total_exposure >= concentration_threshold
    ]
    if concentrated:
        evidence = [
            f"{record.asset_id}: {(record.exposure_amount / total_exposure):.2%}"
            for record in concentrated[:5]
        ]
        findings.append(
            AgentFinding(
                agent="DataAnalystAgent",
                kind="data_quality",
                severity="warning",
                title="Exposure concentration requires review",
                detail=(
                    f"{len(concentrated)} anonymized exposures exceed "
                    f"{concentration_threshold:.0%} of submitted exposure."
                ),
                evidence=evidence,
            )
        )

    if not flags:
        findings.append(
            AgentFinding(
                agent="DataAnalystAgent",
                kind="data_quality",
                severity="info",
                title="Input completeness checks passed",
                detail=(
                    "No duplicate assets, missing outputs, or missing core risk "
                    "parameters were found."
                ),
                evidence=[f"{len(request.rwa_input_data)} input records checked"],
            )
        )
    return findings, flags, actions


def analyze_risk(
    request: RwaAnalysisRequest,
) -> tuple[
    list[AgentFinding],
    list[ValidationFlag],
    list[RecommendedAction],
    list[QuantitativeValidationItem],
]:
    findings: list[AgentFinding] = []
    flags: list[ValidationFlag] = []
    actions: list[RecommendedAction] = []
    validations: list[QuantitativeValidationItem] = []
    input_by_id = {record.asset_id: record for record in request.rwa_input_data}

    for output in request.rwa_output_results:
        input_record = input_by_id.get(output.asset_id)
        if input_record is None:
            continue
        risk_weight = (
            output.risk_weight if output.risk_weight is not None else input_record.risk_weight
        )
        exposure = output.exposure_amount or input_record.exposure_amount
        if risk_weight is None:
            continue
        expected = exposure * risk_weight
        variance = output.rwa_amount - expected
        variance_pct = Decimal("0") if expected == 0 else variance / expected
        passed = abs(variance_pct) <= request.materiality_threshold
        validations.append(
            QuantitativeValidationItem(
                asset_id=output.asset_id,
                expected_rwa_amount=expected,
                reported_rwa_amount=output.rwa_amount,
                variance_amount=variance,
                variance_pct=variance_pct,
                passed=passed,
            )
        )
        if not passed:
            flags.append(
                ValidationFlag(
                    code="RWA_RECALCULATION_VARIANCE",
                    severity="critical",
                    asset_id=output.asset_id,
                    message=(
                        f"Reported RWA differs from deterministic recalculation by "
                        f"{variance_pct:.2%}"
                    ),
                    source="RiskExpertAgent",
                )
            )

    sector_rwa: dict[str, Decimal] = defaultdict(Decimal)
    for output in request.rwa_output_results:
        input_record = input_by_id.get(output.asset_id)
        if input_record is not None:
            sector_rwa[input_record.sector] += output.rwa_amount
    total_rwa = sum(sector_rwa.values(), Decimal("0"))
    if sector_rwa and total_rwa > 0:
        top_sector, top_amount = max(sector_rwa.items(), key=lambda item: item[1])
        findings.append(
            AgentFinding(
                agent="RiskExpertAgent",
                kind="risk",
                severity="info" if top_amount / total_rwa < Decimal("0.4") else "warning",
                title="Largest RWA driver identified",
                detail=f"{top_sector} contributes {(top_amount / total_rwa):.2%} of submitted RWA.",
                evidence=[f"Total submitted RWA: {total_rwa:.2f}"],
            )
        )

    failed_validations = [item for item in validations if not item.passed]
    if failed_validations:
        actions.append(
            RecommendedAction(
                id="risk-review-rwa-variance",
                label="Review deterministic RWA validation variances before publication",
                owner="RWA Analytics",
                priority="high",
                source_agent="RiskExpertAgent",
            )
        )
    elif validations:
        findings.append(
            AgentFinding(
                agent="RiskExpertAgent",
                kind="validation",
                severity="info",
                title="Deterministic RWA validation passed",
                detail=f"{len(validations)} reported RWA outputs reconciled inside materiality.",
                evidence=[f"Materiality threshold: {request.materiality_threshold:.2%}"],
            )
        )
    return findings, flags, actions, validations
