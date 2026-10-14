import { createHash } from "node:crypto";
import {
  mkdir,
  readFile,
  readdir,
  rename,
  rm,
  writeFile,
} from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import * as cheerio from "cheerio";

const toolDirectory = path.dirname(fileURLToPath(import.meta.url));
const languages = JSON.parse(
  await readFile(path.join(toolDirectory, "languages.json"), "utf8"),
);
const sourceLanguage = languages.find(({ code }) => code === "en");
const targetLanguages = languages.filter(({ code }) => code !== "en");
const localeCodes = new Set(languages.map(({ code }) => code));

const options = parseArguments(process.argv.slice(2));
const siteDirectory = path.resolve(options.site);
const cacheDirectory = path.resolve(
  process.env.TRANSLATION_CACHE_DIR || ".translation-cache",
);
const cacheFile = path.join(cacheDirectory, "translations.json");
const basePath = normalizeBasePath(
  process.env.SITE_BASE_PATH ||
    "/experimental-film-restoration-ml",
);
const siteOrigin = (
  process.env.SITE_ORIGIN || "https://fabiocolor.github.io"
).replace(/\/+$/, "");
const model = process.env.TRANSLATION_MODEL || "openai/gpt-4o-mini";
const endpoint =
  process.env.TRANSLATION_ENDPOINT ||
  "https://models.github.ai/inference/chat/completions";
const minimumRequestInterval = Number(
  process.env.TRANSLATION_MIN_INTERVAL_MS || 4500,
);
const maximumBatchCharacters = 12_000;
const maximumBatchItems = 140;

validateConfiguration();

const htmlFiles = (await walk(siteDirectory))
  .filter((file) => file.endsWith(".html"))
  .filter((file) => {
    const relative = toPosix(path.relative(siteDirectory, file));
    return !localeCodes.has(relative.split("/")[0]);
  });

if (htmlFiles.length === 0) {
  throw new Error(`No HTML pages were found in ${siteDirectory}`);
}

if (options.englishOnly) {
  await prepareEnglishOnlySite();
  console.log(
    `Prepared ${htmlFiles.length} canonical English page(s) without unavailable language links.`,
  );
  process.exit(0);
}

if (options.validateOnly) {
  const validationPages = await loadEnglishPages();
  const validationText = collectUniqueText(validationPages);
  const batchesPerLanguage = makeBatches(
    validationText,
    maximumBatchCharacters,
    maximumBatchItems,
  ).length;
  console.log(
    `Validated ${htmlFiles.length} English page(s), ${validationText.length} unique text strings, and ${targetLanguages.length} target language(s).`,
  );
  console.log(
    `A cold translation build is expected to use ${batchesPerLanguage * targetLanguages.length} model request(s); cached builds use only requests for changed text.`,
  );
  process.exit(0);
}

const token = process.env.GITHUB_TOKEN || process.env.TRANSLATION_TOKEN;
if (!token && !options.mockTranslations) {
  throw new Error(
    "GITHUB_TOKEN or TRANSLATION_TOKEN is required to generate translations.",
  );
}

await mkdir(cacheDirectory, { recursive: true });
const cache = await readCache();
const pages = await loadEnglishPages();
const requiredText = collectUniqueText(pages);

for (const language of targetLanguages) {
  const translations = await translateTextSet(
    requiredText,
    language,
    cache,
    token,
  );

  for (const page of pages) {
    const translated = cheerio.load(page.englishHtml, {
      decodeEntities: false,
    });
    applyTranslations(translated, translations);
    localizePage(translated, page.route, language);

    const destination = path.join(
      siteDirectory,
      language.code,
      page.relativeFile,
    );
    await mkdir(path.dirname(destination), { recursive: true });
    await writeFile(destination, translated.html(), "utf8");
  }

  console.log(
    `Generated ${pages.length} ${language.englishName} page(s) at /${language.code}/.`,
  );
}

