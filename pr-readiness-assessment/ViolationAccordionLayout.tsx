import { useState } from 'react';
import { Loader } from 'lucide-react';
import Accordion from './Accordion';

type AccordionKey = 'summary' | 'critical' | 'warning' | 'jas';

interface ViolationBase {
  id: string;
}

interface AccordionSection<T extends ViolationBase> {
  key: AccordionKey;
  label: string;
  items?: T[];
}

interface ViolationAccordionLayoutProps<T extends ViolationBase> {
  isLoading: boolean;
  summaryView: React.ReactNode;
  critical: T[];
  warning: T[];
  jas: T[];
  renderViolationDetail: (item: T) => React.ReactNode;
}

export function ViolationAccordionLayout<T extends ViolationBase>({
  isLoading,
  summaryView,
  critical,
  warning,
  jas,
  renderViolationDetail,
}: ViolationAccordionLayoutProps<T>) {
  const [openAccordion, setOpenAccordion] = useState<AccordionKey | null>('summary');

  const sections: AccordionSection<T>[] = [
    { key: 'summary', label: 'Summary' },
    { key: 'critical', label: 'Critical', items: critical },
    { key: 'warning', label: 'Warning', items: warning },
    { key: 'jas', label: 'Jas', items: jas },
  ];

  if (isLoading) {
    return (
      <div className="flex justify-center mt-40">
        <Loader size={48} className="animate-spin text-progressBar-background" />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 overflow-y-auto py-4 px-6">
      {sections?.map((section) => {
        const sectionKey = section?.key;
        const isOpen = openAccordion === sectionKey;

        if (section?.items?.length === 0) {
          return null;
        }

        return (
          <Accordion
            key={sectionKey}
            title={section?.label ?? ''}
            count={sectionKey === 'summary' ? undefined : section?.items?.length}
            isOpen={isOpen}
            onToggle={() => setOpenAccordion((prev) => (prev === sectionKey ? null : sectionKey))}
          >
            {/* SUMMARY */}
            {sectionKey === 'summary' && summaryView}

            {/* VIOLATIONS */}
            {section?.items?.map((item, itemIndex) => (
              <div key={item?.id ?? itemIndex}>{renderViolationDetail(item)}</div>
            ))}

            {/* EMPTY STATE */}
            {section?.items?.length === 0 && sectionKey !== 'summary' && (
              <div className="text-sm text-muted text-center py-4">No violations found</div>
            )}
          </Accordion>
        );
      })}
    </div>
  );
}
