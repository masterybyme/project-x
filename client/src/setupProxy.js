const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:5000",
      changeOrigin: true, // Keep this line
      secure: false,
      logLevel: "debug", // This will help us see more detailed logs
      pathRewrite: {
        "^/api": "",
      },
    })
  );
};
