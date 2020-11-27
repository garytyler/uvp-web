BASE_URL = process.env.BASE_URL ? process.env.BASE_URL : "https://localhost";

it("Home page", async () => {
  await page.goto(`${BASE_URL}/`);
  await expect(page).toHaveText("[Home]");
});

it("non-existent feature is not found", async () => {
  await page.goto(`${BASE_URL}/live/asdfasdf`);
  await expect(page).toHaveText("Feature not found.");
});
