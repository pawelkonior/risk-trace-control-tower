from __future__ import annotations

import asyncio
import logging
from collections import Counter, defaultdict
from collections.abc import Callable
from decimal import Decimal
from typing import Any, Literal

from .schemas import (
    AgentFinding,
    QuantitativeValidationItem,
    ReactStep,
    RecommendedAction,
    RwaAnalysisRequest,
    ValidationFlag,
    WorkerAnalysisResult,
)

logger = logging.getLogger(__name__)

AgentName = Literal["DataAnalystAgent", "RiskExpertAgent"]


def analyze_data_quality(request: RwaAnalysisRequest) -> WorkerAnalysisResult:
    """Run DataAnalystAgent's internal ReAct-style deterministic tool sequence."""
    agent: AgentName = "DataAnalystAgent"
    react_steps = _react_steps(
        agent=agent,
        tool_name="DataTools",
        selected_actions=[
            "duplicate_asset_id_detection",
            "missing_output_detection",
            "missing_risk_parameter_detection",
            "non_positive_exposure_check",
            "missing_rating_detection",
            "pd_lgd_range_check",
            "exposure_concentration_analysis",
        ],
        observation=f"{len(request.rwa_input_data)} inputs and "
        f"{len(request.rwa_output_results)} outputs inspected.",
    )
    findings: list[AgentFinding] = []
    flags: list[ValidationFlag] = []
    actions: list[RecommendedAction] = []
    input_ids = [record.asset_id for record in request.rwa_input_data]
    output_ids = {record.asset_id for record in request.rwa_output_results}

    duplicates = sorted(asset_id for asset_id, count in Counter(input_ids).items() if count > 1)
    if duplicates:
        flags.append(
            _flag(
                code="DUPLICATE_ASSET_ID",
                severity="critical",
                message=f"Duplicate asset identifiers detected: {', '.join(duplicates)}",
                source_agent=agent,
            )
        )
        actions.append(
            RecommendedAction(
                id="dq-deduplicate-assets",
                label="Resolve duplicate anonymized asset identifiers before sign-off",
                owner="Data Quality",
                priority="high",
                source_agent=agent,
            )
        )

    missing_outputs = sorted(set(input_ids) - output_ids)
    if missing_outputs:
        flags.append(
            _flag(
                code="MISSING_OUTPUT",
                severity="critical",
                message=f"Missing calculated RWA output for {len(missing_outputs)} input records",
                source_agent=agent,
            )
        )
        actions.append(
            RecommendedAction(
                id="dq-complete-calculator-output",
                label="Re-run calculator for anonymized inputs without RWA output",
                owner="RWA Operations",
                priority="high",
                source_agent=agent,
            )
        )

    missing_parameters = [
        record.asset_id
        for record in request.rwa_input_data
        if record.risk_weight is None and (record.pd is None or record.lgd is None)
    ]
    if missing_parameters:
        flags.append(
            _flag(
                code="MISSING_RISK_PARAMETER",
                severity="warning",
                message=f"{len(missing_parameters)} records need risk weight or PD/LGD parameters",
                source_agent=agent,
            )
        )
        actions.append(
            RecommendedAction(
                id="dq-complete-risk-parameters",
                label="Complete missing risk parameters for affected anonymized records",
                owner="Risk Data",
                priority="medium",
                source_agent=agent,
            )
        )

    non_positive_exposures = [
        record.asset_id for record in request.rwa_input_data if record.exposure_amount <= 0
    ]
    if non_positive_exposures:
        flags.append(
            _flag(
                code="NON_POSITIVE_EXPOSURE",
                severity="critical",
                message=f"{len(non_positive_exposures)} records have non-positive exposure",
                source_agent=agent,
            )
        )

    missing_ratings = [record.asset_id for record in request.rwa_input_data if not record.rating]
    if missing_ratings:
        flags.append(
            _flag(
                code="MISSING_RATING",
                severity="warning",
                message=f"{len(missing_ratings)} records are missing external or internal rating",
                source_agent=agent,
            )
        )

    invalid_pd_lgd = [
        record.asset_id
        for record in request.rwa_input_data
        if (record.pd is not None and not Decimal("0") <= record.pd <= Decimal("1"))
        or (record.lgd is not None and not Decimal("0") <= record.lgd <= Decimal("1"))
    ]
    if invalid_pd_lgd:
        flags.append(
            _flag(
                code="INVALID_PD_LGD",
                severity="critical",
                message=f"{len(invalid_pd_lgd)} records have PD or LGD outside [0, 1]",
                source_agent=agent,
            )
        )

    positive_exposure_total = sum(
        record.exposure_amount for record in request.rwa_input_data if record.exposure_amount > 0
    )
    concentration_threshold = Decimal("0.25")
    concentrated = [
        record
        for record in request.rwa_input_data
        if positive_exposure_total > 0
        and record.exposure_amount > 0
        and record.exposure_amount / positive_exposure_total >= concentration_threshold
    ]
    if concentrated:
        evidence = [
            f"{record.asset_id}: {(record.exposure_amount / positive_exposure_total):.2%}"
            for record in concentrated[:5]
        ]
        findings.append(
            AgentFinding(
                agent=agent,
                kind="data_quality",
                severity="warning",
                title="Exposure concentration requires review",
                detail=(
                    f"{len(concentrated)} anonymized exposures exceed "
                    f"{concentration_threshold:.0%} of submitted positive exposure."
                ),
                evidence=evidence,
                react_steps=react_steps,
            )
        )

    if not flags:
        findings.append(
            AgentFinding(
                agent=agent,
                kind="data_quality",
                severity="info",
                title="Input completeness checks passed",
                detail=(
                    "No duplicate assets, missing outputs, missing ratings, invalid "
                    "exposures, or missing core risk parameters were found."
                ),
                evidence=[f"{len(request.rwa_input_data)} input records checked"],
                react_steps=react_steps,
            )
        )

    return WorkerAnalysisResult(
        agent=agent,
        findings=findings,
        validation_flags=flags,
        recommended_actions=actions,
        react_steps=react_steps,
    )


