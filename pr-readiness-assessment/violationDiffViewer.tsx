import { DiffViewer } from '../../coding-standards-view/components/diff-viewer';

export interface IViolationDiffViewerProps {
  code: string;
  suggestedCode: string;
  diffViewType?: 'split' | 'unified';
  lineStart: number;
  lineEnd: number;
}

export default function ViolationDiffViewer({
  code,
  suggestedCode,
  diffViewType = 'split',
  lineStart,
  lineEnd,
}: IViolationDiffViewerProps) {
  const handleClickCodeItem = () => {
    //
  };
  const renderViolationLineItem = () => {
    return (
      <>
        <div className="w-full">
          <DiffViewer
            oldContent={code}
            newContent={suggestedCode}
            lineStartOffset={lineStart - 1}
            theme={'dark'}
            viewType={diffViewType}
            onClickLine={handleClickCodeItem}
          />
        </div>
      </>
    );
  };

  return renderViolationLineItem();
}
