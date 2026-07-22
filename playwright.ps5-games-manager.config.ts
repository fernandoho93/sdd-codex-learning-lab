import { defineConfig, devices } from '@playwright/test';
import path from 'node:path';

const python = process.platform === 'win32'
  ? '.venv\\Scripts\\python.exe'
  : '.venv/bin/python';

const database = path.join(
  process.cwd(),
  'test-results',
  `ps5-games-${process.pid}.sqlite3`,
);

export default defineConfig({
  testDir: './tests-e2e/ps5-games-manager',
  testMatch: '**/*.spec.ts',
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 2 : 0,
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report/ps5-games-manager', open: 'never' }],
  ],
  outputDir: 'test-results/ps5-games-manager',
  use: {
    baseURL: 'http://127.0.0.1:8875',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium-desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'chromium-mobile', use: { ...devices['Pixel 5'] } },
  ],
  webServer: {
    command: `${python} -m ps5_games_manager --host 127.0.0.1 --port 8875`,
    url: 'http://127.0.0.1:8875',
    reuseExistingServer: false,
    timeout: 30_000,
    env: {
      ...process.env,
      PS5_GAMES_DB_PATH: database,
      RAWG_API_KEY: '',
    },
  },
});
