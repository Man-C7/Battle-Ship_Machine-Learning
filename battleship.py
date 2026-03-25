import random
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
    def __init__(self, length, ship_id):
        self.length = length
        self.pieces_hit = 0
        self.ship_id = ship_id
        self.placed = False

class Player():
    def __init__(self):
        self.board = Board()
        self.shipplacementboard = self.board.grid
        self.enemyboard = self.board.EnemyBoardRepresentation
        self.ships = []

        #(Size, Count)
        ship_sizes = [(1,4), (2,3), (3,2), (4,1)]
        ship_counter = 0
        for size, count in ship_sizes:
            for i in range(count):
                ship_id = f"Ship_{size}_{ship_counter}"
                self.ships.append(Ship(size, ship_id))
                ship_counter += 1
    
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

    def all_legal_positions(self):
        legal_moves = []
        ships_to_place = self.availible_ships()

        for ship in ships_to_place:
            # Re-use your fast map-based logic
            positions = self.availible_positions(ship)
            
            for r, c in positions["Horizontal"]:
                legal_moves.append({
                    "ship": ship, 
                    "row": r, 
                    "col": c, 
                    "direction": "Horizontal"
                })
                
            for r, c in positions["Vertical"]:
                legal_moves.append({
                    "ship": ship, 
                    "row": r, 
                    "col": c, 
                    "direction": "Vertical"
                })
                
        return legal_moves

    #Spots Availible on Enemy Board Representation (And Hit Spot)
    def availible_firing_positions(self):
            positions = []
            for r in range(self.board.size):
                for c in range(self.board.size):
                    if self.enemyboard[r][c] == 0:
                        positions.append((r, c))
            return positions
    
    def place_ship(self, ship, r, c, direction):
        for i in range(ship.length):
            nr, nc = (r, c + i) if direction == 'Horizontal' else (r + i, c)
            # Store the  ship object in the grid cell
            self.board.grid[nr][nc] = ship 
        
        ship.placed = True
        self.board.recompute_maps()


    def place_ships_randomly(self):
        #Sorted Ships
        ships_to_place = sorted(self.ships, key=lambda x: x.length, reverse=True)

        for ship in ships_to_place:
            #Get all currently legal moves for this specific ship
            options = []
            positions = self.availible_positions(ship)

            for r, c in positions["Horizontal"]:
                options.append((r, c, "Horizontal"))
            for r, c in positions["Vertical"]:
                options.append((r, c, "Vertical"))
            
            if not options:
                # If we get stuck (rare on 10x10), reset and try again
                self.reset_placements()
                return self.place_ships_randomly()
            # Pick a move at random
            r, c, direction = random.choice(options)
            
            # Place it
            self.place_ship(ship, r, c, direction)
            
    def reset_placements(self):
        self.board.grid = [[0 for _ in range(self.board.size)] for _ in range(self.board.size)]

        for ship in self.ships:
            ship.placed = False

        self.board.recompute_maps()
    
    def fire_shot(self, r, c, opponent):
        target = opponent.board.grid[r][c]
        
        if isinstance(target, Ship):
            target.pieces_hit += 1
            
            # Update the opponent's grid to reflect a hit (2)
            # This 'destroys' the Ship reference in that cell so it can't be hit twice
            opponent.board.grid[r][c] = 2 
            
            # Update your own memory of the enemy board
            self.enemyboard[r][c] = 2 
            
            if target.pieces_hit == target.length:
                return "SUNK", target.ship_id
            return "HIT", target.ship_id
        
        else:
            # Mark the opponent's grid as a Miss
            opponent.board.grid[r][c] = -1
            
            # Update own memory
            self.enemyboard[r][c] = 1
            return "MISS", None

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
                #If Miss, turn+= 1