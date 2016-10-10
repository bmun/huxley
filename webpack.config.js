var path = require('path');
var webpack = require('webpack');

var JS_ROOT = path.join(__dirname, 'huxley/www/js');
var STATIC_ROOT = path.join(__dirname, 'huxley/www/static/js');

var plugins = [
  new webpack.EnvironmentPlugin([
    'NODE_ENV',
  ]),
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
  entry: path.join(JS_ROOT, 'entry.js'),
  output: {
    path: STATIC_ROOT,
    filename: 'bundle.js',
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          plugins: ['transform-object-rest-spread'],
          presets: ['es2015', 'es2017', 'react'],
        },
      },
    ],
  },
  plugins: plugins,
  resolve: {
    modulesDirectories: ['node_modules', JS_ROOT],
  },
};
