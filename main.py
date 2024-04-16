import pyautogui as pg
import engine
import Proto
from plyer import notification
import keyboard
import os
import cv2
import numpy as np

def notify(message):
    '''Notify via Notifications'''
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'Sprites\P.ico')
    notification.notify(
        title="Best Move",
        message=message,
        timeout=3,
        app_icon=path
    )

def draw(obj, text):
    cv2.rectangle(scrn, 
                  (obj.left, obj.top),
                  (obj.left+obj.width, obj.top+obj.height),
                  (255, 0, 0),
                  2
                 )
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    cv2.putText(scrn, text, (obj.left, obj.top), font, 
                fontScale, color, thickness, cv2.LINE_AA
               )

def decideBoardAndSetConfigs():
    '''Decide board and set some configurations in code according to it'''
    global board, Turn
    WhiteBoard = None
    BlackBoard = None

    try:
        WhiteBoard = pg.locateOnScreen('Sprites/WhiteBoard.png', confidence=0.6)
    except Exception:
        pass

    try:
        BlackBoard =  pg.locateOnScreen('Sprites/BlackBoard.png', confidence=0.6)
    except Exception:
        pass
    
    if BlackBoard:
        Turn = 'b'
        notify('Board Identified! : \nBlack')
        print('Board Identified! : Black')
        board = BlackBoard
        alpha_list.reverse()
    
    elif WhiteBoard:
        Turn = 'w'
        notify('Board Identified! : \nWhite')
        print('Board Identified! : White')
        board = WhiteBoard
        num_list.reverse()

def make_blank_board_matrice():
    '''Returns a 2d Dict mocking chessboard from white perspective'''
    global board_matrice
    return dict(list(map(lambda x: (x, ['-' for x in range(8)]), reversed_one_to_eight)))

    # { 8:['-', '-', '-', '-', '-', '-', '-', '-'], 
    #   7:['-', '-', '-', '-', '-', '-', '-', '-'],
    #   6:['-', '-', '-', '-', '-', '-', '-', '-'],
    #   5:['-', '-', '-', '-', '-', '-', '-', '-'],
    #   4:['-', '-', '-', '-', '-', '-', '-', '-'],
    #   3:['-', '-', '-', '-', '-', '-', '-', '-'],
    #   2:['-', '-', '-', '-', '-', '-', '-', '-'],
    #   1:['-', '-', '-', '-', '-', '-', '-', '-']  }

def recognisePieces():
    '''Recognise all the pieces kept on the board and add it into "all_pieces" list'''
    for sample_piece in all_sample_pieces:
        sample_piece, confidence = sample_piece['sample_piece'], sample_piece['confidence']
        try:
            for piece in pg.locateAllOnScreen(f'sprites/{sample_piece}.png', confidence=confidence):
                found = 0
                for singlePiece in all_pieces:
                    #Below If statement checks if targeted square/piece is already inside "all_pieces"
                    if (piece.left-40<singlePiece.position['x'] and 
                        singlePiece.position['x']<piece.left+40 and 
                        piece.top-40<singlePiece.position['y'] and 
                        singlePiece.position['y']<piece.top+40):
                        found = 1
                    elif(piece.left<board.left or board.left+board.width<piece.left+40 or piece.top<board.top or board.top+board.height<piece.top):
                        found = 1
                
                #If piece is not inside "all_pieces" list
                if not found:  
                    draw(piece, FEN_names[sample_piece]) 
                    #Create a new "Proto.Pieces" object and maintain its state
                    #Position of x and y is relative to the screen and depends on where did u keep the window of chess board  
                    piece_position = {
                        'x': piece.left,
                        'y': piece.top
                    }
                    piece_offsets = {
                        'width': piece.width,
                        'height':piece.height
                    }
                    center = {
                        'x': piece.left+square_width/2,
                        'y': piece.top+square_height/2
                    }
                    piece = Proto.Pieces(sample_piece, piece_position, piece_offsets, center)
                    #Add the object inside "all_pieces" list
                    all_pieces.append(piece)
        except Exception:
             pass

def setSquare(piece):
    '''Set chessboard by filling abbr. names of pieces inside "board-matrices" array acc to assigned co-ordiates'''
    piece_alpha = piece.cord[0] #alpha of piece
    piece_num = piece.cord[1] #num of piece
    piece_sno_acc_alpha = a_to_h_list.index(piece_alpha)
    board_matrice[int(piece_num)][piece_sno_acc_alpha] = FEN_names[piece.pieceName]

