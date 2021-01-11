// Jest configuration specific to the E2E tests
// (separated from regular jest.config.js used for unit tests)
// See https://jestjs.io/docs/en/configuration for more information about these options

module.exports = {
  testMatch: ["**/tests/e2e/**/*.spec.(js|ts)"],
  testTimeout: 30000,
  transform: {
    "^.+\\.ts$": "ts-jest",
  },
  testEnvironment: "node",
};
