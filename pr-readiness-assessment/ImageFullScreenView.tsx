import { X } from 'lucide-react';

const ImageFullScreenView = ({ src, onClose }: { src: string; onClose: () => void }) => {
  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-[1100] flex items-center justify-center bg-black/60 backdrop-blur-md p-4"
      onClick={onClose}
    >
      {/* Stop propagation */}
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative max-h-[90vh] max-w-[95vw] overflow-hidden rounded-2xl border bg-panel-background shadow-2xl"
      >
        {/* Close */}
        <button
          onClick={onClose}
          className="absolute right-4 top-7 z-10"
        >
          <X className="h-5 w-5 bg-gray-700 p-2 text-white rounded" />
        </button>

        {/* Image */}
        <div className="flex h-full w-full items-center justify-center p-2">
          <img
            src={src}
            alt="Citation Full View"
            className="max-h-[80vh] max-w-full rounded-xl object-contain"
          />
        </div>
      </div>
    </div>
  );
};

export default ImageFullScreenView;