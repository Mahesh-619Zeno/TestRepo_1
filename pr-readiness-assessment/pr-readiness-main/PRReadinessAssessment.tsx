import { CheckCircle2, Mail } from 'lucide-react';
import PRReadinessAssessmentTable from './PRReadinessAssessmentTable';
import {
  IPrReadinessData,
  IPullRequestDetails,
  ReviewState,
  ReviewType,
} from '@/app/types/pull-request.types';
import { useMemo } from 'react';
export type Status = 'PASS' | 'FAIL';
import { Accordion } from '@/app/components/atoms/accordian';
import { Network } from 'lucide-react';
import { TextShimmer } from '@/app/components/atoms/ShimmerText';
import FocusModeAccordionWrapper from '@/app/views/ecg-view/focus-modes/components/FocusModeAccordionWrapper';
import FocusModeAccordionItem from '@/app/views/ecg-view/focus-modes/components/FocusModeAccordionItem';
import Button from '@/app/components/button';
import { postEmailNotifications, showToast } from '@/app/services/editor';
import usePullRequestKeyValueStore from '@/app/store/usePullRequestKeyValueStore';
import { useMutation } from '@tanstack/react-query';

export interface AssessmentRowData {
  type: string;
  status: Status;
  score?: string;
  details: string;
  assessmentResult: number;
  assessmentUpdates: number;
  subStepId: number;
  // handleSubStepClick: (index: number) => void;
}

interface PRReadinessAssessmentProps {
  // IsOverallStatusPending?: boolean;
  reviewStateMap: Record<ReviewType, ReviewState>;
  overallStatus?: 'Passed' | 'Failed';
  qualityScore?: string;
  setPullRequestDetails: (data: IPullRequestDetails) => void;
  pullRequestDetails: IPullRequestDetails;
  headBranch: string;
  prAnalysis: IPrReadinessData;
  open: string | undefined;
  setOpen: (open: string | undefined) => void;
  handleSubStepClick: (subStepIndex: number) => void;
  isConnected: boolean;
  maxSubStepReached: number;
  isAssessmentResultsEnabled: boolean;
  reassessing: boolean;
}

