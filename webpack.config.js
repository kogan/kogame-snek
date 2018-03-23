// load the needed node modules
const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const webpack = require('webpack')

const extractSass = new MiniCssExtractPlugin({
  filename: '[name].css',
  chunkFilename: '[id].css',
})

// webpack project settings
module.exports = (env, argv) => ({
  context: path.join(__dirname, 'src'),
  entry: [
    'babel-polyfill',
    path.join(__dirname, 'src/index.jsx'),
    path.join(__dirname, 'assets/scss/main.scss'),
  ],
  devtool: 'inline-source-map',
  output: {
    path: path.resolve(__dirname, 'static/build'),
    publicPath: '/static/build',
    pathinfo: argv.mode === 'production',
    filename: '[name].js?[hash:8]',
    chunkFilename: '[name].js?[hash:8][chunkhash:8]',
    // Point sourcemap entries to original disk location (format as URL on Windows)
    devtoolModuleFilenameTemplate: info =>
      path.resolve(info.absoluteResourcePath).replace(/\\/g, '/'),
  },
  resolve: {
    // Allow absolute paths in imports, e.g. import Button from 'components/Button'
    // Keep in sync with .eslintrc
    modules: [
      path.resolve(__dirname, 'src'),
      path.resolve(__dirname, 'assets/scss'),
      path.resolve(__dirname, 'assets/img'),
      path.resolve(__dirname, 'node_modules'),
    ],
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    extractSass,
    new webpack.DefinePlugin({
      'process.env.NODE_ENV_STRING': argv.mode === 'production' ? '"development"' : '"production"',
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
      'process.env.DEBUG': JSON.stringify(process.env.DEBUG),
      'process.env.BROWSER': true,
      __DEV__: argv.mode === 'production',
    }),
  ],
  module: {
    // Make missing exports an error instead of warning
    strictExportPresence: true,
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['env', 'react', 'stage-2'],
          },
        },
      },

      // Rules for Style Sheets
      {
        test: /\.(scss|sass)$/,
        include: [path.resolve(__dirname, 'src'), path.resolve(__dirname, 'assets/scss')],
        use: [
          { loader: 'style-loader', options: { sourceMap: argv.mode === 'production' } },
          // MiniCssExtractPlugin.loader,
          // Process internal/project styles (from assets/scss folder)
          {
            loader: 'css-loader',
            options: {
              // CSS Loader https://github.com/webpack/css-loader
              importLoaders: 2,
              sourceMap: argv.mode === 'production',
              // CSS Modules https://github.com/css-modules/css-modules
              modules: true,
              localIdentName: argv.mode === 'production'
                ? '[name]-[local]-[hash:base64:5]'
                : '[hash:base64:5]',
            },
          },
          { loader: 'sass-loader', options: { sourceMap: argv.mode === 'production' } },
        ],
      },
    ],
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        js: {
          test: /\.js$/,
          name: 'main',
          chunks: 'all',
        },
        css: {
          test: /\.(css|sass|scss)$/,
          name: 'main',
          chunks: 'all',
        },
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },
})
