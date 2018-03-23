import React, { Component } from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { COMPONENT_TITLE } from './constants'
import styles from './styles.scss'

class SnekContainer extends Component {
  static propTypes = {};

  static defaultProps = {};

  constructor(props) {
    super(props)
    this.state = {
      players: [],
    }
  }

  renderBoard = () => (
    <div className={styles.boardLayout}>
      <h2 className="">{COMPONENT_TITLE} Just Another Generic Container</h2>
    </div>
  )

  render() {
    return this.renderBoard()
  }
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
export default connect(mapStateToProps, mapDispatchToProps)(SnekContainer)
