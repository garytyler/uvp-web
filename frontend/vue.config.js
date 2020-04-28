/* eslint-disable @typescript-eslint/no-var-requires */
const { preserveFunctionNamesWithTerser } = require("typesafe-vuex/helpers");
const fs = require("fs");

module.exports = {
  configureWebpack: (config) => {
    if (process.env.NODE_ENV === "production") {
      preserveFunctionNamesWithTerser(config);
    } else if (process.env.NODE_ENV === "development") {
      // config.devtool = "source-map";
      // const useSsl = ["SSL_KEY_FILE", "SSL_CERT_FILE"].every(
      //   (v) => process.env[v] !== "null"
      // );
      // config.devServer = {
      // public: process.env.PUBLIC_HOSTNAME,
      // public: "0.0.0.0:8080",
      //     proxy: {
      //       "/api/*": {
      //         target: `${useSsl ? "https" : "http"}://${
      //           process.env.API_HOSTNAME
      //         }`,
      //       },
      //       "/ws/*": {
      //         target: `${useSsl ? "wss" : "ws"}://${process.env.API_HOSTNAME}/`,
      //         ws: true,
      //       },
      //     },
      //   };
      //   if (useSsl) {
      //     config.devServer.https = {
      //       key: fs.readFileSync(process.env.SSL_KEY_FILE),
      //       cert: fs.readFileSync(process.env.SSL_CERT_FILE),
      //     };
      // };
    }
  },
};
