
var path = require('path');
var webpack = require('webpack');

var ExtractTextPlugin = require('extract-text-webpack-plugin');

var JS_ROOT = path.join(__dirname, 'huxley/www/js');
var STATIC_ROOT = path.join(__dirname, 'huxley/www/static/js');

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
    vendor: [
      'classnames',
      'flux',
      'jquery',
      'jquery-ui',
      'js-cookie',
      'react',
      'react-dom',
      'react-modal',
      'react-router',
    ],
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
    ],
  },
  plugins: plugins,
  resolve: {
    modules: ['node_modules', JS_ROOT],
  },
};
