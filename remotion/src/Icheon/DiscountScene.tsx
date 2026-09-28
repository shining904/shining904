import { AbsoluteFill, Easing, Interactive, interpolate, useCurrentFrame } from "remotion";
import { FONT_FAMILY } from "../KoreanIntro/fonts";

const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
const RING_RADIUS = 250;
const RING_LENGTH = 2 * Math.PI * RING_RADIUS;
const GREEN = "#1f8a4c";

// Key-number scene for the Icheon annual-payment video: counts up to a 10% discount.
export const DiscountScene: React.FC = () => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [12, 60], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE_OUT,
  });

  return (
    <AbsoluteFill
      style={{
        alignItems: "center",
        justifyContent: "center",
        background: "#f4f7f2",
        color: "#10231a",
        fontFamily: FONT_FAMILY,
      }}
    >
      <Interactive.Div
        name="Kicker"
        style={{
          padding: "14px 36px",
          borderRadius: 999,
          background: GREEN,
          color: "#ffffff",
          fontSize: 40,
          fontWeight: 800,
          marginBottom: 48,
          opacity: interpolate(frame, [0, 12], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
          translate: interpolate(frame, [0, 12], ["0px 20px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_OUT,
          }),
        }}
      >
        연납 혜택
      </Interactive.Div>
      <div style={{ position: "relative", width: 580, height: 580 }}>
        <svg viewBox="0 0 580 580" style={{ position: "absolute", inset: 0, rotate: "-90deg" }}>
          <circle cx="290" cy="290" r={RING_RADIUS} fill="none" stroke="#dbe7dd" strokeWidth="28" />
          <circle
            cx="290"
            cy="290"
            r={RING_RADIUS}
            fill="none"
            stroke={GREEN}
            strokeWidth="28"
            strokeLinecap="round"
            strokeDasharray={RING_LENGTH}
            strokeDashoffset={RING_LENGTH * (1 - progress)}
          />
        </svg>
        <Interactive.Div
          name="Discount number"
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            scale: interpolate(frame, [60, 68, 78], [1, 1.08, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          <div style={{ fontSize: 170, fontWeight: 800, letterSpacing: "-0.04em", lineHeight: 1, color: GREEN }}>
            {Math.round(progress * 10)}%
          </div>
          <div style={{ fontSize: 72, fontWeight: 800, marginTop: 8 }}>감면</div>
        </Interactive.Div>
      </div>
      <Interactive.Div
        name="Condition"
        style={{
          marginTop: 56,
          fontSize: 52,
          fontWeight: 500,
          opacity: interpolate(frame, [50, 68], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
          translate: interpolate(frame, [50, 68], ["0px 24px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_OUT,
          }),
        }}
      >
        연납 신청 후 <b style={{ color: GREEN }}>1월 16일 ~ 31일</b>에 납부하면
      </Interactive.Div>
    </AbsoluteFill>
  );
};
