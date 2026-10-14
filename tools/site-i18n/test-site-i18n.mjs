import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const toolDirectory = path.dirname(fileURLToPath(import.meta.url));
const temporaryDirectory = await mkdtemp(
  path.join(tmpdir(), "film-restoration-i18n-"),
);
const siteDirectory = path.join(temporaryDirectory, "_site");
const cacheDirectory = path.join(temporaryDirectory, "cache");

try {
  await mkdir(siteDirectory, { recursive: true });
  await writeFile(
    path.join(siteDirectory, "index.html"),
    `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Film research</title>
  </head>
  <body>
    <main class="main-content">
      <h1>Open research</h1>
      <a href="/experimental-film-restoration-ml/start-here/">Start here</a>
      <img src="/experimental-film-restoration-ml/assets/source.png" alt="Source frame">
      <pre>do not translate</pre>
    </main>
  </body>
</html>`,
    "utf8",
  );

  await run(process.execPath, [
    path.join(toolDirectory, "translate-site.mjs"),
    "--site",
    siteDirectory,
    "--mock-translations",
  ]);

  const english = await readFile(path.join(siteDirectory, "index.html"), "utf8");
  const spanish = await readFile(
    path.join(siteDirectory, "es", "index.html"),
    "utf8",
  );
  const chinese = await readFile(
    path.join(siteDirectory, "zh", "index.html"),
    "utf8",
  );

  assert.match(english, /data-site-locale="en"/);
  assert.match(english, /hreflang="zh-Hans"/);
  assert.match(english, /data-language="hi"/);
  assert.match(english, /class="translation-notice"[^>]*hidden/);
  assert.match(spanish, /<html lang="es">/);
  assert.match(spanish, /<title>\[es\] Film research<\/title>/);
  assert.match(spanish, /\[es\] Open research/);
  assert.match(spanish, /<strong>\[es\] Automatic translation<\/strong>/);
  assert.doesNotMatch(
    spanish,
    /class="translation-notice"[^>]*hidden/,
  );
  assert.match(
    spanish,
    /class="translation-notice"[\s\S]*href="\/experimental-film-restoration-ml\/"/,
  );
  assert.match(
    spanish,
    /href="\/experimental-film-restoration-ml\/es\/start-here\/"/,
  );
  assert.match(
    spanish,
    /src="\/experimental-film-restoration-ml\/assets\/source.png"/,
  );
  assert.match(spanish, /<pre>do not translate<\/pre>/);
  assert.match(spanish, /data-language="es" selected/);
  assert.match(chinese, /<html lang="zh-Hans">/);

  await run(process.execPath, [
    path.join(toolDirectory, "translate-site.mjs"),
    "--site",
    siteDirectory,
    "--english-only",
  ]);
  const englishOnly = await readFile(
    path.join(siteDirectory, "index.html"),
    "utf8",
  );
  assert.match(englishOnly, /<html lang="en">/);
  assert.doesNotMatch(englishOnly, /site-language-select/);
  assert.doesNotMatch(englishOnly, /translation-notice/);
  assert.doesNotMatch(englishOnly, /hreflang=/);
  assert.doesNotMatch(
    englishOnly,
    /\/experimental-film-restoration-ml\/es\//,
  );

  console.log("Multilingual routing, metadata, translation, and asset tests passed.");
} finally {
  await rm(temporaryDirectory, { recursive: true, force: true });
}

function run(command, argumentsList) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, argumentsList, {
      env: {
        ...process.env,
        TRANSLATION_CACHE_DIR: cacheDirectory,
        TRANSLATION_MIN_INTERVAL_MS: "0",
      },
      stdio: "inherit",
    });
    child.on("error", reject);
    child.on("exit", (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Translation test exited with code ${code}.`));
      }
    });
  });
}
