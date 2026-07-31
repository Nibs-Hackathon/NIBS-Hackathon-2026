# Folder: frontend/e2e Code Inventory

Generated: 2026-07-27T04:24:37 UTC

**Folder path:** `frontend/e2e`

Contains 1 project file(s) directly in this folder (nested folders have their own inventory files).

## frontend/e2e/workspaces.spec.js

**Folder path:** `frontend/e2e`

**File path:** `frontend/e2e/workspaces.spec.js`

```javascript
import { test, expect } from '@playwright/test';

/**
 * Epic 6 — smoke: each workspace mounts a focused hero heading.
 * Uses production preview build (no live backend required for chrome).
 */

const workspaces = [
  { path: '/', heading: /command center/i },
  { path: '/assets', heading: /critical assets/i },
  { path: '/incident-simulator', heading: /incident center/i },
  { path: '/agent-monitor', heading: /ai investigation/i },
  { path: '/maintenance', heading: /^maintenance$/i },
  { path: '/health-prediction', heading: /health forecasting/i },
  { path: '/reports', heading: /executive reports/i },
];

test.describe('RigOS workspace smoke', () => {
  for (const workspace of workspaces) {
    test(`${workspace.path} renders hero`, async ({ page }) => {
      await page.goto(workspace.path);
      const heading = page.locator('.product-hero h1');
      await expect(heading).toBeVisible({ timeout: 30_000 });
      await expect(heading).toHaveText(workspace.heading);
    });
  }

  test('skip link targets main content', async ({ page }) => {
    await page.goto('/');
    const skip = page.locator('.e6-skip-link');
    await expect(skip).toHaveAttribute('href', '#main-content');
    await expect(page.locator('#main-content')).toHaveCount(1);
  });

  test('alias redirects resolve', async ({ page }) => {
    await page.goto('/incidents');
    await expect(page).toHaveURL(/incident-simulator/);
    await page.goto('/forecasting');
    await expect(page).toHaveURL(/health-prediction/);
  });
});
```
