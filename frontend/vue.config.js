/* eslint-disable @typescript-eslint/no-var-requires */
const { preserveFunctionNamesWithTerser } = require("typesafe-vuex/helpers");

module.exports = {
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === "production") {
      preserveFunctionNamesWithTerser(config);
    }
  },
  devServer: {
    disableHostCheck: process.env.NODE_ENV !== "production",
  },
};
