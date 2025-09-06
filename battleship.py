
class Board():
    def __init__(self, size=10):
        self.size = size

        #0:Empty, 1:Ship, -1:Missed Shot, 2: Hit Ship
        self.Board = [[0 for i in range(self.size)] for j in range(self.size)]
        
        #1:Miss, 2:Hit, 0:Unkown
        self.EnemyBoardRepresentation = [[0 for i in range(self.size)] for j in range(self.size)]    

class Ship():
    def __init__(self, length):
        self.length = length
        self.pieces_hit = 0
        self.placed = False

class Player():
    def __init__(self):
        self.board = Board.Board
        self.enemyboard = Board.EnemyBoardRepresentation
        self.ships = []
        ship_sizes = [(1,4), (2,3), (3,2), (4,1)]
        for size, count in ship_sizes:
            for i in range(count):
                self.ships.append(Ship(size))
    
    #Ships Availible (And Pick Ship)
    def availible_ships(self):
        return self.ships
    
    def availible_positions(self, ship):
        positions = []
        for row in self.board:
            for collumn in row:
                plots = []
                #vertical
                for i in range(ship.length):
                    if 
                #horizontal
    
    #Positions Availible for the ship both horizontal and Vertical (And Place Ship)
    
    #Spots Availible on Enemy Board Representation (And Hit Spot)


        

class BattleshipGame():
    def __init__(self):
        self.turn = 0
        self.Player1 = Player()
        self.Player2 = Player()
    
    #Ship Placing Phase for player 1 and 2
    #Game Start
        #While won = false:
            #If turn is even, player 1 goes, else player 2
            #Player picks spot on enemy board
                #All Markings Added
                #If Hit, player goes again
                    #If Ship Hit has all pieces hit, surround squares get marked as missed shots, and also gets to go again
                #If Miss, turn+=1