def analyze_risk(request: RwaAnalysisRequest) -> WorkerAnalysisResult:
    """Run RiskExpertAgent's internal ReAct-style deterministic tool sequence."""
    agent: AgentName = "RiskExpertAgent"
    react_steps = _react_steps(
        agent=agent,
        tool_name="RiskTools",
        selected_actions=[
            "deterministic_rwa_validation",
            "sector_rwa_driver_analysis",
            "rwa_density_capital_buffer_screen",
        ],
        observation=f"{len(request.rwa_output_results)} output records inspected.",
    )
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
        if risk_weight is None or exposure <= 0:
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
                _flag(
                    code="RWA_RECALCULATION_VARIANCE",
                    severity="critical",
                    asset_id=output.asset_id,
                    message=(
                        f"Reported RWA differs from deterministic recalculation by "
                        f"{variance_pct:.2%}"
                    ),
                    source_agent=agent,
                )
            )

    sector_rwa: dict[str, Decimal] = defaultdict(Decimal)
    asset_class_rwa: dict[str, Decimal] = defaultdict(Decimal)
    total_positive_exposure = Decimal("0")
    for output in request.rwa_output_results:
        input_record = input_by_id.get(output.asset_id)
        if input_record is not None:
            sector_rwa[input_record.sector] += output.rwa_amount
            asset_class_rwa[input_record.asset_class] += output.rwa_amount
            if input_record.exposure_amount > 0:
                total_positive_exposure += input_record.exposure_amount
    total_rwa = sum(sector_rwa.values(), Decimal("0"))
    if sector_rwa and total_rwa > 0:
        top_sector, top_amount = max(sector_rwa.items(), key=lambda item: item[1])
        top_asset_class, top_asset_amount = max(asset_class_rwa.items(), key=lambda item: item[1])
        findings.append(
            AgentFinding(
                agent=agent,
                kind="risk",
                severity="info" if top_amount / total_rwa < Decimal("0.4") else "warning",
                title="Largest RWA driver identified",
                detail=f"{top_sector} contributes {(top_amount / total_rwa):.2%} of submitted RWA.",
                evidence=[
                    f"Total submitted RWA: {total_rwa:.2f}",
                    f"Top asset class: {top_asset_class} ({(top_asset_amount / total_rwa):.2%})",
                ],
                react_steps=react_steps,
            )
        )

    if total_rwa > 0 and total_positive_exposure > 0:
        rwa_density = total_rwa / total_positive_exposure
        if rwa_density >= Decimal("0.75"):
            findings.append(
                AgentFinding(
                    agent=agent,
                    kind="risk",
                    severity="warning",
                    title="High RWA density may pressure capital buffer",
                    detail=f"Portfolio RWA density is {rwa_density:.2%}.",
                    evidence=["RWA density calculated as total RWA / positive exposure"],
                    react_steps=react_steps,
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
                source_agent=agent,
            )
        )
    elif validations:
        findings.append(
            AgentFinding(
                agent=agent,
                kind="validation",
                severity="info",
                title="Deterministic RWA validation passed",
                detail=f"{len(validations)} reported RWA outputs reconciled inside materiality.",
                evidence=[f"Materiality threshold: {request.materiality_threshold:.2%}"],
                react_steps=react_steps,
            )
        )

    return WorkerAnalysisResult(
        agent=agent,
        findings=findings,
        validation_flags=flags,
        recommended_actions=actions,
        quantitative_validation=validations,
        react_steps=react_steps,
    )


def _flag(
    *,
    code: str,
    severity: Literal["info", "warning", "critical"],
    message: str,
    source_agent: AgentName,
    asset_id: str | None = None,
) -> ValidationFlag:
    return ValidationFlag(
        code=code,
        severity=severity,
        message=message,
        asset_id=asset_id,
        source_agent=source_agent,
        requires_human_intervention=severity == "critical",
    )


