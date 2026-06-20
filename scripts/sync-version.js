#!/usr/bin/env node
/** Sync package.json version from install/VERSION (source of truth). */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const versionPath = path.join(root, "install", "VERSION");
const pkgPath = path.join(root, "package.json");

const version = fs.readFileSync(versionPath, "utf8").trim();
const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));

if (pkg.version !== version) {
  pkg.version = version;
  fs.writeFileSync(pkgPath, `${JSON.stringify(pkg, null, 2)}\n`);
  console.log(`Synced package.json version → ${version}`);
}
