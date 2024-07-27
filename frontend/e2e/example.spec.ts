import { test, expect } from '@playwright/test';
import { _electron } from 'playwright';

test('App launches and quits', async () => {
  const app = await _electron.launch({args: ['dist-electron/main.js']});
  const window = await app.firstWindow();
  window.setViewportSize({ width: 1280, height: 720 });
  await expect(await window.title()).toContain('Trilogy Studio');
  await app.close();
});