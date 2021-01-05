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
  const userName = faker.name.findName();
  const guestName = faker.name.findName();
  const userEmail = faker.internet.exampleEmail();
  const userPassword = faker.internet.password();
  const featureTitle = faker.commerce.productName();
  const featureSlug = faker.lorem.slug();

  const baseUrl = "http://localhost";

  const browser = await chromium.launch({ ignoreHTTPSErrors: true });
  const page = await browser.newPage();

  await page.goto(baseUrl);
  await page.click("//a[normalize-space(.)='Sign up']");
  await page.click('input[type="text"]');
  await page.fill('input[type="text"]', userName);
  await page.press('input[type="text"]', "Tab");
  await page.fill('input[type="email"]', userEmail);
  await page.press('input[type="email"]', "Tab");
  await page.fill('input[type="password"]', userPassword);
  await page.press('input[type="password"]', "Tab");
  await page.fill(
    "//div[normalize-space(.)='Confirm Password']" +
      "/input[normalize-space(@type)='password']",
    userPassword
  );
  await Promise.all([
    page.waitForNavigation(),
    page.click("text=/.*Submit.*/"),
  ]);
  await page.screenshot({
    path: ".pw_screens/1_created_account_login_screen.png",
  });

  expect(page.url()).toContain("/login");

  // Login to new user account
  await page.click('input[name="login"]');
  await page.fill('input[name="login"]', userEmail);
  await page.press('input[name="login"]', "Tab");
  await page.fill('input[name="password"]', userPassword);
  await page.screenshot({ path: ".pw_screens/2_filled_out_login_info.png" });
  await Promise.all([
    page.waitForNavigation(),
    page.click("//button/span[normalize-space(.)='Login']"),
  ]);
  await page.screenshot({ path: ".pw_screens/3_logged_in.png" });

  expect(await page.$(`:text("Welcome ${userName}"):visible`)).toBeTruthy();

  await Promise.all([
    page.waitForNavigation(),
    page.click('text="Create New Feature"'),
  ]);
  await page.click('input[type="text"]');
  await page.fill('input[type="text"]', featureTitle);
  await page.press('input[type="text"]', "Tab");
  await page.fill(
    "//div[normalize-space(.)='Slug']/input[normalize-space(@type)='text']",
    featureSlug
  );
  await page.click("//span[normalize-space(.)='Create']");
  await page.goto(`${baseUrl}/live/${featureSlug}`);
  await page.goto(`${baseUrl}/live/${featureSlug}/lobby`);
  await page.click(`div[role="document"] >> text="${featureTitle}"`);

  expect(await page.$(`:text("${featureTitle}"):visible`)).toBeTruthy();

  await page.click('input[type="text"]');
  await page.fill('input[type="text"]', guestName);

  await captureNycCoverage(page);

  await page.close();
  await browser.close();
});
