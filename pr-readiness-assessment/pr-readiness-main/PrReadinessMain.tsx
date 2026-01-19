import React, { Dispatch, SetStateAction, useMemo, useState } from 'react';
import PRReadinessAssessment from './PRReadinessAssessment';
import DevopsReleaseAutomationReview from '../devops-release-automation/DevopsReleaseAssessment';
import TechnicalQualityAssessment from '../technical-quality-assessment/TechnicalQualityAssessment';
import ComplianceSecurityReview from '../compliance-security/ComplianceSecurity';
import FunctionalAssessment from '../functional-assessment/FunctionalAssessment';
import {
  IPrReadinessData,
  IPullRequestDetails,
  ReviewState,
  ReviewType,
  TOnReAssessViolation,
} from '@/app/types/pull-request.types';
import Button from '@/app/components/button';
import { Loader, RefreshCcw } from 'lucide-react';
import { TextShimmer } from '@/app/components/atoms/ShimmerText';
import { cn } from '@/lib/utils';

interface PRReadinessMainProps {
  activeSubStepIndex: number;
  maxSubStepReached: number;
  prAnalysis: IPrReadinessData;
  handleSubStepClick: (subStepIndex: number) => void;
  showSummary: boolean;
  setShowSummary: (bool: boolean) => void;
  setPullRequestDetails: (data: IPullRequestDetails) => void;
  pullRequestDetails: IPullRequestDetails;
  headBranch: string;
  setShowReassessConfirmModal: (show: boolean) => void;
  open: string | undefined;
  setOpen: (open: string | undefined) => void;
  isConnected: boolean;
  reviewStateMap: Record<ReviewType, ReviewState>;
  setReviewStateMap: Dispatch<SetStateAction<Record<ReviewType, ReviewState>>>;
  reassessing: boolean;
  onReAssessViolation: TOnReAssessViolation;
}

type SubStepIndex = 0 | 1 | 2 | 3;

const stepTitles: Omit<Record<SubStepIndex, string>, 0> = {
  1: 'DevOps & Release Automation',
  2: 'Technical Quality Assessment',
  3: 'Compliance & Security',
};

const getStepTitle = (activeSubStepIndex: SubStepIndex, showSummary: boolean): string => {
  if (activeSubStepIndex === 0) {
    return showSummary ? 'PR Readiness Assessment' : 'Functional Assessment';
  }
  return stepTitles[activeSubStepIndex as keyof typeof stepTitles] || '';
};

