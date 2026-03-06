#!/usr/bin/env node

// SPDX-FileCopyrightText: 2026 PlainLicense
//
// SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

// Applies local patches to node_modules after install.
// Each patch is idempotent: skipped if already applied, warns if target not found.

import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');

function patch(label, filePath, oldStr, newStr) {
  let content;
  try {
    content = readFileSync(filePath, 'utf8');
  } catch {
    console.warn(`[patches] SKIP ${label}: file not found at ${filePath}`);
    return;
  }
  if (content.includes(newStr)) {
    console.log(`[patches] OK    ${label}: already applied`);
  } else if (content.includes(oldStr)) {
    writeFileSync(filePath, content.replace(oldStr, newStr));
    console.log(`[patches] APPLY ${label}`);
  } else {
    console.warn(`[patches] WARN  ${label}: target string not found — patch may need updating`);
  }
}

// ── Patch 1: Vite 6 mergeConfigRecursively — noExternal=true ignored at rootPath ""
// When @astrojs/cloudflare sets ssr.noExternal=true, it gets merged with the resolved
// environments.ssr.resolve.noExternal (an array of Astro packages) at rootPath "".
// Vite's special-case only fires at rootPath "ssr"|"resolve", so arraify(true).concat([...])
// produces [true, "astro", ...], which then breaks normalizePath(true). Fix: extend the
// special case to also cover rootPath "".
const chunksDir = resolve(root, 'node_modules/astro/node_modules/vite/dist/node/chunks');
let vitePatchApplied = false;
for (const file of readdirSync(chunksDir)) {
  if (!file.endsWith('.js')) continue;
  const filePath = join(chunksDir, file);
  const OLD = '} else if (key === "noExternal" && (rootPath === "ssr" || rootPath === "resolve") && (existing === true || value === true)) {';
  const NEW = '} else if (key === "noExternal" && (rootPath === "ssr" || rootPath === "resolve" || rootPath === "") && (existing === true || value === true)) {';
  const content = readFileSync(filePath, 'utf8');
  if (content.includes(NEW)) {
    console.log(`[patches] OK    Vite mergeConfig noExternal fix: already applied (${file})`);
    vitePatchApplied = true;
    break;
  } else if (content.includes(OLD)) {
    writeFileSync(filePath, content.replace(OLD, NEW));
    console.log(`[patches] APPLY Vite mergeConfig noExternal fix (${file})`);
    vitePatchApplied = true;
    break;
  }
}
if (!vitePatchApplied) {
  console.warn('[patches] WARN  Vite mergeConfig noExternal fix: target not found in any chunk — patch may need updating');
}

// ── Patch 2: starlight-contextual-menu — remove `export default` from injected script
// The plugin injects contextual-menu.js as a page script. The file ends with
// `export default initContextualMenu;` which creates a duplicate default export
// in Astro's virtual astro:scripts/page.js when combined with other plugins.
patch(
  'starlight-contextual-menu export default',
  resolve(root, 'node_modules/starlight-contextual-menu/contextual-menu.js'),
  '\nexport default initContextualMenu;\n',
  '\n',
);

// ── Patch 3: starlight-scroll-to-top — remove `export default` from injected script
// Same issue as Patch 2: scroll-to-top.js ends with `export default initScrollToTop;`.
patch(
  'starlight-scroll-to-top export default',
  resolve(root, 'node_modules/starlight-scroll-to-top/libs/scroll-to-top.js'),
  '\nexport default initScrollToTop;\n',
  '\n',
);
