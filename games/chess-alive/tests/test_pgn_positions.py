"""Real ChessGame/chess.pgn roundtrips, no UI/provider. CHESS_SOURCE selects src tree.
Run from games/chess-alive: python -m unittest discover -s tests -p test_pgn_positions.py
"""
import io
import os
from pathlib import Path
import sys
import unittest
ATTEMPTS=[]
def guard(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.bind','socket.sendto'}:
        ATTEMPTS.append(event)
        raise RuntimeError('Network forbidden')
sys.addaudithook(guard)
sys.path.insert(0,os.environ.get('CHESS_SOURCE',str(Path(__file__).resolve().parents[1]/'src')))
import chess
import chess.pgn
from chess_alive.core.game import ChessGame
CASES=[('normal',None,['e4','e5','Nf3']),('white_promotion','7k/P7/8/8/8/8/8/7K w - - 0 1',['a8=Q+']),('black_promotion','7k/8/8/8/8/8/p7/7K b - - 0 23',['a1=Q+']),('castle','r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 7',['O-O']),('en_passant','7k/8/8/3pP3/8/8/8/7K w - d6 0 12',['exd6']),('no_moves','7k/8/8/8/8/8/8/7K b - - 4 33',[])]
def setup(fen,moves):
    game=ChessGame()
    if fen:assert game.load_fen(fen)
    for san in moves:assert game.make_move_san(san)
    return game
class PgnPositionTests(unittest.TestCase):
    def assert_roundtrip(self,game):
        text=game.to_pgn()
        parsed=chess.pgn.read_game(io.StringIO(text))
        self.assertEqual(parsed.errors,[])
        self.assertEqual(parsed.end().board().fen(),game.fen)
        return parsed
    def test_frozen_position_roundtrips(self):
        for name,fen,moves in CASES:
            with self.subTest(case=name):self.assert_roundtrip(setup(fen,moves))
    def test_custom_setup_headers_describe_root_not_final_position(self):
        for name,fen,moves in CASES[1:]:
            with self.subTest(case=name):
                game=setup(fen,moves)
                parsed=self.assert_roundtrip(game)
                self.assertEqual(parsed.headers.get('SetUp'),'1')
                self.assertEqual(parsed.board().fen(),chess.Board(fen).fen())
    def test_normal_start_does_not_add_setup_headers(self):
        game=setup(None,['e4','e5','Nf3'])
        parsed=self.assert_roundtrip(game)
        self.assertNotIn('FEN',parsed.headers)
        self.assertNotIn('SetUp',parsed.headers)
        self.assertIn('1. e4 e5 2. Nf3',str(parsed))
    def test_custom_board_constructor_is_preserved(self):
        game=ChessGame(board=chess.Board(CASES[2][1]))
        self.assertTrue(game.make_move_san('a1=Q+'))
        self.assert_roundtrip(game)
    def test_undo_then_export_uses_root_and_remaining_moves(self):
        game=setup(CASES[3][1],['O-O','O-O-O'])
        self.assertIsNotNone(game.undo_move())
        parsed=self.assert_roundtrip(game)
        self.assertEqual(len(list(parsed.mainline_moves())),1)
    def test_comments_result_and_event_retained(self):
        game=setup(CASES[1][1],['a8=Q+'])
        game.move_history[0].commentary='Synthetic promotion comment'
        parsed=self.assert_roundtrip(game)
        self.assertEqual(parsed.headers['Event'],'ChessAlive Game')
        self.assertEqual(parsed.headers['Result'],game.board.result())
        self.assertEqual(parsed.variations[0].comment,'Synthetic promotion comment')
    def test_network_guard(self):self.assertEqual(ATTEMPTS,[])
if __name__=='__main__':unittest.main()
