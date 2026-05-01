import os
from datetime import datetime

LOG_FILE = "win_log.txt"


def write_log(message):
    print(message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def view_log():
    if not os.path.exists(LOG_FILE):
        print("Log is empty.")
        return
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    if content.strip() == "":
        print("Log is empty.")
    else:
        print(content)


def clear_log():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")
    print("Log cleared.")


def make_board():
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board):
    print()
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("---------")
    print()


def check_winner(board, symbol):
    for row in board:
        if all(cell == symbol for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == symbol for row in range(3)):
            return True
    if all(board[i][i] == symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == symbol for i in range(3)):
        return True
    return False


def is_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_move(player_name):
    try:
        row = int(input(f"{player_name}, enter row (1-3): ")) - 1
        col = int(input(f"{player_name}, enter column (1-3): ")) - 1
        if row not in range(3) or col not in range(3):
            print("Numbers must be between 1 and 3.")
            return None
        return row, col
    except ValueError:
        print("Please enter a number.")
        return None


def play_game(player1, player2, score):
    board = make_board()
    players = [(player1, "X"), (player2, "O")]
    turn = 0

    while True:
        print_board(board)
        name, symbol = players[turn % 2]
        print(f"{name}'s turn ({symbol})")

        move = get_move(name)
        if move is None:
            continue

        row, col = move
        if board[row][col] != " ":
            print("That cell is already taken.")
            continue

        board[row][col] = symbol

        if check_winner(board, symbol):
            print_board(board)
            now = datetime.now().strftime("%d.%m.%Y %H:%M")
            write_log(f"{now} – {name} won")
            score[name] = score.get(name, 0) + 1
            return "win"

        if is_full(board):
            print_board(board)
            print("Draw!")
            return "draw"

        turn += 1


def print_score(player1, player2, score):
    p1 = score.get(player1, 0)
    p2 = score.get(player2, 0)
    print(f"\nScore: {player1} – {p1} | {player2} – {p2}\n")


def start_session():
    player1 = input("Enter name for Player 1 (X): ").strip() or "Player 1"
    player2 = input("Enter name for Player 2 (O): ").strip() or "Player 2"
    score = {}

    while True:
        play_game(player1, player2, score)
        print_score(player1, player2, score)
        again = input("Play again with same players? (y/n): ").strip().lower()
        if again != "y":
            break


def show_menu():
    print("\n--- Tic Tac Toe ---")
    print("1. Play")
    print("2. View win log")
    print("3. Clear win log")
    print("4. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose option: ").strip()

        if choice == "1":
            start_session()
        elif choice == "2":
            view_log()
        elif choice == "3":
            clear_log()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
