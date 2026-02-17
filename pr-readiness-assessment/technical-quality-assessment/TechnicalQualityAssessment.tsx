import { useMemo, useState } from 'react';
import { Loader } from 'lucide-react';
import { cn } from '@/lib/utils';
import Banner from '@/app/components/molecules/Banner';
import {
  IAdaptedFinding,
  IPrAnalysisReportData,
} from '../../../../types/pull-request-report.types';
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

export interface ITechnicalQualitySummaryViewProps {
  data: IPrAnalysisReportData;
}

interface ITechnicalQualityProps {
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

/* Severity */
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

/* Main Component */
const TechnicalQualityAssessment = ({
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
}: ITechnicalQualityProps) => {
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

  const headCommitSha = data?.commits?.head_commit_sha ?? '';

  const combinedFindings = useMemo(() => {
    return (
      data?.file_summaries?.flatMap((file_summary: any) =>
        file_summary?.feedback?.map((feedbackItem: any, index: number) => ({
          feedback: feedbackItem,
          introspection: file_summary?.introspection?.from_training?.[index],
        })),
      ) ?? []
    );
  }, [data]);

  const adaptedFindings: IAdaptedFinding[] = useMemo(
    () =>
      combinedFindings?.map((item: any, index: number) => ({
        id: `${item?.feedback?.path}-${item?.feedback?.line}-${index}`,
        title: item?.feedback?.title ?? '',
        severity: normalizeSeverity(item?.feedback?.severity),
        category: item?.feedback?.category,
        body: item?.feedback?.body ?? item?.feedback?.description ?? '',
        confidentScore: item?.feedback?.confident_score,
        reason: item?.feedback?.Reason,
        reasons: item?.feedback?.Reasons,
        gap: item?.feedback?.Gap,
        violatedCode: item?.feedback?.code,
        suggestedCode: item?.feedback?.suggestion,
        filePath: item?.feedback?.path,
        fileName: item?.feedback?.path?.split('/')?.pop() || '',
        lineStart: item?.feedback?.start_line,
        lineEnd: item?.feedback?.line,
        isResolved: null,
        citation: item?.introspection,
        citationUrl: item?.feedback?.citation_highlighted_url,
        citationImage: item?.feedback?.citation_screenshot_url,
        citationTitle: item?.feedback?.citation_title,
        citationConfidenceScore: item?.feedback?.citation_confidence,
      })),
    [combinedFindings],
  );

  const sections = [
    { key: 'critical', label: 'Critical' },
    { key: 'warning', label: 'Warning' },
    { key: 'information', label: 'Jas' },
  ];

  const findingsWithStatus = useMemo(() => {
    return adaptedFindings?.map((finding) => {
      const reassess = reAssessResultMap[finding.id];

      return {
        ...finding,
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
    [findingsWithStatus, sections],
  );

  const criticalFindings = useMemo(
    () => orderedFindings?.filter((finding) => finding?.severity === 'critical'),
    [orderedFindings],
  );

  const warningFindings = useMemo(
    () => orderedFindings?.filter((finding) => finding?.severity === 'warning'),
    [orderedFindings],
  );

  const informationFindings = useMemo(
    () => orderedFindings?.filter((finding) => finding?.severity === 'information'),
    [orderedFindings],
  );

  const TechnicalQualitySummaryView = ({ data }: ITechnicalQualitySummaryViewProps) => {
    const businessImpact = data?.overall_summary?.businessImpact;
    const status =
      prAnalysis?.key_metrics?.quality_score >= 70 && prAnalysis?.risk_assessment?.status !== false
        ? 'PASS'
        : 'FAIL';
    return (
      <>
        <div className="flex gap-4 mt-5">
          <div className="flex-1 flex">
            <InfoCard
              title="Status"
              value={status}
              valueColor={status === 'PASS' ? 'text-green-500' : 'text-red-500'}
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
            <InfoCard
              title="JAS"
              value={informationFindings?.length || 0}
              valueColor="text-blue-500"
            />
          </div>
        </div>
        <div
          className="rounded-lg p-4 border bg-card space-y-6"
          // mt-5 space-y-4
        >
          <h2 className="text-xl font-semibold mb-4">Technical Quality Assessment Summary</h2>

          <div>
            <div className="font-medium mb-1">What Changed</div>
            <div className="text-muted">{businessImpact?.whatChanged ?? 'No data.'}</div>
          </div>

          <div>
            <div className="font-medium mb-1">Why It Matters</div>
            <div className="text-muted">{businessImpact?.whyItMatters ?? 'No data.'}</div>
          </div>

          <div>
            <div className="font-medium mb-1">User Experience Impact</div>
            <div className="text-muted">{businessImpact?.userExperience ?? 'No data.'}</div>
          </div>
        </div>
      </>
    );
  };

  const renderTechnicalQualityAssessment = () => {
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
        summaryView={<TechnicalQualitySummaryView data={data} />}
        critical={criticalFindings}
        warning={warningFindings}
        jas={informationFindings}
        renderViolationDetail={(finding) => (
          <ViolationDetailView
            key={finding.id}
            finding={finding}
            headBranch={headBranch}
            baseBranch={baseBranch}
            headCommitSha={headCommitSha}
            isLoading={!!reAssessLoadingMap[finding.id]}
            violationSection={'TQA'}
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
      {/* Header */}
      <div className="px-6 py-2 border-b">
        {/* <h1 className="text-xl font-semibold">Technical Quality Assessment</h1> */}
        {isLoading ? (
          <Banner message="Technical Quality Assessment is loading..." className="my-2" />
        ) : (
          <Banner
            message="We are currently in the Technical Quality Assessment phase of the PR Readiness Assessment"
            className="my-2"
          />
        )}
      </div>

      <div className="px-6 py-4">
        <AssessmentSectionTable
          name="Technical Quality Assessment"
          isLoading={false}
          isAssessmentResultsEnabled={isAssessmentResultsEnabled}
          row={{
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
              (result) => result.resolved === true,
            ).length,
          }}
        />
      </div>

      {renderTechnicalQualityAssessment()}
    </div>
  );
};

export default TechnicalQualityAssessment;
