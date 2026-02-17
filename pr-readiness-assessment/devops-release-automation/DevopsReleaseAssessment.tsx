import { useMemo, useState } from 'react';
import { Loader } from 'lucide-react';
import { cn } from '@/lib/utils';
import Banner from '@/app/components/molecules/Banner';
import AskmodMarkdown from '../../../ecg-view/components/pr-genie/PrGenieMarkdownOld';
import { IAdaptedFinding } from '../../../../types/pull-request-report.types';
import {
  IPrReadinessData,
  IPullRequestDetails,
  ReviewState,
  ReviewType,
  TOnReAssessViolation,
} from '@/app/types/pull-request.types';
import { ViolationAccordionLayout } from '../ViolationAccordionLayout';
import ViolationDetailView from '../ViolationDetailView';
import InfoCard from '../infoCards';
import AssessmentSectionTable from '../AssessmentSection';

interface DevopsReleaseAutomationReviewProps {
  reviewType: ReviewType;
  reviewState: ReviewState;
  updateReviewState: (type: ReviewType, updater: (prev: ReviewState) => ReviewState) => void;
  setPullRequestDetails: (data: IPullRequestDetails) => void;
  pullRequestDetails: IPullRequestDetails;
  headBranch: string;
  prAnalysis: IPrReadinessData;
  isAssessmentResultsEnabled: boolean;
  reviewStateMap: Record<ReviewType, ReviewState>;
  onReAssessViolation: TOnReAssessViolation;
}
const normalizeSeverity = (severity?: string): 'critical' | 'warning' | 'information' => {
  switch (severity?.toLowerCase()) {
    case 'critical':
      return 'critical';
    case 'warning':
      return 'warning';
    default:
      return 'information';
  }
};

