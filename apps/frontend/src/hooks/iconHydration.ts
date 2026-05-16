import type { ComponentType } from "react";
import {
  AlertCircle,
  BarChart3,
  Bell,
  BookOpenCheck,
  Calculator,
  CheckCircle2,
  ClipboardCheck,
  ClipboardList,
  CloudUpload,
  Database,
  FileArchive,
  FileClock,
  FileText,
  FolderDown,
  GitBranch,
  Layers3,
  LineChart,
  Network,
  Scale,
  ShieldCheck,
  Target,
  WalletCards,
} from "lucide-react";

import type { IconName } from "../api/types";

export type HydratedIcon = ComponentType<{ size?: number; strokeWidth?: number; className?: string }>;

const icons: Record<IconName, HydratedIcon> = {
  AlertCircle,
  BarChart3,
  Bell,
  BookOpenCheck,
  Calculator,
  CheckCircle2,
  ClipboardCheck,
  ClipboardList,
  CloudUpload,
  Database,
  FileArchive,
  FileClock,
  FileText,
  FolderDown,
  GitBranch,
  Layers3,
  LineChart,
  ListChecks: ClipboardList,
  Network,
  Scale,
  ShieldCheck,
  Target,
  WalletCards,
};

export function hydrateIcon(icon: IconName): HydratedIcon {
  return icons[icon] ?? AlertCircle;
}
