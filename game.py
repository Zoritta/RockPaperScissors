import sys
from tkinter import *
from network import connect, send, close
from tkinter import simpledialog, PhotoImage, Frame
from random import randint
import tkinter as tk


def tk_sleep(window, t):
    ms = int(t*1000)
    var = tk.IntVar(window)
    window.after(ms, lambda:
                 var.set(1))
    window.wait_variable(var)


# Create Object
window = Tk()

# Set geometry
window.geometry("500x500")
game_exit = False

#closing event handler


def on_closing():
    close()
    window.destroy()
    game_exit = True


def close():
    print("Closing the game...")


window.protocol("WM_DELETE_WINDOW", on_closing)

# Set title
window.title("Rock Paper Scissor Game")

game_state = {
    'player1': None,
    'player2': None,
    'player1_selection': None,
    'player2_selection': None
}

result_assessment = [
    ['Rock', 'Paper', 'player2'],
    ['Paper', 'Rock', 'player1'],
    ['Scissor', 'Rock', 'player2'],
    ['Rock', 'Scissor', 'player1'],
    ['Paper', 'Scissor', 'player2'],
    ['Scissor', 'Paper', 'player1']
]


def evaluate_result():
    if game_state['player1_selection'] and game_state['player2_selection']:
        player1_selection_label.config(
            text=game_state['player1_selection'] + "         ")
        player2_selection_label.config(text=game_state['player2_selection'])
        if game_state['player1_selection'] == game_state['player2_selection']:
            status_label.config(text="It is a tie :(")
        else:
            for x in result_assessment:
                if x[0] == game_state['player1_selection'] and x[1] == game_state['player2_selection']:
                    status_label.config(text=game_state[x[2]] + " Won")

# Reset The Game


def reset_game():
    rock_button["state"] = "active"
    paper_button["state"] = "active"
    scissor_button["state"] = "active"
    player1_selection_label.config(text="Player 1       ")
    player2_selection_label.config(text="Player 2")
    status_label.config(text="")
    game_state['player1_selection'] = None
    game_state['player2_selection'] = None
    status_label.config(text=game_state['player2'] + " connected")

# Disable the Button


def button_disable():
    rock_button["state"] = "disable"
    paper_button["state"] = "disable"
    scissor_button["state"] = "disable"

# If player selected rock


def isrock():
    game_state['player1_selection'] = 'Rock'
    send('Rock')
    evaluate_result()
    button_disable()

# If player selected paper


def ispaper():
    game_state['player1_selection'] = 'Paper'
    send('Paper')
    evaluate_result()
    button_disable()

# If player selected scissor


def isscissor():
    game_state['player1_selection'] = 'Scissor'
    send('Scissor')
    evaluate_result()
    button_disable()



Label(window,
      text="Rock Paper Scissor",
      font="normal 20 bold",
      fg="light blue").pack(pady=20)

frame = Frame(window)
frame.pack()

player_name_label = Label(window,
                          text="",
                          font="normal 20 bold",
                          bg="green",
                          width=15,
                          borderwidth=2,
                          relief="solid")
player_name_label.pack(pady=20)

player1_selection_label = Label(frame,
                                text="Player 1       ",
                           font=10)

versus_label = Label(frame,
                     text="VS             ",
                     font="normal 10 bold")

player2_selection_label = Label(frame, text="Player 2", font=10)

player1_selection_label.pack(side=LEFT)
versus_label.pack(side=LEFT)
player2_selection_label.pack()

status_label = Label(window,
                     text="",
                     font="normal 20 bold",
                     bg="white",
                     width=15,
                     borderwidth=2,
                     relief="solid")
status_label.pack(pady=20)

frame1 = Frame(window)
frame1.pack()

rock_button = Button(frame1, text="Rock",
                     font=10, width=7,
                     command=isrock)

paper_button = Button(frame1, text="Paper",
                      font=10, width=7,
                      command=ispaper)

scissor_button = Button(frame1, text="Scissor",
                        font=10, width=7,
                        command=isscissor)

rock_button.pack(side=LEFT, padx=10)
paper_button.pack(side=LEFT, padx=10)
scissor_button.pack(padx=10)

Button(window, text="Reset Game",
       font=10, fg="red",
       bg="black", command=reset_game).pack(pady=20)


def get_player2_and_decide_game_runner(user, message):
    # who is the server (= the creator of the channel)
    if 'created the channel' in message:
        name = message.split("'")[1]
    # who is the player2 (= the one that joined that is not player1)
    if 'joined channel' in message:
        name = message.split(' ')[1]
        if name != game_state['player1']:
            game_state['player2'] = name


def message_handler(timestamp, user, message):
    if user == 'system':
        get_player2_and_decide_game_runner(user, message)

    if user == game_state['player2'] and type(message) is str:
        game_state['player2_selection'] = message
        evaluate_result()

# start - before game loop


def start():
    status_label.config(text="Not Connected")
    # connect to network
    game_state['player1'] = simpledialog.askstring(
        'Input', 'Your user name', parent=window)
    channel = simpledialog.askstring(
        'Input', 'Channel', parent=window)
    connect(channel, game_state['player1'], message_handler)
    player_name_label.config(text=game_state['player1'])
    # wait for player2
    while game_state['player2'] == None and game_exit == False:
        tk_sleep(window, 1 / 10)
    status_label.config(text=game_state['player2'] + " connected")


# Execute Tkinter
start()
window.mainloop()
