import CustomTooltip from '@/app/components/atoms/CustomTooltip';
import { cn } from '@/lib/utils';

interface IStatusPillProps {
  status: string;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  toolTipContent?: string;
  placement?: 'top' | 'bottom' | 'left' | 'right';
}

export function StatusPill({
  status,
  className,
  size = 'sm',
  toolTipContent = 'AI confidence status',
  placement = 'top',
}: IStatusPillProps) {
  const statusStyles: Record<string, string> = {
    Critical: 'bg-red-100 text-red-700 border-red-300',
    Warning: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    Jas: 'bg-blue-100 text-blue-700 border-blue-300',
  };

  const statusLabels: Record<string, string> = {
    Critical: 'Critical',
    Warning: 'Warning',
    Jas: 'JAS',
  };

  const getSizes = (size: 'sm' | 'md' | 'lg') => {
    switch (size) {
      case 'lg':
        return 'px-4 py-2 text-base';
      case 'md':
        return 'px-3 py-1.5 text-sm';
      default:
        return 'px-2 py-1 text-xs';
    }
  };

  return (
    <CustomTooltip content={toolTipContent} placement={placement} withArrow>
      <div
        className={cn(
          'flex items-center rounded-full border font-medium transition-colors',
          statusStyles[status] || 'bg-gray-100 text-gray-800 border-gray-300',
          getSizes(size),
          className,
        )}
      >
        {statusLabels[status] || status}
      </div>
    </CustomTooltip>
  );
}
