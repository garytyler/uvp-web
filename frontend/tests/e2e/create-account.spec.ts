const { chromium, globals } = require("playwright");
const faker = require("faker");
const assert = require("assert");
const { userNameMaxLength, featureTitleMaxLength } = require("../../src/env");
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

const createFakeUserName = () =>
  faker.name.findName().substring(0, userNameMaxLength).trim();
const createFakeGuestName = () => faker.name.findName();
const createFakeUserEmail = () => faker.internet.exampleEmail();
const createFakeUserPassword = () => faker.internet.password();
const createFakeFeatureTitle = () =>
  faker.commerce.productName().substring(0, featureTitleMaxLength).trim();
const createFakeFeatureSlug = () => faker.lorem.slug();

it("Round trip user test", async () => {
  const userName = createFakeUserName();
  const guestName = createFakeGuestName();
  const userEmail = createFakeUserEmail();
  const userPassword = createFakeUserPassword();
  const featureTitle = createFakeFeatureTitle();
  const featureSlug = createFakeFeatureSlug();

  const baseUrl = "http://localhost:8080";

  const browser = await chromium.launch({ ignoreHTTPSErrors: true });
  const page = await browser.newPage();
  try {
    await page.goto(baseUrl);

    // Go to signup form
    await Promise.all([
      page.waitForNavigation({ url: `${baseUrl}/signup` }),
      page.click("//a[normalize-space(.)='Sign up']"),
    ]);

    // Fill out signup form
    await page.click("//div[normalize-space(.)='Name']");
    await page.keyboard.type(userName);
    await page.click("//div[normalize-space(.)='Email']");
    await page.keyboard.type(userEmail);
    await page.click("//div[normalize-space(.)='Password']");
    await page.keyboard.type(userPassword);
    await page.click("//div[normalize-space(.)='Confirm Password']");
    await page.keyboard.type(userPassword);

    // Submit signup form
    await Promise.all([
      page.waitForNavigation({ url: `${baseUrl}/login` }),
      page.click("//button[normalize-space(.)='Submit']"),
    ]);

    // Test redirect to login page
    await page.screenshot({
      path: ".pw_screens/login_screen.png",
    });
    expect(page.url()).toContain("/login");

    // Fill out login form
    await page.click("//div[normalize-space(.)='Email']");
    await page.keyboard.type(userEmail);
    await page.click("//div[normalize-space(.)='Password']");
    await page.keyboard.type(userPassword);
    await page.screenshot({ path: ".pw_screens/login_form_filled_out.png" });

    // Submit login form
    await Promise.all([
      page.waitForNavigation(),
      page.click("//button/span[normalize-space(.)='Login']"),
    ]);
    await page.screenshot({ path: ".pw_screens/logged_in_redirect_page.png" });

    // Test redirect to dashboard
    expect(await page.$(`:text("Welcome ${userName}"):visible`));

    // Go to 'create feature' form
    await Promise.all([
      page.waitForNavigation(),
      page.click('text="Create Feature"'),
    ]);

    // Fill out 'create feature' form
    await page.click("//div[normalize-space(.)='Title']");
    await page.keyboard.type(featureTitle);
    await page.click("//div[normalize-space(.)='Slug']");
    await page.keyboard.type(featureSlug);
    await page.click("//div[normalize-space(.)='Turn Duration']");
    await page.click('text="30 seconds"');

    await page.screenshot({
      path: ".pw_screens/create_feature_form_filled_out.png",
    });

    // Submit 'create feature' form
    await page.click("//span[normalize-space(.)='Create']");

    // Go to feature live page
    const featureLiveBaseUrl = `${baseUrl}/live/${featureSlug}`;
    await Promise.all([
      page.goto(featureLiveBaseUrl),
      page.waitForLoadState("load"),
      page.waitForNavigation({ url: `${featureLiveBaseUrl}/lobby` }),
    ]);

    // Test feature live page display
    await page.screenshot({ path: ".pw_screens/feature_live_page.png" });
    expect(await page.$(`:text("${featureTitle}"):visible`)).toBeTruthy();

    // Fill out 'guest' signin form
    await page.click("//div[normalize-space(.)='Your Name']");
    await page.keyboard.type(guestName);

    await captureNycCoverage(page);
  } finally {
    await page.close();
    await browser.close();
  }
});