/* Main Review Component */
const DevopsReleaseAutomationReview = ({
  setPullRequestDetails,
  pullRequestDetails,
  headBranch,
  reviewType,
  reviewState,
  updateReviewState,
  prAnalysis,
  isAssessmentResultsEnabled,
  reviewStateMap,
  onReAssessViolation,
}: DevopsReleaseAutomationReviewProps) => {
  // const headBranch = 'new-report-apis';
  const isLoading = false;
  // const baseBranch = 'feature-branch';
  // const [resolvedMap, setResolvedMap] = useState<Record<string, boolean>>({});
  // const [reAssessLoadingMap, setReAssessLoadingMap] = useState<Record<string, boolean>>({});
  // const [reAssessResultMap, setReAssessResultMap] = useState<Record<string, ReAssessResult>>({});

  const { baseBranch } = pullRequestDetails;
  const { resolvedMap, reAssessLoadingMap, reAssessResultMap } = reviewState;
  const data = prAnalysis;
  // const { data, isLoading } = useQuery({
  //   queryKey: ['pull-request', 'details'],
  //   queryFn: () =>
  //     getPRReadinessDetails({
  //       base_branch: baseBranch,
  //       head_branch: headBranch,
  //     }),
  //   enabled: !!baseBranch && !!headBranch,
  // });

  const { devops_assessment } = data || {};
  const headCommitSha = data?.commits?.head_commit_sha ?? '';

  const {
    findings = [],
    review_summary,
    introspection = {},
    overall_recommendations,
    status,
  } = devops_assessment || {};

  const adaptedFindings: IAdaptedFinding[] = useMemo(
    () =>
      findings?.map((item: any, index: number) => ({
        id: `${item?.title}-${index}`,
        title: item?.title,
        severity: normalizeSeverity(item?.severity),
        category: item?.category,
        body: item?.description ?? item?.comment?.recommendation,
        confidentScore: item?.comment?.confidence_score,
        reasons: item?.comment?.Reasons,
        gap: item?.comment?.gap,
        violatedCode: item?.comment?.code,
        suggestedCode: item?.comment?.suggested_code,
        filePath: item?.file_path,
        fileName: item?.file_path?.split('/')?.pop(),
        lineStart: item?.line_numbers?.[0],
        lineEnd: item?.line_numbers?.[1] ?? item?.line_numbers?.[0],
        isResolved: null,
        citation: introspection?.from_training?.find(
          (data: any) => data?.feedback_id === item?.finding_id, // TODO : remove any
        ),
      })),
    [findings],
  );

  const sections = [
    { key: 'critical', label: 'Critical' },
    { key: 'warning', label: 'Warning' },
    { key: 'information', label: 'Jas' },
  ];

  const findingsWithStatus = useMemo(() => {
    return adaptedFindings?.map((s) => {
      const reassess = reAssessResultMap[s.id];

      return {
        ...s,
        isResolved: reassess?.resolved !== undefined ? reassess.resolved : null,
        reAssessReason: reassess?.resolved === false ? reassess.reason : undefined,
        reAssessResult: reassess,
      };
    });
  }, [adaptedFindings, reAssessResultMap]);

  const orderedFindings = useMemo(
    () =>
      sections?.flatMap((section) =>
        findingsWithStatus?.filter((finding) => finding?.severity === section?.key),
      ),
    [findingsWithStatus],
  );

  const criticalFindings = useMemo(
    () => orderedFindings?.filter((finding) => finding?.severity === 'critical'),
    [orderedFindings],
  );

  const warningFindings = useMemo(
    () => orderedFindings?.filter((finding) => finding?.severity === 'warning'),
    [orderedFindings],
  );

  const jasFindings = useMemo(
    () => orderedFindings?.filter((finding) => finding?.severity === 'information'),
    [orderedFindings],
  );

  const DevopsSummaryDetailView = ({
    reviewSummary,
    recommendations,
    status,
  }: {
    reviewSummary?: string;
    recommendations?: string[];
    status?: string;
  }) => {
    return (
      <>
        <div className="flex gap-4 mt-5">
          <div className="flex-1 flex">
            <InfoCard
              title="Status"
              value={status === 'Passed' ? 'Pass' : 'Fail'}
              valueColor={status === 'Passed' ? 'text-green-500' : 'text-red-500'}
            />
          </div>
          <div className="flex-1 flex">
            <InfoCard
              title="Critical Issues"
              value={criticalFindings?.length || 0}
              valueColor="text-red-500"
            />
          </div>
          <div className="flex-1 flex">
            <InfoCard
              title="Warning"
              value={warningFindings?.length || 0}
              valueColor="text-orange-500"
            />
          </div>
          <div className="flex-1 flex">
            <InfoCard title="JAS" value={jasFindings?.length || 0} valueColor="text-blue-500" />
          </div>
        </div>
        <div
          className="rounded-lg p-4 border bg-card space-y-6"
          // mt-5 space-y-3
        >
          <div className="flex items-center gap-3">
            {/* {status && <StatusPill status={SEVERITY_MAP[status]} />} */}
            <h2 className="text-xl font-semibold">DevOps Review Summary</h2>
          </div>

          {reviewSummary && (
            <AskmodMarkdown
              className="prose dark:prose-invert max-w-none"
              content={reviewSummary}
            />
          )}

          {!!recommendations?.length && (
            <div>
              <div className="font-medium mb-2">Overall Recommendations</div>
              <ul className="list-disc list-inside text-muted space-y-1">
                {recommendations?.map((recommendation, idx) => (
                  <li key={idx}>{recommendation ?? ''}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </>
    );
  };

  const renderDevopsReleaseAutomation = () => {
    if (isLoading) {
      return (
        <div className="flex justify-center mt-40">
          <Loader
            size={48}
            style={{ animationDuration: '5s' }}
            className={cn('animate-spin', 'text-progressBar-background')}
          />
        </div>
      );
    }

    return (
      <ViolationAccordionLayout
        isLoading={isLoading}
        summaryView={
          <DevopsSummaryDetailView
            reviewSummary={review_summary}
            recommendations={overall_recommendations}
            status={status}
          />
        }
        critical={criticalFindings}
        warning={warningFindings}
        jas={jasFindings}
        renderViolationDetail={(finding) => (
          <ViolationDetailView
            key={finding.id}
            finding={finding}
            headBranch={headBranch}
            baseBranch={baseBranch}
            headCommitSha={headCommitSha}
            isLoading={!!reAssessLoadingMap[finding.id]}
            violationSection={'devops'}
            onReAssessViolation={onReAssessViolation}
            onReAssessStart={(id) =>
              updateReviewState(reviewType, (prev) => ({
                ...prev,
                reAssessLoadingMap: {
                  ...prev.reAssessLoadingMap,
                  [id]: true,
                },
              }))
            }
            onReAssessEnd={(id) =>
              updateReviewState(reviewType, (prev) => ({
                ...prev,
                reAssessLoadingMap: {
                  ...prev.reAssessLoadingMap,
                  [id]: false,
                },
              }))
            }
            onResolved={(id) =>
              updateReviewState(reviewType, (prev) => ({
                ...prev,
                resolvedMap: {
                  ...prev.resolvedMap,
                  [id]: true,
                },
              }))
            }
            onReAssessResult={(id, result) =>
              updateReviewState(reviewType, (prev) => ({
                ...prev,
                reAssessResultMap: {
                  ...prev.reAssessResultMap,
                  [id]: result,
                },
              }))
            }
          />
        )}
      />
    );
  };

  return (
    <div className="h-screen flex flex-col bg-editor-background w-full">
      <div className="px-6 py-2 border-b">
        {/* <h1 className="text-xl font-semibold">DevOps & Release Automation Review</h1> */}
        <Banner
          message={
            isLoading
              ? 'Devops & release automation is loading...'
              : 'We are currently in the DevOps & Release Automation phase of the PR Readiness Assessment.'
          }
          className="my-2"
        />
      </div>
      <div className="px-6 py-4">
        <AssessmentSectionTable
          name="Devops Assessment"
          isLoading={false}
          isAssessmentResultsEnabled={isAssessmentResultsEnabled}
          row={{
            type: 'DevOps Assessment',
            status: prAnalysis?.devops_assessment?.status === 'Passed' ? 'PASS' : 'FAIL',
            details: prAnalysis?.devops_assessment?.review_summary ?? '',
            assessmentResult: prAnalysis?.devops_assessment_inline?.length ?? 0,
            assessmentUpdates: Object.values(
              reviewStateMap?.devops?.reAssessResultMap ?? {},
            ).filter((review) => review.resolved === true).length,
          }}
        />
      </div>

      {renderDevopsReleaseAutomation()}
    </div>
  );
};

export default DevopsReleaseAutomationReview;
