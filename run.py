import random

# Initialize the grids
player_grid = [['_' for _ in range(10)] for _ in range(10)]
opponent_grid = [['_' for _ in range(10)] for _ in range(10)]
player_visible_grid = [['_' for _ in range(10)] for _ in range(10)]  # To show hits and misses to the player
opponent_visible_grid = [['_' for _ in range(10)] for _ in range(10)]  # To show hits and misses to the opponent

# Define ship sizes
ships = [5, 4, 4, 3, 3, 2, 2, 2, 2]  # 1 carrier, 2 battleships, 2 frigates, 4 minesweepers

def display_grid(grid):
    """Display the grid."""
    print(" 1 2 3 4 5 6 7 8 9 10")
    alphabet = 'ABCDEFGHIJ'
    for i, row in enumerate(grid):
        print(alphabet[i], " ".join(row))

def validate_input(user_input):
    if len(user_input) < 2 or len(user_input) > 3:
        return False
    row, col = user_input[0], user_input[1:]
    if not row.isalpha() or not col.isdigit():
        return False
    col = int(col) - 1
    row = 'ABCDEFGHIJ'.index(row.upper())
    if row < 0 or row >= len(player_grid) or col < 0 or col >= len(player_grid[0]):
        return False
    return True

def convert_input(user_input):
    row, col = user_input[0], user_input[1:]
    col = int(col) - 1
    row = 'ABCDEFGHIJ'.index(row.upper())
    return row, col

def place_ship(grid, size):
    placed = False
    while not placed:
        orientation = random.choice(['H', 'V'])
        if orientation == 'H':
            row = random.randint(0, 9)
            col = random.randint(0, 9 - size)
            if all(grid[row][c] == '_' for c in range(col, col + size)):
                for c in range(col, col + size):
                    grid[row][c] = 'S'
                placed = True
        else:  # Vertical
            row = random.randint(0, 9 - size)
            col = random.randint(0, 9)
            if all(grid[r][col] == '_' for r in range(row, row + size)):
                for r in range(row, row + size):
                    grid[r][col] = 'S'
                placed = True

# Randomly place ships on both grids
for size in ships:
    place_ship(player_grid, size)
    place_ship(opponent_grid, size)

def user_guess():
    while True:
        user_input = input("Enter your guess (e.g., A1 or A10): ").replace(' ', '')
        if validate_input(user_input):
            return convert_input(user_input)
        else:
            print("Invalid input. Please enter valid coordinates in the format A1 or A10.")

def computer_guess():
    while True:
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        if player_visible_grid[row][col] == '_':
            return row, col

def check_guess(grid, visible_grid, row, col):
    if grid[row][col] == 'S':
        visible_grid[row][col] = 'X'
        grid[row][col] = 'X'
        return "Hit!"
    else:
        visible_grid[row][col] = 'O'
        return "Miss!"

def check_all_ships_sunk(grid):
    return all(cell != 'S' for row in grid for cell in row)

# Game loop
turn_count = 0
print("Player's Grid:")
display_grid(player_grid)
print("\nOpponent's Grid (hidden):")
display_grid(opponent_visible_grid)

game_over = False

while not game_over:
    if turn_count % 2 == 0:
        row, col = user_guess()
        result = check_guess(opponent_grid, opponent_visible_grid, row, col)
        print(result)
        print("\nOpponent's Grid:")
        display_grid(opponent_visible_grid)
        if check_all_ships_sunk(opponent_grid):
            print("Congratulations! You've sunk all opponent's ships. You win!")
            game_over = True
    else:
        row, col = computer_guess()
        result = check_guess(player_grid, player_visible_grid, row, col)
        print(f"Computer guessed {chr(row + 65)}{col + 1}: {result}")
        print("\nPlayer's Grid:")
        display_grid(player_visible_grid)
        if check_all_ships_sunk(player_grid):
            print("All your ships have been sunk. The computer wins!")
            game_over = True

    turn_count += 1