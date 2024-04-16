class Pieces:
    '''Maintain state of recognised pieces from screen'''
    def __init__(self, pieceName, position, offset, center):
        self.pieceName = pieceName
        self.position = position
        self.offset = offset
        self.center = center