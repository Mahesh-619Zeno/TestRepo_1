import { ChevronDown, ChevronRight, ChevronUp, Sparkle, Sparkles } from 'lucide-react';
import StreamlineBrain from '@/app/components/icons/StreamlineBrain';
import { useEffect, useRef, useState } from 'react';
import PrGenieMarkdown from '../../ecg-view/components/pr-genie/PrGenieMarkdown';
import { IReAssessResultReason } from '@/app/types/pull-request.types';

type TCognitiveDecisioning = {
  confidence_score?: number;
  gap: string;
  reasons: IReAssessResultReason[];
};

type ReasonWithCitationProps = {
  text: string;
  index: number;
  isOpen: boolean;
  reasons: IReAssessResultReason[];
  openCitationIndex: number | null;
  setOpenCitationIndex: React.Dispatch<React.SetStateAction<number | null>>;
};

const ReasonWithCitation = ({
  text,
  index,
  isOpen,
  reasons,
  openCitationIndex,
  setOpenCitationIndex,
}: ReasonWithCitationProps) => {
  const anchorRegex = /<a>(.*?)<\/a>/g;
  const parts = text.split(anchorRegex);
  const item = openCitationIndex !== null && reasons[openCitationIndex];
  const markdownContainerRef = useRef<HTMLDivElement | null>(null);
  const [highlights, setHighlights] = useState<HTMLElement[]>([]);
  const [activeIndex, setActiveIndex] = useState(0);

  const content = item
    ? `**Topic**: ${item.topic}<br>**Rule Description:** ${item.ruleDescription}`
    : '';

  useEffect(() => {
    if (!markdownContainerRef.current) return;

    const nodes = Array.from(
      markdownContainerRef.current.querySelectorAll<HTMLElement>('span[id^="highlighted"]'),
    );

    setHighlights(nodes);
    setActiveIndex(0);
  }, [content]);

  useEffect(() => {
    const el = highlights[activeIndex];
    if (!el) return;

    el.scrollIntoView({
      behavior: 'smooth',
      block: 'center',
    });
  }, [activeIndex, highlights]);

  const goNext = () => {
    setActiveIndex((prev) => Math.min(prev + 1, highlights.length - 1));
  };

  const goPrev = () => {
    setActiveIndex((prev) => Math.max(prev - 1, 0));
  };

  return parts.map((part, i) => {
    // Even index → normal text
    if (i % 2 === 0) {
      return <span key={i}>{part}</span>;
    }

    return (
      <>
        <button
          key={i}
          onClick={() => setOpenCitationIndex((prev) => (prev === index ? null : index))}
          className="ml-1 text-sm text-accent-foreground hover:underline inline-flex items-center gap-1"
        >
          <Sparkle size={14} />
          {part}
          <span className="text-xs">
            {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </span>
        </button>
        {openCitationIndex !== null && isOpen && reasons?.[openCitationIndex] && (
          <div className="w-full mt-2 rounded-lg border bg-card shadow-sm flex flex-col">
            {/* Header */}
            <div className="px-4 py-2 border-b font-medium text-sm flex justify-between items-center gap-2">
              <span className="font-semibold">{'Source: GPT - Gemini 2.5 pro > ' + part}</span>
              <div className="flex flex-row gap-2">
                <div className="flex items-center justify-end gap-1 border rounded px-2 py-1">
                  <button
                    onClick={goPrev}
                    disabled={activeIndex === 0}
                    className="p-1 disabled:opacity-50"
                  >
                    <ChevronUp size={14} />
                  </button>

                  <span className="text-xs px-1">
                    {activeIndex + 1} / {highlights.length}
                  </span>

                  {/* Next arrow */}
                  <button
                    onClick={goNext}
                    disabled={activeIndex === highlights.length - 1}
                    className="p-1 disabled:opacity-50"
                  >
                    <ChevronDown size={14} />
                  </button>
                </div>

                <div className="flex items-center gap-1 px-3 py-1 rounded-full border border-emerald-500 text-emerald-500 font-medium">
                  <Sparkles size={14} /> {reasons[openCitationIndex].relevanceScore}%
                </div>
              </div>
            </div>

            <div className="px-2 py-3 max-h-48 overflow-y-auto">
              <div ref={markdownContainerRef} className="relative rounded-md p-4">
                <PrGenieMarkdown
                  listStyleType="lower-alpha"
                  className="prose dark:prose-invert"
                  content={content}
                />
              </div>
            </div>

            {/* Footer / Visit link */}
            {reasons[openCitationIndex].whereIthHasLearnedFrom && (
              <div className="px-4 py-2 border-t text-sm flex justify-end">
                <span className="">
                  Learned From {reasons[openCitationIndex].whereIthHasLearnedFrom}
                </span>
              </div>
            )}
          </div>
        )}
      </>
    );
  });
};

// COGNITIVE DECISIONING
const CognitiveDecisioning = ({ gap, reasons, confidence_score }: TCognitiveDecisioning) => {
  const [openCitationIndex, setOpenCitationIndex] = useState<number | null>(null);
  // useEffect(() => {
  //   setOpenCitationIndex(null);
  // }, [finding.id]);

  if (!reasons && !gap) return null;
  //  {(finding?.reasons?.length || finding?.gap) && (

  return (
    <details className="group">
      <summary className="flex items-center cursor-pointer gap-2 text-sm font-medium text-muted-foreground hover:text-foreground w-[50px]">
        <span className="px-2 py-1 border rounded-md border-button-background text-accent-foreground flex flex-row">
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

        <div className="space-y-3 ml-5">
          <div className="flex flex-row">
            <div className="w-full">
              {reasons?.length > 0 && (
                <div className="space-y-4">
                  <div className="font-medium">Reason</div>
                  {reasons?.map((reason: IReAssessResultReason, index: number) => {
                    const isOpen = openCitationIndex === index;

                    return (
                      <div key={index} className="ml-3">
                        {/* Reason text */}
                        <div className="text-muted whitespace-pre-line mr-4">
                          {index + 1}.{' '}
                          <ReasonWithCitation
                            text={reason.reason}
                            index={index}
                            isOpen={isOpen}
                            reasons={reasons}
                            openCitationIndex={openCitationIndex}
                            setOpenCitationIndex={setOpenCitationIndex}
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

          <div>
            <div className="font-medium mb-1">Gap Identified</div>
            <div className="text-muted whitespace-pre-line ml-3 mb-3">
              {gap ? gap : 'No Gap Identified'}
            </div>
          </div>
        </div>
      </div>
    </details>
  );
};

export default CognitiveDecisioning;
