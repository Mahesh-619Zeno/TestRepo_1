import React, { useEffect, useRef, useState } from 'react';
import { TCognitiveDecisioning } from './CognitiveDecisioning';
import {
  ChevronDown,
  ChevronRight,
  ChevronUp,
  Maximize,
  Sparkle,
  Sparkles,
  SquareArrowOutUpRight,
} from 'lucide-react';
import PrGenieMarkdown from '../../ecg-view/components/pr-genie/PrGenieMarkdown';
import ImageFullScreenView from './ImageFullScreenView';
import { IAdaptedReasons } from '../../../types/pull-request-report.types';

type ReasonWithButtonProps = {
  text: string;
  index: number;
  isOpen: boolean;
  reason: any;
  citation: TCognitiveDecisioning['citation'];
  openCitationIndex: number | null;
  setOpenCitationIndex: React.Dispatch<React.SetStateAction<number | null>>;
  reasons: IAdaptedReasons[];
  violationSection: 'devops' | 'CS' | 'TQA';
};

interface IImageCitation {
  citationImage: string;
  citationTitle: string;
  citationUrl: string;
  reason?: string;
}

const ImageCitation = ({ citationImage, citationUrl }: IImageCitation) => {
  const [isImageView, setIsImageView] = useState(false);
  return (
    <>
      <div className="flex flex-col">
        {/* IMAGE  */}
        <div className="p-4 flex items-center justify-center">
          <div className="relative">
            <img src={citationImage} alt="Citation" className="rounded-lg border max-h-[260px]" />

            <button
              onClick={(e) => {
                e.stopPropagation();
                setIsImageView(true);
              }}
              className="absolute bottom-3 right-3 flex items-center gap-1 px-2 py-1 text-sm font-medium"
            >
              {/* View */}
              <Maximize className="h-4 w-4 bg-gray-700 p-2 text-white rounded" />
            </button>
          </div>
        </div>
        {citationUrl && (
          <div className="flex justify-end">
            <span className="ml-4 bg-blue-600/20 w-fit inline-flex px-2 py-1 rounded">
              <a
                href={citationUrl}
                target="_blank"
                rel="noreferrer"
                className="text-primary flex items-center gap-1 font-medium"
              >
                Visit Source
                <SquareArrowOutUpRight className="h-5 w-5" />
              </a>
            </span>
          </div>
        )}
      </div>
      {/* IMAGE MODAL / WEB VIEW (optional hook) */}
      {isImageView && (
        <ImageFullScreenView src={citationImage} onClose={() => setIsImageView(false)} />
      )}
    </>
  );
};

const ReasonWithButton: React.FC<ReasonWithButtonProps> = ({
  text,
  index,
  isOpen,
  reason,
  citation,
  openCitationIndex,
  setOpenCitationIndex,
  violationSection,
  reasons,
}) => {
  const anchorRegex = /<a>(.*?)<\/a>/g;
  const parts = text?.split(anchorRegex);
  const item = openCitationIndex !== null && citation?.insiderKnowledge?.[openCitationIndex];
  const markdownContainerRef = useRef<HTMLDivElement | null>(null);
  const [highlights, setHighlights] = useState<HTMLElement[]>([]);
  const [activeIndex, setActiveIndex] = useState(0);

  const content = item
    ? `**Topic**: ${item?.topic}<br>**Rule Description:** ${item?.ruleDescription}`
    : violationSection === 'CS'
    ? reason?.citationMarkdown
    : `<h2 align="center">AI Summary</h2> ${reason?.citationMarkdown}`;

  const markdownSource = content?.trim()?.length ? content : reason?.citationMarkdown;

  useEffect(() => {
    if (!isOpen) return;
    if (openCitationIndex === null) return;
    if (!markdownContainerRef.current) return;

    const nodes = Array.from(
      markdownContainerRef.current.querySelectorAll<HTMLElement>('span[id^="highlighted"]'),
    );

    setHighlights(nodes);
    setActiveIndex(0);
  }, [markdownSource, isOpen, openCitationIndex]);

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

  const hasImageCitation = !!reason?.citation_highlighted_url && !!reason?.citation_screenshot_url;

  // const hasIntrospectionContent = !!content?.trim();

  // const showIntrospection = !hasImageCitation && hasIntrospectionContent;
  // const showCitationMarkdown = !hasImageCitation && !hasIntrospectionContent;
  // const showHeaderButtons = showIntrospection;

  return parts?.map((part, i) => {
    // Even index → normal text
    if (i % 2 === 0) {
      return <span key={i}>{part}</span>;
    }

    // Odd index → text inside <a>...</a>
    return (
      <React.Fragment key={i}>
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
                {!hasImageCitation && (
                  <div className="flex items-center justify-end gap-1 border rounded px-2 py-1">
                    <button
                      onClick={goPrev}
                      disabled={activeIndex === 0}
                      className="p-1 disabled:opacity-50"
                    >
                      <ChevronUp size={14} />
                    </button>

                    <span className="text-xs px-1">
                      {activeIndex + 1} / {highlights?.length}
                    </span>

                    {/* Next arrow */}
                    <button
                      onClick={goNext}
                      disabled={activeIndex === highlights?.length - 1}
                      className="p-1 disabled:opacity-50"
                    >
                      <ChevronDown size={14} />
                    </button>
                  </div>
                )}
                <div className="flex items-center gap-1 px-3 py-1 rounded-full border border-emerald-500 text-emerald-500 font-medium">
                  <Sparkles size={14} /> {reasons[openCitationIndex]?.relevanceScore}%
                </div>
              </div>
            </div>

            {/* Scrollable markdown */}
            {hasImageCitation ? (
              <ImageCitation
                key={index}
                citationImage={reason?.citation_screenshot_url}
                citationTitle={reason?.citation_title}
                citationUrl={reason?.citation_highlighted_url}
                reason={reason?.reason}
              />
            ) : (
              <div className="px-2 py-3 max-h-48 overflow-y-auto">
                <div ref={markdownContainerRef} className="relative rounded-md p-4">
                  <PrGenieMarkdown
                    listStyleType="lower-alpha"
                    className="prose dark:prose-invert"
                    content={markdownSource}
                  />
                </div>
              </div>
            )}

            {/* Footer / Visit link */}
            {reasons[openCitationIndex]?.whereIthHasLearnedFrom && (
              <div className="px-4 py-2 border-t text-sm flex justify-end">
                <span className="">
                  Learned From {reasons[openCitationIndex]?.whereIthHasLearnedFrom}
                </span>
              </div>
            )}
          </div>
        )}
      </React.Fragment>
    );
  });
};

export default ReasonWithButton;
