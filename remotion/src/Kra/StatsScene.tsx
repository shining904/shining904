import { loadFont } from "@remotion/fonts";
import {
  AbsoluteFill,
  Easing,
  Interactive,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { FONT_FAMILY } from "../KoreanIntro/fonts";

const DISPLAY = "Black Han Sans";
for (const subset of [
  { name: "latin", unicodeRange: "U+0000-00FF, U+2190-21FF" },
  { name: "korean", unicodeRange: "U+1100-11FF, U+3130-318F, U+AC00-D7AF" },
]) {
  loadFont({
    family: DISPLAY,
    url: staticFile(`fonts/black-han-sans-${subset.name}-400-normal.woff2`),
    weight: "400",
    unicodeRange: subset.unicodeRange,
  });
}

const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
const LIME = "#d9ec7c";
// Each number starts on its narration cue (0s, 2.3s, 4.15s of the scene).
const STAT_STARTS = [0, 69, 125];
const SCENE_FRAMES = 195;

type Stat = {
  label: string;
  prefix?: string;
  value: number;
  format: (n: number) => string;
  unit: string;
  note: string;
};

const STATS: Stat[] = [
  {
    label: "연간 세입",
    value: 490,
    prefix: "약",
    format: (n) => `${n}`,
    unit: "억 원",
    note: "과천 수준 운영 시 · 레저세 교부금 약 63억 포함",
  },
  {
    label: "근무 기반 이동",
    value: 3000,
    format: (n) => n.toLocaleString("en-US"),
    unit: "명",
    note: "마사회·협력업체 등 + 지역 주민 우선 채용",
  },
  {
    label: "연간 방문객",
    value: 200,
    format: (n) => `${n}`,
    unit: "만 명+",
    note: "숙박·음식·교통, 지역 소비가 늘어나요",
  },
];

const StatCard: React.FC<{ stat: Stat; frames: number }> = ({ stat, frames }) => {
  const frame = useCurrentFrame();
  const count = interpolate(frame, [6, 30], [0, stat.value], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: EASE_OUT,
  });

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <Interactive.Div
        name="Stat"
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          translate: interpolate(frame, [0, 8, frames - 7, frames], ["900px 0px", "0px 0px", "0px 0px", "-900px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: EASE_OUT,
          }),
        }}
      >
        <div
          style={{
            padding: "14px 44px",
            borderRadius: 999,
            background: LIME,
            color: "#14472d",
            fontSize: 52,
            fontWeight: 800,
          }}
        >
          {stat.label}
        </div>
        <div
          style={{
            marginTop: 40,
            display: "flex",
            alignItems: "baseline",
            gap: 16,
            fontFamily: DISPLAY,
            color: "#ffffff",
            scale: interpolate(frame, [30, 35, 42], [1, 1.12, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          {stat.prefix ? <span style={{ fontSize: 110, color: LIME }}>{stat.prefix}</span> : null}
          <span style={{ fontSize: 230, lineHeight: 1 }}>{stat.format(Math.round(count))}</span>
          <span style={{ fontSize: 110, color: LIME }}>{stat.unit}</span>
        </div>
        <div
          style={{
            marginTop: 40,
            fontSize: 42,
            fontWeight: 500,
            color: "#e6efe3",
            opacity: interpolate(frame, [24, 36], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
          }}
        >
          {stat.note}
        </div>
      </Interactive.Div>
    </AbsoluteFill>
  );
};

// Three key numbers for the Icheon racecourse campaign, counted up one after another.
export const KraStatsScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ background: "#14472d", fontFamily: FONT_FAMILY, overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          background:
            "repeating-linear-gradient(115deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 40px, transparent 40px, transparent 120px)",
          translate: `${interpolate(frame, [0, SCENE_FRAMES], [0, -360])}px 0px`,
          width: 1800,
        }}
      />
      <Interactive.Div
        name="Header"
        style={{
          position: "absolute",
          top: 300,
          left: 0,
          right: 0,
          textAlign: "center",
          fontFamily: DISPLAY,
          fontSize: 96,
          color: "#ffffff",
          opacity: interpolate(frame, [0, 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        경마공원이 오면
      </Interactive.Div>
      {STATS.map((stat, i) => (
        <Sequence
          key={stat.label}
          name={stat.label}
          from={STAT_STARTS[i]}
          durationInFrames={(STAT_STARTS[i + 1] ?? SCENE_FRAMES) - STAT_STARTS[i]}
        >
          <StatCard stat={stat} frames={(STAT_STARTS[i + 1] ?? SCENE_FRAMES) - STAT_STARTS[i]} />
        </Sequence>
      ))}
      <div
        style={{
          position: "absolute",
          bottom: 360,
          left: 0,
          right: 0,
          textAlign: "center",
          fontSize: 30,
          fontWeight: 500,
          color: "rgba(230, 239, 227, 0.75)",
        }}
      >
        ※ 수치는 사업 규모·운영 방식·협약 조건 등에 따라 달라질 수 있습니다
      </div>
    </AbsoluteFill>
  );
};