def setCords():
    '''Set Co-ordinates of pieces acc to board'''
    for piece in all_pieces:
        alpha_sno = int((piece.center['x']-board.left)//int(square_width))
        num_sno = int((piece.center['y']-board.top)//int(square_height))        
        piece.cord = f'{alpha_list[alpha_sno]}{num_list[num_sno]}'
        setSquare(piece) 

def convertIntoFEN(board):
    '''Convert and Return a string of FEN system of a board(2D array mocking a chessboard)'''
    FEN_string = ""
    for col, matrice in board.items():
        blank_count = 0
        for single_piece in matrice:
            if single_piece.isalpha():
                if blank_count!=0:
                    FEN_string+=str(blank_count)
                    blank_count=0
                FEN_string+=single_piece
            elif single_piece=='-':
                blank_count+=1
        if blank_count!=0:
            FEN_string+=str(blank_count)
            blank_count=0
        if col>1:
            FEN_string+='/'
    FEN_string+=f' {Turn}'
    return FEN_string

#Pieces abbr. names, and confidence which is nedded to assure if recognised pieces matched or not (used during live recognition and undertsanding board)
all_sample_pieces = [
    {'sample_piece': 'BP', 'confidence': 0.7},
    {'sample_piece': 'BB', 'confidence': 0.7},
    {'sample_piece': 'BK', 'confidence': 0.6},
    {'sample_piece': 'BQ', 'confidence': 0.6},
    {'sample_piece': 'BR', 'confidence': 0.6},
    {'sample_piece': 'BN', 'confidence': 0.5},
    # -------------------------------------
    {'sample_piece': 'WQ', 'confidence': 0.5},
    {'sample_piece': 'WP', 'confidence': 0.4},
    {'sample_piece': 'WN', 'confidence': 0.4},
    {'sample_piece': 'WK', 'confidence': 0.4},
    {'sample_piece': 'WB', 'confidence': 0.4},
    {'sample_piece': 'WR', 'confidence': 0.4},
]

#Relation of abbr. names and notion which is being used in FEN system (a system to express whole board in single string)
FEN_names = {
    'BR': 'r',
    'BN': 'n',
    'BB': 'b',
    'BK': 'k',
    'BQ': 'q',
    'BP': 'p',
    
    'WR': 'R',
    'WN': 'N',
    'WB': 'B',
    'WK': 'K',
    'WQ': 'Q',
    'WP': 'P',
}

# Environment Variable which is used to serve different puposes further in code

# see any chess board to undertsand things mentioned below 
# eg: https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/ColinStapczynski/phpa2wQPr.png

#List of Alphabets used in naming different column from (left to right) acc to with which pieces you are playin in your current game (Either  a-h or h-a)
#White: (a-h); Black: (h-a) 
alpha_list = [chr(x) for x in range(97, 105)] 

#List of Alphabets used in naming different column from (top to bottom) acc to with which pieces you are playin in your current game (Either  1-8 or 8-1)
#White: (8-1); Black: (1-8) 
num_list = [x for x in range(1, 9)]

#All object of class Proto.Pieces will get stored here
all_pieces = []

#From which side you are playing (either w or b)
Turn = None

#Some lists to use further in code if needed
a_to_h_list = [chr(x) for x in range(97, 105)]
reversed_one_to_eight =  [x for x in reversed(range(1, 9))]

board = None
square_width = None
square_height = None
board_matrice = None

if __name__ == '__main__':
    
    decideBoardAndSetConfigs()
    try:
        square_width = board.width/8
        square_height = board.height/8
        scrn = pg.screenshot()
        scrn = cv2.cvtColor(np.array(scrn), cv2.COLOR_RGB2BGR)
        while 1:
            print('Waiting for opponent to move....')
            keyboard.wait('ctrl')
            
            print('Opponnet Moved! Figuring Out Positions')
            board_matrice = make_blank_board_matrice()
            
            #(Re)initialising the positions
            all_pieces = []
            
            recognisePieces()
            setCords()
            
            # Feeding that FEN string into engine      
            engine.chessboard.set_fen(convertIntoFEN(board_matrice))

            #Print the recognised chessboard from the screen
            print(engine.chessboard)
            
            #Getting the best move
            best_move = str(engine.get_best_move())
            
            from_square = {
                "alpha": best_move[0:2][0],
                "num": best_move[0:2][1] 
            }
            to_square = {
                "alpha": best_move[2:5][0],
                "num": best_move[2:5][1] 
            }
            pg.moveTo(board.left+alpha_list.index(from_square['alpha'])*square_width+square_width/2, board.top+num_list.index(int(from_square['num']))*square_width+square_height/2)
            pg.dragTo(board.left+alpha_list.index(to_square['alpha'])*square_width+square_width/2, board.top+num_list.index(int(to_square['num']))*square_width+square_height/2)
                    
            print(f'best move: {best_move}')
            notify(best_move)
    except Exception as e:
        print(e)
        print("Board Not Found : (")