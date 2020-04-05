module.exports = {
  assetsDir: "static",
  outputDir: "./dist/",
  configureWebpack: {
    devtool: "source-map",
    // baseUrl: process.env.NODE_ENV === 'production'
    // ? 'http://cdn123.com'
    // : '/',
    // For Production, replace set baseUrl to CDN
    // And set the CDN origin to `yourdomain.com/static`
    // Whitenoise will serve once to CDN which will then cache
    // and distribute
    devServer: {
      inline: true,
      disableHostCheck: true,
      proxy: {
        "/api/*": {
          target: `http://${process.env.BACKEND_URL_BASENAME}/`,
          changeOrigin: true,
        },
        "/ws/*": {
          target: `ws://${process.env.BACKEND_URL_BASENAME}/`,
          changeOrigin: true,
          ws: true,
        },
      },
    },
  },
  // vuejs configuration
  transpileDependencies: ["vuetify"],
};
