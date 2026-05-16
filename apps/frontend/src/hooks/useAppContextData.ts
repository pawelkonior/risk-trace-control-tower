import { fetchAppContext } from "../api/rwaApi";
import type { AppContext } from "../api/types";
import { useApiResource } from "./useApiResource";

export function useAppContextData() {
  return useApiResource<AppContext>((signal) => fetchAppContext(signal), []);
}
