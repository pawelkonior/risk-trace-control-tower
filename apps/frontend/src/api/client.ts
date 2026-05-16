const DEFAULT_API_BASE_URL = "/api";

export async function requestJson<T>(
  path: string,
  options: RequestInit & { signal?: AbortSignal } = {},
): Promise<T> {
  const response = await fetch(`${apiBaseUrl()}${path}`, {
    ...options,
    headers: {
      Accept: "application/json",
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export function apiBaseUrl() {
  return (import.meta.env.VITE_RWA_API_BASE_URL ?? DEFAULT_API_BASE_URL).replace(/\/$/, "");
}

async function readErrorMessage(response: Response) {
  try {
    const payload = (await response.json()) as { message?: string; detail?: string };
    return payload.message ?? payload.detail ?? `REST API returned HTTP ${response.status}`;
  } catch {
    return `REST API returned HTTP ${response.status}`;
  }
}
