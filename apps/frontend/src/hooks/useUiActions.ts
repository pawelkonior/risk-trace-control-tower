import { useCallback, useState } from "react";

import { postExport, postUiAction } from "../api/rwaApi";
import type { UiActionPayload } from "../api/types";

export type UiActionRunner = (actionId: string, payload?: UiActionPayload) => Promise<void>;
export type ExportRunner = (exportType: string, payload?: UiActionPayload) => Promise<void>;

export function useUiActions(notify: (message: string) => void) {
  const [isPending, setIsPending] = useState(false);

  const runAction = useCallback<UiActionRunner>(
    async (actionId, payload = {}) => {
      setIsPending(true);
      try {
        const result = await postUiAction(actionId, payload);
        notify(result.message);
      } catch (error) {
        notify(error instanceof Error ? error.message : "Action API unavailable");
      } finally {
        setIsPending(false);
      }
    },
    [notify],
  );

  const runExport = useCallback<ExportRunner>(
    async (exportType, payload = {}) => {
      setIsPending(true);
      try {
        const result = await postExport(exportType, payload);
        notify(result.message);
      } catch (error) {
        notify(error instanceof Error ? error.message : "Export API unavailable");
      } finally {
        setIsPending(false);
      }
    },
    [notify],
  );

  return { isPending, runAction, runExport };
}
