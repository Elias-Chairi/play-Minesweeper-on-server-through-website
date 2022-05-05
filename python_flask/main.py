from flask import Flask
from flask import request
from flask import render_template
from time import sleep
import subprocess


def get_game_info():
    sleep(0.3)
    command_file = open("command_files/flask_command.txt","r") #get command from command file

    bomb_number_grid = command_file.readline()
    bomb_number_grid = bomb_number_grid.strip(']\n[').split(', ')

    revealed_grid = command_file.readline()
    revealed_grid = revealed_grid.strip(']\n[').split('>, <')
    revealed_grid[0] = revealed_grid[0].strip('<') # clean up first list item
    revealed_grid[len(revealed_grid) -1] = revealed_grid[len(revealed_grid) -1].strip('>') # clean up last list item

    gridRects = command_file.readline()
    gridRects = gridRects.strip(']\n[').split('>, <')
    gridRects[0] = gridRects[0].strip('<') # clean up first list item
    gridRects[len(gridRects) -1] = gridRects[len(gridRects) -1].strip('>') # clean up last list item

    marked_bombs = command_file.readline()
    marked_bombs = marked_bombs.strip(']\n[').split('>, <')
    marked_bombs[0] = marked_bombs[0].strip('<') # clean up first list item
    marked_bombs[len(marked_bombs) -1] = marked_bombs[len(marked_bombs) -1].strip('>') # clean up last list item

    no_bombs = None
    hit_bomb = None
    win_loose = command_file.readline().split(" ")
    if win_loose != ['']:
        no_bombs = win_loose[0]
        hit_bomb = win_loose[1]

    command_file.close()

    return bomb_number_grid, revealed_grid, gridRects, marked_bombs, no_bombs, hit_bomb


def get_website():
    bomb_number_grid, revealed_grid, gridRects, marked_bombs, no_bombs, hit_bomb = get_game_info()

    html_buttons = ""

    start_restart_button = ""
    if gridRects == [""]:
        return (
             """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel= "stylesheet" type= "text/css" href= "/static/style.css">
                <title>PYTHON MINESEEPER</title>
            </head>
            <body>
                <h1>Python Minesweeper!</h1>
                <form action="." method="POST" id="gameBoardForm">
                    <div id="menu"></div>
                    <button type='submit' id='startRestartButton' name='gridBox' value='start'> Start </button>
                </form>

                <script src="/static/script.js"></script>
            </body>
            </html>
            """
        )

    elif gridRects == ["new"]: #if clean give clean
        for i in range(100):
            html_buttons += "<button type='submit' class='gridBox' name='gridBox' value="+ str(i) +"></button>"
    
    elif hit_bomb == "True" or no_bombs == "True": #if game over or win
        for i in range(len(gridRects)):
            if bomb_number_grid[i] == "9":
                if hit_bomb == "True":
                    html_buttons += "<button type='submit' class='bomb' name='gridBox'> <img src='/static/bomb.png' width='50' height='50'> </button>"
                else:
                    html_buttons += "<button type='submit' class='winBomb' name='gridBox'>  </button>"
            else:
                rect_is_revealed = False
                for rect in revealed_grid:
                    if rect == gridRects[i]:
                        html_buttons += "<button type='submit' class='revealed' name='gridBox'></button>"
                        rect_is_revealed = True
                        break

                if rect_is_revealed == False:
                    html_buttons += "<button type='submit' class='gridBox' name='gridBox'></button>"
        start_restart_button = "<button type='submit' id='startRestartButton' name='gridBox' value='start'> Start </button>"
        pygame_shell.kill()
    
    else: #if game is still going
        for i in range(len(gridRects)):
            if bomb_number_grid != [""]:
                bomb_number = bomb_number_grid[i]
                if bomb_number_grid[i] == "0":
                    bomb_number = ""
            else:
                bomb_number = ""

            rect_is_revealed = False
            for rect in revealed_grid:
                if rect == gridRects[i]:
                    html_buttons += "<button type='submit' class='revealed' name='gridBox' value="+ str(i) +">"+ str(bomb_number) +"</button>"
                    rect_is_revealed = True
                    break

            if rect_is_revealed == False: # if not revealed check if marked
            
                rect_is_marked = False
                for rect in marked_bombs:
                    if rect == gridRects[i]:
                        html_buttons += "<button type='submit' class='gridBox' name='gridBox' value="+ str(i) +"> <img src='/static/flag.png' width='50' height='50'> </button>"
                        rect_is_marked = True
                        break

                if rect_is_marked == False: # if not marked or revealed do this
                    html_buttons += "<button type='submit' class='gridBox' name='gridBox' value="+ str(i) +"></button>"

    return (
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel= "stylesheet" type= "text/css" href= "/static/style.css">
            <title>PYTHON MINESEEPER</title>
        </head>
        <body>
            <h1>Python Minesweeper!</h1>
            <form action="." method="POST" id="gameBoardForm">
                <div id="menu"></div>
                """ + html_buttons
                    + start_restart_button #start/restart button is made if lost or won
                    + """
            </form>

            <script src="/static/script.js"></script>
        </body>
        </html>
        """
    )



app = Flask(__name__)

@app.route('/')
def my_form():
    return get_website()
    # return render_template("index.html") # this should be the name of your html file

@app.route('/', methods=['POST'])
def my_form_post():
    gridbox_clicked = request.form["gridBox"]

    if gridbox_clicked == "start":
        global pygame_shell
        pygame_shell = subprocess.Popen("python3 python_pygame/main.py", shell=True)
        sleep(2)
        return get_website()

    elif gridbox_clicked == "":
        return get_website()

    elif int(gridbox_clicked) > 99: #trying to place/remove flag
        flag_index = int(gridbox_clicked) - 100
        command_file = open("command_files/pygame_command.txt","w") #send command
        command_file.write("flag")
        command_file.write("\n")
        command_file.write(str(flag_index))
        command_file.close()
    else:
        command_file = open("command_files/pygame_command.txt","w") #send command
        command_file.write(gridbox_clicked)
        command_file.close()

    return get_website()
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
