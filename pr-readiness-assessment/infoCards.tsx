import React from 'react';

interface InfoCardProps {
  title: string;
  value: React.ReactNode;
  valueColor?: string;
}

const InfoCard: React.FC<InfoCardProps> = ({ title, value, valueColor = 'text-gray-900' }) => {
  return (
    <div className="flex h-full w-full flex-1 flex-col gap-7 rounded-md border bg-card px-4 py-2">
      {/* Title */}
      <div className="flex items-center justify-between">
        <span className="font-semibold uppercase tracking-wide">{title}</span>
      </div>

      {/* Value */}
      <div className={`font-medium ${valueColor}`}>{value}</div>
    </div>
  );
};

export default InfoCard;
