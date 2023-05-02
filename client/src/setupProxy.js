const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/",
    createProxyMiddleware({
      target:
        //needs to adjusted to port local adress
        //normal target: 'http://localhost:5000',
        "https://dr-sirm-fictional-acorn-5ppv6pp657vhvw5v-5000.preview.app.github.dev",
      changeOrigin: true,
      secure: false,
    })
  );
};
