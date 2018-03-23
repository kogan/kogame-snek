import React from 'react'
import PropTypes from 'prop-types'
import styles from './styles.scss'

// display a single cell
const GridCell = ({ size, cellType }) => {
  let cellClassName = ''
  switch (cellType) {
    case 'food':
      cellClassName = styles.food
      break
    case 'snake':
      cellClassName = styles.snake
      break
    default:
      cellClassName = ''
  }

  return (
    <div
      className={cellClassName}
      style={{ height: `${size}px`, width: `${size}px` }}
    />
  )
}

GridCell.defaultProps = {
  size: 20,
  cellType: '',
}

GridCell.propTypes = {
  size: PropTypes.number,
  cellType: PropTypes.string,
}

export default GridCell
