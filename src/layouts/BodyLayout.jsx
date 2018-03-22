import PropTypes from 'prop-types'
import React from 'react'

function BodyLayout(props) {
  return (
    <section className="l-bd">
      <div className="l-pg l-pg--width">
        {props.children}
      </div>
    </section>
  )
}

BodyLayout.propTypes = {
  children: PropTypes.element.isRequired,
}

export default BodyLayout
