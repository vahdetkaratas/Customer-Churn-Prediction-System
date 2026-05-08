#!/usr/bin/env node
/**
 * Render shell HTML for a profile from a multi-profile body template.
 *
 * Usage (from repo root):
 *   node shell/render-shell.mjs --project shell/projects/customer-churn.json \
 *     --body shell/body/customer-churn.html --out layout-shell --profile recruiter
 */
import { mkdirSync, readFileSync, writeFileSync } from "fs";
import { dirname, join, resolve } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--project" || a === "--body" || a === "--out" || a === "--profile") {
      out[a.slice(2)] = argv[++i];
    }
  }
  return out;
}

function extractProfile(html, profile) {
  const begin = `<!-- BEGIN_SHELL_PROFILE:${profile} -->`;
  const end = `<!-- END_SHELL_PROFILE:${profile} -->`;
  const i0 = html.indexOf(begin);
  const i1 = html.indexOf(end);
  if (i0 === -1 || i1 === -1 || i1 <= i0) {
    throw new Error(`Missing profile segment "${profile}" in body template (markers ${begin} / ${end}).`);
  }
  return html.slice(i0 + begin.length, i1).trim();
}

const args = parseArgs(process.argv);
const { project, body, out, profile } = args;
if (!project || !body || !out || !profile) {
  console.error(
    "Usage: node shell/render-shell.mjs --project <json> --body <html> --out <dir> --profile <recruiter|commercial>"
  );
  process.exit(1);
}

const profilePath = resolve(ROOT, "shell", "profiles", `${profile}.json`);
let links;
try {
  links = JSON.parse(readFileSync(profilePath, "utf8"));
} catch (e) {
  console.error(`Cannot read profile JSON: ${profilePath}`, e.message);
  process.exit(1);
}

const bodyPath = resolve(ROOT, body);
const bodyHtml = readFileSync(bodyPath, "utf8");
let html = extractProfile(bodyHtml, profile);

for (const [key, value] of Object.entries(links)) {
  if (typeof value !== "string") continue;
  const token = `__${key}__`;
  if (!html.includes(token)) continue;
  html = html.split(token).join(value);
}

const leftover = html.match(/__([A-Z0-9_]+)__/g);
if (leftover?.length) {
  console.warn("Warning: unreplaced placeholders:", [...new Set(leftover)].join(", "));
}

const outDir = resolve(ROOT, out);
mkdirSync(outDir, { recursive: true });
const indexPath = join(outDir, "index.html");
writeFileSync(indexPath, html + "\n", "utf8");
console.log(`Wrote ${indexPath}`);
