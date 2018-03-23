import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import GridCell from 'components/GridCell'
import { KEYS } from './constants'
import styles from './styles.scss'

class SnekContainer extends PureComponent {
  static propTypes = {
    cellSize: PropTypes.number,
    board: PropTypes.object,
    players: PropTypes.array,
    sendKeyUpdate: PropTypes.func,
  };

  static defaultProps = {
    cellSize: 36,
    board: {
      dimensions: [50, 50],
      food: [[10, 10], [20, 20]],
      blocks: [],
      tick: 1,
    },
    players: [
      {
        username: 'none@null.kgn.io',
        snake: [
          [0, 0],
          [0, 1],
          [0, 2],
          [0, 3],
          [1, 3],
          [2, 3],
          [3, 3],
          [3, 4],
          [3, 5],
        ],
        direction: 's',
        alive: true,
        start_tick: 1,
        colour: '#FF0000',
      },
    ],
    sendKeyUpdate: f => f,
  };

  setDirection = ({ keyCode }) => {
    const { sendKeyUpdate } = this.props

    let activeDirection = null

    switch (keyCode) {
      case KEYS.left:
        activeDirection = 'LEFT'
        break
      case KEYS.right:
        activeDirection = 'RIGHT'
        break
      case KEYS.up:
        activeDirection = 'UP'
        break
      case KEYS.down:
        activeDirection = 'DOWN'
        break
      default:
        break
    }
    sendKeyUpdate({ direction: activeDirection })
  };

  renderBoard = () => {
    const { cellSize, board, players } = this.props

    const { dimensions, food } = board

    const cells = []
    const numRows = dimensions[1]
    const numCols = dimensions[0]
    const renderedGridCells = []

    const layoutWidth = dimensions[1] * cellSize
    const layoutHeight = dimensions[0] * cellSize

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
        if (snakePos === 0) {
          cells[snakeX][snakeY] = { cellType: 'snake', bodyType: 'head' }
        } else if (snakePos === (player.snake.length - 1)) {
          cells[snakeX][snakeY] = { cellType: 'snake', bodyType: 'tail' }
        } else {
          cells[snakeX][snakeY] = { cellType: 'snake', bodyType: 'body' }
        }
      }
    }

    for (let row = 0; row < numRows; row += 1) {
      for (let col = 0; col < numCols; col += 1) {
        const cellObject = cells[row][col]
        renderedGridCells.push(<GridCell
          key={Math.random().toString()}
          size={cellSize}
          cellType={cellObject.cellType}
          bodyType={cellObject.bodyType}
        />)
      }
    }
    return (
      <div
        tabIndex="0"
        role="presentation"
        className={styles.boardLayout}
        onKeyDown={this.setDirection}
        style={{ height: `${layoutHeight}px`, width: `${layoutWidth}px` }}
      >
        {renderedGridCells}
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
