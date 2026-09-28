import { AbsoluteFill, Easing, Interactive, interpolate, useCurrentFrame } from "remotion";

const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
const EASE_OUT_SOFT = Easing.bezier(0.25, 0.46, 0.45, 0.94);
const RING_LENGTH = 277;
const MARK_LENGTH = 60;

export const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <svg viewBox="0 0 100 100" style={{ width: 180, height: 180, marginBottom: 48 }}>
        <circle
          cx="50"
          cy="50"
          r="44"
          fill="none"
          stroke="#818cf8"
          strokeWidth="6"
          strokeDasharray={RING_LENGTH}
          strokeDashoffset={interpolate(frame, [3, 21], [RING_LENGTH, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_OUT_SOFT,
          })}
        />
        <path
          d="M30 52 L45 66 L71 38"
          fill="none"
          stroke="#f472b6"
          strokeWidth="8"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray={MARK_LENGTH}
          strokeDashoffset={interpolate(frame, [16.5, 28.5], [MARK_LENGTH, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_OUT_SOFT,
          })}
        />
      </svg>
      <Interactive.Div
        name="Done title"
        style={{
          fontSize: 120,
          fontWeight: 800,
          letterSpacing: "-0.03em",
          opacity: interpolate(frame, [18, 36], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_OUT,
          }),
          translate: interpolate(frame, [18, 36], ["0px 40px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_OUT,
          }),
        }}
      >
        설치 완료
      </Interactive.Div>
      <Interactive.Div
        name="Subtitle"
        style={{
          marginTop: 24,
          fontSize: 44,
          fontWeight: 500,
          color: "#a1a1aa",
          opacity: interpolate(frame, [30, 45], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        이제 영상을 만들어 볼까요?
      </Interactive.Div>
    </AbsoluteFill>
  );
};
