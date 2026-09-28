import { AbsoluteFill, Easing, Interactive, interpolate, useCurrentFrame } from "remotion";

const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
const EASE_IN = Easing.bezier(0.55, 0, 1, 0.45);
const WORDS = ["코드로", "만드는", "영상"];

export const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <Interactive.Div
        name="Intro"
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          opacity: interpolate(frame, [72, 84], [1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_IN,
          }),
          translate: interpolate(frame, [72, 84], ["0px 0px", "0px -40px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_IN,
          }),
        }}
      >
        <Interactive.Div
          name="Kicker"
          style={{
            fontSize: 36,
            fontWeight: 500,
            letterSpacing: "0.3em",
            color: "#a5b4fc",
            marginBottom: 28,
            opacity: interpolate(frame, [3, 18], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
            translate: interpolate(frame, [3, 18], ["0px 20px", "0px 0px"], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: EASE_OUT,
            }),
          }}
        >
          HYPERFRAMES × REMOTION
        </Interactive.Div>
        <div style={{ display: "flex", gap: 28, fontSize: 128, fontWeight: 800, letterSpacing: "-0.03em" }}>
          {WORDS.map((word, i) => {
            const start = 9 + i * 4.5;
            const isAccent = i === WORDS.length - 1;
            return (
              <div
                key={word}
                style={{
                  opacity: interpolate(frame, [start, start + 21], [0, 1], {
                    extrapolateLeft: "clamp",
                    extrapolateRight: "clamp",
                    easing: EASE_OUT,
                  }),
                  translate: interpolate(frame, [start, start + 21], ["0px 80px", "0px 0px"], {
                    extrapolateLeft: "clamp",
                    extrapolateRight: "clamp",
                    easing: EASE_OUT,
                  }),
                  ...(isAccent
                    ? {
                        background: "linear-gradient(90deg, #818cf8, #f472b6)",
                        WebkitBackgroundClip: "text",
                        backgroundClip: "text",
                        color: "transparent",
                      }
                    : {}),
                }}
              >
                {word}
              </div>
            );
          })}
        </div>
      </Interactive.Div>
    </AbsoluteFill>
  );
};
