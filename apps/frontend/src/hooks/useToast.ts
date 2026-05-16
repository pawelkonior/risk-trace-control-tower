import { useCallback, useEffect, useState } from "react";

export function useToast(durationMs = 4800) {
  const [toast, setToast] = useState<string | null>(null);

  const notify = useCallback((message: string) => {
    setToast(message);
  }, []);

  useEffect(() => {
    if (!toast) {
      return;
    }

    const timer = window.setTimeout(() => setToast(null), durationMs);
    return () => window.clearTimeout(timer);
  }, [durationMs, toast]);

  return { notify, toast };
}
