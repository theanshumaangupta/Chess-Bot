import chess
import chess.engine
stockfish_location = "PATH_TO_YOUR_STOCKFISH_ENGINE"
engine = chess.engine.SimpleEngine.popen_uci(stockfish_location)
chessboard = chess.Board()

def get_best_move():
    '''Returns Best move acc to the board'''
    return engine.play(chessboard, chess.engine.Limit(time=0.1)).move
    # return "b4b5"