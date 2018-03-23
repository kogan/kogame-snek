import { COMPONENT_TITLE } from 'constants'

export const GENERIC_ACTION = 'GENERIC_ACTION'

export function genericAction() {
  return {
    type: GENERIC_ACTION,
    payload: COMPONENT_TITLE,
  }
}
