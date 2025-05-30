from sudoku import Sudoku
from flask import Flask, request, render_template
from typing import Tuple
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
sudoku:Sudoku

@app.route('/',methods=['GET'])
def check():
    return "Success",200

@app.route('/is_valid', methods=['POST'])
def is_valid():
    global sudoku
    data = request.get_json()
    row = data.get("row")
    column = data.get("column")
    value = data.get("value")
    if row != None or column != None or value != None:
        if sudoku.is_valid(row, column, value):
            sudoku.make_move(row, column, value)
            output:Tuple[str,int] = "Valid move",200
        else:
            if sudoku.decrement_chance():
                output:Tuple[str,int] = "Invalid move",400
            else:
                output:Tuple[str,int] = "Chances Exhausted \n Game Over",400
    else:
        output:Tuple[str,int] = "Enter all the inputs",400
    return output

@app.route('/check_chance', methods=['GET'])
def check_chance():
    global sudoku
    return str(sudoku.chance()), 200    

@app.route('/init_game', methods=['POST'])
def new_game():
    global sudoku
    data = request.get_json()
    n = data.get("size")
    if n != None:
        sudoku = Sudoku(n)
        output:Tuple[str,int] = "Game started",200
    else:
        output:Tuple[str,int] = "Enter the input",400
    return output

@app.route('/get_sudoku', methods=['GET'])
def any_sudoku():
    global sudoku
    return "{" + str(sudoku) + "}"

@app.route('/restart', methods=['POST'])
def restart():
    global sudoku
    sudoku.restore()
    return "Game restarted", 200

@app.route('/check_winner', methods = ['POST'])
def check_winner():
    return str(sudoku.check_winner()),200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)

