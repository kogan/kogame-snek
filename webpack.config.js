// load the needed node modules
var path = require("path");

// webpack project settings
module.exports = {
  context: path.join(__dirname, 'src'),
  entry: {
    main: './index',
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
