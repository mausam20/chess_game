
from abc import ABC, abstractmethod
from typing import List, Optional
from enum import Enum

class Spot:
    def __init__(self, x, y, piece=None):
        self._x = x
        self._y = y
        self._piece = piece

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, piece):
        self._piece = piece

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y



class Piece(ABC):
    def __init__(self, white: bool):
        self._white = white
        self._killed = False

    @property
    def white(self) -> bool:
        return self._white

    @white.setter
    def white(self, value: bool):
        self._white = value

    @property
    def killed(self) -> bool:
        return self._killed

    @killed.setter
    def killed(self, value: bool):
        self._killed = value

    @abstractmethod
    def can_move(self, board, start, end) -> bool:
        pass



class King(Piece):
    def __init__(self, white: bool):
        super().__init__(white)
        self._castling_done = False

    @property
    def castling_done(self) -> bool:
        return self._castling_done

    @castling_done.setter
    def castling_done(self, value: bool):
        self._castling_done = value

    def can_move(self, board, start, end) -> bool:
        # We can't move the piece to a spot that has a piece of the same color
        if end.piece is not None and end.piece.white == self.white:
            return False

        x = abs(start.x - end.x)
        y = abs(start.y - end.y)
        if x + y == 1:
            # In a full implementation, check if this move would put the king in check
            return True

        return self.is_valid_castling(board, start, end)

    def is_valid_castling(self, board, start, end) -> bool:
        if self.castling_done:
            return False

        # Add detailed castling rules and return True if valid, False otherwise
        # e.g. Rook hasn't moved, path is clear, king not in check etc.
        return False  # Placeholder

    def is_castling_move(self, start, end) -> bool:
        # Example placeholder logic for castling move
        # e.g. if king moves two squares horizontally on the same row
        return start.y == end.y and abs(start.x - end.x) == 2
    
    def __str__(self):
        return 'K' if self.white else 'k'


class Knight(Piece):
    def __init__(self, white: bool):
        super().__init__(white)

    def can_move(self, board, start, end) -> bool:
        # Can't move to a spot with a piece of the same color
        if end.piece is not None and end.piece.white == self.white:
            return False

        x = abs(start.x - end.x)
        y = abs(start.y - end.y)

        # Knight moves in L-shape: x * y should equal 2
        return x * y == 2
    
    def __str__(self):
        return 'N' if self.white else 'n'

class Bishop(Piece):
    def __init__(self, white: bool):
        super().__init__(white)

    def can_move(self, board, start, end) -> bool:
        # Can't move to a spot with a piece of the same color
        if end.piece is not None and end.piece.white == self.white:
            return False

        x = abs(start.x - end.x)
        y = abs(start.y - end.y)

        # Bishop moves diagonally: x and y should be equal
        return x == y
    
    def __str__(self):
        return 'K' if self.white else 'k'
    

class Rook(Piece):
    def __init__(self, white: bool):
        super().__init__(white)

    def can_move(self, board, start, end) -> bool:
        # Can't move to a spot with a piece of the same color
        if end.piece is not None and end.piece.white == self.white:
            return False

        x = abs(start.x - end.x)
        y = abs(start.y - end.y)
    
        # Rook moves horizontally or vertically: x or y should be 0
        return x == 0 or y == 0
    
    def __str__(self):
        return 'R' if self.white else 'r'
    

class Queen(Piece):
    def __init__(self, white: bool):
        super().__init__(white)

    def can_move(self, board, start, end) -> bool:
        # Can't move to a spot with a piece of the same color
        if end.piece is not None and end.piece.white == self.white:
            return False

        x = abs(start.x - end.x)
        y = abs(start.y - end.y)

        # Queen moves horizontally, vertically, or diagonally: x or y should be 0, or x and y should be equal
        return x == 0 or y == 0 or x == y
    
    def __str__(self):
        return 'Q' if self.white else 'q'
    

class Pawn(Piece):
    def __init__(self, white: bool):
        super().__init__(white)

    def can_move(self, board, start, end) -> bool:
        # Can't move to a spot with a piece of the same color
        if end.piece is not None and end.piece.white == self.white:
            return False

        x = abs(start.x - end.x)
        y = abs(start.y - end.y)

        # Pawn moves forward one step: x should be 0, y should be 1
        return x == 0 and y == 1 

    def __str__(self):
        return 'P' if self.white else 'p'
    



