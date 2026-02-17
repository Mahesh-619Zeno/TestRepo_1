import { cn } from '@/app/lib/utils';
import { CheckCircle2, Loader, Mail, XCircle } from 'lucide-react';
import { AssessmentRowData, Status } from './PRReadinessAssessment';
import { useMutation } from '@tanstack/react-query';
import usePullRequestKeyValueStore from '@/app/store/usePullRequestKeyValueStore';
import { postEmailNotifications, showToast } from '@/app/services/editor';
import Button from '@/app/components/button';

interface TableRowItem {
  key: string;
  isLoading: boolean;
  name: string;
  id: string;
  row?: AssessmentRowData;
}

interface TableRowProps extends AssessmentRowData {
  handleSubStepClick: (index: number) => void;
  isAssessmentResultsEnabled: boolean;
  maxSubStepReached:number
}

interface PRReadinessAssessmentTableProps {
  rows: TableRowItem[];
  handleSubStepClick: (index: number) => void;
  isAssessmentResultsEnabled: boolean;
  maxSubStepReached:number
}
const successMessages: Record<string, string> = {
  functional_assessment:
    'We will notify you via email once the Functional Assessment is completed.',
  devops_assessment: 'We will notify you via email once the DevOps Assessment is completed.',
  technical_quality_assessment:
    'We will notify you via email once the Technical Quality Assessment is completed.',
  coding_standards_assessment:
    'We will notify you via email once the Coding Standards Assessment is completed.',
};

const SkeletonRow = ({
  name,
  id,
  isAssessmentResultsEnabled,
}: {
  name: string;
  id: string;
  isAssessmentResultsEnabled: boolean;
}) => {
  const pullRequestStateData = usePullRequestKeyValueStore((store) => store.pullRequestStoreData);
  const chatSession = pullRequestStateData.sessionId ?? '';
  const { mutate: mutateSendNotifications } = useMutation({
    mutationFn: postEmailNotifications as (params: any) => Promise<any>,
    onSuccess: (data) => {
      const message = successMessages[data?.assessment_type];

      if (message) {
        showToast({ message, type: 'success' });
      }
    },
    onError: (err) => {
      console.error(err);
    },
  });

  const handleMailClick = (e: React.MouseEvent, id: string) => {
    if (!id) return;
    mutateSendNotifications({
      session_id: chatSession,
      assessment_type: [id],
    });
  };

  return (
    <tr className="border-b border-border last:border-none">
      <td className="px-4 py-4">
        <div className="flex items-center gap-2 text-sm text-foreground">
          <Loader
            size={14}
            style={{ animationDuration: '5s' }}
            className={cn('animate-spin', 'text-progressBar-background')}
          />
          <span>{name}</span>
        </div>
      </td>

      <td className="px-4 py-4">
        <div className="h-4 w-16 rounded bg-muted animate-pulse" />
      </td>

      <td className="px-4 py-4">
        <div className="h-4 w-12 rounded bg-muted animate-pulse" />
      </td>

      <td className="px-4 py-4">
        <div className="h-4 w-full rounded bg-muted animate-pulse" />
      </td>

      <td className="px-4 py-4">
        <div className="h-4 w-20 rounded bg-muted animate-pulse" />
      </td>

      {isAssessmentResultsEnabled ? (
        <td className="px-4 py-4">
          <div className="h-4 w-20 rounded bg-muted animate-pulse" />
        </td>
      ) : null}

      <td className="px-4 py-4">
        <button
          onClick={(e) => handleMailClick(e, id)}
          className="text-xs px-3 py-1 rounded-md bg-button-background text-button-foreground hover:opacity-90 transition"
        >
          <Mail />
        </button>
      </td>
    </tr>
  );
};

export const StatusPill = ({ status }: { status: Status }) => {
  const isPass = status === 'PASS';

  return (
    <span
      className={cn(
        'px-3 py-1 rounded-full text-xs font-semibold border',
        isPass
          ? 'bg-emerald-500/20 text-emerald-500 border-emerald-500/40'
          : 'bg-destructive/20 text-destructive border-destructive/40',
      )}
    >
      {status}
    </span>
  );
};

