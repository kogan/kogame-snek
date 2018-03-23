import React from 'react'
import PropTypes from 'prop-types'
import styles from './styles.scss'

// display a single cell
const GridCell = ({ size, cellType, bodyType }) => {
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

  let bodyTypeClassName = ''
  switch (bodyType) {
    case 'head':
      bodyTypeClassName = styles.bodyHead
      break
    case 'tail':
      bodyTypeClassName = styles.bodyTail
      break
    case 'body':
      bodyTypeClassName = styles.bodyDefault
      break
    default:
      bodyTypeClassName = ''
  }
  return (
    <div
      className={`${styles.cellStyle} ${cellClassName} ${bodyTypeClassName}`}
      style={{ height: `${size}px`, width: `${size}px` }}
    />
  )
}

GridCell.defaultProps = {
  size: 20,
  cellType: '',
  bodyType: '',
}

GridCell.propTypes = {
  size: PropTypes.number,
  cellType: PropTypes.string,
  bodyType: PropTypes.string,
}

export default GridCell
