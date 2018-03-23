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
      players: [],
      board: {},
      leaderBoard: {},
    }
    const hostName = window.location.host

    // TODO MODIFY THIS ENDPOINT
    this.chatSocket = new WebSocket(`ws://${hostName}/ws/chat/$/`)
  }

  componentDidMount() {
    const { chatSocket } = this
    chatSocket.onmessage = (e) => {
      const data = JSON.parse(e.data)
      const { message } = data

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
