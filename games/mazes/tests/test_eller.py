"""Real-module Eller regressions, no CLI/leaderboard/network.
Run from games/mazes: python -m unittest discover -s tests -p test_eller.py
Requires the project's genuine matplotlib; MPLBACKEND is set to Agg before import.
MAZE_SOURCE optionally selects another module path for baseline comparison.
"""
import importlib.util
import os
from pathlib import Path
import random
import sys
import unittest
from collections import deque

os.environ['MPLBACKEND'] = 'Agg'
NETWORK_ATTEMPTS = []
def deny_network(event, args):
    if event in {'socket.connect', 'socket.getaddrinfo', 'socket.bind', 'socket.sendto'}:
        NETWORK_ATTEMPTS.append(event)
        raise RuntimeError('Network forbidden during maze regression')
sys.addaudithook(deny_network)
SOURCE = Path(os.environ.get('MAZE_SOURCE', str(Path(__file__).resolve().parents[1] / 'maze_completion.py')))
spec = importlib.util.spec_from_file_location('actual_maze_completion', SOURCE)
maze_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maze_module)
CASES = [(w, h, seed) for w, h in [(3, 3), (7, 7), (15, 11), (31, 31), (3, 15), (15, 3)] for seed in range(10)]

def maze(w, h, seed):
    state = random.getstate()
    try:
        random.seed(seed)
        return maze_module.ellers_maze(w, h)
    finally:
        random.setstate(state)

def reachable(grid):
    start = (0, 1)
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for nx, ny in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == 0 and (nx,ny) not in seen:
                seen.add((nx,ny))
                queue.append((nx,ny))
    return seen

class EllerTests(unittest.TestCase):
    def test_entrance_reaches_exit(self):
        for w,h,seed in CASES:
            with self.subTest(w=w,h=h,seed=seed):
                grid=maze(w,h,seed)
                self.assertIn((w-1,h-2),reachable(grid))

    def test_all_passages_are_connected(self):
        for w,h,seed in CASES:
            with self.subTest(w=w,h=h,seed=seed):
                grid=maze(w,h,seed)
                passages={(x,y) for y,row in enumerate(grid) for x,c in enumerate(row) if c==0}
                self.assertEqual(reachable(grid),passages)

    def test_connected_passages_form_a_tree(self):
        for w,h,seed in CASES:
            with self.subTest(w=w,h=h,seed=seed):
                grid=maze(w,h,seed)
                passages={(x,y) for y,row in enumerate(grid) for x,c in enumerate(row) if c==0}
                edges=sum((x+1,y) in passages for x,y in passages)+sum((x,y+1) in passages for x,y in passages)
                self.assertEqual(edges,len(passages)-1)

    def test_shape_values_and_boundary_openings(self):
        for w,h,seed in CASES:
            with self.subTest(w=w,h=h,seed=seed):
                grid=maze(w,h,seed)
                self.assertEqual(len(grid),h)
                self.assertTrue(all(len(row)==w for row in grid))
                self.assertTrue(all(c in (0,1) for row in grid for c in row))
                openings={(0,1),(w-1,h-2)}
                for y in range(h):
                    for x in range(w):
                        if x in (0,w-1) or y in (0,h-1):self.assertEqual(grid[y][x],0 if (x,y) in openings else 1)

    def test_seeded_replay_is_deterministic(self):
        for w,h,seed in CASES:
            with self.subTest(w=w,h=h,seed=seed):self.assertEqual(maze(w,h,seed),maze(w,h,seed))

    def test_no_network(self):
        self.assertEqual(NETWORK_ATTEMPTS,[])

if __name__ == '__main__':
    unittest.main()
