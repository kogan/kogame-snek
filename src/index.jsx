/* eslint no-console: ["error", { allow: ["log"] }], comma-dangle: ["error", "never"] */
import 'babel-polyfill' // okay so i still got a bit of love for IE9...
import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware, compose } from 'redux'
import ReduxPromise from 'redux-promise' // middleware
import ReduxThunk from 'redux-thunk' // used to fire other actions sequentially

import AppLayout from './layouts/AppLayout'
import reducers from './reducers'

import { ENABLE_DEV_TOOLS } from './globals/constants'

const middleware = [ReduxThunk, ReduxPromise]
const consoleStyle = 'background: #555; color: #bada55'

let devToolsExtension = f => f // Initialise as an empty function

if (ENABLE_DEV_TOOLS === true) {
  console.log('%c_____ PROJECT HAS REDUX TOOLS ENABLED _____', consoleStyle)
  devToolsExtension = window.devToolsExtension
    ? window.devToolsExtension()
    : f => f
}

const middlewareComposed = compose(
  applyMiddleware(...middleware),
  devToolsExtension
)
const store = createStore(reducers, middlewareComposed)

// Render react when document is ready.
ReactDOM.render(
  <Provider store={store}>
    <AppLayout store={store} />
  </Provider>,
  document.querySelector('.app')
)
