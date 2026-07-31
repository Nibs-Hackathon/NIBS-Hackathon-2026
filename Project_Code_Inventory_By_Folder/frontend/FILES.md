# Folder: frontend Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend`

Contains 8 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/.gitignore

**Folder path:** `frontend`

**File path:** `frontend/.gitignore`

```
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local
.env
.env.*
!.env.example
test-results
playwright-report
blob-report

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
```

## frontend/eslint.config.js

**Folder path:** `frontend`

**File path:** `frontend/eslint.config.js`

```javascript
import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
])
```

## frontend/index.html

**Folder path:** `frontend`

**File path:** `frontend/index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

## frontend/package.json

**Folder path:** `frontend`

**File path:** `frontend/package.json`

```json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "test:e2e": "npm run build && playwright test",
    "test:e2e:ui": "playwright test --ui"
  },
  "dependencies": {
    "@emotion/react": "^11.14.0",
    "@emotion/styled": "^11.14.1",
    "@mui/icons-material": "^9.2.0",
    "@mui/material": "^9.2.0",
    "animejs": "^4.5.0",
    "axios": "^1.18.1",
    "motion": "^12.42.2",
    "react": "^19.2.7",
    "react-dom": "^19.2.7",
    "react-hot-toast": "^2.6.0",
    "react-router-dom": "^7.18.1"
  },
  "devDependencies": {
    "@eslint/js": "^10.0.1",
    "@playwright/test": "^1.62.0",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^6.0.3",
    "eslint": "^10.6.0",
    "eslint-plugin-react-hooks": "^7.1.1",
    "eslint-plugin-react-refresh": "^0.5.3",
    "globals": "^17.7.0",
    "vite": "^8.1.1"
  }
}
```

## frontend/PERFORMANCE.md

**Folder path:** `frontend`

**File path:** `frontend/PERFORMANCE.md`

```markdown
# Epic 6 — Frontend performance budget

## Targets

| Metric | Target |
|--------|--------|
| Vite `chunkSizeWarningLimit` | 450 KB |
| Route workspace chunk (gzip) | ~150 KB |
| First paint | Command Center shell + mission chunk |

## Implemented

- **Lazy routes:** each workspace view is a separate chunk under `src/redesign/views/`
- **Vendor split:** `vendor-react`, `vendor-mui`, `vendor-motion`, `vendor-utils`
- **CSS trim:** dropped unused legacy sheets (`mission-control`, `incidents`, `investigation`, `operations-v2`, `refinery-twin`)
- **Deps trim:** removed `@mui/lab`, `socket.io-client`
- **Tokens:** new UI should use `design-system/tokens.js` + `catalog.css`; `product.css` remains shell chrome

## Measure

```bash
npm run build
```

Inspect `dist/assets/*` sizes after each release.
```

## frontend/playwright.config.js

**Folder path:** `frontend`

**File path:** `frontend/playwright.config.js`

```javascript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 60_000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: 'list',
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4173',
    trace: 'on-first-retry',
  },
  webServer: process.env.PLAYWRIGHT_BASE_URL
    ? undefined
    : {
        command: 'npm run preview -- --host 127.0.0.1 --port 4173',
        url: 'http://127.0.0.1:4173',
        reuseExistingServer: false,
        timeout: 120_000,
      },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
```

## frontend/README.md

**Folder path:** `frontend`

**File path:** `frontend/README.md`

```markdown
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
```

## frontend/vite.config.js

**Folder path:** `frontend`

**File path:** `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const apiTarget = process.env.VITE_API_PROXY || 'http://127.0.0.1:8080';
const wsTarget = process.env.VITE_WS_PROXY || 'ws://127.0.0.1:8080';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: apiTarget,
        changeOrigin: true,
      },
      '/ws': {
        target: wsTarget,
        ws: true,
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    // Epic 6 performance budget — warn above this; prefer route chunks under ~150kb gzip
    chunkSizeWarningLimit: 450,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return undefined;
          if (id.includes('react-dom') || id.includes('/react/') || id.includes('react-router')) {
            return 'vendor-react';
          }
          if (id.includes('@mui') || id.includes('@emotion')) {
            return 'vendor-mui';
          }
          if (id.includes('motion') || id.includes('animejs')) {
            return 'vendor-motion';
          }
          if (id.includes('axios') || id.includes('react-hot-toast')) {
            return 'vendor-utils';
          }
          return 'vendor';
        },
      },
    },
  },
})
```
