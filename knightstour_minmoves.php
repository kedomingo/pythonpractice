<?php
ini_set('xdebug.max_nesting_level', 500);


class Cell {
  private $step = null;
  private $isMarked = false;
  private $row;
  private $col;
  /**
   * @var Cell[]
   */
  private $connections;
  private $minMoves;

  public function __construct($row, $col) {
    $this->row = $row;
    $this->col = $col;
  }

  public function setMarked(bool $marked, int $step = null) {
    $this->isMarked = $marked;
    $this->step     = $marked ? $step : null;
  }

  public function isMarked() : bool {
    return $this->isMarked;
  }

  public function getStep() : ?int {
    return $this->step;
  }

  public function addNextConnection(Cell $cell) : void {
    $this->connections[$cell->getRow() . '.' . $cell->getCol()] = $cell;
    $this->minMoves[$cell->getRow() . '.' . $cell->getCol()]    = 1;
  }

  /**
   * @return Cell[]
   */
  public function getConnections() : array {
    return $this->connections;
  }

  /**
   * @return mixed
   */
  public function getRow() {
    return $this->row;
  }

  /**
   * @return mixed
   */
  public function getCol() {
    return $this->col;
  }

  public function equals(Cell $cell) {
    return $this->row === $cell->getRow() && $this->col === $cell->getCol();
  }

  public function setMinMovesFrom(Cell $cell, int $moves) : void {
    $key = $cell->getRow() . '.' . $cell->getCol();
    // Do not overwrite if larger
    if (isset($this->minMoves[$key]['moves']) && $moves > $this->minMoves[$key]['moves']) {
      return;
    }
    $this->minMoves[$key] = [
        'moves' => $moves,
        'via'   => $cell,
    ];
  }

  public function getMinMovesFrom(Cell $cell) : ?int {
    return $this->minMoves[$cell->getRow() . '.' . $cell->getCol()]['moves'] ?? null;
  }

  public function getIntermediateCellFrom(Cell $cell) : ?Cell {
    return $this->minMoves[$cell->getRow() . '.' . $cell->getCol()]['via'] ?? null;
  }

  public function getCoordinates() : string {
    return $this->row . ', ' . $this->col;
  }
}


class Board {
  private $side;
  private $board = [];
  private $impossibleMoves;

  public function __construct(int $side) {
    $this->side = $side;
    for ($i = 0; $i < $side; $i++) {
      for ($j = 0; $j < $side; $j++) {
        $this->board[$i][$j] = new Cell($i, $j);
      }
    }

    // Setup the graph
    for ($i = 0; $i < $side; $i++) {
      for ($j = 0; $j < $side; $j++) {
        $connections = $this->getPossibleNextPositions($i, $j);
        foreach ($connections as $connection) {
          $this->board[$i][$j]->addNextConnection($this->getCellAt($connection[0], $connection[1]));
        }
      }
    }
  }

  /**
   * @param Cell $start
   * @param Cell $target
   * @param int  $step
   *
   * @return array
   */
  public function getMin(Cell $start, Cell $target, int $step = 0) {
    // arrived at target cell. 0 moves required
    if ($start->equals($target)) {
      return [0, null];
    }
    // If min moves is known, use that
    if (($minMoves = $target->getMinMovesFrom($start)) !== null) {
      return [$minMoves, $target->getIntermediateCellFrom($start)];
    }
    if ($step >= 400) {
      return null;
    }

    $min     = null;
    // For all unmarked connections, get the minimum from the connection to the target
    foreach ($start->getConnections() as $connection) {
      if ($connection->isMarked()) {
        continue;
      }
      $connection->setMarked(true, $step + 1);
      $result = $this->getMin($connection, $target, $step + 1) + 1;

      if ($min === null || ($result !== null && $result < $min)) {
        $min     = $result;
      }
      $connection->setMarked(false);
    }
    if ($min !== null) {
      $target->setMinMovesFrom($start, $min);
    }

    return $min;
  }

  /**
   * Determine where the knight can go
   *
   * @param int $row
   * @param int $col
   *
   * @return array
   */
  public function getPossibleNextPositions(int $row, int $col) {
    $positions = [
        [$row - 2, $col - 1],
        [$row - 2, $col + 1],
        [$row + 2, $col - 1],
        [$row + 2, $col + 1],
        [$row - 1, $col - 2],
        [$row + 1, $col - 2],
        [$row - 1, $col + 2],
        [$row + 1, $col + 2],
    ];
    foreach ($positions as $k => $position) {
      if ($position[0] < 0 || $position[1] < 0 || $position[0] >= $this->side || $position[1] >= $this->side ||
          $this->getCellAt($position[0], $position[1])->isMarked()) {
        unset($positions[$k]);
      }
    }

    return $positions;
  }

  public function getCellAt(int $row, int $col) : Cell {
    return $this->board[$row][$col];
  }
}


$board = new Board(150);
$board->getCellAt(0, 0)->setMarked(true, 0);

$start  = $board->getCellAt(0, 0);
$target = $board->getCellAt(100, 100);

echo $board->getMin($start, $target) . "\n";
