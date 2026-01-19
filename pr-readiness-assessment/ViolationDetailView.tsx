import CustomTooltip from '@/app/components/atoms/CustomTooltip';
import { ConfidenceScore } from '@/app/components/atoms/ConfidenceScore';
import {
  ButtonIcon,
  ReusableButton,
  ReusableButtonVariant,
} from '@/app/components/molecules/ReusableButton';
import useWebMessage from '@/app/lib/use-web-message';
import { IReAssessResult, TOnReAssessViolation } from '@/app/types/pull-request.types';
import { StatusPill } from './statusPill';
import AskmodMarkdown from '../../ecg-view/components/pr-genie/PrGenieMarkdownOld';
import CognitiveDecisioning from './CognitiveDecisioning';
import ViolationDiffViewer from './violationDiffViewer';
import { IAdaptedFinding } from '../../../types/pull-request-report.types';
import { ReassessmentResultCard } from './ReassessmentResultCard';
import { ChevronRight, CircleCheck, CircleX, CodeXml, Copy, CheckCheck } from 'lucide-react';
import { useState } from 'react';

export const SEVERITY_MAP: Record<string, string> = {
  critical: 'Critical',
  warning: 'Warning',
  information: 'Jas',
};

interface IViolationDetailViewProps {
  finding: IAdaptedFinding;
  baseBranch: string;
  headBranch: string;
  headCommitSha: string;
  isLoading: boolean;
  violationSection: 'devops' | 'CS' | 'TQA';
  onReAssessStart: (id: string) => void;
  onReAssessEnd: (id: string) => void;
  onResolved: (id: string) => void;
  onReAssessResult: (id: string, result: IReAssessResult) => void;
  onReAssessViolation: TOnReAssessViolation;
}

