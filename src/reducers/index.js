import { combineReducers } from 'redux'
import snekReducer from 'containers/SnekContainer/reducer'

// a function that returns a piece of the application state
// because application can have many different pieces of state == many reducers
const rootReducer = combineReducers({
  snekReducer,
})

export default rootReducer
