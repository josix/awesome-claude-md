# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Cloudflare Workers SDK** monorepo containing tools and libraries for developing, testing, and deploying serverless applications on Cloudflare's edge network. The main components are Wrangler (CLI), Miniflare (local dev simulator), and Create Cloudflare (project scaffolding).

## Development Commands

**Package Management:**
- Use `pnpm` - never use npm or yarn
- `pnpm install` - Install dependencies for all packages
- `pnpm build` - Build all packages (uses Turbo for caching)

**Testing:**
- `pnpm test:ci` - Run tests in CI mode
- `pnpm test:e2e` - Run end-to-end tests (requires Cloudflare credentials)

**Code Quality:**
- `pnpm check` - Run all checks (lint, type, format)
- `pnpm fix` - Auto-fix linting issues and format code

**Working with Specific Packages:**
- `pnpm run build --filter <package-name>` - Build specific package
- `pnpm run test:ci --filter <package-name>` - Test specific package

## Architecture Overview

**Core Tools:**
- `packages/wrangler/` - Main CLI tool for Workers development and deployment
- `packages/miniflare/` - Local development simulator powered by workerd runtime
- `packages/create-cloudflare/` - Project scaffolding CLI (C3)

**Development & Testing:**
- `packages/vitest-pool-workers/` - Vitest integration for testing Workers in actual runtime
- `packages/chrome-devtools-patches/` - Modified Chrome DevTools for Workers debugging

**Shared Libraries:**
- `packages/pages-shared/` - Code shared between Wrangler and Cloudflare Pages
- `packages/workers-shared/` - Code shared between Wrangler and Workers Assets

**Build System:**
- Turbo (turborepo) orchestrates builds across packages
- TypeScript compilation with custom configurations per package
- Rollup/esbuild for bundling
- Vitest for testing

## Key Workflows

**Development:**
1. Run `pnpm install` to install dependencies
2. Run `pnpm build` to build all packages
3. Use `pnpm run dev --filter <package>` for watch mode development
4. Run `pnpm check` before committing

**Testing:**
1. Unit tests run with Vitest
2. Integration tests simulate real Workers environment
3. E2E tests deploy to actual Cloudflare infrastructure
4. Use `pnpm test:ci --filter <package>` for focused testing

**Publishing:**
- Changesets manage versioning and publishing
- CI automatically publishes on PR merge
- Beta releases available via `beta` dist-tag

## Important Notes

- **Never use npm/yarn** - This repository requires pnpm for proper workspace management
- **Cloudflare credentials** needed for E2E tests - set `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`
- **Node.js version** - Use Node.js 18+ (specified in .nvmrc)
- **Build caching** - Turbo provides intelligent caching across packages

## Package Structure

Each package follows consistent patterns:
- `package.json` - Dependencies and scripts
- `tsconfig.json` - TypeScript configuration
- `vitest.config.ts` - Test configuration
- `src/` - Source code
- `test/` - Test files
- `dist/` - Built output (git-ignored)

## Debugging

- Use `--verbose` flag on pnpm commands for detailed output
- Enable debug logging: `DEBUG=* pnpm <command>`
- Chrome DevTools integration available for Workers debugging
- Source maps preserved for production debugging