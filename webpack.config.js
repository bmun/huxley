var path = require("path");
var webpack = require("webpack");

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");

var package = require("./package.json");

var JS_ROOT = path.join(__dirname, "huxley/www/js");
var STATIC_ROOT = path.join(__dirname, "huxley/www/static/js");

const marked = require("marked");
const renderer = new marked.Renderer();

var plugins = [
  new webpack.EnvironmentPlugin(["NODE_ENV"]),
  new MiniCssExtractPlugin({ filename: "huxley.css" }),
];

module.exports = {
  entry: {
    huxley: path.join(JS_ROOT, "entry.js"),
    vendor: Object.keys(package.dependencies),
  },
  output: {
    path: STATIC_ROOT,
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            plugins: ["@babel/plugin-proposal-object-rest-spread", '@babel/plugin-proposal-class-properties'],
            presets: ["@babel/preset-env", "@babel/preset-react"],
          },
        },
      },
      {
        test: /\.less$/,
        exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "less-loader",
        ],
      },
      {
        test: /\.md$/,
        use: [
          { loader: "html-loader" },
          {
            loader: "markdown-loader",
            options: {
              pedantic: true,
              renderer,
            },
          },
        ],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        exclude: /node_modules/,
        use: [
          {loader: "url-loader"},
        ]
      },
    ],
  },
  plugins: plugins,
  resolve: {
    modules: ["node_modules", JS_ROOT],
    fallback: {
      "path": require.resolve("path-browserify"),
      "crypto": require.resolve("crypto-browserify"),
      "buffer": require.resolve("buffer/"),
      "stream": require.resolve("stream-browserify")
    }
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        extractComments: false,
      }),
    ]
  },
  // optimization: {
  //   runtimeChunk: "single", // enable "runtime" chunk
  //   splitChunks: {
  //     cacheGroups: {
  //       vendor: {
  //         test: /[\\/]node_modules[\\/]/,
  //         chunks: "all",
  //       },
  //     },
  //   },
  // },
  mode: process.env.NODE_ENV,
};
