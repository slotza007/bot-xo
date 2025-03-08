from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ข้อมูลบอร์ดเริ่มต้น
game_state = {
    "board": [[" " for _ in range(3)] for _ in range(3)],
    "board_size": [[0 for _ in range(3)] for _ in range(3)],
    "player_turn": "X",
    "X_sizes": [3, 3, 2],  # จำนวนหมากของ X
    "O_sizes": [3, 3, 2],  # จำนวนหมากของ O
    "winner": None
}

# ฟังก์ชันตรวจสอบผู้ชนะ
def check_winner(board):
    # ตรวจสอบแถว
    for row in board:
        if all(cell == row[0] and cell != ' ' for cell in row):
            return row[0]
    # ตรวจสอบคอลัมน์
    for col in range(3):
        if all(board[row][col] == board[0][col] and board[row][col] != ' ' for row in range(3)):
            return board[0][col]
    # ตรวจสอบแนวทแยง
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset_game():
    global game_state
    game_state = {
        "board": [[" " for _ in range(3)] for _ in range(3)],
        "board_size": [[0 for _ in range(3)] for _ in range(3)],
        "player_turn": "X",
        "X_sizes": [3, 3, 2],
        "O_sizes": [3, 3, 2],
        "winner": None
    }
    return jsonify(game_state)

@app.route('/move', methods=['POST'])
def make_move():
    global game_state
    data = request.json
    row, col, size = int(data['row']), int(data['col']), int(data['size'])
    player = game_state["player_turn"]

    # ตรวจสอบว่าหมากวางได้หรือไม่
    if game_state["board_size"][row][col] < size and game_state[f"{player}_sizes"][size - 1] > 0:
        game_state["board"][row][col] = player
        game_state["board_size"][row][col] = size
        game_state[f"{player}_sizes"][size - 1] -= 1

        # ตรวจสอบผู้ชนะ
        winner = check_winner(game_state["board"])
        if winner:
            game_state["winner"] = winner
        else:
            # สลับตา
            game_state["player_turn"] = "O" if player == "X" else "X"

    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True)