const PRReadinessAssessment = ({
  // IsOverallStatusPending = true,
  reviewStateMap,
  setPullRequestDetails,
  pullRequestDetails,
  headBranch,
  handleSubStepClick,
  prAnalysis,
  open,
  setOpen,
  isConnected,
  reassessing,
  maxSubStepReached,
  isAssessmentResultsEnabled,
}: PRReadinessAssessmentProps) => {
  // const baseBranch = 'feature-branch';
  // const headBranch = 'new-report-apis';
  // const { baseBranch } = pullRequestDetails;
  // const { data } = useQuery({
  //   //
  //   queryKey: ['pull-request', 'details'],
  //   queryFn: () =>
  //     getPRReadinessDetails({
  //       base_branch: baseBranch,
  //       head_branch: headBranch,
  //     }),
  //   enabled: !!baseBranch && !!headBranch,
  //   refetchInterval: 1000, // poll every 2 seconds
  //   refetchIntervalInBackground: true, // continue polling even if tab not active
  //   retry: true, // avoid polling stops on error
  // });

  const overallStatus =
    prAnalysis?.risk_assessment?.level === 'High' || prAnalysis?.key_metrics?.quality_score < 70
      ? 'Failed'
      : 'Passed';
  const isPassed = overallStatus === 'Passed';
  const isLoadingOverallStatus =
    prAnalysis?.risk_assessment?.level === undefined ||
    prAnalysis?.key_metrics?.quality_score === undefined;
  const qualityScore = prAnalysis?.key_metrics?.quality_score;
  const isQualityPassed = typeof qualityScore === 'number' && qualityScore >= 70;
  const pullRequestStateData = usePullRequestKeyValueStore((store) => store.pullRequestStoreData);
  const chatSession = pullRequestStateData.sessionId ?? '';
  const { mutate: mutateSendNotifications } = useMutation({
    mutationFn: postEmailNotifications as (params: any) => Promise<any>,
    onSuccess: () => {
      showToast({
        message: 'We will notify you by email once the complete assessment is finished.',
        type: 'success',
      });
    },
    onError: (err) => {
      console.error(err);
    },
  });

  // const isAssessmentResultsEnabled = useMemo(() => {
  //   return Object.values(reviewStateMap).some((review) =>
  //     Object.values(review?.reAssessResultMap ?? {}).some((result) => result?.resolved === true),
  //   );
  // }, [reviewStateMap]);

  // move it inside the component
  const rows = useMemo(
    () => [
      {
        key: 'functional',
        isLoading: !prAnalysis?.functional_assessment,
        name: 'Functional Assessment',
        id: 'functional_assessment',
        row: prAnalysis?.functional_assessment && {
          type: 'Functional Assessment',
          status: prAnalysis?.functional_assessment?.metRequirements ? 'PASS' : 'FAIL',
          score: `${prAnalysis?.functional_assessment?.overallProgress ?? 0}%`,
          details:
            prAnalysis?.functional_assessment?.overallConclusion ??
            `${prAnalysis?.functional_assessment?.conclusion?.completedFeatures ?? ''}
           ${prAnalysis?.functional_assessment?.conclusion?.incompleteFeatures ?? ''}`,
          assessmentResult: prAnalysis?.functional_assessment?.userStories?.length ?? 0,
          assessmentUpdates: '-',
          subStepId: 0,
        },
      },
      {
        key: 'devops',
        isLoading: !prAnalysis?.devops_assessment,
        name: 'DevOps Assessment',
        id: 'devops_assessment',
        row: prAnalysis?.devops_assessment && {
          type: 'DevOps Assessment',
          status: prAnalysis?.devops_assessment?.status === 'Passed' ? 'PASS' : 'FAIL',
          details: prAnalysis?.devops_assessment?.review_summary ?? '',
          assessmentResult: prAnalysis?.devops_assessment_inline?.length ?? 0,
          assessmentUpdates: Object.values(reviewStateMap?.devops?.reAssessResultMap ?? {}).filter(
            (r) => r.resolved === true,
          ).length,
          subStepId: 1,
        },
      },
      {
        key: 'tech',
        isLoading: !prAnalysis?.key_metrics,
        name: 'Technical Quality Assessment',
        id: 'technical_quality_assessment',
        row: prAnalysis?.key_metrics && {
          type: 'Technical Quality Assessment',
          status:
            prAnalysis?.key_metrics?.quality_score >= 70 &&
            prAnalysis?.risk_assessment?.level !== 'High'
              ? 'PASS'
              : 'FAIL',
          score: `${prAnalysis?.key_metrics?.quality_score ?? 0}%`,
          details: prAnalysis?.overall_summary?.summary?.businessDescription ?? '',
          assessmentResult: prAnalysis?.key_metrics?.total_issues ?? 0,
          assessmentUpdates: Object.values(reviewStateMap?.TQA?.reAssessResultMap ?? {}).filter(
            (r) => r.resolved === true,
          ).length,
          subStepId: 2,
        },
      },
      {
        key: 'security',
        isLoading: !prAnalysis?.key_metrics,
        name: 'Compliance & Security Assessment',
        id: 'coding_standards_assessment',
        row: prAnalysis?.key_metrics && {
          type: 'Compliance & Security Assessment',
          status: prAnalysis?.key_metrics?.cs_errors === 0 ? 'PASS' : 'FAIL',
          details: `The submitted pre-peer review assessment changes were analyzed for violations.
        ${prAnalysis?.key_metrics?.cs_errors ?? 0} Critical,
        ${prAnalysis?.key_metrics?.cs_warnings ?? 0} Warnings,
        ${prAnalysis?.key_metrics?.cs_information ?? 0} JAS.`,
          assessmentResult: prAnalysis?.key_metrics?.total_cs_violations ?? 0,
          assessmentUpdates: Object.values(reviewStateMap?.CS?.reAssessResultMap ?? {}).filter(
            (r) => r.resolved === true,
          ).length,
          subStepId: 3,
        },
      },
    ],
    [prAnalysis, reviewStateMap],
  );

  const handleMailClick = () => {
    if (!chatSession) return;
    mutateSendNotifications({
      session_id: chatSession,
      assessment_type: ['full_assessment'],
    });
  };

  return (
    <div className="rounded-xl bg-editor-info-background p-6">
      {/* Header */}
      <div className="mb-4">
        <div className="flex items-start justify-between">
          <div>
            {/* <h2 className="text-xl font-semibold">PR Readiness Assessment</h2> */}

            {isLoadingOverallStatus && (
              <span className="h-fit w-fit flex gap-2 bg-primary/60 text-menu-foreground text-xs font-semibold px-2 ml-1 py-0.5 rounded-lg shadow-sm mt-1">
                <TextShimmer>In Progress</TextShimmer>
              </span>
            )}
          </div>
        </div>

        {/* Status Pills */}
        <div className="flex items-center justify-between gap-3 mt-2">
          <div className="flex gap-3">
            {/* Overall Status */}
            {isLoadingOverallStatus ? (
              <div className="h-4 w-32 rounded bg-muted  animate-pulse" />
            ) : (
              <span
                className={`
                inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm
                ${
                  isPassed
                    ? 'border border-emerald-500 text-emerald-400'
                    : 'border border-red-500 text-red-400'
                }
              `}
              >
                {isPassed && <CheckCircle2 className="w-4 h-4" />}
                Overall Status: {overallStatus}
              </span>
            )}

            {/* Quality Score*/}
            {/* {prAnalysis?.key_metrics?.quality_score !== undefined ? (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm border border-emerald-500 text-emerald-400">
              Quality: {prAnalysis?.key_metrics?.quality_score}
            </span>
          ) : (
            <div className="h-4 w-32 rounded bg-muted  animate-pulse" />
          )} */}
            {qualityScore !== undefined ? (
              <span
                className={`
              inline-flex items-center px-3 py-1 rounded-full text-sm
              ${
                isQualityPassed
                  ? 'border border-emerald-500 text-emerald-400'
                  : 'border border-red-500 text-red-400'
              }
            `}
              >
                Quality: {qualityScore ? `${qualityScore}%` : ''}
              </span>
            ) : (
              <div className="h-4 w-32 rounded bg-muted animate-pulse" />
            )}
          </div>
          <Button
            onClick={handleMailClick}
            disabled={maxSubStepReached === 4}
            className="flex items-center bg-primary  text-primary-foreground gap-2 px-4 py-2 rounded-md text-sm font-medium"
          >
            <Mail size={16} />
            Notify All
          </Button>
        </div>
      </div>
      <div className="mb-4">
        <Accordion
          type="single"
          collapsible
          value={open}
          disabled={prAnalysis?.workflowSubSteps?.length === 0}
          onValueChange={setOpen}
          className="w-full"
        >
          <FocusModeAccordionWrapper
            value="workflow"
            hideChevron={prAnalysis?.workflowSubSteps?.length === 0}
            trigger={
              <div className="flex items-center gap-2 w-full">
                <Network className="w-4 h-4" />
                <span className="text-left flex-1">Watch Me Work</span>
              </div>
            }
          >
            {prAnalysis?.workflowSubSteps?.length > 0 ? (
              <FocusModeAccordionItem
                items={prAnalysis?.workflowSubSteps}
                openLatestStreamingAccordion={maxSubStepReached < 4}
              />
            ) : null}
          </FocusModeAccordionWrapper>
        </Accordion>
        {maxSubStepReached < 4 ? (
          <TextShimmer className="app-assistant__loading px-2 mt-2 text-base">
            {reassessing ? 'PRR Genie is Re-assessing' : 'PRR Genie is Thinking'}
          </TextShimmer>
        ) : null}
      </div>

      {/* Table */}
      <PRReadinessAssessmentTable
        handleSubStepClick={handleSubStepClick}
        rows={rows}
        maxSubStepReached={maxSubStepReached}
        isAssessmentResultsEnabled={isAssessmentResultsEnabled}
      />
    </div>
  );
};

export default PRReadinessAssessment;
