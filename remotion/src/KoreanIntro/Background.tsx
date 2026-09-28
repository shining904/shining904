import { AbsoluteFill } from "remotion";
import { FONT_FAMILY } from "./fonts";

export const Background: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill
    style={{
      color: "#f4f4f5",
      fontFamily: FONT_FAMILY,
      background:
        "radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.35), transparent 55%), radial-gradient(circle at 80% 75%, rgba(236, 72, 153, 0.28), transparent 55%), #0b0d12",
    }}
  >
    {children}
  </AbsoluteFill>
);
