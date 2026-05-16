import { fetchNotifications } from "../api/rwaApi";
import type { NotificationItem } from "../api/types";
import { useApiResource } from "./useApiResource";

export function useNotificationsData(enabled: boolean) {
  return useApiResource<NotificationItem[]>(
    (signal) => fetchNotifications(signal),
    [enabled],
    { enabled },
  );
}