await saveCache(cache);
console.log(
  `Multilingual site complete: English plus ${targetLanguages.length} generated languages.`,
);

function parseArguments(argumentsList) {
  const parsed = {
    englishOnly: false,
    mockTranslations: false,
    site: "_site",
    validateOnly: false,
  };

  for (let index = 0; index < argumentsList.length; index += 1) {
    const argument = argumentsList[index];
    if (argument === "--site") {
      parsed.site = argumentsList[index + 1];
      index += 1;
    } else if (argument === "--validate-only") {
      parsed.validateOnly = true;
    } else if (argument === "--english-only") {
      parsed.englishOnly = true;
    } else if (argument === "--mock-translations") {
      parsed.mockTranslations = true;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }

  if (!parsed.site) {
    throw new Error("--site requires a directory.");
  }
  return parsed;
}

async function prepareEnglishOnlySite() {
  for (const file of htmlFiles) {
    const document = cheerio.load(await readFile(file, "utf8"), {
      decodeEntities: false,
    });
    document(".language-switch, .site-language, .translation-notice").remove();
    document('link[rel="alternate"][hreflang]').remove();
    document('script[data-site-language-routing="true"]').remove();
    document("html").attr("lang", sourceLanguage.htmlLang);
    document("body").removeAttr("data-site-locale");
    await writeFile(file, document.html(), "utf8");
  }
}

function validateConfiguration() {
  const seen = new Set();
  for (const language of languages) {
    if (!/^[a-z]{2}$/.test(language.code)) {
      throw new Error(`Invalid language code: ${language.code}`);
    }
    if (seen.has(language.code)) {
      throw new Error(`Duplicate language code: ${language.code}`);
    }
    if (!language.name || !language.englishName || !language.htmlLang) {
      throw new Error(`Incomplete language definition: ${language.code}`);
    }
    seen.add(language.code);
  }
  if (!sourceLanguage) {
    throw new Error("The English source language is missing.");
  }
}

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(
    entries.map(async (entry) => {
      const entryPath = path.join(directory, entry.name);
      return entry.isDirectory() ? walk(entryPath) : [entryPath];
    }),
  );
  return nested.flat();
}

async function loadEnglishPages() {
  const loadedPages = [];
  for (const file of htmlFiles) {
    const relativeFile = toPosix(path.relative(siteDirectory, file));
    const route = routeForFile(relativeFile);
    const document = cheerio.load(await readFile(file, "utf8"), {
      decodeEntities: false,
    });

    document(".language-switch, .site-language, .translation-notice").remove();
    preparePageChrome(document, route, sourceLanguage);
    const englishHtml = document.html();
    await writeFile(file, englishHtml, "utf8");
    loadedPages.push({ relativeFile, route, englishHtml });
  }
  return loadedPages;
}

function collectUniqueText(pages) {
  const values = new Set();
  for (const page of pages) {
    const document = cheerio.load(page.englishHtml, {
      decodeEntities: false,
    });
    for (const unit of collectTranslationUnits(document)) {
      values.add(unit.source);
    }
  }
  return [...values];
}

function collectTranslationUnits(document) {
  const units = [];
  const skippedTags = new Set([
    "code",
    "kbd",
    "math",
    "noscript",
    "pre",
    "script",
    "style",
    "svg",
    "textarea",
  ]);

  document("title, body, body *").each((_, element) => {
    const tagName = element.tagName?.toLowerCase();
    if (!tagName || skippedTags.has(tagName)) return;

    const selection = document(element);
    if (
      selection.closest(
        "[data-no-translate], code, kbd, math, noscript, pre, script, style, svg, textarea",
      ).length
    ) {
      return;
    }

    for (const child of element.children || []) {
      if (child.type !== "text") continue;
      const source = child.data.trim();
      if (shouldTranslate(source)) {
        units.push({ type: "text", node: child, source });
      }
    }

    for (const attribute of ["alt", "aria-label", "placeholder", "title"]) {
      const source = selection.attr(attribute)?.trim();
      if (shouldTranslate(source)) {
        units.push({
          type: "attribute",
          node: element,
          attribute,
          source,
        });
      }
    }
  });

  document(
    'meta[name="description"], meta[property="og:title"], meta[property="og:description"], meta[name="twitter:title"], meta[name="twitter:description"]',
  ).each((_, element) => {
    const source = document(element).attr("content")?.trim();
    if (shouldTranslate(source)) {
      units.push({
        type: "attribute",
        node: element,
        attribute: "content",
        source,
      });
    }
  });

  return units;
}

