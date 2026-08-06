import InfoAccordion from './infoAccordion';
import CompletedComponentsTable from './completedFeaturesTable';
import FeaturesTable from './implementationTable';
import IncompleteComponentsTable from './incompleteTable';
import { CircleCheck, CircleX } from 'lucide-react';
import { IUserStory } from '../../../../types/pull-request-report.types';

export interface IUserStoryDetailsProps {
  userStory?: IUserStory;
  index: number;
}

export default function UserStoryDetails({ userStory, index }: IUserStoryDetailsProps) {
  const storyCompletedCount = userStory?.storyCompletedCount ?? 0;
  const storyIncompleteCount = userStory?.storyIncompleteCount ?? 0;
  // const status = `${storyCompletedCount}/${storyIncompleteCount+storyCompletedCount}`;
  const status = (() => {
    const total = storyIncompleteCount + storyCompletedCount;
    const isComplete = storyCompletedCount === total;

    return (
      <span
        className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium
        ${isComplete ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}
      `}
      >
        {isComplete ? <CircleCheck className="h-5" /> : <CircleX className="h-5" />}
        {storyCompletedCount}/{total} Completed
      </span>
    );
  })();

  const renderUserStoryDetails = () => {
    return (
      <InfoAccordion
        index={`1.${index + 1}`}
        title={`User Story ID: ${userStory?.title_id ?? ''} - ${userStory?.title ?? ''}`}
        status={status}
      >
        <h4 className="font-semibold">Feature Completeness</h4>

        <div className="mt-4 flex flex-col gap-2">
          <h5 className=" font-semibold">The Requirement was...</h5>
          <p className="">{userStory?.actualRequirement ?? ''}</p>
        </div>

        <div className="mt-2 flex flex-col gap-2">
          <h5 className="font-semibold">That is what is built...</h5>
          <p className="">{userStory?.whatWasImplemented ?? ''}</p>
        </div>

        <FeaturesTable features={userStory?.features ?? []} />

        <CompletedComponentsTable features={userStory?.features ?? []} />

        <IncompleteComponentsTable features={userStory?.features ?? []} />
      </InfoAccordion>
    );
  };

  return renderUserStoryDetails();
}
