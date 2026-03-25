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
        self.board = Board()
        self.shipplacementboard = self.board.Board
        self.enemyboard = self.board.EnemyBoardRepresentation
        self.ships = []
        ship_sizes = [(1,4), (2,3), (3,2), (4,1)]
        for size, count in ship_sizes:
            for i in range(count):
                self.ships.append(Ship(size))
    
    #Ships Availible (And Pick Ship)
    def availible_ships(self):
        return [ship for ship in self.ships if not ship.placed]
    
    def availible_positions(self, ship):
            positions = {"Horizontal-Right":[], "Horizontal-Left":[], "Vertical-Down":[], "Vertical-Up":[]}
            
            for r in range(self.board.size):
                for c in range(self.board.size):
                    # 0: Right, 1: Left, 2: Down, 3: Up
                    plots = [[], [], [], []]
                    
                    for i in range(ship.length):
                        # Horizontal Right
                        plots[0].append(self.shipplacementboard[r][c+i] if c+i < self.board.size else -1)
                        # Horizontal Left
                        plots[1].append(self.shipplacementboard[r][c-i] if c-i >= 0 else -1)
                        # Vertical Down
                        plots[2].append(self.shipplacementboard[r+i][c] if r+i < self.board.size else -1)
                        # Vertical Up
                        plots[3].append(self.shipplacementboard[r-i][c] if r-i >= 0 else -1)

                    keys = list(positions.keys())
                    for i in range(4):
                        if all(val == 0 for val in plots[i]):
                            positions[keys[i]].append((r, c))
            return positions
    #Spots Availible on Enemy Board Representation (And Hit Spot)
    def availible_firing_positions(self):
            positions = []
            for r in range(self.board.size):
                for c in range(self.board.size):
                    if self.enemyboard[r][c] == 0:
                        positions.append((r, c))
            return positions

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