def _react_steps(
    *,
    agent: AgentName,
    tool_name: str,
    selected_actions: list[str],
    observation: str,
) -> list[ReactStep]:
    return [
        ReactStep(
            phase="inspect_state",
            action=f"{agent} inspected anonymized AgentState",
            observation="Only anonymized risk and financial fields were used.",
        ),
        ReactStep(
            phase="select_tool",
            tool_name=tool_name,
            action="Selected deterministic analysis actions",
            observation=", ".join(selected_actions),
        ),
        ReactStep(
            phase="execute_tool",
            tool_name=tool_name,
            action="Executed deterministic Python checks",
            observation="No LLM formula calculation was used.",
        ),
        ReactStep(
            phase="observe_result",
            tool_name=tool_name,
            action="Recorded tool observations",
            observation=observation,
        ),
        ReactStep(
            phase="emit_finding",
            action="Emitted structured findings, flags, actions, and evidence",
            observation="Worker output is structured for supervisor fan-in.",
        ),
    ]



class ToolExecutor:
    """
    Base class for tool executors with parallel execution support.
    
    Tools can declare whether they can run in parallel with other tools.
    """

    def __init__(self, name: str, can_run_parallel: bool = False) -> None:
        """
        Initialize tool executor.

        Args:
            name: Tool name
            can_run_parallel: Whether this tool can run in parallel with others
        """
        self.name = name
        self.can_run_parallel = can_run_parallel

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the tool.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Tool execution result
        """
        raise NotImplementedError("Subclasses must implement execute()")


class DataAnalystTool(ToolExecutor):
    """Data analyst tool executor."""

    def __init__(self) -> None:
        super().__init__(name="DataAnalystAgent", can_run_parallel=True)

    def execute(self, request: RwaAnalysisRequest) -> WorkerAnalysisResult:
        """Execute data quality analysis."""
        return analyze_data_quality(request)


class RiskExpertTool(ToolExecutor):
    """Risk expert tool executor."""

    def __init__(self) -> None:
        super().__init__(name="RiskExpertAgent", can_run_parallel=True)

    def execute(self, request: RwaAnalysisRequest) -> WorkerAnalysisResult:
        """Execute risk analysis."""
        return analyze_risk(request)


async def execute_tools_parallel(
    tools: list[tuple[ToolExecutor, tuple[Any, ...], dict[str, Any]]],
) -> list[Any]:
    """
    Execute multiple tools in parallel if they support it.

    Args:
        tools: List of (tool, args, kwargs) tuples

    Returns:
        List of results in same order as input tools
    """
    if not tools:
        return []

    # Separate parallel and sequential tools
    parallel_tools: list[tuple[int, ToolExecutor, tuple[Any, ...], dict[str, Any]]] = []
    sequential_tools: list[tuple[int, ToolExecutor, tuple[Any, ...], dict[str, Any]]] = []

    for idx, (tool, args, kwargs) in enumerate(tools):
        if tool.can_run_parallel:
            parallel_tools.append((idx, tool, args, kwargs))
        else:
            sequential_tools.append((idx, tool, args, kwargs))

    results: dict[int, Any] = {}

    # Execute parallel tools concurrently
    if parallel_tools:
        logger.info("Executing %d tools in parallel", len(parallel_tools))

        async def run_tool(
            idx: int, tool: ToolExecutor, args: tuple[Any, ...], kwargs: dict[str, Any]
        ) -> tuple[int, Any]:
            """Run a single tool and return its index and result."""
            try:
                # Run in thread pool since tools are synchronous
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: tool.execute(*args, **kwargs))
                logger.debug("Tool %s completed successfully", tool.name)
                return idx, result
            except Exception as exc:
                logger.error("Tool %s failed: %s", tool.name, exc)
                return idx, exc

        # Execute all parallel tools concurrently
        parallel_results = await asyncio.gather(
            *[run_tool(idx, tool, args, kwargs) for idx, tool, args, kwargs in parallel_tools],
            return_exceptions=False,  # We handle exceptions in run_tool
        )

        # Store results by index
        for idx, result in parallel_results:
            results[idx] = result

    # Execute sequential tools one by one
    for idx, tool, args, kwargs in sequential_tools:
        logger.info("Executing tool %s sequentially", tool.name)
        try:
            result = tool.execute(*args, **kwargs)
            results[idx] = result
            logger.debug("Tool %s completed successfully", tool.name)
        except Exception as exc:
            logger.error("Tool %s failed: %s", tool.name, exc)
            results[idx] = exc

    # Return results in original order
    return [results[i] for i in range(len(tools))]


def execute_tools_parallel_sync(
    tools: list[tuple[ToolExecutor, tuple[Any, ...], dict[str, Any]]],
) -> list[Any]:
    """
    Synchronous wrapper for execute_tools_parallel.

    Args:
        tools: List of (tool, args, kwargs) tuples

    Returns:
        List of results in same order as input tools
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(execute_tools_parallel(tools))
            finally:
                loop.close()
        else:
            return loop.run_until_complete(execute_tools_parallel(tools))
    except RuntimeError:
        # No event loop, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(execute_tools_parallel(tools))
        finally:
            loop.close()


# Made with Bob
