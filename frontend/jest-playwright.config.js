// See https://github.com/smooth-code/jest-puppeteer for more information about these options

module.exports = {
  contextOptions: {
    ignoreHTTPSErrors: true,
  },
  setupFilesAfterEnv: ["expect-puppeteer"],
};
