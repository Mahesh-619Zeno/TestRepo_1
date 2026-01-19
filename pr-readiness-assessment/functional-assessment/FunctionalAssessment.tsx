import Banner from '@/app/components/molecules/Banner';
import InfoCard from '../infoCards';
import { cn } from '@/lib/utils';
import UserStoryDetails from './userStoryDetails';
import {
  IPrReadinessData,
  IPullRequestDetails,
  ReviewState,
  ReviewType,
} from '@/app/types/pull-request.types';
import { Loader } from 'lucide-react';
import { IUserStory } from '../../../../types/pull-request-report.types';
import AssessmentSectionTable from '../AssessmentSection';

const FunctionalAssessment = ({
  setPullRequestDetails,
  pullRequestDetails,
  headBranch,
  prAnalysis,
  isAssessmentResultsEnabled,
  reviewStateMap,
}: {
  setPullRequestDetails: (data: IPullRequestDetails) => void;
  pullRequestDetails: IPullRequestDetails;
  headBranch: string;
  prAnalysis: IPrReadinessData;
  isAssessmentResultsEnabled: boolean;
  reviewStateMap: Record<ReviewType, ReviewState>;
}) => {
  const isLoading = false;
  const data = prAnalysis;
  // const { baseBranch } = pullRequestDetails;
  // const { data, isLoading } = useQuery({
  //   queryKey: ['pull-request', 'details'],
  //   queryFn: () =>
  //     getPRReadinessDetails({
  //       base_branch: baseBranch,
  //       head_branch: headBranch,
  //     }),
  //   enabled: !!baseBranch && !!headBranch,
  // });

  const { functional_assessment } = data || {};

  const renderFunctionalAssessment = () => {
    const status = prAnalysis?.functional_assessment?.metRequirements ? 'PASS' : 'FAIL';
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
      <div className="px-6">
        <div className="flex gap-4 mt-1">
          <div className="flex-1 flex">
            <InfoCard
              title="Requirement Met"
              // value={functional_assessment?.metRequirements ? 'Yes' : 'No'}
              value={status}
              valueColor={status === 'PASS' ? 'text-green-500' : 'text-red-500'}
            />
          </div>
          <div className="flex-1 flex">
            <InfoCard
              title="Overall Progress"
              value={functional_assessment?.overallProgress || 0}
              valueColor="text-orange-500"
            />
          </div>
          <div className="flex-1 flex">
            <InfoCard
              title="Completed"
              value={functional_assessment?.completedCount || 0}
              valueColor="text-green-500"
            />
          </div>
          <div className="flex-1 flex">
            <InfoCard
              title="Incomplete"
              value={functional_assessment?.incompleteCount || 0}
              valueColor="text-red-500"
            />
          </div>
        </div>

        <div className="flex flex-col gap-4 rounded-md border bg-card px-2 py-2 mt-5">
          {/* <AskmodMarkdown
          className={cn(
            '!w-[95%]',
            'prose dark:prose-invert w-[100%]', // Apply prose for better markdown rendering
            'text-base text-foreground leading-relaxed',
          )}
          content={content as string}
        /> */}
          <div className="flex flex-col gap-1">
            <div className="flex items-center">Completed features:</div>
            <div className="px-2">{functional_assessment?.conclusion?.completedFeatures ?? ''}</div>
          </div>
          <div className="flex flex-col gap-1">
            <div className="flex items-center">Incomplete features:</div>
            <div className="px-2">
              {functional_assessment?.conclusion?.incompleteFeatures ?? ''}
            </div>
          </div>
          <div></div>
        </div>

        {functional_assessment?.userStories?.map((userStory: IUserStory, index: number) => (
          <div key={`userStory-${userStory.id}-${index}`} className="mt-4">
            <UserStoryDetails userStory={userStory} index={index} />
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="h-screen w-full bg-editor-background flex flex-col gap-4 overflow-auto">
      <div className="px-6 py-2 border-b">
        <div className="flex justify-between items-center">
          {/* <h1 className="text-xl font-semibold">Functional Assessment Review</h1> */}
        </div>
        {isLoading ? (
          <Banner message="Functional Assessment is loading..." className="my-2" />
        ) : (
          <Banner
            message="We are currently in the Functional Assessment phase of the PR Readiness Assessment."
            className="my-2"
          />
        )}
      </div>
      <div className="px-6 py-4">
        <AssessmentSectionTable
          name="Functional Assessment"
          isLoading={false}
          isAssessmentResultsEnabled={false}
          row={{
            type: 'Functional Assessment',
            status: prAnalysis?.functional_assessment?.metRequirements ? 'PASS' : 'FAIL',
            score: `${prAnalysis?.functional_assessment?.overallProgress ?? 0}%`,
            details:
              prAnalysis?.functional_assessment?.overallConclusion ??
              `${prAnalysis?.functional_assessment?.conclusion?.completedFeatures ?? ''}
           ${prAnalysis?.functional_assessment?.conclusion?.incompleteFeatures ?? ''}`,
            assessmentResult: prAnalysis?.functional_assessment?.userStories?.length ?? 0,

            assessmentUpdates: 0,
          }}
        />
      </div>

      {renderFunctionalAssessment()}
    </div>
  );
};
export default FunctionalAssessment;
