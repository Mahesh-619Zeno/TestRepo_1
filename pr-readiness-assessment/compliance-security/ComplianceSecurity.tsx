import { useMemo, useState } from 'react';
import { Loader } from 'lucide-react';
import { cn } from '@/lib/utils';
import Banner from '@/app/components/molecules/Banner';
import { IAdaptedFinding, IComplianceSecurity } from '../../../../types/pull-request-report.types';
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

const normalizeSeverity = (severity?: string): string => {
  switch (severity?.toLowerCase()) {
    case 'critical':
    case 'error':
      return 'critical';
    case 'warning':
      return 'warning';
    default:
      return 'information';
  }
};

interface ComplianceSecurityProps {
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

const ComplianceSecurityReview = ({
  reviewType,
  reviewState,
  updateReviewState,
  setPullRequestDetails,
  pullRequestDetails,
  headBranch,
  prAnalysis,
  isAssessmentResultsEnabled,
  reviewStateMap,
  onReAssessViolation,
}: ComplianceSecurityProps) => {
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

  const { coding_standards } = data || {};
  const headCommitSha = data?.commits?.head_commit_sha ?? '';

  const adaptedFindings: IAdaptedFinding[] = useMemo(() => {
    return (coding_standards || [])?.map((item: IComplianceSecurity, index: number) => ({
      id: `${item?.CodingStandardId}-${item?.FileName}-${item?.LineStart}-${item?.LineEnd}`,
      title: item?.title,
      severity: normalizeSeverity(item?.severity),
      category: item?.Category,
      body: item?.Comment?.body,
      confidentScore: item?.ConfidentScore,
      reasons: item?.Reasons,
      gap: item?.Gap,
      violatedCode: item?.Code,
      suggestedCode: item?.Comment?.SuggestedCode,
      filePath: item?.FileName,
      fileName: item?.FileName?.split('/')?.pop() || '',
      lineStart: item?.LineStart,
      lineEnd: item?.LineEnd,
      isResolved: null,
      citationUrl: item?.citation_highlighted_url,
      citationImage: item?.citation_screenshot_url,
      citationTitle: item?.citation_title,
      citationConfidenceScore: item?.citation_confidence,
    }));
  }, [coding_standards]);

  const findingsWithStatus = useMemo(() => {
    return adaptedFindings.map((s) => {
      const reassess = reAssessResultMap[s.id];
      return {
        ...s,
        isResolved: reassess?.resolved !== undefined ? reassess.resolved : null,
        reAssessReason: reassess?.resolved === false ? reassess.reason : undefined,
        reAssessResult: reassess,
      };
    });
  }, [adaptedFindings, reAssessResultMap]);

  const sections: { key: string; severity: string }[] = [
    { key: 'critical', severity: 'Critical' },
    { key: 'warning', severity: 'Warning' },
    { key: 'information', severity: 'Jas' },
  ];

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

  const ComplianceSecuritySummaryDetailView = () => {
    const status = prAnalysis?.key_metrics?.cs_errors === 0 ? 'PASS' : 'FAIL';
    return (
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
          <InfoCard title="JAS" value={jasFindings?.length || 0} valueColor="text-blue-500" />
        </div>
      </div>
    );
  };

  const renderComplianceSecurity = () => {
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
        summaryView={<ComplianceSecuritySummaryDetailView />}
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
            violationSection={'CS'}
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
    <div className="h-screen w-full bg-editor-background flex flex-col">
      <div className="px-6 py-2 border-b">
        {/* <h1 className="text-xl font-semibold">Compliance & Security Review</h1> */}
        {isLoading ? (
          <Banner message="Compliance & Security is loading..." className="my-2" />
        ) : (
          <Banner
            message="We are currently in the Compliance & Security phase of the PR Readiness Assessment."
            className="my-2"
          />
        )}
      </div>

      <div className="px-6 py-4">
        <AssessmentSectionTable
          name="Compliance & Security Assessment"
          isLoading={isLoading}
          isAssessmentResultsEnabled={isAssessmentResultsEnabled}
          row={{
            type: 'Compliance & Security Assessment',
            status: prAnalysis?.key_metrics?.cs_errors === 0 ? 'PASS' : 'FAIL',
            details: `The submitted pre-peer review assessment changes were analyzed for violations.
        ${prAnalysis?.key_metrics?.cs_errors ?? 0} Critical,
        ${prAnalysis?.key_metrics?.cs_warnings ?? 0} Warnings,
        ${prAnalysis?.key_metrics?.cs_information ?? 0} JAS.`,
            assessmentResult: prAnalysis?.key_metrics?.total_cs_violations ?? 0,
            assessmentUpdates: Object.values(reviewStateMap?.CS?.reAssessResultMap ?? {})?.filter(
              (record) => record.resolved === true,
            ).length,
          }}
        />
      </div>

      {renderComplianceSecurity()}
    </div>
  );
};

export default ComplianceSecurityReview;
