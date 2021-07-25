const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const sassConfig = {
  entry: {
    'landing':
      path.resolve(__dirname, 'homepage/static/css/landing.scss'),
    'book':
      path.resolve(__dirname, 'homepage/static/css/book.scss'),
    'ink':
      path.resolve(__dirname, 'homepage/static/css/ink.scss'),
    'nav':
      path.resolve(__dirname, 'homepage/static/css/nav.scss'),
    'text':
      path.resolve(__dirname, 'homepage/static/css/text.scss'),
  },

  output: {
    path: path.resolve(__dirname, 'homepage/static/css/'),
    filename: '[name].js'
  },

  plugins: [
    new CleanWebpackPlugin(),
  ],

  module: {
    rules: [
      {
        test: /\.s[ac]ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              url: false,
              sourceMap: true,
            },
          },
          'sass-loader',
          'postcss-loader',
        ],
      },
    ],
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].min.css",
      chunkFilename: "[id].min.css",
    }),
  ],
};


module.exports = {
    sassConfig: sassConfig
};
