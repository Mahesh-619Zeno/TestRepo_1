import { useState } from 'react';
import { ChevronDown, AlertCircle, Sparkles, ChevronRight } from 'lucide-react';
import { ConfidenceScore } from '@/app/components/atoms/ConfidenceScore';
import { StatusPill } from './statusPill';
import CognitiveDecisioning from './CognitiveDecisioningReassess';
import { IReAssessResultReason } from '@/app/types/pull-request.types';

type ResultCardProps = {
  title: string;
  description: string;
  statusLabel: string;
  confidence_score: number;
  severity?: string;
  defaultOpen?: boolean;
  reasons?: IReAssessResultReason[];
  gap?: string;
};

export const SEVERITY_MAP: Record<string, string> = {
  critical: 'Critical',
  warning: 'Warning',
  information: 'Jas',
  jas: 'Jas',
};

export function ReassessmentResultCard({
  title,
  description,
  statusLabel,
  confidence_score,
  severity,
  defaultOpen = true,
  reasons,
  gap,
}: ResultCardProps) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="px-2 py-1 text-sm border rounded-lg text-primary border-button-background bg-primary/10 flex flex-row items-center"
      >
        Re-Assessment Result{' '}
        <ChevronDown
          className={`h-5 transition-transform duration-300 ${open ? 'rotate-180' : ''}`}
        />
      </button>
      {open && (
        <div
          className="
        w-full rounded-xl border p-4 transition-colors
        border-[var(--vscode-focusBorder)] bg-primary/10
      "
        >
          <div className="flex items-center justify-between">
            <div
              className="
            inline-flex items-center gap-2 rounded-lg px-3 py-1 text-sm
            border border-[var(--vscode-notificationsErrorIcon-foreground)]
            text-[var(--vscode-notificationsErrorIcon-foreground)]
            bg-[var(--vscode-notificationsErrorIcon-foreground)]/10
          "
            >
              <AlertCircle className="h-4 w-4" />
              {statusLabel}
            </div>

            <div className="flex items-center gap-2">
              {severity && (
                <StatusPill
                  toolTipContent="Violation Severity"
                  status={SEVERITY_MAP[severity.toLowerCase()]}
                />
              )}
              <ConfidenceScore score={confidence_score} />
            </div>
          </div>

          <div className="grid transition-all duration-300 ease-in-out grid-rows-[1fr] opacity-100 mt-4 mb-2">
            <div className="overflow-hidden">
              <h3 className="mb-2 font-semibold text-[12px]">{title}</h3>

              <p
                className="
              text-[12px] leading-relaxed
              text-[var(--vscode-descriptionForeground)]
            "
              >
                {description}
              </p>
            </div>
          </div>

          {reasons && reasons.length !== 0 && (
            <CognitiveDecisioning gap={gap ?? 'No gap identified'} reasons={reasons} />
          )}
        </div>
      )}
    </div>
  );
}
