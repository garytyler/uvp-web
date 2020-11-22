module.exports = {
  preset: "@vue/cli-plugin-unit-jest/presets/typescript-and-babel",
  testMatch: ["**/tests/unit/**/*.spec.(js|ts)"],
  moduleNameMapper: {
    "\\.(css|less)$": "identity-obj-proxy",
  },
};
