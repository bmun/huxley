var path = require('path');
var webpack = require('webpack');

var JS_ROOT = path.join(__dirname, 'huxley/www/static/js');

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
  entry: path.join(JS_ROOT, 'huxley.browserify.js'),
  output: {
    path: JS_ROOT,
    filename: 'bundle.js',
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['es2015', 'react'],
        },
      },
    ],
  },
  plugins: plugins,
  resolve: {
    modulesDirectories: ['node_modules', path.join(JS_ROOT, 'huxley')],
  },
};
