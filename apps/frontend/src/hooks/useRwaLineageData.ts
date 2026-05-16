import { fetchLineageTrace } from "../api/rwaApi";
import type {
  ApiLineageDirection,
  ApiLineageTotals,
  ApiLineageTrace,
  ApiTransformationStep,
  LineageNodeTone,
  LineageTraceSnapshot,
} from "../api/types";
import { hydrateIcon, type HydratedIcon } from "./iconHydration";
import { useApiResource } from "./useApiResource";

export type LineageNode = {
  id: string;
  layer: string;
  title: string;
  icon: HydratedIcon;
  tone: LineageNodeTone;
  details: Array<[string, string]>;
  status: "Success" | "Warning" | "Failed";
};

export type LineageArtifact = {
  label: string;
  count: number;
  icon: HydratedIcon;
};

export type LineageDirection = Omit<ApiLineageDirection, "icon"> & {
  icon: HydratedIcon;
};

export type RwaLineageData = {
  trace: ApiLineageTrace;
  nodes: LineageNode[];
  summary: Array<[string, string]>;
  transformationSteps: ApiTransformationStep[];
  artifacts: LineageArtifact[];
  totals: ApiLineageTotals;
  directions: LineageDirection[];
};

export function useRwaLineageData(traceId: string) {
  return useApiResource<RwaLineageData>(
    (signal) => fetchLineageTrace(traceId, signal).then(hydrateLineageSnapshot),
    [traceId],
  );
}

function hydrateLineageSnapshot(snapshot: LineageTraceSnapshot): RwaLineageData {
  return {
    trace: snapshot.trace,
    nodes: snapshot.nodes.map((node) => ({ ...node, icon: hydrateIcon(node.icon) })),
    summary: snapshot.summary,
    transformationSteps: snapshot.transformationSteps,
    artifacts: snapshot.artifacts.map((artifact) => ({
      ...artifact,
      icon: hydrateIcon(artifact.icon),
    })),
    totals: snapshot.totals,
    directions: snapshot.directions.map((direction) => ({
      ...direction,
      icon: hydrateIcon(direction.icon),
    })),
  };
}
