// BASE_URL = process.env.BASE_URL ? process.env.BASE_URL : "https://localhost";
// const BASE_URL = "https://localhost:80";
const BASE_URL = "https://localhost";
// const BASE_URL = "http://frontend:8080";
// const BASE_URL = "https://172.17.0.1";
// const BASE_URL = "http://frontend:8080";
// const BASE_URL = "https://172.17.0.1";
// const BASE_URL = "https://frontend:8080";

it("Home page", async () => {
  await page.goto(`${BASE_URL}/`);
  await page.screenshot({ path: "screen.png" });
  // await expect(page).toHaveText("UVP Interactive");
});

it("non-existent feature is not found", async () => {
  await page.goto(`${BASE_URL}/live/asdfasdf`);
  await expect(page).toHaveText("404");
});
