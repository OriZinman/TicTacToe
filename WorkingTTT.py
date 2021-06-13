#noughts and crosses game - made by Ori Zinman
from tkinter import *
from functools import partial
from tkinter import messagebox


# Used to mark whenever its the X's turn or the O's turn.
sign = 0

# Creates a 3 by 3 board with ' ' string inside.
global board
board = [[' ' for x in range(3)] for y in range(3)]


#checks who had won (by symbol)
def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))


# sets the text on the button whenever someone plays (1v1 mode)
def get_text(i, j, gb, l1, l2):
    global sign
    if isfree(i,j):
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    if winner(board, "X"):
        gb.destroy()
        box = messagebox.showinfo("P1 WON", "X's won!")
    elif winner(board, "O"):
        gb.destroy()
        box = messagebox.showinfo("P2 WON", "O's won!")
    elif (isfull()):
        gb.destroy()
        box = messagebox.showinfo("Tied", "tied game")


# checks if the slot is empty or not
def isfree(i, j):
    return board[i][j] == " "


# Check the board is full or not
def isfull():
    for i in board:
        if (i.count(' ') > 0):
            return False
    return True


# Sets up the GUI for the 1v1 mode
def gameboard_pl(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


# Decide the next move of system - by using the MiniMax method.
def compmove():
    bestScore = -10
    bestmove = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, False)
                board[i][j] = ' '
                if (score > bestScore):
                    bestScore = score
                    bestmove = [[i],[j]]


    return bestmove


def minimax(nboard,  isMaximizing): #minimax recursion
    if winner(nboard, 'O'):
        return 1
    if winner(nboard, 'X'):
        return -1
    if isfull():
        return 0

    if isMaximizing:
        bestScore = -800
        for i in range(3):
            for j in range(3):
                if nboard[i][j] == ' ':
                    nboard[i][j] = 'O'
                    score = minimax(nboard, False)
                    nboard[i][j] = ' '
                    if score > bestScore:
                        bestScore = score
        return bestScore

    else:
        bestScore = 800
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(nboard, True)
                    board[i][j] = ' '
                    if (score < bestScore):
                        bestScore = score
        return bestScore


# sets up the text on the buttons (vs the pc mode)
def get_text_pc(i, j, gb, l1, l2):
    global sign
    if isfree(i,j): #checks if the button was already clicked before(by the pc/the user)
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"

        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"

        sign += 1
        button[i][j].config(text=board[i][j])
    continue_game = True
    if winner(board, 'X'):
        gb.destroy()
        continue_game = False
        box = messagebox.showinfo("Winner", "Player won the match")
    elif winner(board, 'O'):
        gb.destroy()
        continue_game = False
        box = messagebox.showinfo("Loser", "The evil computer has won")
    elif (isfull()):
        gb.destroy()
        continue_game = False
        box = messagebox.showinfo("Tied.", "Well... at least you tried.")
    if (continue_game):
        if sign % 2 != 0:
            move = compmove()
            get_text_pc(move[0][0], move[1][0], gb, l1, l2) #move[0][0]=i, move[1][0]=j



# sets up the actual visual board on vs pc mode
def gameboard_pc(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        #print(button)
        button[i] = []
        #print(button)
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text_pc, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


# creates the game board vs pc
def withpc(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="You are : X", width=10)
    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="PC : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pc(game_board, l1, l2)


# creates the game board when playing with another person
def withplayer(game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("noughts and crosses")
    l1 = Button(game_board, text="P1 : X", width=10)

    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="P2 : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pl(game_board, l1, l2)


# main function
def play():
    menu = Tk()
    menu.geometry("250x250")
    menu.title("TTT")
    wpc = partial(withpc, menu)
    wpl = partial(withplayer, menu)

    head = Label(menu, text="Tic Tac Toe - Made by Ori Zinman",
                 activeforeground='blue',
                 activebackground="cyan", bg="blue",
                 fg="cyan", width=500, font='Arial', )

    B1 = Button(menu, text="vs pc", command=wpc,
                activeforeground='blue',
                activebackground="cyan", bg="blue",
                fg="cyan", width=500, font='Arial', )

    B2 = Button(menu, text="1v1", command=wpl, activeforeground='blue',
                activebackground="cyan", bg="blue", fg="cyan",
                width=500, font='Arial', )

    B3 = Button(menu, text="Quit", command=menu.quit, activeforeground='blue',
                activebackground="cyan", bg="blue", fg="cyan",
                width=500, font='Arial', )
    head.pack(side='top')
    B1.pack(side='top')
    B2.pack(side='top')
    B3.pack(side='bottom')
    menu.mainloop()


# Call main function
if __name__ == '__main__':
    play()