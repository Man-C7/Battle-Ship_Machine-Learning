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
        return self.ships
    
    def availible_positions(self, ship):
        #Takes in ship object shows availible positions for said ship
        positions = {"Vertical-Left":[],"Vertical-Right":[],"Horizontal-Down":[],"Horizontal-Up":[]}
        for row in self.shipplacementboard:
            for column in row:
                plots = [[],[],[],[]]
                #vertical left
                for i in range(ship.length):
                    if column + i <= self.board.size -1:
                        plots[0].append(self.shipplacementboard[row][column + i])
                    else:
                        plots[0].append(-1)
                #vertical right
                for i in range(ship.length):
                    if column - i >= 0:
                        plots[1].append(self.shipplacementboard[row][column - i])
                    else:
                        plots[1].append(-1)
                #horizontal down
                for i in range(ship.length):
                    if row + i <= self.board.size -1:
                        plots[2].append(self.shipplacementboard[row + i][column])
                    else:
                        plots[2].append(-1)
                #horizontal up
                for i in range(ship.length):
                    if row - i >= 0:
                        plots[2].append(self.shipplacementboard[row - 1][column])
                    else:
                        plots[2].append(-1)
                for i in range(len(plots)):
                    if all(numbers == 0 for numbers in plots[list]):
                        if i == 0:
                            positions["Vertical-Left"].append((row,column))
                        elif i == 1:
                            positions["Vertical-Right"].append((row,column))
                        elif i == 2:
                            positions["Horizontal-Down"].append((row,column))
                        elif i == 3:
                            positions["Horizontal-Up"].append((row,column))
        return positions
    #Spots Availible on Enemy Board Representation (And Hit Spot)
    def availible_firing_positions(self):
        positions = []
        for row in self.enemyboard:
            for column in row:
                if self.enemyboard[row][column] == 0:
                    positions.append((row,column))

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