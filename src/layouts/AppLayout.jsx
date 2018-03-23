// import PropTypes from 'prop-types'
import React, { PureComponent } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import SnekContainer from 'containers/SnekContainer'
import HeaderLayout from './HeaderLayout'
import BodyLayout from './BodyLayout'
import FooterLayout from './FooterLayout'

import styles from './styles.scss'

// Container is a react component that gets bonded with application state
class AppLayout extends PureComponent {
  constructor(props) {
    super(props)
    this.state = {}
  }
  render() {
    // const { componentBeingRendered } = this.props
    const players = [
      {
        username: 'none@null.kgn.io',
        snake: [
          [0, 0],
          [0, 1],
          [0, 2],
          [0, 3],
          [1, 3],
          [2, 3],
          [3, 3],
          [3, 4],
          [3, 5],
        ],
        direction: 'UP',
        alive: true,
        start_tick: 1,
        colour: '#FF0000',
      },
    ]

    const board = {
      dimensions: [50, 50],
      food: [[10, 10], [20, 20]],
      blocks: [],
    }

    return (
      <div className={styles.appLayout}>
        <HeaderLayout />
        <BodyLayout>
          <SnekContainer
            players={players}
            board={board}
            cellSize={20}
          />
        </BodyLayout>
        <FooterLayout />
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    appState: state.appState,
  }
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({}, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(AppLayout)
