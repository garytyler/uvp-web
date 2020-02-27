module.exports = {
  outputDir: "./dist/",
  assetsDir: "static",
  // baseUrl: process.env.NODE_ENV === 'production'
  // ? 'http://cdn123.com'
  // : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  devServer: {
    // https: true
    disableHostCheck: true,
    // public: "gt.ngrok.io"
    proxy: {
      "/api*": {
        // Forward frontend dev server request for /api to django dev server
        // target: process.env.BACKEND_URL_BASENAME
        target: `http://${process.env.BACKEND_URL_BASENAME}/`
      },
      "/ws*": {
        // Forward frontend dev server request for /ws to django dev server
        // target: "ws://localhost:8000/"
        target: `ws://${process.env.BACKEND_URL_BASENAME}/`,
        // target: process.env.BACKEND_URL_BASENAME,
        ws: true
      }
    }
  },
  // vuejs configuration
  transpileDependencies: ["vuetify"]
};