function shouldTranslate(value) {
  if (!value || value.length < 2) return false;
  if (/^(https?:|mailto:|tel:|\/|#)/i.test(value)) return false;
  if (/^[\d\s.,:;()[\]{}%+–—-]+$/u.test(value)) return false;
  return /\p{L}/u.test(value);
}

async function translateTextSet(values, language, cache, tokenValue) {
  const translations = new Map();
  const missing = [];

  for (const value of values) {
    const key = cacheKey(language.code, value);
    if (cache[key]) {
      translations.set(value, cache[key]);
    } else {
      missing.push(value);
    }
  }

  const batches = makeBatches(
    missing,
    maximumBatchCharacters,
    maximumBatchItems,
  );
  let lastRequestAt = 0;
  for (let index = 0; index < batches.length; index += 1) {
    const elapsed = Date.now() - lastRequestAt;
    if (elapsed < minimumRequestInterval) {
      await delay(minimumRequestInterval - elapsed);
    }

    const translatedBatch = await requestTranslation(
      batches[index],
      language,
      tokenValue,
    );
    lastRequestAt = Date.now();

    for (const [source, translated] of translatedBatch) {
      translations.set(source, translated);
      cache[cacheKey(language.code, source)] = translated;
    }
    await saveCache(cache);
    console.log(
      `${language.code}: translated batch ${index + 1}/${batches.length}; ${translations.size}/${values.length} strings ready.`,
    );
  }

  return translations;
}

function makeBatches(values, maximumCharacters, maximumItems) {
  const batches = [];
  let batch = [];
  let characters = 0;

  for (const value of values) {
    if (
      batch.length > 0 &&
      (batch.length >= maximumItems ||
        characters + value.length > maximumCharacters)
    ) {
      batches.push(batch);
      batch = [];
      characters = 0;
    }
    batch.push(value);
    characters += value.length;
  }

  if (batch.length > 0) batches.push(batch);
  return batches;
}

async function requestTranslation(values, language, tokenValue) {
  if (options.mockTranslations) {
    return new Map(
      values.map((value) => [value, `[${language.code}] ${value}`]),
    );
  }

  const entries = Object.fromEntries(
    values.map((value, index) => [String(index), value]),
  );
  const instructions = [
    `Translate every JSON value from English into ${language.englishName}.`,
    "Write for a public research website: clear, natural, calm, and understandable to film-restoration practitioners and interested non-specialists.",
    "Preserve meaning and uncertainty. Do not strengthen experimental claims.",
    "Keep model, product, institution, event, software, and project names unchanged, including Qwen Image Edit, CopyCat, Nuke, ComfyUI, DaVinci Resolve, SEAPAVAA, Muralla Verde, and GitHub.",
    "Preserve filenames, command names, URLs, Markdown-like tokens, numbers, and technical abbreviations.",
    "Return only one valid JSON object with exactly the same keys. Do not add commentary.",
  ].join(" ");

  const payload = {
    model,
    messages: [
      { role: "system", content: instructions },
      { role: "user", content: JSON.stringify(entries) },
    ],
    max_tokens: 4000,
    temperature: 0.1,
    response_format: { type: "json_object" },
  };

  let response;
  for (let attempt = 0; attempt < 6; attempt += 1) {
    response = await fetch(endpoint, {
      method: "POST",
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${tokenValue}`,
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2026-03-10",
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) break;
    const body = await response.text();
    if (![429, 500, 502, 503, 504].includes(response.status)) {
      throw new Error(
        `Translation request failed (${response.status}): ${body.slice(0, 500)}`,
      );
    }

    const retryAfter = Number(response.headers.get("retry-after") || 0) * 1000;
    const wait = Math.max(retryAfter, 2 ** attempt * 2000);
    console.warn(
      `Translation service returned ${response.status}; retrying in ${Math.ceil(wait / 1000)} seconds.`,
    );
    await delay(wait);
  }

  if (!response?.ok) {
    throw new Error(
      `Translation request did not succeed after retries (${response?.status || "no response"}).`,
    );
  }

  const result = await response.json();
  const rawContent = result.choices?.[0]?.message?.content;
  if (typeof rawContent !== "string") {
    throw new Error("Translation response did not contain message content.");
  }

  const decoded = JSON.parse(
    rawContent.replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, ""),
  );
  const translated = new Map();
  for (let index = 0; index < values.length; index += 1) {
    const key = String(index);
    const value = decoded[key];
    if (typeof value !== "string" || !value.trim()) {
      throw new Error(`Translation response is missing key ${key}.`);
    }
    translated.set(values[index], value.trim());
  }
  return translated;
}

function applyTranslations(document, translations) {
  for (const unit of collectTranslationUnits(document)) {
    const translated = translations.get(unit.source);
    if (!translated) continue;

    if (unit.type === "text") {
      const original = unit.node.data;
      const start = original.match(/^\s*/u)?.[0] || "";
      const end = original.match(/\s*$/u)?.[0] || "";
      unit.node.data = `${start}${translated}${end}`;
    } else {
      document(unit.node).attr(unit.attribute, translated);
    }
  }
}

function localizePage(document, route, language) {
  rewriteInternalLinks(document, language.code);
  preparePageChrome(document, route, language);
}

function preparePageChrome(document, route, language) {
  document("html").attr("lang", language.htmlLang);
  document("body").attr("data-site-locale", language.code);
  document(".site-language").remove();
  document('link[rel="canonical"], link[rel="alternate"][hreflang]').remove();

  const head = document("head");
  head.append(
    `<link rel="canonical" href="${escapeAttribute(absolutePageUrl(language.code, route))}">`,
  );
  for (const available of languages) {
    head.append(
      `<link rel="alternate" hreflang="${escapeAttribute(available.htmlLang)}" href="${escapeAttribute(absolutePageUrl(available.code, route))}">`,
    );
  }
  head.append(
    `<link rel="alternate" hreflang="x-default" href="${escapeAttribute(absolutePageUrl("en", route))}">`,
  );

  const selector = buildLanguageSelector(language.code, route);
  const mainContent = document(".main-content").first();
  if (mainContent.length) {
    mainContent.prepend(selector);
  } else {
    document("body").prepend(selector);
  }
  prepareTranslationNotice(document, route, language);

  document('script[data-site-language-routing="true"]').remove();
  document("body").append(buildLanguageScript());
}

function prepareTranslationNotice(document, route, language) {
  let notice = document(".translation-notice").first();
  if (!notice.length) {
    document(".site-language").first().after(buildTranslationNotice(route));
    notice = document(".translation-notice").first();
  }

  notice
    .find("a")
    .attr("href", localizedPath("en", route));
  if (language.code === "en") {
    notice.attr("hidden", "");
  } else {
    notice.removeAttr("hidden");
  }
}

function buildTranslationNotice(route) {
  return [
    '<aside class="translation-notice" data-no-localize hidden>',
    "<strong>Automatic translation</strong>",
    "<p>This page was translated automatically to improve accessibility and may contain errors. The English page is the authoritative version.</p>",
    `<a href="${escapeAttribute(localizedPath("en", route))}">Read the English original</a>`,
    "</aside>",
  ].join("");
}

function buildLanguageSelector(selectedCode, route) {
  const optionsMarkup = languages
    .map((language) => {
      const selected = language.code === selectedCode ? " selected" : "";
      const value = localizedPath(language.code, route);
      return `<option value="${escapeAttribute(value)}" data-language="${language.code}"${selected}>${escapeHtml(language.name)}</option>`;
    })
    .join("");

  return [
    '<div class="site-language" data-no-translate>',
    '<label for="site-language-select">Language</label>',
    `<select id="site-language-select" aria-label="Choose language">${optionsMarkup}</select>`,
    "</div>",
  ].join("");
}

function buildLanguageScript() {
  const supported = JSON.stringify(
    targetLanguages.map(({ code }) => code),
  ).replace(/</g, "\\u003c");
  return `<script data-site-language-routing="true" data-no-translate>
(() => {
  const select = document.getElementById("site-language-select");
  if (!select) return;
  const storageKey = "film-restoration-language";
  select.addEventListener("change", () => {
    const option = select.options[select.selectedIndex];
    try { localStorage.setItem(storageKey, option.dataset.language); } catch {}
    window.location.assign(option.value);
  });
  if (document.body.dataset.siteLocale !== "en") return;
  let saved = null;
  try { saved = localStorage.getItem(storageKey); } catch {}
  if (saved) return;
  const supported = ${supported};
  const preferred = (navigator.languages || [navigator.language])
    .map((value) => String(value || "").toLowerCase().split("-")[0])
    .find((value) => supported.includes(value));
  if (!preferred) return;
  const option = [...select.options].find((item) => item.dataset.language === preferred);
  if (option) window.location.replace(option.value);
})();
</script>`;
}

function rewriteInternalLinks(document, locale) {
  document("a[href]").each((_, anchor) => {
    const selection = document(anchor);
    if (
      selection.closest("[data-no-translate], [data-no-localize]").length
    ) {
      return;
    }
    const href = selection.attr("href");
    if (!href || !href.startsWith(basePath)) return;

    const [withoutFragment, fragment = ""] = href.split("#", 2);
    const [pathname, query = ""] = withoutFragment.split("?", 2);
    const relative = pathname.slice(basePath.length);
    if (!isPagePath(relative)) return;

    const localized = `${basePath}/${locale}${relative.startsWith("/") ? "" : "/"}${relative}`;
    selection.attr(
      "href",
      `${localized}${query ? `?${query}` : ""}${fragment ? `#${fragment}` : ""}`,
    );
  });
}

function isPagePath(relativePath) {
  if (!relativePath || relativePath === "/") return true;
  const extension = path.posix.extname(relativePath);
  return extension === "" || extension === ".html";
}

function routeForFile(relativeFile) {
  if (relativeFile === "index.html") return "/";
  if (relativeFile.endsWith("/index.html")) {
    return `/${relativeFile.slice(0, -"index.html".length)}`;
  }
  return `/${relativeFile}`;
}

function localizedPath(locale, route) {
  if (locale === "en") return `${basePath}${route}`;
  return `${basePath}/${locale}${route}`;
}

function absolutePageUrl(locale, route) {
  return `${siteOrigin}${localizedPath(locale, route)}`;
}

function normalizeBasePath(value) {
  const normalized = `/${value}`.replace(/\/+/g, "/").replace(/\/$/, "");
  return normalized === "/" ? "" : normalized;
}

function cacheKey(locale, value) {
  return createHash("sha256")
    .update(`${locale}\0${value}`)
    .digest("hex");
}

async function readCache() {
  try {
    return JSON.parse(await readFile(cacheFile, "utf8"));
  } catch (error) {
    if (error.code === "ENOENT") return {};
    throw error;
  }
}

async function saveCache(cache) {
  const temporary = `${cacheFile}.tmp`;
  await writeFile(temporary, `${JSON.stringify(cache, null, 2)}\n`, "utf8");
  await rm(cacheFile, { force: true });
  await rename(temporary, cacheFile);
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}

function toPosix(value) {
  return value.split(path.sep).join("/");
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}
