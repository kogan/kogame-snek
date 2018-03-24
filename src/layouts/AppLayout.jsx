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
        dimensions: { x: 50, y: 50 },
        food: [{ x: 10, y: 10 }, { x: 20, y: 20 }],
        blocks: [],
        tick: 0,
      },
      players: [
        {
          username: 'none@null.kgn.io',
          snake: [
            { x: 0, y: 0 },
            { x: 0, y: 1 },
            { x: 0, y: 2 },
            { x: 0, y: 3 },
            { x: 1, y: 3 },
            { x: 2, y: 3 },
            { x: 3, y: 3 },
            { x: 3, y: 4 },
            { x: 3, y: 5 },
          ],
          direction: 'UP',
          alive: true,
          start_tick: 1,
          colour: '#FF0000',
        },
      ],
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
