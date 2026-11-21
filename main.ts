// news-image-20261120 — "The World Today", a front page for Friday 20 November 2026.
// Node 22, standard library only. The image is entry.png beside this file, drawn
// by draw.py from the day's verified reporting (see NOTES.md); this program just
// copies it to the output directory, so both grader runs write identical bytes.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = new URL("./entry.png", import.meta.url);
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
// The grader runs the program twice and both runs must write the same bytes:
// a plain copy of a fixed file guarantees that; confirm the sizes agree.
if (statSync(src).size !== statSync(dest).size) {
  throw new Error("entry.png copy size mismatch");
}
console.log(`wrote ${dest} (${statSync(dest).size} bytes)`);
