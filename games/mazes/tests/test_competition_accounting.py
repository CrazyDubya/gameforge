"""Competition persistence regressions using real local players and JSON storage.
Run from games/mazes: python -m unittest discover -s tests -p test_competition_accounting.py
Requires genuine matplotlib. MAZE_SOURCE optionally selects baseline module.
"""
import importlib.util
import io
import json
import os
from pathlib import Path
import random
import sys
import tempfile
import unittest
from unittest.mock import patch

os.environ['MPLBACKEND'] = 'Agg'
NETWORK_ATTEMPTS = []
def deny_network(event, args):
    if event in {'socket.connect', 'socket.getaddrinfo', 'socket.bind', 'socket.sendto'}:
        NETWORK_ATTEMPTS.append(event)
        raise RuntimeError('Network forbidden during accounting regression')
sys.addaudithook(deny_network)
SOURCE = Path(os.environ.get('MAZE_SOURCE', str(Path(__file__).resolve().parents[1] / 'maze_completion.py')))
spec = importlib.util.spec_from_file_location('actual_maze_accounting', SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
FIELDS = ['total_time', 'total_path_length', 'total_nodes_explored', 'run_count']

def values(player):
    return {field: getattr(player, field) for field in FIELDS}

def fixtures():
    state = random.getstate()
    try:
        grids = []
        for seed in [0, 1, 2]:
            random.seed(seed)
            grids.append(m.generate_maze(7, 7))
        return grids
    finally:
        random.setstate(state)

class CompetitionAccountingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.filename = str(Path(self.temp.name) / 'leaderboard.json')
        self.board = m.Leaderboard(self.filename)
        self.players = [m.Player('BFS', m.bfs_with_stats), m.Player('DFS', m.dfs_with_stats)]
        self.grids = fixtures()
        self.expected = {p.name: dict.fromkeys(FIELDS, 0) for p in self.players}
        self.last_expected = None

    def run_rounds(self, count):
        grids = self.grids[:count]
        gen = iter(grids)
        ticks = []
        now = 0
        self.last_expected = {p.name: dict.fromkeys(FIELDS, 0) for p in self.players}
        for i, grid in enumerate(grids):
            for j, player in enumerate(self.players):
                duration = 1 + 2 * i + j
                ticks.extend([now, now + duration])
                now += duration + 10
                path, nodes = player.algorithm(grid, (0, 1), (6, 5))
                for target in [self.expected[player.name], self.last_expected[player.name]]:
                    target['total_time'] += duration
                    target['total_path_length'] += len(path)
                    target['total_nodes_explored'] += nodes
                    target['run_count'] += 1
        with patch.object(m.time, 'time', side_effect=ticks), patch.object(m, 'visualize_maze_with_paths') as visual, patch('sys.stdout', new=io.StringIO()):
            m.run_competition(count, 7, 7, [('Backtracking', lambda w,h: next(gen))], self.players, self.board, self.temp.name)
        self.assertEqual(visual.call_count, count)

    def test_one_round_counts_once(self):
        self.run_rounds(1)
        for p in self.players:
            self.assertEqual(values(self.board.players[p.name]), self.expected[p.name])

    def test_three_round_totals_count_each_sample_once(self):
        self.run_rounds(3)
        for p in self.players:
            with self.subTest(player=p.name):
                self.assertEqual(values(self.board.players[p.name]), self.expected[p.name])

    def test_prior_saved_samples_are_preserved_once(self):
        prior = {'total_time': 19, 'total_path_length': 43, 'total_nodes_explored': 71, 'run_count': 2}
        Path(self.filename).write_text(json.dumps({'BFS': prior}))
        self.board = m.Leaderboard(self.filename)
        for field in FIELDS:
            self.expected['BFS'][field] += prior[field]
        self.run_rounds(3)
        for p in self.players:
            with self.subTest(player=p.name):
                self.assertEqual(values(self.board.players[p.name]), self.expected[p.name])

    def test_reusing_players_across_calls_does_not_recount_history(self):
        self.run_rounds(1)
        self.run_rounds(3)
        for p in self.players:
            with self.subTest(player=p.name):
                self.assertEqual(values(self.board.players[p.name]), self.expected[p.name])

    def test_original_player_objects_keep_cumulative_totals(self):
        originals = list(self.players)
        self.run_rounds(3)
        for old, player in zip(originals, self.players):
            self.assertIs(old, player)
            self.assertEqual(values(player), self.expected[player.name])

    def test_saved_json_and_reload_match_once_per_sample(self):
        self.run_rounds(3)
        data = json.loads(Path(self.filename).read_text())
        self.assertEqual(data, self.expected)
        loaded = m.Leaderboard(self.filename)
        self.assertEqual({name: values(p) for name,p in loaded.players.items()}, self.expected)

    def test_direct_add_player_still_adds_a_whole_batch(self):
        batch = m.Player('Batch', m.bfs_with_stats)
        batch.update_stats(2, 5, 7)
        batch.update_stats(3, 6, 8)
        self.board.add_player(batch)
        self.board.add_player(batch)
        self.assertEqual(values(self.board.players['Batch']), {field: 2*getattr(batch, field) for field in FIELDS})

    def test_unsolvable_rounds_do_not_count(self):
        blocked = [[1] * 7 for _ in range(7)]
        blocked[1][0] = blocked[5][6] = 0
        with patch.object(m, 'visualize_maze_with_paths') as visual, patch('sys.stdout', new=io.StringIO()):
            m.run_competition(2, 7, 7, [('Blocked', lambda w,h: blocked)], self.players, self.board, self.temp.name)
        self.assertEqual(self.board.players, {})
        self.assertFalse(visual.called)
        self.assertTrue(all(p.run_count == 0 for p in self.players))

    def test_no_network(self):
        self.assertEqual(NETWORK_ATTEMPTS, [])

if __name__ == '__main__':
    unittest.main()
