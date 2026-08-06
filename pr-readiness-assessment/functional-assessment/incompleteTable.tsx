import React from 'react';

import InfoAccordion from './infoAccordion';
import { IUserStoryFeature } from '../../../../types/pull-request-report.types';
import { cn } from '@/lib/utils';

interface IncompleteComponentsTableProps {
  features: IUserStoryFeature[];
}

/**
 * Tailwind-only priority styles
 */
const priorityStyles: Record<string, { label: string; classes: string }> = {
  Low: {
    label: 'Low',
    classes: 'bg-green-50 text-green-700 border-green-300',
  },
  Medium: {
    label: 'Medium',
    classes: 'bg-yellow-50 text-yellow-700 border-yellow-300',
  },
  High: {
    label: 'High',
    classes: 'bg-red-50 text-red-700 border-red-300',
  },
};

const IncompleteComponentsTable: React.FC<IncompleteComponentsTableProps> = ({ features }) => {
  const incompleteData = features
    ?.map((feature) => {
      const incompleteSubFeatures =
        feature?.subFeatures?.filter((sub) => sub && sub?.status !== 'Completed') ?? [];

      if (feature?.status !== 'Completed' || incompleteSubFeatures.length > 0) {
        return { ...feature, subFeatures: incompleteSubFeatures };
      }
      return null;
    })
    .filter((feature): feature is IUserStoryFeature => feature !== null);

  if (incompleteData?.length === 0) {
    return <p className="py-4 text-center  italic">No gaps and issues found.</p>;
  }

  return (
    <InfoAccordion title="Gaps & Issues">
      <div className="my-2 w-full">
        <div className="overflow-hidden rounded-lg border shadow-sm">
          <table className="min-w-full border-collapse ">
            <thead className="bg-card">
              <tr className="border-b">
                <th className="px-3 py-2 text-left font-semibold">ID</th>
                <th className="px-3 py-2 text-left font-semibold">Feature</th>
                <th className="px-3 py-2 text-left font-semibold">Summary</th>
                <th className="px-3 py-2 text-center font-semibold">Priority</th>
              </tr>
            </thead>

            <tbody>
              {incompleteData?.map((feature) => (
                <React.Fragment key={feature?.id}>
                  {/* Parent Feature */}
                  <tr className="border-b">
                    <td className="px-3 py-3">{feature?.id ?? 'N/A'}</td>
                    <td className="px-3 py-3">{feature?.name ?? 'N/A'}</td>
                    <td className="px-3 py-3">
                      <p className="">{feature?.details}</p>
                    </td>
                    <td className="px-3 py-3 text-center">
                      <span
                        className={cn(
                          'inline-flex rounded-full border px-2 py-1 font-medium text-sm',
                          priorityStyles[feature?.priority ?? 'Low']?.classes,
                        )}
                      >
                        {priorityStyles[feature?.priority ?? 'Low']?.label}
                      </span>
                    </td>
                  </tr>

                  {/* Sub-features */}
                  {feature?.subFeatures?.map((sub, index) => (
                    // <tr key={sub?.id ?? index} className="border-b">
                    <tr key={sub?.id ?? `sub-${feature?.id}-${index}`} className="border-b">
                      <td className="px-3 py-3">{sub?.id ?? 'N/A'}</td>
                      <td className="px-3 py-3">{sub?.name ?? 'N/A'}</td>
                      <td className="px-3 py-3">
                        <p className="">{sub?.details}</p>
                      </td>
                      <td className="px-3 py-3 text-center">
                        <span
                          className={cn(
                            'inline-flex rounded-full border px-2 py-1 font-medium text-sm',
                            priorityStyles[sub?.priority ?? 'Low']?.classes,
                          )}
                        >
                          {priorityStyles[sub?.priority ?? 'Low']?.label}
                        </span>
                      </td>
                    </tr>
                  ))}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </InfoAccordion>
  );
};

export default IncompleteComponentsTable;
