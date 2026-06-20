#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const installSh = path.join(root, "scripts", "install.sh");

function usage() {
  console.log(`agent-sage — SDLC skills for Cursor, Claude Code, and Codex

Usage:
  sage install [--all | --cursor | --claude | --codex]
  sage init [DIR] [--no-agents-md | --copy-agents-md]
  sage status
  sage uninstall

Examples:
  npx agent-sage install --all    Global skills + ~/.sage
  sage init                         Bootstrap ./runs/ in current project
  sage init ../my-app --no-agents-md

Requires: bash, python3`);
}

function buildInitArgs(rest) {
  const flags = rest.filter((arg) => arg.startsWith("--"));
  const dirs = rest.filter((arg) => !arg.startsWith("--"));
  return ["--project", dirs[0] || ".", ...flags];
}

function main() {
  const argv = process.argv.slice(2);

  if (argv.length === 0 || argv[0] === "--help" || argv[0] === "-h") {
    usage();
    process.exit(argv.length === 0 ? 1 : 0);
  }

  const [cmd, ...rest] = argv;
  let args;

  switch (cmd) {
    case "install":
      args = rest.length === 0 ? [] : rest;
      break;
    case "init":
      args = buildInitArgs(rest);
      break;
    case "status":
      args = ["--status"];
      break;
    case "uninstall":
      args = ["--uninstall"];
      break;
    default:
      args = [cmd, ...rest];
      break;
  }

  if (!existsSync(installSh)) {
    console.error(`install.sh not found at ${installSh}`);
    process.exit(1);
  }

  const result = spawnSync("bash", [installSh, ...args], {
    stdio: "inherit",
    cwd: process.cwd(),
    env: process.env,
  });

  process.exit(result.status ?? 1);
}

main();
