import { fetchBriefingSnapshot } from "../api/rwaApi";
import type {
  ApiBoardPack,
  ApiControlChecklistItem,
  ApiDataQualityFinding,
  ApiManualReviewInput,
  ApiMovementDriver,
  ApiRegulatoryWatchItem,
  ApiReviewPackStat,
  ApiSimulatorAction,
  ApiVarianceReviewItem,
  ApiWaterfallItem,
  BriefingSnapshot,
  BriefingTone,
} from "../api/types";
import { hydrateIcon, type HydratedIcon } from "./iconHydration";
import { useApiResource } from "./useApiResource";

export type BriefingKpi = {
  label: string;
  value: string;
  detail: string;
  icon: HydratedIcon;
  tone: BriefingTone;
};

export type EvidenceItem = {
  label: string;
  value: string;
  icon: HydratedIcon;
  tone: BriefingTone;
  actionId: string;
};

export type BoardPack = Omit<ApiBoardPack, "icon"> & {
  icon: HydratedIcon;
};

export type ManagementReviewPack = {
  tabs: string[];
  stats: ApiReviewPackStat[];
  varianceReviewItems: ApiVarianceReviewItem[];
  controlChecklist: ApiControlChecklistItem[];
  manualReviewInputs: ApiManualReviewInput[];
};

export type RwaBriefingData = {
  generatedAt: string;
  kpis: BriefingKpi[];
  movementAttribution: {
    waterfallData: ApiWaterfallItem[];
    movementDrivers: ApiMovementDriver[];
    totalChange: string;
    totalChangePct: string;
  };
  reviewPack: ManagementReviewPack;
  regulatoryWatch: ApiRegulatoryWatchItem[];
  dataQualityFindings: ApiDataQualityFinding[];
  simulatorActions: ApiSimulatorAction[];
  evidenceItems: EvidenceItem[];
  boardPack: BoardPack;
};

export function useRwaBriefingData() {
  return useApiResource<RwaBriefingData>(
    (signal) => fetchBriefingSnapshot(signal).then(hydrateBriefingSnapshot),
    [],
  );
}

function hydrateBriefingSnapshot(snapshot: BriefingSnapshot): RwaBriefingData {
  return {
    generatedAt: snapshot.generatedAt,
    kpis: snapshot.kpis.map((kpi) => ({ ...kpi, icon: hydrateIcon(kpi.icon) })),
    movementAttribution: snapshot.movementAttribution,
    reviewPack: snapshot.reviewPack,
    regulatoryWatch: snapshot.regulatoryWatch,
    dataQualityFindings: snapshot.dataQualityFindings,
    simulatorActions: snapshot.simulatorActions,
    evidenceItems: snapshot.evidenceItems.map((item) => ({
      ...item,
      icon: hydrateIcon(item.icon),
    })),
    boardPack: {
      ...snapshot.boardPack,
      icon: hydrateIcon(snapshot.boardPack.icon),
    },
  };
}