class Board:
    def __init__(self):
        self.boxes = [[None for _ in range(8)] for _ in range(8)]
        self.reset_board()

    def get_box(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            raise IndexError("Index out of bounds")
        return self.boxes[x][y]

    def reset_board(self):
        # Initialize white pieces
        self.boxes[0][0] = Spot(0, 0, Rook(True))
        self.boxes[0][1] = Spot(0, 1, Knight(True))
        self.boxes[0][2] = Spot(0, 2, Bishop(True))
        self.boxes[0][3] = Spot(0, 3, Queen(True))
        self.boxes[0][4] = Spot(0, 4, King(True))
        self.boxes[0][5] = Spot(0, 5, Bishop(True))
        self.boxes[0][6] = Spot(0, 6, Knight(True))
        self.boxes[0][7] = Spot(0, 7, Rook(True))
        for j in range(8):
            self.boxes[1][j] = Spot(1, j, Pawn(True))

        # Initialize black pieces
        self.boxes[7][0] = Spot(7, 0, Rook(False))
        self.boxes[7][1] = Spot(7, 1, Knight(False))
        self.boxes[7][2] = Spot(7, 2, Bishop(False))
        self.boxes[7][3] = Spot(7, 3, Queen(False))
        self.boxes[7][4] = Spot(7, 4, King(False))
        self.boxes[7][5] = Spot(7, 5, Bishop(False))
        self.boxes[7][6] = Spot(7, 6, Knight(False))
        self.boxes[7][7] = Spot(7, 7, Rook(False))
        for j in range(8):
            self.boxes[6][j] = Spot(6, j, Pawn(False))

        # Initialize empty boxes
        for i in range(2, 6):
            for j in range(8):
                self.boxes[i][j] = Spot(i, j, None)

    def print_board(self):
        print("  a b c d e f g h")
        for i in range(7, -1, -1):
            print(i + 1, end=' ')
            for j in range(8):
                piece = self.boxes[i][j].piece
                print(str(piece) if piece else '.', end=' ')
            print()
        print()

class Player(ABC):
    def __init__(self, white_side: bool, human_player: bool):
        self.white_side = white_side
        self.human_player = human_player

    def is_white_side(self) -> bool:
        return self.white_side

    def is_human_player(self) -> bool:
        return self.human_player


class HumanPlayer(Player):
    def __init__(self, white_side: bool):
        super().__init__(white_side, True)


class ComputerPlayer(Player):
    def __init__(self, white_side: bool):
        super().__init__(white_side, False)


class Move:
    def __init__(self, player, start, end):
        self.player = player
        self.start = start
        self.end = end
        self.piece_moved = start.piece
        self.piece_killed = end.piece if end.piece else None
        self.castling_move = False

    def is_castling_move(self):
        return self.castling_move

    def set_castling_move(self, castling_move: bool):
        self.castling_move = castling_move

class GameStatus(Enum):
    ACTIVE = 1
    BLACK_WIN = 2
    WHITE_WIN = 3
    FORFEIT = 4
    STALEMATE = 5
    RESIGNATION = 6


class Game:
    def __init__(self):
        self.players = [None, None]  # type: List[Optional[Player]]
        self.board = Board()
        self.current_turn = None  # type: Optional[Player]
        self.status = GameStatus.ACTIVE
        self.moves_played = []

    def initialize(self, p1, p2):
        self.players[0] = p1
        self.players[1] = p2

        self.board.reset_board()

        self.current_turn = p1 if p1.is_white_side() else p2
        self.moves_played.clear()

    def is_end(self):
        return self.status != GameStatus.ACTIVE

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def player_move(self, player, start_x, start_y, end_x, end_y):
        try:
            start_box = self.board.get_box(start_x, start_y)
            end_box = self.board.get_box(end_x, end_y)
        except Exception as e:
            return False

        move = Move(player, start_box, end_box)
        return self.make_move(move, player)

    def make_move(self, move, player):
        source_piece = move.start.piece
        if source_piece is None:
            return False

        # valid player
        if player != self.current_turn:
            print("Invalid player")
            return False

        if source_piece.white != player.is_white_side():
            print("Invalid piece")
            return False

        # valid move?
        if not source_piece.can_move(self.board, move.start, move.end):
            print("Invalid move")
            return False

        # kill?
        dest_piece = move.end.piece
        if dest_piece is not None:
            print("Killed")
            dest_piece.set_killed(True)
            move.set_piece_killed(dest_piece)

        # castling?
        if isinstance(source_piece, King) and source_piece.is_castling_move(move.start, move.end):
            print("Castling")
            move.set_castling_move(True)

        # store the move
        self.moves_played.append(move)

        # move piece from start to end box
        move.end.piece = move.start.piece
        move.start.piece = None

        if isinstance(dest_piece, King):
            print("Game over")
            self.set_status(GameStatus.WHITE_WIN if player.is_white_side() else GameStatus.BLACK_WIN)
            print(self.get_status())

        # switch turns
        self.current_turn = self.players[1] if self.current_turn == self.players[0] else self.players[0]

        self.board.print_board()

        return True



if __name__ == "__main__":
    game = Game()
    p1 = HumanPlayer(True)
    p2 = HumanPlayer(False)
    game.initialize(p1, p2)

    print("\nWhite player moves:")
    game.player_move(p1, 1, 4, 3, 4)  # White pawn e2 to e4

    print("\nBlack player moves:")
    game.player_move(p2, 6, 4, 4, 4)  # Black pawn e7 to e5

    print("\nWhite player moves:")
    game.player_move(p1, 0, 6, 2, 5)  # White knight g1 to f3


    print("\nBlack player moves:")
    game.player_move(p2, 7, 6, 5, 5)  # Black knight g8 to f6

    print("\nWhite player moves:")
    game.player_move(p1, 0, 5, 1, 4)  # White bishop f1 to e2

    print("\nBlack player moves:")
    game.player_move(p2, 7, 1, 5, 2)  # Black knight b8 to c6

    print("\nWhite player moves:")
    game.player_move(p1, 0, 3, 4, 7)  # White queen d1 to h5

    print("\nBlack player moves:")
    game.player_move(p2, 6, 6, 5, 6)  # Black pawn g7 to g6

    print("\nWhite player moves:")
    game.player_move(p1, 4, 7, 5, 6)  # Queen h5 takes g6
