import { cn } from '@/lib/utils';
import { Loader } from 'lucide-react';
import { StatusIcon, StatusPill } from './pr-readiness-main/PRReadinessAssessmentTable';
// import { StatusPill } from './statusPill';

/* ---------------- Types ---------------- */

export type Status = 'PASS' | 'FAIL';

export interface TableRowData {
  type: string;
  status: Status;
  score?: string;
  details: string;
  assessmentResult: number;
  assessmentUpdates?: number;
}

interface SkeletonRowProps {
  name: string;
  isAssessmentResultsEnabled: boolean;
}

interface TableRowProps extends TableRowData {
  isAssessmentResultsEnabled: boolean;
}

interface PRReadinessAssessmentTableProps {
  row?: TableRowData;
  isLoading: boolean;
  name: string;
  isAssessmentResultsEnabled: boolean;
}

/* ---------------- Skeleton Row ---------------- */

const SkeletonRow = ({ name, isAssessmentResultsEnabled }: SkeletonRowProps) => {
  return (
    <tr className="border-b border-border last:border-none animate-pulse">
      <td className="px-4 py-4">
        <div className="flex items-center gap-2 text-sm">
          <Loader size={14} className="animate-spin text-progressBar-background" />
          <span>{name}</span>
        </div>
      </td>

      <td className="px-4 py-4">
        <div className="h-4 w-16 rounded bg-muted" />
      </td>

      <td className="px-4 py-4">
        <div className="h-4 w-12 rounded bg-muted" />
      </td>

      <td className="px-4 py-4">
        <div className="h-4 w-full rounded bg-muted" />
      </td>

      <td className="px-4 py-4">
        <div className="h-4 w-20 rounded bg-muted" />
      </td>

      {isAssessmentResultsEnabled && (
        <td className="px-4 py-4">
          <div className="h-4 w-20 rounded bg-muted" />
        </td>
      )}
    </tr>
  );
};

/* ---------------- Data Row ---------------- */

const TableRow = ({
  type,
  status,
  score = '-',
  details,
  assessmentResult,
  assessmentUpdates = 0,
  isAssessmentResultsEnabled,
}: TableRowProps) => {
  return (
    <tr className="border-b border-border last:border-none">
      {/* Type */}
      <td className="px-4 py-4">
        <div className="flex items-center gap-2 text-sm">
          <StatusIcon status={status} />
          <span>{type}</span>
        </div>
      </td>

      {/* Status */}
      <td className="px-4 py-4">
        <StatusPill status={status} />
      </td>

      {/* Score */}
      <td className="px-4 py-4 text-sm">{score}</td>

      {/* Details */}
      <td className="px-4 py-4 text-xs text-foreground/80 leading-relaxed">{details}</td>

      {/* Assessment Results */}
      <td className="px-4 py-4 text-xs font-semibold">
        <span className={cn(status === 'PASS' ? 'text-accent-foreground' : 'text-destructive')}>
          {type === 'Functional Assessment'
            ? `${assessmentResult} Stories`
            : `${assessmentResult - assessmentUpdates} Violations`}
        </span>
      </td>

      {/* Assessment Updates (conditional) */}
      {isAssessmentResultsEnabled && (
        <td className="px-4 py-4 text-xs font-semibold">
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
    </tr>
  );
};

/* ---------------- Main Table ---------------- */

const AssessmentSectionTable = ({
  row,
  isLoading,
  name,
  isAssessmentResultsEnabled,
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
          </tr>
        </thead>

        <tbody>
          {isLoading ? (
            <SkeletonRow name={name} isAssessmentResultsEnabled={isAssessmentResultsEnabled} />
          ) : row ? (
            <TableRow {...row} isAssessmentResultsEnabled={isAssessmentResultsEnabled} />
          ) : null}
        </tbody>
      </table>
    </div>
  );
};

export default AssessmentSectionTable;
