import { chromium } from "playwright";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const rootDir = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const catalogDir = path.join(rootDir, "catalog");
const previewDir = path.join(catalogDir, "previews");
const host = "127.0.0.1";

function parseArgs(argv) {
  const parsed = { starter: null };
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--starter") {
      parsed.starter = argv[index + 1];
      index += 1;
    }
  }
  return parsed;
}

async function readStarters() {
  const sitesDir = path.join(rootDir, "sites");
  const entries = await fs.readdir(sitesDir, { withFileTypes: true });
  const starters = [];
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const manifestPath = path.join(sitesDir, entry.name, "starter.manifest.json");
    try {
      const payload = JSON.parse(await fs.readFile(manifestPath, "utf8"));
      starters.push(payload);
    } catch {
      // Ignore directories that are not starter roots.
    }
  }
  starters.sort((left, right) => left.key.localeCompare(right.key));
  return starters;
}

function waitForExit(child) {
  return new Promise((resolve) => {
    child.once("exit", resolve);
  });
}

async function waitForUrl(url, attempts = 40) {
  for (let index = 0; index < attempts; index += 1) {
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (response.ok) return;
    } catch {
      // Server is still warming up.
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error(`Timed out waiting for ${url}`);
}

async function captureStarter(browser, starter, port) {
  const url = `http://${host}:${port}${starter.preview.path}`;
  const child = spawn(
    "bash",
    ["scripts/preview-starter.sh", starter.key],
    {
      cwd: rootDir,
      env: {
        ...process.env,
        PORT: String(port),
        HOST: host,
        RELOAD: "false",
      },
      stdio: "pipe",
    },
  );

  child.stdout.on("data", (chunk) => process.stdout.write(chunk));
  child.stderr.on("data", (chunk) => process.stderr.write(chunk));

  try {
    await waitForUrl(url);
    const page = await browser.newPage({ viewport: { width: 1440, height: 1024 } });
    await page.goto(url, { waitUntil: "networkidle" });
    await page.screenshot({
      path: path.join(previewDir, `${starter.key}.png`),
      fullPage: false,
    });
    await page.close();
    console.log(`Captured ${starter.key}`);
  } finally {
    child.kill("SIGTERM");
    await Promise.race([
      waitForExit(child),
      new Promise((resolve) => setTimeout(resolve, 3000)),
    ]);
    if (!child.killed) {
      child.kill("SIGKILL");
    }
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const starters = (await readStarters()).filter((starter) => !args.starter || starter.key === args.starter);
  if (!starters.length) {
    throw new Error("No starters matched the capture request.");
  }

  await fs.mkdir(previewDir, { recursive: true });
  const browser = await chromium.launch();
  try {
    for (const [index, starter] of starters.entries()) {
      await captureStarter(browser, starter, 4100 + index);
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
