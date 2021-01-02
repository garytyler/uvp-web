module.exports = {
  contextOptions: {
    ignoreHTTPSErrors: true,
  },
  browsers: ["chromium"],
  collectCoverage: true,
  collectCoverageFrom: ["src/**/*.{js,jsx,vue,ts,tsx}"],
  // coverageProvider: "v8",
};
