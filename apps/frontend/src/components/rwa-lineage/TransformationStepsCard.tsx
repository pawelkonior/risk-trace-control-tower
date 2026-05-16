import { Check } from "lucide-react";

import type { ApiLineageTotals, ApiTransformationStep } from "../../api/types";
import { Card } from "../rwa-dashboard/Card";
import { StatusBadge } from "../rwa-dashboard/StatusBadge";

export function TransformationStepsCard({
  steps,
  totals,
}: {
  steps: ApiTransformationStep[];
  totals: ApiLineageTotals;
}) {
  return (
    <Card className="transformation-card lineage-section-card">
      <h3>Transformation Steps</h3>
      <div className="lineage-table-wrap">
        <table className="transformation-table">
          <thead>
            <tr>
              <th>Step</th>
              <th>Service</th>
              <th>Description</th>
              <th>Input Records</th>
              <th>Output Records</th>
              <th>Duration</th>
              <th>Status</th>
              <th>Executed At</th>
            </tr>
          </thead>
          <tbody>
            {steps.map((step) => (
              <tr key={step.step}>
                <td>{step.step}</td>
                <td>{step.service}</td>
                <td>{step.description}</td>
                <td>{step.inputRecords}</td>
                <td>{step.outputRecords}</td>
                <td>{step.duration}</td>
                <td>
                  <StatusBadge>
                    <Check size={11} />
                    {step.status}
                  </StatusBadge>
                </td>
                <td>{step.executedAt}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="transformation-footer">
        <span>
          Total Duration: <strong>{totals.duration}</strong>
        </span>
        <span>
          Total Input Records: <strong>{totals.totalInputRecords}</strong>
        </span>
        <span>
          Total Output Records: <strong>{totals.totalOutputRecords}</strong>
        </span>
      </div>
    </Card>
  );
}
