import { TransitionSeries } from "@remotion/transitions";
import { Background } from "./Background";
import { IntroScene } from "./IntroScene";
import { OutroScene } from "./OutroScene";
import { ToolsScene } from "./ToolsScene";

// Same 8-second intro as hyperframes/index.html, at 30fps.
export const KoreanIntro: React.FC = () => (
  <Background>
    <TransitionSeries>
      <TransitionSeries.Sequence name="Intro" durationInFrames={84}>
        <IntroScene />
      </TransitionSeries.Sequence>
      <TransitionSeries.Sequence name="Tools" durationInFrames={84}>
        <ToolsScene />
      </TransitionSeries.Sequence>
      <TransitionSeries.Sequence name="Outro" durationInFrames={72}>
        <OutroScene />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  </Background>
);
