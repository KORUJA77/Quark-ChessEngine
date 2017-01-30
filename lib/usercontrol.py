# DESCRIPTION: The classes that pertain to the UI and GUI.

# 50726f6772616d6d696e6720697320627265616b696e67206f66206f6e652062696720696d706f
# 737369626c65207461736b20696e746f207365766572616c207665727920736d616c6c20706f73
# 7369626c65207461736b732e

# NOTE:
# ================
# This file is currently a work in progress. The original chessboard.py file has
# become overly bloated and is detrimental to the moral of the project. This new
# script is aimed at taking only the methods that pertain to the UI and GUI,
# while separating the other components into their own scrips

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from lib import core, vectors, pieces

 #     # ###
 #     #  #
 #     #  #
 #     #  #
 #     #  #
 #     #  #
  #####  ###


class EngineUI:
    """The class that handles the UI for the engine."""

    def __init__(self):
        self.history = list()
        self._symboltopiece = {
            'R': pieces.RookPiece,
            'N': pieces.KnightPiece,
            'B': pieces.BishopPiece,
            'Q': pieces.QueenPiece,
            'K': pieces.KingPiece,
            'P': pieces.PawnPiece
        }
        self._ranksymbols = '12345678'
        self._filesymbols = 'abcdefgh'

    def processusermove(self, userstring):
        """Converts the movement notation into an action within the engine."""
        # Determine what piece the user is using.
        def determinepiece(symbol):
            try:
                return self._symboltopiece[symbol]
            except KeyError:
                if symbol.upper() in self._symboltopiece:
                    raise NameError(
                        "I don't know the piece %r. Did you mean %r?" % \
                        (symbol, symbol.upper()))
                else:
                    raise core.UnknownPieceError(
                        "I don't know the piece with the symbol %r." % symbol)

        # Convert the notation into a positon.
        def notationtopositions(notationstring):
            try:
                assert 'x' in notationstring or '->' in notationstring
                (startpos, endpos) = (notationstring[:2], notationstring[-2:])

                filefunc = lambda x: self._filesymbols.index(x[0])
                rankfunc = lambda x: self._ranksymbols.index(x[1])

                startvec = Vector(rankfunc(startpos), filefunc(startpos))
                endvec = Vector(rankfunc(endpos), filefunc(endpos))
            except AssertionError:
                raise Exception(
                    "The notation string doesn't follow correct syntax rules.")
            else:
                return startvec, endvec

        # Now execute the process in order.
        piecetomove = self.determinepiece(userstring[0])
        startvec, endvec = self.notationtopositions(userstring[1:])
        return piecetomove, (startvec, endvec)

    def addmovetohistory(self, piecesymbol, startpos, endpos,
                         capture=False, check=False, checkmate=False,
                         castlelong=False, castleshort=False, promotionto=False):
        """Add a move to the recorded history."""
        # First turn the position into a notation string.
        def convertpositiontonotation():
            def getpositionstring(pos):
                (rank_, file_) = core.convert(pos, tocoordinate=True)
                return self._filesymbols[file_] + self._ranksymbols[rank_]

            startnotation = getpositionstring(startpos)
            endnotation = getpositionstring(endpos)
            if capture: concat = 'x'
            else: concat = '->'

            movestring = piecesymbol + startnotation + concat + endnotation

            if check:
                movestring += '+'
            elif checkmate:
                movestring += '#'
            if castlelong:
                movestring = '0-0-0'
            elif castleshort:
                movestring = '0-0'
            if promotionto:
                movestring += '=' + promotionto

            return movestring

        # Now add it to the history.
        self.history.append(self.convertpositiontonotation())
        return None

  #####  #     # ###
 #     # #     #  #
 #       #     #  #
 #  #### #     #  #
 #     # #     #  #
 #     # #     #  #
  #####   #####  ###


class EngineGUI:
    """The class that handles displaying and creating the GUI for the engine.

    The board, once decorated, looks like so:

    + -------- +
    | ....kq.. |
    | .bb..... |
    | ........ |
    | ..pp.... |
    | ..P..N.. |
    | ........ |
    | ....Q... |
    | ..k..... |
    + -------- +

    Where each '.' is a square on the board and the letter are the pieces.
    """

    def __init__(self):
        self.topborder = ' + -------- + \n'
        self.bottomborder = ' + -------- + \n'
        self.leftedgeborder = ' | '
        self.rightedgeborder = ' | \n'
        return None

    def drawasciiboard(self, boardlist):
        """Draws the ascii board."""
        # Start by drawing an empty board.
        # Iterate through boardlist.
        # If there is a piece there, get the piece symbol and draw it on the board.
        rankstrings = ['........'] * 8

        # Assign piece symbols to the undecorated board.
        for ii, square in enumerate(boardlist):
            if square == None:
                continue
            else:
                piece = square
                symbol = piece.notationsymbol
                (rank_, file_) = core.convert(ii, tocoordinate=True)
                rankstrings[rank_][file_] = symbol

        # Now decorate board.
        board = reduce(lambda x, y: x+y, map(
            lambda x: self.leftedgeborder + x self.rightedgeborder,
            rankstrings
        ))
        board = self.topborder + board + self.bottomborder
        return board