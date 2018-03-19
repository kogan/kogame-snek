import PropTypes from 'prop-types'
import React, { Component } from 'react'

class ChatContainer extends Component {
  static propTypes = {
    roomName: PropTypes.string,
  }

  static defaultProps = {
    roomName: 'public',
  }

  constructor(props) {
    super(props)
    const { roomName } = props
    const hostName = window.location.host
    this.chatSocket = new WebSocket(`ws://${hostName}/ws/chat/${roomName}/`)
  }

  componentDidMount() {
    const { chatSocket } = this
    chatSocket.onmessage = (e) => {
      const data = JSON.parse(e.data)
      const { message } = data
      document.querySelector('#chat-log').value += `${message}\n`
    }

    chatSocket.onclose = (e) => { // eslint-disable-line no-unused-vars
      console.error('Chat socket closed unexpectedly')
    }

    document.querySelector('#chat-message-input').focus()
    document.querySelector('#chat-message-input').onkeyup = (e) => {
      if (e.keyCode === 13) { // enter, return
        document.querySelector('#chat-message-submit').click()
      }
    }

    document.querySelector('#chat-message-submit').onclick = (e) => { // eslint-disable-line no-unused-vars
      const messageInputDom = document.querySelector('#chat-message-input')
      const message = messageInputDom.value
      chatSocket.send(JSON.stringify({
        message,
      }))

      messageInputDom.value = ''
    }
  }

  render() {
    return (
      <div>
        <textarea id="chat-log" cols="100" rows="20" /><br />
        <input id="chat-message-input" type="text" size="100" /><br />
        <button id="chat-message-submit" type="button">Send</button>
      </div>
    )
  }
}
export default ChatContainer