export const StatusIcon = ({ status }: { status: Status }) =>
  status === 'PASS' ? (
    <CheckCircle2 className="w-5 h-5 text-emerald-500" />
  ) : (
    <XCircle className="w-5 h-5 text-destructive" />
  );

const TableRow = ({
  type,
  status,
  score = '-',
  details,
  assessmentResult,
  subStepId,
  assessmentUpdates,
  isAssessmentResultsEnabled,
  handleSubStepClick,
  maxSubStepReached
}: TableRowProps) => {
  return (
    <tr className="border-b border-border last:border-none">
      {/* Type */}
      <td className="px-4 py-4">
        <div className="flex items-center gap-2 text-sm text-foreground">
          <StatusIcon status={status} />
          <span>{type}</span>
        </div>
      </td>

      {/* Status */}
      <td className="px-4 py-4">
        <StatusPill status={status} />
      </td>

      {/* Score */}
      <td className="px-4 py-4 text-sm text-foreground">{score}</td>

      {/* Details */}
      <td className="px-4 py-4 text-xs text-foreground/80 leading-relaxed">{details}</td>

      {/* Assessment Results */}
      <td className="px-4 py-4 text-xs">
        <span
          className={cn(
            'font-semibold',
            status === 'PASS' ? 'text-accent-foreground' : 'text-destructive',
          )}
        >
          {type === 'Functional Assessment'
            ? `${assessmentResult} Stories`
            : `${assessmentResult - assessmentUpdates} Violations`}
        </span>
      </td>

      {/* Assessment Updates */}
      {isAssessmentResultsEnabled && (
        <td className="px-4 py-4 text-xs">
          <span
            className={cn(
              'font-semibold',
              assessmentUpdates > 0 ? 'text-emerald-500' : 'text-accent-foreground',
            )}
          >
            {assessmentUpdates}
            {type === 'Functional Assessment' ? `` : ` Resolved`}
          </span>
        </td>
      )}

      {/* Actions */}
      <td className="px-4 py-4">
        <Button
          onClick={() => handleSubStepClick(subStepId)}
          disabled={subStepId>=maxSubStepReached}
          className="text-xs px-3 py-1 rounded-md bg-button-background text-button-foreground hover:opacity-90 transition"
        >
          View
        </Button>
      </td>
    </tr>
  );
};

/* ---------------- Main Table ---------------- */

const PRReadinessAssessmentTable = ({
  rows,
  handleSubStepClick,
  isAssessmentResultsEnabled,
  maxSubStepReached
}: PRReadinessAssessmentTableProps) => {
  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <table className="w-full table-fixed">
        <thead className="bg-button-secondary-background">
          <tr className="text-xs">
            <th className="px-4 py-3 text-left w-[22%]">Type</th>
            <th className="px-4 py-3 text-left w-[8%]">Status</th>
            <th className="px-4 py-3 text-left w-[8%]">Score</th>
            <th className="px-4 py-3 text-left w-[42%]">Details</th>
            <th className="px-4 py-3 text-left w-[12%]">Assessment Results</th>
            {isAssessmentResultsEnabled && (
              <th className="px-4 py-3 text-left w-[12%]">Assessment Updates</th>
            )}
            <th className="px-4 py-3 text-left w-[8%]">Actions</th>
          </tr>
        </thead>

        <tbody>
          {rows.map(({ key, isLoading, name, id, row }) =>
            isLoading ? (
              <SkeletonRow
                key={key}
                name={name}
                id={id}
                isAssessmentResultsEnabled={isAssessmentResultsEnabled}
              />
            ) : row ? (
              <TableRow
                key={key}
                isAssessmentResultsEnabled={isAssessmentResultsEnabled}
                handleSubStepClick={handleSubStepClick}
                maxSubStepReached={maxSubStepReached}
                {...row}
              />
            ) : null,
          )}
        </tbody>
      </table>
    </div>
  );
};

export default PRReadinessAssessmentTable;
