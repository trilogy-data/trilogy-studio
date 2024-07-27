import { _electron as electron } from "playwright";
import { test, expect, ElectronApplication, Page } from "@playwright/test";

test.describe("All Tests", async () => {
  let electronApp: ElectronApplication;
  let firstWindow: Page;

  test.beforeAll(async () => {
    const electronApp = await electron.launch({ args: ["."] });
    const firstWindow = await electronApp.firstWindow();
    firstWindow.setViewportSize({ width: 1280, height: 720 });
  });

  test("Starts", async () => {
    await expect(await firstWindow.title()).toContain('Trilogy Studio');
  });

  test.afterAll(async () => {
    if (electronApp) {
      await electronApp.close();
    }
  });
});
