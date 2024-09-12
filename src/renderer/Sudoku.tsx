/* eslint-disable import/prefer-default-export */
/* eslint-disable react/function-component-definition */
import * as d3 from 'd3';
import { useRef, useEffect, useState } from 'react';
import { range, cloneDeep } from 'lodash';
import { get_color as xkcd } from 'xkcd-colors';

const initialGrid = [
  [0, 0, 0, 8, 0, 6, 0, 0, 0],
  [0, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [5, 0, 0, 0, 0, 0, 0, 7, 0],
  [0, 4, 0, 0, 0, 0, 0, 2, 0],
  [0, 1, 0, 0, 0, 0, 0, 0, 3],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 3, 0, 0, 0, 0],
  [0, 0, 0, 4, 0, 8, 0, 0, 0],
];

const Circle = () => {
  const ref = useRef();
  //   dummy value [100, 100]
  const [selectedRect, setSelectedRect] = useState<[number, number]>();

  const [grid, setGrid] = useState(initialGrid);

  useEffect(() => {
    document.addEventListener('keydown', (e: KeyboardEvent) => {
      console.log(e);
      console.log('❤️‍🔥 selectedRect', selectedRect);

      if (selectedRect) {
        const newGrid = cloneDeep(grid);
        newGrid[selectedRect[0]][selectedRect[1]] = Number(e.key);
        console.log('❤️‍🔥 newGrid', newGrid);

        setGrid(newGrid);
      }
    });
  }, [selectedRect, grid]);

  useEffect(() => {
    const svgElement = d3.select(ref.current);
    svgElement.append('circle').attr('cx', 150).attr('cy', 70).attr('r', 50);
  }, []);
  return (
    <div>
      <svg style={{ width: '500px' }} viewBox="0 0 100 100">
        {range(9).map((row: number) =>
          range(9).map((col: number) => (
            <g key={`${row}-${col}`}>
              <rect
                x={col * 10}
                y={row * 10}
                width={9}
                height={9}
                fill={
                  selectedRect?.[0] === row && selectedRect[1] === col
                    ? xkcd('tiffany blue')
                    : '#fff'
                }
                // eslint-disable-next-line @typescript-eslint/no-unused-vars
                onClick={(_evt) => setSelectedRect([row, col])}
              />
              <text x={col * 10 + 2.5} y={row * 10 + 6.5} fontSize={6}>
                {grid[row][col] === 0 ? '' : grid[row][col]}
              </text>
            </g>
          )),
        )}
        <rect width={89} height={1.5} x={0} y={29} fill="black" />
        <rect width={89} height={1.5} x={0} y={59} fill="black" />
        <rect width={1.5} height={89} x={29} y={0} fill="black" />
        <rect width={1.5} height={89} x={59} y={0} fill="black" />
      </svg>
      <button
        type="button"
        onClick={() =>
          window.electron.ipcRenderer.sendMessage('solve-sudoku', [
            JSON.stringify(grid),
          ])
        }
      >
        solve
      </button>
    </div>
  );
};

export const Sudoku = () => (
  <div>
    <Circle />
  </div>
);
