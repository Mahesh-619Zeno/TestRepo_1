import React from 'react';
import { MessageSquareWarning } from 'lucide-react';

import { IFileItem, IUserStoryFeature } from '../../../../types/pull-request-report.types';
import { cn } from '@/lib/utils';

interface IFeaturesTableProps {
  features: IUserStoryFeature[];
}

const statusStyles: Record<string, { label: string; classes: string }> = {
  Completed: {
    label: 'Completed',
    classes: 'bg-green-50 text-green-700 border-green-300',
  },
  'In Progress': {
    label: 'In Progress',
    classes: 'bg-yellow-50 text-yellow-700 border-yellow-300',
  },
  'Not Started': {
    label: 'Not Started',
    classes: 'bg-gray-50 text-gray-600 border-gray-300',
  },
  Incomplete: {
    label: 'Incomplete',
    classes: 'bg-red-50 text-red-700 border-red-300',
  },
};

/**
 * File icon + tooltip (native title)
 */
const getFileIcon = (file: IFileItem) => {
  const fullPath = file?.name || '';
  const fileName = fullPath.split('/').pop() || fullPath;

  return (
    <div className="flex max-w-[200px] items-center gap-1">
      {/* <CustomFileIcon name={fileName} /> */}
      <span title={fullPath} className="cursor-help truncate font-mono ">
        {fileName}
      </span>
    </div>
  );
};

const FeaturesTable: React.FC<IFeaturesTableProps> = ({ features }) => {
  return (
    <div className="my-2 flex flex-col gap-6">
      <h4 className=" font-semibold">Implementation Status</h4>

      {features?.map((feature, index: number) => (
        <div
          key={feature?.id ?? `feature-${index}`}
          className="overflow-hidden rounded-lg border bg-card"
        >
          <table className="min-w-full border-collapse ">
            <thead className="bg-card">
              <tr className="border-b">
                <th className="w-[10%] px-3 py-2 text-left font-semibold ">ID</th>
                <th className="w-[30%] px-3 py-2 text-left font-semibold ">File</th>
                <th className="w-[10%] px-3 py-2 text-left font-semibold">Status</th>
                <th className="w-[60%] px-3 py-2 text-left font-semibold ">
                  Feature / Sub-feature
                </th>
              </tr>
            </thead>

            <tbody>
              {/* Main Feature Row */}
              <tr className="border-b text-base">
                <td className="px-3 py-3 ">{feature?.id ?? ''}</td>

                <td className="px-3 py-3">
                  {feature?.files?.length ? (
                    feature?.files?.map((file, idx) => (
                      <div
                        key={`${file?.name}-${idx}`}
                        className="flex items-center gap-1 break-all"
                      >
                        {getFileIcon(file)}
                      </div>
                    ))
                  ) : (
                    <p className="">No Files found</p>
                  )}
                </td>

                <td className="px-3 py-3">
                  <span
                    className={cn(
                      'inline-flex rounded-full border px-2 py-1 font-medium text-sm',
                      statusStyles[feature?.status]?.classes,
                    )}
                  >
                    {statusStyles[feature?.status]?.label ?? ''}
                  </span>
                </td>

                <td className="px-3 py-3">
                  <p className="">{feature?.name ?? ''}</p>
                </td>
              </tr>

              {/* Sub-feature Rows */}
              {feature?.subFeatures?.map((sub, idx) => (
                <tr key={`${sub?.id}-${idx}`} className="border-b text-base">
                  <td className="px-3 py-3">{sub?.id ?? ''}</td>

                  <td className="px-3 py-3">
                    {sub?.files?.length ? (
                      sub?.files?.map((file, idx) => (
                        <div
                          key={`${file?.name}-${idx}`}
                          className="flex items-center gap-1 break-all"
                        >
                          {getFileIcon(file)}
                        </div>
                      ))
                    ) : (
                      <p className=" text-gray-500">No Files found</p>
                    )}
                  </td>

                  <td className="px-3 py-3">
                    <span
                      className={cn(
                        'inline-flex rounded-full border px-2 py-1 font-medium text-sm',
                        statusStyles[sub?.status]?.classes,
                      )}
                    >
                      {statusStyles[sub?.status]?.label ?? ''}
                    </span>
                  </td>

                  <td className="px-3 py-3">
                    <p className="">{sub?.name ?? ''}</p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}

      {/* Info Box */}
      <div className="my-4">
        <div className="w-full rounded border-l-4 border-blue-500 bg-card p-4">
          <div className="mb-1 flex items-center gap-1  font-semibold text-blue-500">
            <MessageSquareWarning size={16} />
            Important
          </div>
          <p className="">
            If there is any change in the file related to the feature or sub-feature, the file name
            will be listed in the table; otherwise, it will not be displayed.
          </p>
        </div>
      </div>
    </div>
  );
};

export default FeaturesTable;
