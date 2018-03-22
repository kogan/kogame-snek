import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { COMPONENT_TITLE } from './constants'

function GenericContainer() {
  return <h2 className="">{COMPONENT_TITLE} Just Another Generic Container</h2>
}

function mapStateToProps(state) {
  // whatever is returned will show up as props
  return {
    state,
  }
}

// Anything returned from this function will end up as props
function mapDispatchToProps(dispatch) {
  // Whenever dispatch is called the result should be passed
  // to all of the reducers
  return bindActionCreators({}, dispatch)
}

// To promote a component to a container (smart component) - it needs
// to know about this new dispatch method. Make it available
// as a prop.
export default connect(mapStateToProps, mapDispatchToProps)(GenericContainer)
