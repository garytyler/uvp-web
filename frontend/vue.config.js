/* eslint-disable @typescript-eslint/no-var-requires */
const { preserveFunctionNamesWithTerser } = require("typesafe-vuex/helpers");
const fs = require("fs");

module.exports = {
  assetsDir: "static",
  outputDir: "./dist/",
  configureWebpack: config => {
    preserveFunctionNamesWithTerser(config);
    config.devtool = "source-map";
    config.devServer = {
      // inline: true,
      // disableHostCheck: true,
      https: {
        key: fs.readFileSync(process.env.SSL_KEYFILE),
        cert: fs.readFileSync(process.env.SSL_CERTFILE)
      },
      public: `${process.env.PUBLIC_URL_BASENAME}/`,
      proxy: {
        "/api/*": {
          target: `https://${process.env.BACKEND_URL_BASENAME}/`,
          changeOrigin: true
        },
        "/ws/*": {
          target: `wss://${process.env.BACKEND_URL_BASENAME}/`,
          changeOrigin: true,
          ws: true
        }
      }
    };
  }
};