const PRReadinessMain: React.FC<PRReadinessMainProps> = ({
  activeSubStepIndex,
  maxSubStepReached,
  prAnalysis,
  handleSubStepClick,
  showSummary,
  setShowSummary,
  setPullRequestDetails,
  pullRequestDetails,
  headBranch,
  setShowReassessConfirmModal,
  open,
  setOpen,
  isConnected,
  reviewStateMap,
  setReviewStateMap,
  reassessing,
  onReAssessViolation,
}) => {
  const isDisabled = maxSubStepReached < 4;
  const [showTooltip, setShowTooltip] = useState(false);

  const updateReviewState = (type: ReviewType, updater: (prev: ReviewState) => ReviewState) => {
    setReviewStateMap((prev) => ({
      ...prev,
      [type]: updater(prev[type]),
    }));
  };

  const handleClickBack = () => {
    const newIndex = activeSubStepIndex === 0 ? 0 : activeSubStepIndex - 1;
    setShowSummary(activeSubStepIndex === 0);
    handleSubStepClick(newIndex);
  };

  const isNextButtonDisabled = React.useMemo(() => {
    if (showSummary) {
      return maxSubStepReached === 0;
    }

    if (activeSubStepIndex === 0) {
      return maxSubStepReached <= 1;
    }

    if (activeSubStepIndex === 1) {
      return maxSubStepReached <= 2;
    }

    if (activeSubStepIndex === 2) {
      return maxSubStepReached <= 3;
    }

    if (activeSubStepIndex === 3) {
      // return maxSubStepReached <= 4;
      return false; // enable by default
    }
  }, [showSummary, maxSubStepReached, activeSubStepIndex]);

  const isAssessmentResultsEnabled = useMemo(() => {
    return Object.values(reviewStateMap).some((review) =>
      Object.values(review?.reAssessResultMap ?? {}).some((result) => result?.resolved === true),
    );
  }, [reviewStateMap]);

  return (
    <div>
      <div className="flex justify-between items-center gap-4 pl-7 pb-8">
        {/* <strong>Active Sub Step: {activeSubStepIndex}</strong> */}
        <h1 className="text-2xl font-semibold">
          {getStepTitle(activeSubStepIndex as SubStepIndex, showSummary)}
        </h1>
        <div className="flex gap-4 px-8">
          {!showSummary && (
            <button
              onClick={handleClickBack}
              className="flex items-center gap-2 px-4 py-2 rounded-md bg-primary text-primary-foreground text-sm font-medium ml-4"
            >
              {'← Back'}
            </button>
          )}
          {showSummary && activeSubStepIndex === 0 ? (
            <div className="relative inline-flex">
              <Button
                aria-disabled={isDisabled}
                tabIndex={isDisabled ? -1 : 0}
                onClick={() => {
                  if (isDisabled) return;
                  setShowReassessConfirmModal(true);
                }}
                onMouseEnter={() => {
                  if (isDisabled) {
                    setShowTooltip(true);
                  }
                }}
                onMouseLeave={() => setShowTooltip(false)}
                className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium
      ${isDisabled ? 'opacity-80 cursor-not-allowed' : ''}
    `}
              >
                {reassessing ? (
                  <span className='flex gap-2'>
                    <Loader
                      size={16}
                      style={{ animationDuration: '5s' }}
                      className={cn('animate-spin', 'text-progressBar-background')}
                    />
                  <TextShimmer className="text-foreground font-base">
                    Re-assessing...
                  </TextShimmer>
                  </span>
                ) : (
                  <span className="flex gap-2">
                    <RefreshCcw size={16} />
                    Re-Assess All
                  </span>
                )}
              </Button>

              {isDisabled && showTooltip && (
                <div
                  role="tooltip"
                  className="absolute top-full mt-2 left-1/2 -translate-x-1/2
                 whitespace-nowrap rounded bg-black px-2 py-1
                 text-xs text-white z-50"
                >
                  Wait for PR Readiness assessment to complete
                </div>
              )}
            </div>
          ) : null}

          {activeSubStepIndex >= 0 && activeSubStepIndex < 4 ? (
            <Button
              onClick={() => handleSubStepClick(showSummary ? 0 : activeSubStepIndex + 1)}
              disabled={isNextButtonDisabled}
              className="flex items-center gap-2 px-4 py-2 rounded-md bg-primary text-primary-foreground text-sm font-medium"
            >
              {showSummary ? 'Proceed to Functional Assessment →' : 'Proceed Next →'}
            </Button>
          ) : null}
        </div>
      </div>
      {/* Render content based on active sub step */}
      <div className="overflow-y-auto h-[calc(100vh-200px)]">
        {showSummary === true && (
          <PRReadinessAssessment
            reviewStateMap={reviewStateMap}
            setPullRequestDetails={setPullRequestDetails}
            pullRequestDetails={pullRequestDetails}
            headBranch={headBranch}
            prAnalysis={prAnalysis}
            handleSubStepClick={handleSubStepClick}
            open={open}
            setOpen={setOpen}
            isConnected={isConnected}
            maxSubStepReached={maxSubStepReached}
            isAssessmentResultsEnabled={isAssessmentResultsEnabled}
            reassessing={reassessing}
          />
        )}

        {!showSummary && (
          <>
            {activeSubStepIndex === 0 && (
              <FunctionalAssessment
                prAnalysis={prAnalysis}
                setPullRequestDetails={setPullRequestDetails}
                pullRequestDetails={pullRequestDetails}
                headBranch={headBranch}
                isAssessmentResultsEnabled={isAssessmentResultsEnabled}
                reviewStateMap={reviewStateMap}
              />
            )}
            {activeSubStepIndex === 1 && (
              <DevopsReleaseAutomationReview
                reviewType="devops"
                prAnalysis={prAnalysis}
                reviewState={reviewStateMap.devops}
                updateReviewState={updateReviewState}
                setPullRequestDetails={setPullRequestDetails}
                pullRequestDetails={pullRequestDetails}
                headBranch={headBranch}
                isAssessmentResultsEnabled={isAssessmentResultsEnabled}
                reviewStateMap={reviewStateMap}
                onReAssessViolation={onReAssessViolation}
              />
            )}
            {activeSubStepIndex === 2 && (
              <TechnicalQualityAssessment
                reviewType="TQA"
                prAnalysis={prAnalysis}
                reviewState={reviewStateMap.TQA}
                updateReviewState={updateReviewState}
                setPullRequestDetails={setPullRequestDetails}
                pullRequestDetails={pullRequestDetails}
                headBranch={headBranch}
                isAssessmentResultsEnabled={isAssessmentResultsEnabled}
                reviewStateMap={reviewStateMap}
                onReAssessViolation={onReAssessViolation}
              />
            )}
            {activeSubStepIndex === 3 && (
              <ComplianceSecurityReview
                reviewType="CS"
                prAnalysis={prAnalysis}
                reviewState={reviewStateMap.CS}
                updateReviewState={updateReviewState}
                setPullRequestDetails={setPullRequestDetails}
                pullRequestDetails={pullRequestDetails}
                headBranch={headBranch}
                isAssessmentResultsEnabled={isAssessmentResultsEnabled}
                reviewStateMap={reviewStateMap}
                onReAssessViolation={onReAssessViolation}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default PRReadinessMain;
