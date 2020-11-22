it("Home page", async () => {
  await page.goto("https://localhost/");
  await expect(page).toHaveText("[Home]");
});

it("non-existent feature is not found", async () => {
  await page.goto("https://localhost/live/qpwomqpmviemg");
  await expect(page).toHaveText("Feature not found.");
});
