import chess
import chess.engine
stockfish_location = "E:\\Chess\\stockfish_15.1_win_x64_avx2\\stockfish-windows-2022-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(stockfish_location)
chessboard = chess.Board()

def get_best_move():
    '''Returns Best move acc to the board'''
    return engine.play(chessboard, chess.engine.Limit(time=0.1)).move
    # return "b4b5"