import { useEffect, useState } from "react";

export type ApiResourceState<T> = {
  data: T | null;
  isLoading: boolean;
  error: string | null;
};

export function useApiResource<T>(
  load: (signal: AbortSignal) => Promise<T>,
  deps: unknown[] = [],
  options: { enabled?: boolean } = {},
) {
  const enabled = options.enabled ?? true;
  const [state, setState] = useState<ApiResourceState<T>>({
    data: null,
    error: null,
    isLoading: enabled,
  });

  useEffect(() => {
    if (!enabled) {
      setState((current) => ({ ...current, isLoading: false }));
      return;
    }

    const controller = new AbortController();

    setState((current) => ({ ...current, error: null, isLoading: true }));

    load(controller.signal)
      .then((data) => {
        setState({ data, error: null, isLoading: false });
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) {
          return;
        }

        setState({
          data: null,
          error: error instanceof Error ? error.message : "REST API unavailable",
          isLoading: false,
        });
      });

    return () => controller.abort();
  }, [enabled, ...deps]);

  return state;
}
