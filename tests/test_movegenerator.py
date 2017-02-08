# DESCRIPTION: Tests the move generator.

# 4920646f6e5c2774206361726520696620697420776f726b73206f6e20796f7572206d61636869
# 6e652120576520617265206e6f74207368697070696e6720796f7572206d616368696e6521

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest
from lib import core, chessboard, pieces, movegenerator
from tests.test_core import errormessage

class TestCoreMoveGenerator(unittest.TestCase):
    """Goes about testing the core methods of the move generator."""

    def setUp(self):
        self.board = chessboard.ChessBoard()
        self.board[18] = pieces.QueenPiece('white')
        self.board[19] = pieces.PawnPiece('white')
        self.board[23] = pieces.RookPiece('black')
        self.board[42] = pieces.KnightPiece('black')

        self.generator = movegenerator._CoreMoveGenerator(self.board)

    def test_piecesareonsameside_white(self):
        self.assertTrue(
            self.generator._piecesareonsameside(self.board[18], self.board[19]),
            errormessage(False, True)
        )
        return None

    def test_piecesareonsameside_black(self):
        self.assertTrue(
            self.generator._piecesareonsameside(self.board[23], self.board[42]),
            errormessage(False, True)
        )
        return None

    def test_piecesareonsameside_bothcolours(self):
        self.assertFalse(
            self.generator._piecesareonsameside(self.board[18], self.board[23]),
            errormessage(True, False)
        )
        return None

    def test_piecesareonsameside_nonpieces(self):
        with self.assertRaises(TypeError):
            self.generator._piecesareonsameside(12, 15)
        return None

    def test_piecesbetween_onepiece(self):
        self.assertEqual(
            len(self.generator._piecesbetween(18, 23)), 1,
            errormessage(
            '%s pieces' % len(self.generator._piecesbetween(18, 23)),
            '1 piece'
            )
        )
        return None

    def test_piecesbetween_twopieces(self):
        self.assertEqual(
            len(self.generator._piecesbetween(16, 23)), 2,
            errormessage(
            '%s piece(s)' % len(self.generator._piecesbetween(16, 23)),
            '2 pieces'
            )
        )
        return None


if __name__ == '__main__':
    unittest.main(verbosity=2)
