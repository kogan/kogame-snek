import { combineReducers } from 'redux'
import genericContainerReducer from '../containers/GenericContainer/reducer'

// a function that returns a piece of the application state
// because application can have many different pieces of state == many reducers
const rootReducer = combineReducers({
  genericContainerReducer,
})

export default rootReducer
