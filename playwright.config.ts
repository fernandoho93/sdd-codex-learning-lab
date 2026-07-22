import { defineConfig, devices } from '@playwright/test';
import path from 'node:path';

const python = process.platform === 'win32'
  ? '.venv\\Scripts\\python.exe'
  : '.venv/bin/python';
const dataFile = path.join(
  process.cwd(),
  'test-results',
  `e2e-experiments-${process.pid}.jsonl`,
);

export default defineConfig({
  testDir: './tests-e2e',
  testMatch: 'prompt-lab.spec.ts',
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 2 : 0,
  reporter: [['list'], ['html', { open: 'never' }]],
  outputDir: 'test-results/artifacts',
  use: {
    baseURL: 'http://127.0.0.1:8765',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: `${python} -m prompt_lab.web --host 127.0.0.1 --port 8765`,
    url: 'http://127.0.0.1:8765',
    reuseExistingServer: false,
    timeout: 30_000,
    env: {
      ...process.env,
      PROMPT_LAB_DATA_FILE: dataFile,
    },
  },
});
