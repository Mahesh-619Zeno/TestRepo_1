import { cn } from '@/lib/utils';
import { ChevronRight } from 'lucide-react';

interface AccordionProps {
  title: string;
  count?: number;
  isOpen: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}

const getSeverityColor = (title: string): string => {
  const lowerTitle = title.toLowerCase();
  if (lowerTitle === 'critical') return 'text-red-500';
  if (lowerTitle === 'warning') return 'text-orange-500';
  if (lowerTitle === 'jas') return 'text-blue-500';
  return 'text-gray-400';
};

const Accordion = ({ title, count, isOpen, onToggle, children }: AccordionProps) => {
  return (
    <div className="w-full border rounded-xl bg-editor-background">
      {/* Header */}
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={isOpen}
        className={cn(
          'w-full flex items-center justify-between px-4 py-3',
          'text-left font-medium',
          'hover:bg-muted/40 transition-colors rounded-t-lg',
          isOpen ? 'border-b' : 'rounded-b-lg',
        )}
      >
        <span className={getSeverityColor(title)}>
          {title}
          {count !== undefined && (
            <span className={cn('text-muted ml-1', getSeverityColor(title))}>({count})</span>
          )}
        </span>

        <ChevronRight
          className={cn(
            'h-4 w-4 shrink-0 transition-transform duration-200',
            isOpen && 'rotate-90',
          )}
        />
      </button>

      {/* Content */}
      <div className={cn('transition-all duration-200 ease-out', isOpen ? 'block' : 'hidden')}>
        <div className="px-4 py-3 space-y-3">{children}</div>
      </div>
    </div>
  );
};

export default Accordion;
