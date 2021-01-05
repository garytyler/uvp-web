/* eslint-disable @typescript-eslint/no-var-requires */
const { preserveFunctionNamesWithTerser } = require("typesafe-vuex/helpers");

module.exports = {
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === "production") {
      preserveFunctionNamesWithTerser(config);
    }
  },
  devServer: {
    proxy: {
      "/api/": {
        target: "http://backend:80",
        https: true,
      },
      "/ws/": {
        target: "ws://backend:80",
        secure: false,
        ws: true,
      },
    },
  },
};
