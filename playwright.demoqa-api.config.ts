import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests-api/demoqa',
  testMatch: '**/*.spec.ts',
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 2 : 0,
  timeout: 30_000,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report/demoqa-api', open: 'never' }],
  ],
  outputDir: 'test-results/demoqa-api',
  use: {
    baseURL: 'https://demoqa.com',
    extraHTTPHeaders: {
      Accept: 'application/json',
    },
  },
  projects: [
    {
      name: 'api-demoqa',
    },
  ],
});
