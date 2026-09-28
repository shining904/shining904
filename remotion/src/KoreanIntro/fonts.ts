import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

export const FONT_FAMILY = "Noto Sans KR";

const SUBSETS = [
  { name: "latin", unicodeRange: "U+0000-00FF, U+2190-21FF" },
  { name: "korean", unicodeRange: "U+1100-11FF, U+3130-318F, U+AC00-D7AF" },
];

for (const weight of ["500", "800"]) {
  for (const subset of SUBSETS) {
    loadFont({
      family: FONT_FAMILY,
      url: staticFile(`fonts/noto-sans-kr-${subset.name}-${weight}-normal.woff2`),
      weight,
      unicodeRange: subset.unicodeRange,
    });
  }
}
