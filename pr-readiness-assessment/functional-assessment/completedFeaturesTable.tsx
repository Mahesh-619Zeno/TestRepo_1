import React from 'react';
import { IUserStoryFeature } from '../../../../types/pull-request-report.types';

interface CompletedComponentsTableProps {
  features: IUserStoryFeature[];
}

const CompletedComponentsTable: React.FC<CompletedComponentsTableProps> = ({ features }) => {
  const completedData = features
    ?.map((feature) => {
      const completedSubFeatures =
        feature?.subFeatures?.filter(
          (subFeature) => subFeature && subFeature.status === 'Completed',
        ) ?? [];

      if (feature.status === 'Completed' || completedSubFeatures.length > 0) {
        return { ...feature, subFeatures: completedSubFeatures };
      }
      return null;
    })
    .filter((feature): feature is IUserStoryFeature => feature !== null);

  if (completedData?.length === 0) {
    return <p className="py-4 text-center  italic">No complete components found.</p>;
  }

  return (
    <div className="my-4 w-full">
      <h4 className="mb-4  font-semibold">Completed Components</h4>

      <div className="overflow-hidden rounded-lg border shadow-sm">
        <table className="min-w-full border-collapse ">
          <thead className="bg-card">
            <tr className="border-b ">
              <th className="px-3 py-2 text-left font-semibold ">ID</th>
              <th className="px-3 py-2 text-left font-semibold ">Feature</th>
              <th className="px-3 py-2 text-left font-semibold ">Summary</th>
            </tr>
          </thead>

          <tbody>
            {completedData?.map((feature, index: number) => (
              <React.Fragment key={feature?.id || index}>
                {/* Parent Feature */}
                {feature?.status === 'Completed' && (
                  <tr className="border-b text-base">
                    <td className="px-3 py-3 ">{feature?.id ?? ''}</td>
                    <td className="px-3 py-3 ">{feature?.name ?? ''}</td>
                    <td className="px-3 py-3 ">
                      <p className="">{feature?.details ?? ''}</p>
                    </td>
                  </tr>
                )}

                {/* Sub-features */}
                {feature?.subFeatures?.map((subFeature, subIndex: number) => (
                  <tr key={subFeature.id ?? `subFeature-${subIndex}`} className="border-b text-base">
                    <td className="px-3 py-3 ">{subFeature?.id ?? ''}</td>
                    <td className="px-3 py-3 ">{subFeature?.name ?? ''}</td>
                    <td className="px-3 py-3 ">
                      <p className="">{subFeature?.details ?? ''}</p>
                    </td>
                  </tr>
                ))}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CompletedComponentsTable;
