from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import RisktraceUiAction, RisktraceUiActionEvent, RisktraceUiDataset


class RisktraceDatasetNotFoundError(LookupError):
    """Raised when a frontend dataset has not been seeded into the database."""


class RisktraceActionNotFoundError(LookupError):
    """Raised when a frontend action is missing from the database registry."""


class RisktraceUiRepository:
    """Persistence gateway for frontend-facing RiskTrace data."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_dataset(self, dataset_key: str) -> RisktraceUiDataset:
        dataset = self.session.scalar(
            select(RisktraceUiDataset).where(RisktraceUiDataset.dataset_key == dataset_key)
        )
        if dataset is None:
            raise RisktraceDatasetNotFoundError(dataset_key)
        return dataset

    def get_payload(self, dataset_key: str) -> dict[str, Any]:
        return dict(self.get_dataset(dataset_key).payload)

    def upsert_dataset(
        self,
        dataset_key: str,
        payload: dict[str, Any],
        *,
        as_of_date: date | None = None,
    ) -> RisktraceUiDataset:
        dataset = self.session.scalar(
            select(RisktraceUiDataset).where(RisktraceUiDataset.dataset_key == dataset_key)
        )
        now = datetime.now(UTC)
        if dataset is None:
            dataset = RisktraceUiDataset(
                dataset_key=dataset_key,
                as_of_date=as_of_date,
                generated_at=now,
                payload=payload,
            )
            self.session.add(dataset)
        else:
            dataset.as_of_date = as_of_date
            dataset.generated_at = now
            dataset.payload = payload
        return dataset

    def get_action(self, action_id: str) -> RisktraceUiAction:
        action = self.session.scalar(
            select(RisktraceUiAction).where(RisktraceUiAction.action_id == action_id)
        )
        if action is None:
            raise RisktraceActionNotFoundError(action_id)
        return action

    def upsert_action(
        self,
        *,
        action_id: str,
        label: str,
        category: str,
        response_message: str,
        job_type: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> RisktraceUiAction:
        action = self.session.scalar(
            select(RisktraceUiAction).where(RisktraceUiAction.action_id == action_id)
        )
        if action is None:
            action = RisktraceUiAction(
                action_id=action_id,
                label=label,
                category=category,
                response_message=response_message,
                job_type=job_type,
                payload=payload or {},
            )
            self.session.add(action)
        else:
            action.label = label
            action.category = category
            action.response_message = response_message
            action.job_type = job_type
            action.payload = payload or {}
        return action

    def create_action_event(
        self,
        *,
        action_id: str,
        status: str,
        request_payload: dict[str, Any],
        response_payload: dict[str, Any],
    ) -> RisktraceUiActionEvent:
        event = RisktraceUiActionEvent(
            action_id=action_id,
            status=status,
            request_payload=request_payload,
            response_payload=response_payload,
        )
        self.session.add(event)
        return event

    def commit(self) -> None:
        self.session.commit()
