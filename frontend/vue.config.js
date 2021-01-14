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
        target: `http://${process.env.VUE_APP_DEV_PROXY_API_HOST}`,
        https: true,
      },
      "/ws/": {
        target: `ws://${process.env.VUE_APP_DEV_PROXY_API_HOST}`,
        secure: false,
        ws: true,
      },
    },
  },
};
