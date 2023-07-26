  <?php

class Cell
{
    private $step = null;
    private $isMarked = false;

    public function setMarked(bool $marked, int $step = null)
    {
        $this->isMarked = $marked;
        $this->step = $marked ? $step : null;
    }

    public function isMarked(): bool
    {
        return $this->isMarked;
    }

    public function getStep(): ?int
    {
        return $this->step;
    }
}

class Board
{
    private $side;
    private $board = [];
    private $impossibleMoves;

    public function __construct(int $side)
    {
        $this->side = $side;
        for ($i = 0; $i < $side; $i++) {

            for ($j = 0; $j < $side; $j++) {
                $this->board[$i][$j] = new Cell();
            }
        }
    }

    public function isComplete()
    {
        for ($i = 0; $i < $this->side; $i++) {
            for ($j = 0; $j < $this->side; $j++) {
                if (!$this->getCellAt($i, $j)->isMarked()) {
                    return false;
                }
            }
        }

        return true;
    }

    public function getBoardConfiguration(): string
    {
        $cells = [];

        for ($i = 0; $i < $this->side; $i++) {
            for ($j = 0; $j < $this->side; $j++) {
                $cells[] = $this->getCellAt($i, $j)->isMarked() ? 1 : 0;
            }
        }

        return implode('.', $cells);
    }

    public function start(int $row, int $col, int $step = 0, int &$iterations)
    {
        $iterations++;
        $cell = $this->getCellAt($row, $col);
        $possibleNextPositions = $this->getPossibleNextPositions($row, $col);

        if (isset($this->impossibleMoves[$row][$col][$this->getBoardConfiguration()])) {
            return false;
        }

        $cell->setMarked(true, $step);
        if (empty($possibleNextPositions)) {
            if (!$this->isComplete()) {
                $cell->setMarked(false);
                return false;
            }

            return true;
        }
        foreach ($possibleNextPositions as $position) {
            if ($this->start($position[0], $position[1], $step + 1, $iterations)) {
                return true;
            }
        }

        // Remember that the board at this configuration (knight at this position and these possible moves)
        // Cannot be completed
        $this->impossibleMoves[$row][$col][$this->getBoardConfiguration()] = 1;

        $cell->setMarked(false);
        return false;
    }

    /**
     * Determine where the knight can go
     *
     * @param int $row
     * @param int $col
     * @return array
     */
    public function getPossibleNextPositions(int $row, int $col)
    {
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
        shuffle($positions);
        foreach ($positions as $k => $position) {
            if ($position[0] < 0 || $position[1] < 0 || $position[0] >= $this->side || $position[1] >= $this->side ||
                $this->getCellAt($position[0], $position[1])->isMarked()) {
                unset($positions[$k]);
            }
        }
        return $positions;
    }

    public function getCellAt(int $row, int $col): Cell
    {
        return $this->board[$row][$col];
    }

    public function render()
    {
        $s = str_repeat('-', $this->side * 5 + 1) . "\n";
        for ($i = 0; $i < $this->side; $i++) {
            for ($j = 0; $j < $this->side; $j++) {
                $step = $this->getCellAt($i, $j)->getStep();
                $s .= sprintf('| %2d ', $step);
            }
            $s .= "|\n";
            $s .= str_repeat('-', $this->side * 5 + 1) . "\n";
        }
        $s .= "\n";

        return $s;
    }

    public function clear()
    {
        for ($i = 0; $i < $this->side; $i++) {
            for ($j = 0; $j < $this->side; $j++) {
                $this->getCellAt($i, $j)->setMarked(false);
            }
        }
    }
}


$board = new Board(5);
$minIterations = 10000000000;
$minboard = '';
for ($i = 0; $i < 20; $i++) {
    $iterations = 0;
    $board->clear();
    if ($board->start(0, 0, 0, $iterations)) {
        if ($iterations < $minIterations) {
            $minIterations = $iterations;
            $minboard = $board->render();
        }
    }
}
echo "Min solution at $minIterations iterations\n";
echo $minboard;