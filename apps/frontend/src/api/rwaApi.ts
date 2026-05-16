import { requestJson } from "./client";
import type {
  AppContext,
  BriefingSnapshot,
  DashboardFilters,
  ExportResult,
  LineageTraceSnapshot,
  NotificationItem,
  RwaDashboardSnapshot,
  SearchResponse,
  UiActionPayload,
  UiActionResult,
} from "./types";

export function fetchAppContext(signal?: AbortSignal) {
  return requestJson<AppContext>("/v1/app/context", { signal });
}

export function fetchRwaDashboardSnapshot(
  filters?: DashboardFilters,
  signal?: AbortSignal,
) {
  const params = new URLSearchParams();
  if (filters) {
    params.set("period", filters.period);
    params.set("scenario", filters.scenario);
    params.set("businessUnit", filters.businessUnit);
    params.set("currency", filters.currency);
  }
  const query = params.toString();
  return requestJson<RwaDashboardSnapshot>(`/v1/dashboard/snapshot${query ? `?${query}` : ""}`, {
    signal,
  });
}

export function fetchLineageTrace(traceId: string, signal?: AbortSignal) {
  return requestJson<LineageTraceSnapshot>(`/v1/lineage/traces/${encodeURIComponent(traceId)}`, {
    signal,
  });
}

export function fetchBriefingSnapshot(signal?: AbortSignal) {
  return requestJson<BriefingSnapshot>("/v1/briefing/snapshot", { signal });
}

export function fetchNotifications(signal?: AbortSignal) {
  return requestJson<NotificationItem[]>("/v1/notifications", { signal });
}

export function postUiAction(actionId: string, payload: UiActionPayload = {}, signal?: AbortSignal) {
  return requestJson<UiActionResult>(`/v1/ui/actions/${encodeURIComponent(actionId)}`, {
    body: JSON.stringify({ context: payload }),
    method: "POST",
    signal,
  });
}

export function postExport(exportType: string, payload: UiActionPayload = {}, signal?: AbortSignal) {
  return requestJson<ExportResult>(`/v1/exports/${encodeURIComponent(exportType)}`, {
    body: JSON.stringify({ context: payload }),
    method: "POST",
    signal,
  });
}

export function searchRwa(query: string, signal?: AbortSignal) {
  const params = new URLSearchParams({ q: query });
  return requestJson<SearchResponse>(`/v1/search?${params.toString()}`, { signal });
}
