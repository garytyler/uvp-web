module.exports = {
  presets: ["@vue/cli-plugin-babel/preset"],
  plugins: [
    [
      "istanbul",
      {
        useInlineSourceMaps: false,
        extension: [".js", ".cjs", ".mjs", ".ts", ".tsx", ".jsx", ".vue"],
      },
      "istanbul-plugin-custom-config", // unique name incase loaded twice
    ],
  ],
};
