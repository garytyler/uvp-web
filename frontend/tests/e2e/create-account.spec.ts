const { chromium, globals } = require("playwright");
const faker = require("faker");
const {
  cleanMergeFiles,
  captureNycCoverage,
  mergeNycCoverage,
} = require("./coverage");

beforeAll(async () => {
  await cleanMergeFiles();
});

afterAll(async () => {
  await mergeNycCoverage();
});

it("Create account and login", async () => {
  const user_name = faker.name.findName();
  const user_email = faker.internet.exampleEmail();
  const user_password = faker.internet.password();

  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto("http://localhost");
  await page.click("//a[normalize-space(.)='Sign up']");
  await page.click('input[type="text"]');
  await page.fill('input[type="text"]', user_name);
  await page.press('input[type="text"]', "Tab");
  await page.fill('input[type="email"]', user_email);
  await page.press('input[type="email"]', "Tab");
  await page.fill('input[type="password"]', user_password);
  await page.press('input[type="password"]', "Tab");
  await page.fill(
    "//div[normalize-space(.)='Confirm Password']" +
      "/input[normalize-space(@type)='password']",
    user_password
  );
  await page.click("text=/.*Submit.*/");
  await page.waitForNavigation({ waitUntil: "load" });
  await page.screenshot({
    path: ".pw_screens/1_created_account_login_screen.png",
  });

  expect(page.url()).toContain("/login");

  // Login to new user account
  await page.click('input[name="login"]');
  await page.fill('input[name="login"]', user_email);
  await page.press('input[name="login"]', "Tab");
  await page.fill('input[name="password"]', user_password);
  await page.screenshot({ path: ".pw_screens/2_filled_out_login_info.png" });
  await page.click("//button/span[normalize-space(.)='Login']");
  await page.waitForNavigation({ waitUntil: "load" });
  await page.screenshot({ path: ".pw_screens/3_logged_in.png" });

  expect(await page.$(`:text("Welcome ${user_name}"):visible`)).toBeTruthy();

  await captureNycCoverage(page);

  await page.close();
  await browser.close();
});
