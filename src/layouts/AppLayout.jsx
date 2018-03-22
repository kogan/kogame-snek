// import PropTypes from 'prop-types'
import React, { PureComponent } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import ChatContainer from 'containers/ChatContainer'
import HeaderLayout from './HeaderLayout'
import BodyLayout from './BodyLayout'
import FooterLayout from './FooterLayout'

// Container is a react component that gets bonded with application state
class AppLayout extends PureComponent {
  constructor(props) {
    super(props)
    this.state = {}
  }
  render() {
    // const { componentBeingRendered } = this.props
    return (
      <div className="l-home">
        <HeaderLayout />
        <BodyLayout>
          <ChatContainer />
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
