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
    players: PropTypes.object,
    sendKeyUpdate: PropTypes.func,
  };

  static defaultProps = {
    cellSize: 36,
    board: {
      dimensions: [24, 24],
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
        direction: 'DOWN',
        alive: true,
        start_tick: 0,
        colour: '#FF0000',
      },
    ],
    sendKeyUpdate: f => f,
  };

  setDirection = ({ keyCode }) => {
    const { sendKeyUpdate } = this.props

    switch (keyCode) {
      case KEYS.left:
      case KEYS.a:
        sendKeyUpdate({ direction: 'LEFT' })
        break
      case KEYS.right:
      case KEYS.d:
        sendKeyUpdate({ direction: 'RIGHT' })
        break
      case KEYS.up:
      case KEYS.w:
        sendKeyUpdate({ direction: 'UP' })
        break
      case KEYS.down:
      case KEYS.s:
        sendKeyUpdate({ direction: 'DOWN' })
        break
      default:
        break
    }
  };

  renderBoard = () => {
    const { cellSize, board, players } = this.props

    const { dimensions, food } = board

    const cells = []
    const [numCols, numRows] = dimensions
    const renderedGridCells = []

    const layoutWidth = numRows * cellSize
    const layoutHeight = numCols * cellSize

    for (let row = 0; row < numRows; row += 1) {
      const currentRow = []
      for (let col = 0; col < numCols; col += 1) {
        currentRow.push({ cellType: null })
      }
      cells.push(currentRow)
    }

    for (let foodPos = 0; foodPos < food.length; foodPos += 1) {
      const [foodX, foodY] = food[foodPos]
      cells[foodY][foodX] = { cellType: 'food' }
    }

    Object.keys(players).forEach((playerName) => {
      const player = players[playerName]
      for (let snakePos = 0; snakePos < player.snake.length; snakePos += 1) {
        const [snakeX, snakeY] = player.snake[snakePos]
        if (snakeX < 0 || snakeX >= dimensions[0]) { continue }
        if (snakeY < 0 || snakeY >= dimensions[1]) { continue }
        if (snakePos === 0) {
          // TODO: for some reason this is backward
          cells[snakeY][snakeX] = { cellType: 'snake', bodyType: 'tail' }
        } else if (snakePos === (player.snake.length - 1)) {
          cells[snakeY][snakeX] = { cellType: 'snake', bodyType: 'head' }
        } else {
          cells[snakeY][snakeX] = { cellType: 'snake', bodyType: 'body' }
        }
      }
    })

    for (let col = 0; col < numCols; col += 1) {
      for (let row = 0; row < numRows; row += 1) {
        const cellObject = cells[col][row]
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
