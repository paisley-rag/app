interface OverlayProps {
  handleOverlayClick: (e: React.SyntheticEvent) => void;
}

export function Overlay({ handleOverlayClick }: OverlayProps) {
  return (
    <div
      className="z-20 absolute top-0 left-0 h-screen w-screen bg-black/[0.3]"
      onClick={handleOverlayClick}
    ></div>
  );
}
