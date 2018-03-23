import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import Snek from 'components/Snek'
import GridCell from 'components/GridCell'
import { KEYS } from './constants'
import styles from './styles.scss'

class SnekContainer extends Component {
  static propTypes = {
    cellSize: PropTypes.number,
    board: PropTypes.object,
    players: PropTypes.object,
  };

  static defaultProps = {
    cellSize: 20,
    board: {},
    players: {},
  };

  constructor(props) {
    super(props)
    this.state = {
      activeDirection: null,
    }
  }
  setDirection = ({ keyCode }) => {
    let activeDirection = null

    switch (keyCode) {
      case KEYS.left:
        activeDirection = 'UP'
        break
      case KEYS.right:
        activeDirection = 'RIGHT'
        break
      case KEYS.up:
        activeDirection = 'LEFT'
        break
      case KEYS.down:
        activeDirection = 'DOWN'
        break
      default:
        break
    }
    this.setState({ activeDirection })
  };

  renderBoard = () => {
    const {
      cellSize,
      board,
      players,
    } = this.props

    const {
      dimensions,
      food,
    } = board

    const cells = []
    const numRows = dimensions[1]
    const numCols = dimensions[0]
    const renderedGridCells = []

    for (let row = 0; row < numRows; row += 1) {
      const currentRow = []
      for (let col = 0; col < numCols; col += 1) {
        currentRow.push({ cellType: null })
      }
      cells.push(currentRow)
    }

    for (let foodPos = 0; foodPos < food.length; foodPos += 1) {
      const foodX = food[foodPos][0]
      const foodY = food[foodPos][1]
      cells[foodX][foodY] = { cellType: 'food' }
    }

    for (let playerPos = 0; playerPos < players.length; playerPos += 1) {
      const player = players[playerPos]
      for (let snakePos = 0; snakePos < player.snake.length; snakePos += 1) {
        const snakeX = player.snake[snakePos][0]
        const snakeY = player.snake[snakePos][1]
        cells[snakeX][snakeY] = { cellType: 'snake' }
      }
    }

    for (let row = 0; row < numRows; row += 1) {
      for (let col = 0; col < numCols; col += 1) {
        const cellObject = cells[row][col]
        console.log(cellObject)
        renderedGridCells.push(<GridCell size={cellSize} cellType={cellObject.cellType} />)
      }
    }
    return (
      <div
        tabIndex="1"
        role="presentation"
        className={styles.boardLayout}
        onKeyDown={this.setDirection}
      >
        {renderedGridCells}
        <Snek />
      </div>
    )
  };

  render() {
    return this.renderBoard()
  }
}

function mapStateToProps(state) {
  // whatever is returned will show up as props
  return {
    state,
  }
}

// Anything returned from this function will end up as props
function mapDispatchToProps(dispatch) {
  // Whenever dispatch is called the result should be passed
  // to all of the reducers
  return bindActionCreators({}, dispatch)
}

// To promote a component to a container (smart component) - it needs
// to know about this new dispatch method. Make it available
// as a prop.
export default connect(mapStateToProps, mapDispatchToProps)(SnekContainer)
