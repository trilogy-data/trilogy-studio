import { _electron as electron } from "playwright";
import { test, expect, ElectronApplication, Page } from "@playwright/test";

test.describe("All Tests", async () => {
  let electronApp: ElectronApplication;
  let firstWindow: Page;

  test.beforeAll(async () => {
    electronApp = await electron.launch({ args: ["."],
     });
    firstWindow = await electronApp.firstWindow();
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