const ViolationDetailView = ({
  finding,
  baseBranch,
  headBranch,
  headCommitSha,
  isLoading,
  violationSection,
  onReAssessStart,
  onReAssessEnd,
  onResolved,
  onReAssessResult,
  onReAssessViolation,
}: IViolationDetailViewProps) => {
  const { send } = useWebMessage();
  const [isShowSuggestedCode, setShowSuggestedCode] = useState(false);
  const onClickViolation = () => {
    send({
      type: 'pr-genie-feature-mod:highlight-in-file',
      value: {
        filePath: finding?.filePath,
        startLine: finding?.lineStart,
        endLine: finding?.lineEnd,
        snippet: finding?.violatedCode,
      },
    });
  };

  // const isLoading = reviewStateMap[violationSection]?.reAssessLoadingMap?.[finding.id] ?? false;

  const onClickReAssess = () => {
    onReAssessViolation(
      {
        headBranch,
        baseBranch,
        // baseBranch: 'appmod-cw-dev',
        violationSection,
        violationBody: finding,
        suggestedCode: finding?.suggestedCode ?? '',
        commitSha: headCommitSha,
        filePath: finding?.filePath ?? '',
      },
      {
        onStart: onReAssessStart,
        onSuccess: onReAssessResult,
        onResolved: onResolved,
        onError: (id, error) => {
          console.error('Error in reassess individual', error);
          onReAssessResult(id, {
            resolved: false,
            reason: 'Something went wrong, The re-assessment failed, please try again',
          });
        },
        onEnd: onReAssessEnd,
      },
    );
  };

  function CopyButton({ text }: { text?: string }) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
      if (!text) return;

      await navigator.clipboard.writeText(text);
      setCopied(true);

      setTimeout(() => setCopied(false), 1500);
    };

    return (
      <button
        onClick={handleCopy}
        disabled={!text}
        aria-live="polite"
        title={copied ? 'Copied' : 'Copy'}
        className="
        flex items-center gap-1.5
        px-2 py-1 rounded
        text-xs font-medium
        transition-all duration-200
        hover:bg-[var(--vscode-toolbar-hoverBackground)]
        disabled:opacity-50
      "
      >
        {copied ? (
          <>
            <CheckCheck size={14} className="text-green-500 transition-transform scale-110" />
            <span className="text-green-500">Copied</span>
          </>
        ) : (
          <>
            <Copy size={14} className="text-[var(--vscode-icon-foreground)]" />
            <span className="text-[var(--vscode-foreground)]">Copy</span>
          </>
        )}
      </button>
    );
  }

  return (
    <div
      className={`rounded-lg m-1 p-6 bg-card flex flex-col gap-4
      ${isLoading ? 'border animate-border-glow' : 'border'}
      ${finding?.isResolved === true ? 'border-green-700' : 'border'}
    `}
    >
      {/* Header  */}
      <div>
        <div className="flex justify-between">
          {/* Title */}
          <h2 className="text-xl font-semibold text-foreground">
            {finding?.title ?? 'Untitled finding'}
          </h2>

          {/* Severity + Confidence */}
          <div className="flex items-center gap-3">
            {finding?.severity && (
              <StatusPill
                toolTipContent="Violation Severity"
                status={SEVERITY_MAP[finding?.severity]}
              />
            )}

            {finding?.confidentScore !== undefined && (
              <CustomTooltip content="AI Confidence Score" placement="top">
                <ConfidenceScore score={finding?.confidentScore} />
              </CustomTooltip>
            )}
          </div>
        </div>

        {/* File + Line */}
        <div className="text-muted">
          <CustomTooltip content={finding?.filePath ?? ''} placement="top">
            <span>{finding?.fileName ?? 'Unknown file'}</span>
          </CustomTooltip>
          {finding?.lineStart !== undefined && finding?.lineEnd !== undefined && (
            <>
              • Lines {finding?.lineStart}–{finding?.lineEnd}
            </>
          )}
        </div>
      </div>

      {/* Body */}
      <div className="space-y-4">
        {finding?.body && (
          <AskmodMarkdown className="prose dark:prose-invert max-w-none" content={finding?.body} />
        )}

        <CognitiveDecisioning
          gap={finding?.gap}
          reasons={finding?.reasons}
          citation={finding?.citation}
          violationSection={violationSection}
        />

        {finding?.violatedCode && finding?.suggestedCode && (
          <div>
            <button
              onClick={() => setShowSuggestedCode(!isShowSuggestedCode)}
              className="px-2 py-1 text-sm border rounded-lg border-button-background text-primary flex flex-row items-center"
            >
              View Suggested Fix{' '}
              <ChevronRight
                className={`h-5 transition-transform duration-300 ${
                  isShowSuggestedCode ? 'rotate-90' : ''
                }`}
              />
            </button>
            {isShowSuggestedCode && (
              <div
                className="
                  w-full rounded-xl border p-4 transition-colors"
              >
                <div className="rounded-lg overflow-hidden border border-[var(--vscode-editorGroup-border)] bg-[var(--vscode-editor-background)]">
                  {/* Header */}
                  <div className="grid grid-cols-2 text-sm font-medium border-b border-[var(--vscode-editorGroup-border)]">
                    <div className="px-4 py-2 text-[var(--vscode-errorForeground)] bg-[var(--vscode-editor-background)] flex flex-row gap-2">
                      <CodeXml size={16} /> Violated Code
                    </div>
                    <div className="px-4 py-2 text-[var(--vscode-gitDecoration-addedResourceForeground)] bg-[var(--vscode-editor-background)] border-l border-[var(--vscode-editorGroup-border)] flex flex-row justify-between">
                      <div className="flex flex-row gap-2">
                        <CodeXml size={16} /> Suggested Code
                      </div>
                      <div className="hover:opacity-90 transition-opacity">
                        <CopyButton text={finding?.suggestedCode} />
                      </div>
                    </div>
                  </div>

                  {/* Diff Viewer */}
                  <ViolationDiffViewer
                    code={finding?.violatedCode}
                    suggestedCode={finding?.suggestedCode}
                    lineStart={finding?.lineStart}
                    lineEnd={finding?.lineEnd}
                  />
                </div>
              </div>
            )}
          </div>
        )}

        {/* Diff View */}
        {/* {finding?.violatedCode && finding?.suggestedCode && (
          <ViolationDiffViewer
            code={finding?.violatedCode}
            suggestedCode={finding?.suggestedCode}
            lineStart={finding?.lineStart}
            lineEnd={finding?.lineEnd}
          />
        )} */}

        <div className="flex justify-between gap-3 pt-2">
          <ReusableButton
            onClick={onClickViolation}
            label="Go to Violations"
            disabled={!finding?.filePath}
          />

          {/* 1️⃣ First time */}
          {finding?.isResolved === null && (
            <ReusableButton
              onClick={onClickReAssess}
              startIcon={ButtonIcon.REFRESH_CW}
              variant={ReusableButtonVariant.OUTLINED}
              label={isLoading ? `Re-assessing...` : 'Re-Assess'}
              disabled={isLoading}
            />
          )}

          {/* 2️⃣ Resolved */}
          {finding?.isResolved === true && (
            <div className="px-2 py-1 border border-green-700 rounded-full font-semibold text-xs text-green-700 bg-green-100 flex flex-row gap-1 items-center">
              <CircleCheck fontWeight={700} size={14} /> Resolved
            </div>
          )}

          {/* 3️⃣ Not Resolved */}
          {finding?.isResolved === false && (
            <div className="flex gap-2 items-end">
              <div className="px-2 py-1 border border-red-700 rounded-full font-semibold text-xs text-red-700 bg-red-100 flex flex-row gap-1 items-center">
                <CircleX fontWeight={700} size={14} /> Not Resolved
              </div>

              <ReusableButton
                onClick={onClickReAssess}
                startIcon={ButtonIcon.REFRESH_CW}
                variant={ReusableButtonVariant.OUTLINED}
                label={isLoading ? `Re-assessing...` : 'Re-Assess'}
                disabled={isLoading}
              />
            </div>
          )}
        </div>
      </div>

      {/* {finding?.reAssessReason && (
        <div>
          <div className="font-medium">Re-Assessment Reason</div>
          <div className="text-sm text-muted whitespace-pre-line ml-3">
            {finding?.reAssessReason ?? ''}
          </div>
        </div>
      )} */}

      {finding?.reAssessReason && (
        <ReassessmentResultCard
          reasons={finding?.reAssessResult?.Reasons}
          gap={finding?.reAssessResult?.Gap}
          title={finding?.reAssessResult?.title ?? finding?.title ?? ''}
          statusLabel={
            finding?.reAssessResult?.resolution_status === 'partial_resolved'
              ? 'Partially Resolved'
              : 'Not Resolved'
          }
          confidence_score={finding?.reAssessResult?.confidence_score ?? 0}
          description={finding?.reAssessResult?.reason ?? 'Something went wrong, please try again'}
        />
      )}
      {/* {finding?.reAssessReason && (
        <div className="rounded-lg border p-4 space-y-3">
          <div className="flex items-center justify-start">
            <div className="font-semibold">Re-Assessment Result</div>
          </div>

          <div className="flex items-center justify-between">
            <div className="">Reliance on Platform-Default Encoding</div>

            <div className="flex items-center gap-2">
              {finding?.severity && (
                <StatusPill
                  toolTipContent="Re-assessment Severity"
                  status={SEVERITY_MAP[finding?.severity]}
                />
              )}

              {finding?.confidentScore !== undefined && (
                <ConfidenceScore score={finding?.confidentScore} />
              )}
            </div>
          </div>

          <div className="rounded-md p-3 text-sm text-muted whitespace-pre-line">
            {finding.reAssessReason}
          </div>

          <div className="flex items-center justify-between">
            {finding?.isResolved === false && (
              <div className="px-2 py-1 rounded-full text-xs border border-red-400 text-red-400">
                Not Resolved
              </div>
            )}

            {finding?.isResolved === true && (
              <div className="px-2 py-1 rounded-full text-xs border border-green-400 text-green-400">
                Resolved
              </div>
            )}
          </div>
        </div>
      )} */}
    </div>
  );
};

export default ViolationDetailView;
