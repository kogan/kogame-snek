import React, { Component } from 'react'
import ReactDom from 'react-dom'
import ChatContainer from 'containers/ChatContainer'

class App extends Component {
  render() {
    return (
      <div>
        <ChatContainer />
      </div>
    )
  }
}

ReactDom.render(
  <App />,
  document.getElementById('app'),
)
