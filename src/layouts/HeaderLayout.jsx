import React from 'react'

function HeaderLayout() {
  const BROWSE_HAPPY = `<!--[if lte IE 8]>
    <p className="browsehappy">
      You are using an <strong>outdated</strong> browser.
      Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.
    </p>
  <![endif]-->`
  return (
    <header className="l-hd">
      <div dangerouslySetInnerHTML={{ __html: BROWSE_HAPPY }} />
      <div className="l-pg l-pg--width">
        <h1>Kogame - Snek</h1>
      </div>
    </header>
  )
}

export default HeaderLayout
