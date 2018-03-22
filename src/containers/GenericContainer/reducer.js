import { GENERIC_ACTION } from './actions'

const DEFAULT_APP_SCHEMA = {
  genericAction: null,
}

export default function (state = DEFAULT_APP_SCHEMA, action) {
  switch (action.type) {
    case GENERIC_ACTION:
      return {
        ...state,
        genericAction: action.payload,
      }
    default:
      return state
  }
}
