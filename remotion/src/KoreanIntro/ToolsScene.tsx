import { AbsoluteFill, Easing, Interactive, interpolate, useCurrentFrame } from "remotion";

const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
const EASE_IN = Easing.bezier(0.55, 0, 1, 0.45);

const cardStyle: React.CSSProperties = {
  width: 640,
  padding: "56px 60px",
  borderRadius: 32,
  background: "rgba(255, 255, 255, 0.06)",
  border: "2px solid rgba(255, 255, 255, 0.12)",
};
const nameStyle: React.CSSProperties = { fontSize: 72, fontWeight: 800, letterSpacing: "-0.02em" };
const flowStyle: React.CSSProperties = { marginTop: 20, fontSize: 44, fontWeight: 500, color: "#c7d2fe" };

export const ToolsScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <Interactive.Div
        name="Cards"
        style={{
          display: "flex",
          gap: 64,
          opacity: interpolate(frame, [72, 84], [1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_IN,
          }),
          scale: interpolate(frame, [72, 84], [1, 0.96], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_IN,
          }),
        }}
      >
        <Interactive.Div
          name="HyperFrames card"
          style={{
            ...cardStyle,
            opacity: interpolate(frame, [3, 24], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: EASE_OUT,
            }),
            translate: interpolate(frame, [3, 24], ["-120px 0px", "0px 0px"], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: EASE_OUT,
            }),
          }}
        >
          <div style={nameStyle}>HyperFrames</div>
          <div style={flowStyle}>HTML → MP4</div>
        </Interactive.Div>
        <Interactive.Div
          name="Remotion card"
          style={{
            ...cardStyle,
            opacity: interpolate(frame, [7.5, 28.5], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: EASE_OUT,
            }),
            translate: interpolate(frame, [7.5, 28.5], ["120px 0px", "0px 0px"], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: EASE_OUT,
            }),
          }}
        >
          <div style={nameStyle}>Remotion</div>
          <div style={flowStyle}>React → MP4</div>
        </Interactive.Div>
      </Interactive.Div>
    </AbsoluteFill>
  );
};
