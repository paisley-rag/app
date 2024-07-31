import { SetStateAction, Dispatch } from "react";

interface OverlayProps {
  setModalVisible: Dispatch<SetStateAction<boolean>>;
}

export function Overlay({ setModalVisible }: OverlayProps) {
  return (
    <div
      className="z-20 absolute top-0 left-0 h-screen w-screen bg-black/[0.3]"
      onClick={() => setModalVisible(false)}
    ></div>
  );
}
