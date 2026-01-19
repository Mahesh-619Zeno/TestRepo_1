import { ChevronRight } from 'lucide-react';
import StreamlineBrain from '@/app/components/icons/StreamlineBrain';
import { useState } from 'react';

import {
  IAdaptedIntrospectionCitation,
  IAdaptedReasons,
} from '../../../types/pull-request-report.types';
import ReasonWithButton from './ReasonWithButton';

export type TCognitiveDecisioning = {
  confidence?: string | number;
  citationImage?: string;
  citationTitle?: string;
  citationUrl?: string;
  citation?: IAdaptedIntrospectionCitation;
  gap: string;
  reasons?: IAdaptedReasons[];
  violationSection: 'devops' | 'CS' | 'TQA';
};

// COGNITIVE DECISIONING
const CognitiveDecisioning = ({
  citation,
  gap,
  reasons,
  violationSection,
}: TCognitiveDecisioning) => {
  const [openCitationIndex, setOpenCitationIndex] = useState<number | null>(null);
  // useEffect(() => {
  //   setOpenCitationIndex(null);
  // }, [finding.id]);

  if ((!reasons || reasons.length === 0) && !gap) return null;

  return (
    <details className="group">
      <summary className="flex items-center cursor-pointer gap-2 text-sm font-medium text-muted-foreground hover:text-foreground w-[50px]">
        <span className="px-2 py-1 border rounded-md border-button-background text-primary flex flex-row">
          Source <ChevronRight className="h-4 transition-transform group-open:rotate-90" />
        </span>
      </summary>

      <div className="border rounded-xl bg-background">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 cursor-pointer">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-md bg-primary flex items-center justify-center cursor-default">
              <StreamlineBrain className="w-4 h-4" />
            </div>
            <span className="font-semibold text-foreground">Cognitive Decisioning AI</span>
          </div>

          <div className="flex items-center gap-3">
            {/* <div className="flex items-center gap-1 px-3 py-1 rounded-full border border-emerald-500 text-emerald-500 font-medium">
                    ✨ {confidence}%
                  </div> */}
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex flex-row  ml-5">
            <div className="w-full">
              {reasons && reasons?.length > 0 && (
                <div className="space-y-4">
                  <div className="font-medium">Reason</div>
                  {reasons?.map((reason: any, index: number) => {
                    const isOpen = openCitationIndex === index;

                    return (
                      <div key={reason.id ?? index} className="ml-3">
                        {/* Reason text */}
                        <div className="text-muted whitespace-pre-line mr-4">
                          {index + 1}.{' '}
                          <ReasonWithButton
                            key={index}
                            text={reason?.reason}
                            index={index}
                            reason={reason}
                            citation={citation}
                            isOpen={isOpen}
                            openCitationIndex={openCitationIndex}
                            setOpenCitationIndex={setOpenCitationIndex}
                            reasons={reasons}
                            violationSection={violationSection}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          <div className="border-[0.5px]" />

          {gap ? (
            <div className=" ml-5">
              <div className="font-medium mb-1">Gap Identified</div>
              <div className="text-muted whitespace-pre-line ml-3 mb-3">{gap}</div>
            </div>
          ) : (
            <div className=" ml-5">
              <div className="font-medium mb-1">Gap Identified</div>
              <div className="text-muted whitespace-pre-line ml-3 mb-3">
                1. No gap is identified.
              </div>
            </div>
          )}
        </div>
      </div>
    </details>
  );
};

export default CognitiveDecisioning;
