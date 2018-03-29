// import PropTypes from 'prop-types'
import React, { PureComponent } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import SnekContainer from 'containers/SnekContainer'
import HeaderLayout from './HeaderLayout'
import BodyLayout from './BodyLayout'
import FooterLayout from './FooterLayout'

import styles from './styles.scss'

// TContainer is a react component that gets bonded with application state
class AppLayout extends PureComponent {
  constructor(props) {
    super(props)
    this.state = {
      board: {
        dimensions: [50, 50],
        food: [[10, 10], [20, 20]],
        blocks: [],
        tick: 0,
      },
      players: {
        'none@null.kgn.io': {
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
      },
    }
    const hostName = window.location.host

    // TODO MODIFY THIS ENDPOINT
    this.chatSocket = new WebSocket(`ws://${hostName}/ws/game/`)
  }

  componentDidMount() {
    const { chatSocket } = this
    chatSocket.onmessage = (e) => {
      const data = JSON.parse(e.data)
      const message = data

      this.setState({
        players: message.players ? message.players : [],
        board: message.board ? message.board : {},
        leaderBoard: message.leaderBoard ? message.leaderBoard : {},
      })
    }
  }

  sendKeyUpdate = (updateObj) => {
    const { chatSocket } = this
    chatSocket.send(JSON.stringify({ updateObj }))
  }

  render() {
    return (
      <div className={styles.appLayout}>
        <HeaderLayout />
        <BodyLayout>
          <SnekContainer
            board={this.state.board}
            players={this.state.players}
            leaderBoard={this.state.leaderBoard}
            sendKeyUpdate={this.sendKeyUpdate}
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
