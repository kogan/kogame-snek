// load the needed node modules
var path = require("path");

// webpack project settings
module.exports = {
  context: path.join(__dirname, 'src'),
  entry: {
    main: './index',
  },
  resolve: {
    // Allow absolute paths in imports, e.g. import Button from 'components/Button'
    // Keep in sync with .eslintrc
    modules: [
      path.resolve(__dirname, 'src'),
      path.resolve(__dirname, 'node_modules'),
    ],
    extensions: ['.js', '.jsx'],
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['env', 'react', 'stage-2']
          }
        }
      }
    ]
  },
  output: {
    path: path.resolve('./static/js/'),
    filename: "[name].js"
  },
}
