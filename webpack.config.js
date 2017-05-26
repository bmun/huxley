
var path = require('path');
var webpack = require('webpack');

var ExtractTextPlugin = require('extract-text-webpack-plugin');

var package = require('./package.json');

var JS_ROOT = path.join(__dirname, 'huxley/www/js');
var STATIC_ROOT = path.join(__dirname, 'huxley/www/static/js');

const marked = require("marked");
const renderer = new marked.Renderer();

var plugins = [
  new webpack.EnvironmentPlugin([
    'NODE_ENV',
  ]),
  new ExtractTextPlugin('huxley.css'),
  new webpack.optimize.CommonsChunkPlugin({
    name: 'vendor',
    filename: 'vendor.js',
  }),
];
if (process.env.NODE_ENV === 'production') {
  plugins.push(
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false,
      },
      mangle: true,
    })
  );
}

module.exports = {
  entry: {
    huxley: path.join(JS_ROOT, 'entry.js'),
    vendor: Object.keys(package.dependencies),
  },
  output: {
    path: STATIC_ROOT,
    filename: '[name].js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            plugins: ['transform-object-rest-spread'],
            presets: ['es2015', 'es2017', 'react'],
          }
        },
      },
      {
        test: /\.less$/,
        exclude: /node_modules/,
        use: ExtractTextPlugin.extract({
          use: [
            {loader: 'css-loader'},
            {loader: 'less-loader'},
          ],
          fallback: 'style-loader',
        }),
      },
      {
        test: /\.md$/,
        use: [
          {loader: "html-loader"},
          {
            loader: "markdown-loader",
            options: {
              pedantic: true,
              renderer
            }
          }
        ]
      },
    ],
  },
  plugins: plugins,
  resolve: {
    modules: ['node_modules', JS_ROOT],
  },
};
