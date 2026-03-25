class Board():
    def __init__(self, size=10):
        self.size = size

        #0:Empty, 1:Ship, -1:Missed Shot, 2: Hit Ship
        self.grid = [[0 for i in range(self.size)] for j in range(self.size)]
        
        #1:Miss, 2:Hit, 0:Unkown
        self.EnemyBoardRepresentation = [[0 for i in range(self.size)] for j in range(self.size)] 

        # Pre-scan Maps
        self.h_map = [[0 for i in range(size)] for j in range(size)]
        self.v_map = [[0 for i in range(size)] for j in range(size)]
        self.recompute_maps()  

    def recompute_maps(self):
        for r in range(self.size):
            count = 0
            # Scan Right to Left for Horizontal
            for c in range(self.size - 1, -1, -1):
                if self.grid[r][c] == 0:
                    count += 1
                else:
                    count = 0
                self.h_map[r][c] = count

        for c in range(self.size):
            count = 0
            # Scan Bottom to Top for Vertical
            for r in range(self.size - 1, -1, -1):
                if self.grid[r][c] == 0:
                    count += 1
                else:
                    count = 0
                self.v_map[r][c] = count

    def is_valid_fast(self, r, c, length, horizontal=True):
        if horizontal:
            return self.h_map[r][c] >= length
        return self.v_map[r][c] >= length

class Ship():
    def __init__(self, length):
        self.length = length
        self.pieces_hit = 0
        self.placed = False

class Player():
    def __init__(self):
        self.board = Board()
        self.shipplacementboard = self.board.grid
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
        # We still return a dictionary for compatibility with your previous setup
        positions = {"Horizontal": [], "Vertical": []}
        length = ship.length
        
        for r in range(self.board.size):
            for c in range(self.board.size):
                # Horizontal Check: Just look at one number in the h_map
                if self.board.h_map[r][c] >= length:
                    positions["Horizontal"].append((r, c))
                    
                # Vertical Check: Just look at one number in the v_map
                if self.board.v_map[r][c] >= length:
                    positions["Vertical"].append((r, c))
                    
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