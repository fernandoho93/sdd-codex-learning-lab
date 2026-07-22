import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests-e2e/demoqa',
  testMatch: '**/*.spec.ts',
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 2 : 0,
  timeout: 30_000,
  expect: {
    timeout: 7_500,
  },
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report/demoqa', open: 'never' }],
  ],
  outputDir: 'test-results/demoqa',
  use: {
    baseURL: 'https://demoqa.com',
    actionTimeout: 10_000,
    navigationTimeout: 20_000,
    trace: 'retain-on-first-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium-demoqa',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
