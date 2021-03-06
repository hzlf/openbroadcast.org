require("@babel/polyfill");

const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const StyleLintPlugin = require('stylelint-webpack-plugin');
const path = require('path');

const DEV_MODE = process.env.NODE_ENV !== 'production';

// points to STATIC_ROOT configured in django
const STATIC_ROOT = path.resolve(__dirname, 'website', 'static-src');

// pints to static source folder, un project root
const STATIC_SRC = path.resolve(__dirname, 'static');

// must be the same as WEBPACK_DEVSERVER_HEADER
const DEVSERVER_HEADER = 'X-WEBPACK-DEVSERVER';

module.exports = {
  entry: {
    'bundle': [
      "@babel/polyfill",
      "./static/js/bundle.js"
    ],
    // 'legacy': [
    //   "./static/js/legacy.js"
    // ],
  },
  // entry: './static/js/bundle.js',
  output: {
    path: DEV_MODE ? path.resolve(STATIC_ROOT, 'js') : path.resolve(STATIC_ROOT, 'dist', 'js'),
    filename: "[name].js",
    publicPath: 'http://localhost:3000/static/js/'
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.(js|vue)$/,
        loader: 'eslint-loader',
        exclude: [
          /node_modules/,
        ]
      },
      {
        test: /\.js$/,
        exclude: [/node_modules/],
        use: {
          loader: 'babel-loader',
          // options: {
          //     presets: [
          //         'env'
          //     ]
          // }
        }
      },
      {
        test: /\.vue$/,
        use: {
          loader: 'vue-loader',
          options: {
            includePaths: ['./static/js/'],
          },
        }
      },
      {
        test: /\.scss$/,
        use: [
          DEV_MODE ? 'vue-style-loader' : MiniCssExtractPlugin.loader,
          // 'vue-style-loader',
          'css-loader',
          'sass-loader',
          {
            loader: 'sass-resources-loader',
            options: {
              resources: [
                './static/style/abstracts/*.scss',
              ]
            },
          },
        ]
      },
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.sass$/,
        use: [
          DEV_MODE ? 'style-loader' : MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              sourceMap: DEV_MODE,
            }
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: DEV_MODE,
              includePaths: ['./node_modules'],
              query: {
                includePaths: [
                  path.resolve(__dirname, 'node_modules')
                ]
              }
            },
          },

          {
            loader: 'postcss-loader',
          }
        ]
      },
      {
        test: /\.font\.js/,
        use: [
          DEV_MODE ? 'style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          {
            loader: 'webfonts-loader',
            options: {},
          }
        ]
      },
      {
        test: /\.(png|svg|jpg|gif|woff|woff2|eot|ttf)$/,
        use: [
          'file-loader'
        ]
      }
    ]
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new MiniCssExtractPlugin({
      // this is relative to output.path
      filename: '../css/[name].css',
    }),
    new CopyWebpackPlugin([
      {
        from: path.resolve(STATIC_SRC, 'font'),
        to: path.resolve(STATIC_ROOT, 'font')
      },
      {
        from: path.resolve(STATIC_SRC, 'img'),
        to: path.resolve(STATIC_ROOT, 'img')
      },
      {
        from: path.resolve(STATIC_SRC, 'icons'),
        to: path.resolve(STATIC_ROOT, 'icons')
      }
    ], {debug: 'warn'}),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new VueLoaderPlugin(),
    new StyleLintPlugin({
      files: [
        './static/js/**/*.vue',
        './static/style/**/*.scss',
      ],
    })
  ],
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js', // 'vue/dist/vue.common.js' for webpack 1
      src: path.resolve(__dirname, 'static/js/'),
      style: path.resolve(__dirname, 'static/style/'),
    },
  },
  devServer: {
    hot: true,
    inline: true,
    port: 3000,
    compress: true,
    disableHostCheck: true,
    //host: 'local.openbroadcast.org',
    host: '0.0.0.0',
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    proxy: {
      '/': {
        target: 'http://127.0.0.1:8080',
        onProxyReq: proxyReq => {
          proxyReq.setHeader(DEVSERVER_HEADER, 'on');
        }
      },

    }
  }
};
