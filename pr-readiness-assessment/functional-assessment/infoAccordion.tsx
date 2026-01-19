import { useState } from 'react';

import { ChevronRight } from 'lucide-react';

import { cn } from '@/lib/utils';

export interface IInfoAccordionProps {
  className?: string;
  index?: string;
  classes?: {
    root?: string;
    title?: string;
  };
  title?: React.ReactNode;
  children?: React.ReactNode;
  isPrintMode?: boolean;
  isDefaultOpen?: boolean;
  status?: React.ReactNode;
}

export default function InfoAccordion({
  index,
  classes = {},
  className,
  title,
  children,
  isDefaultOpen = false,
  status,
}: IInfoAccordionProps) {
  const [open, setOpen] = useState(isDefaultOpen || false);
  const renderInfoAccordion = () => {
    return (
      <div className={cn('border bg-card rounded-xl overflow-hidden py-2', className)}>
        <div
          className={cn(
            'flex justify-between items-center px-4 py-2 bg-card w-full',
            open ? ' rounded-t-xl border-b-blue-600' : ' rounded-xl',
          )}
          onClick={() => setOpen(!open)}
        >
          <div className="flex items-center gap-1">
            {/* Main title */}
            <div className="flex items-center gap-2 font-jakarta">
              <span className="font-bold">{index}</span>
              <span className="font-semibold">{title}</span>
               <span className='ml-3'>{status}</span>
            </div>
            {/* Status */}
          </div>
          <div className="flex gap-2 items-center justify-center">
            {/* {status} */}
            <ChevronRight
              className={cn('w-4 h-4 transition-transform duration-300', open ? 'rotate-90' : '')}
            />
          </div>
        </div>

        {open && <div className="px-4 py-3">{children}</div>}
      </div>
    );
  };

  return renderInfoAccordion();
}
