const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CompressionPlugin = require("compression-webpack-plugin");

const typeScriptConfig = {
  entry: {
    'navigation': path.resolve(__dirname, 'homepage/static/ts/navigation.ts'),
    'blume': path.resolve(__dirname, 'homepage/static/ts/blume.ts'),
    'hook': path.resolve(__dirname, 'homepage/static/ts/hook.ts'),
    'book': path.resolve(__dirname, 'homepage/static/ts/book.ts'),
  },

  output: {
    path: path.resolve(__dirname, 'homepage/static/js/'),
    filename: '[name].min.js'
  },

  plugins: [
    new CleanWebpackPlugin(),
    new CompressionPlugin(),
  ],

  resolve: {
    extensions: [
      '.ts',
      '.js'
    ],
  },

  module: {
    rules: [
      {
        test: /\.tsx?/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
};

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const sassConfig = {
  entry: {
    'navigation':
      path.resolve(__dirname, 'homepage/static/scss/navigation.scss'),
    'footer':
      path.resolve(__dirname, 'homepage/static/scss/footer.scss'),
    'blume':
      path.resolve(__dirname, 'homepage/static/scss/blume.scss'),
    'landing':
      path.resolve(__dirname, 'homepage/static/scss/landing.scss'),
    'book':
      path.resolve(__dirname, 'homepage/static/scss/book.scss'),
    'ink':
      path.resolve(__dirname, 'homepage/static/scss/ink.scss'),
    'text':
      path.resolve(__dirname, 'homepage/static/scss/text.scss'),
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
  typeScriptConfig: typeScriptConfig,
  sassConfig: sassConfig
};
