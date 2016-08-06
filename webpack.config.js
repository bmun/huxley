var webpack = require('webpack');

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
  entry: './huxley/www/static/js/huxley.browserify.js',
  output: {
    path: './huxley/www/static/js',
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
};
