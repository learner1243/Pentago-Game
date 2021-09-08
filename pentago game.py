import numpy as np
import random


#Display the board
def display_board(board):
    for row in board:
        row_str = [str(number) for number in row]
        row_str = '  '.join(row_str)
        print(row_str)

# Check if someone wins game
def check_victory(board, turn, rot):
    winners = [0, 0]
    boards = [board, board.T]
    for current_board in boards:
        for row in current_board:
            row_str = [str(number) for number in row]
            row_str = ''.join(row_str)
            if '11111' in row_str:
                winners[0] = 1
            elif '22222' in row_str:
                winners[1] = 1

    offsets = [-1, 0, 1]
    boards = [board, np.fliplr(board)]
    for current_board in boards:
        for offset in offsets:
            diagonal = np.diagonal(current_board, offset=offset)
            str_diag = [str(number) for number in diagonal]
            str_diag = ''.join(str_diag)
            if '11111' in str_diag:
                winners[0] = 1
            elif '22222' in str_diag:
                winners[1] = 1

    if winners == [0, 0]:
        return 0
    elif winners == [1, 0]:
        return 1
    elif winners == [0, 1]:
        return 2
    else:
        return 3

#Apply valid move
def apply_move(board,turn,row,col,rot):
    try:
        row = int(row)
    except:
        print('Row you entered is not a number. Enter a valid value.')
        return board

    try:
        col = int(col)
    except:
        print('Column you entered is not a number. Enter a valid value.')
        return board

    try:
        rot = int(rot)
    except:
        print('Rotation index you entered is not a number. Enter a valid value.')
        return board

    if row < 0 or row > 5:
        print('You entered a row that is out of the possible range of 0-5. Enter a valid value.')
        return board
    if col < 0 or col > 5:
        print('You entered a col that is out of the possible range of 0-5. Enter a valid value.')
        return board
    if rot <1 or rot>8:
        print('You entered a rotation number that is out of the possible range of 1-8. Enter a valid value.')
        return board

    acceptable = check_move(board, row, col)
    if acceptable is False:
        print('You chose the point that is already used. Please, choose another point(row, col).')
        return board

    board[row][col] = turn
    victory_status = check_victory(board, turn, rot)
    if victory_status == 0:
        if 0 not in board:
            display_board(board)
            print("It's a draw as got no free place to put a number in. Game is over.")
            print('Press Enter to close the program...')
            input()
            exit()
        else:
            pass
    elif victory_status == 1:
        display_board(board)
        print("First player won. Game over.")
        print('Press Enter to close the program...')
        input()
        exit()
    elif victory_status == 2:
        display_board(board)
        print("Second player won. Game over.")
        print('Press Enter to close the program...')
        input()
        exit()
    elif victory_status == 3:
        display_board(board)
        print("It's a draw. Nobody won. Game over.")
        print('Press Enter to close the program...')
        input()
        exit()



    #Rotate board
    one_two = [board[0][3:], board[1][3:], board[2][3:]]
    three_four = [board[3][3:], board[4][3:], board[5][3:]]
    five_six = [board[3][:3], board[4][:3], board[5][:3]]
    seven_eight = [board[0][:3], board[1][:3], board[2][:3]]

    turn_direction = ()
    if rot in [1, 3, 5, 7]:
        turn_direction = (1, 0)
    else:
        turn_direction = (0, 1)

    if rot==1 or rot==2:
        one_two = np.rot90(one_two, axes=turn_direction)
        board[0][3:] = one_two[0]
        board[1][3:] = one_two[1]
        board[2][3:] = one_two[2]
    elif rot==3 or rot==4:
        three_four = np.rot90(three_four, axes=turn_direction)
        board[3][3:] = three_four[0]
        board[4][3:] = three_four[1]
        board[5][3:] = three_four[2]
    elif rot==5 or rot==6:
        five_six = np.rot90(five_six, axes=turn_direction)
        board[3][:3] = five_six[0]
        board[4][:3] = five_six[1]
        board[5][:3] = five_six[2]
    else:
        seven_eight = np.rot90(seven_eight, axes=turn_direction)
        board[0][:3] = seven_eight[0]
        board[1][:3] = seven_eight[1]
        board[2][:3] = seven_eight[2]

    victory_status = check_victory(board, turn, rot)
    if victory_status == 0:
        if 0 not in board:
            display_board(board)
            print("It's a draw. No free place to put a number in. Game over.")
            print('Press Enter to close the program...')
            input()
            exit()
        else:
            pass
    elif victory_status == 1:
        display_board(board)
        print("First player won. Game over.")
        print('Press Enter to close the program...')
        input()
        exit()
    elif victory_status == 2:
        display_board(board)
        print("Second player won. Game over.")
        print('Press Enter to close the program...')
        input()
        exit()
    elif victory_status == 3:
        display_board(board)
        print("It's a draw. Nobody won. Game over.")
        print('Press Enter to close the program...')
        input()
        exit()

    return board

#See if mood is valid
def check_move(board, row, col):
    number = board[row, col]
    if number == 0:
        return True
    else:
        return False

#Computer level, give me headache i swear.....
def computer_move(board,turn,level):
    empty_cells = []
    for line in range(len(board)):
        for col in range(len(board[line])):
            if board[line][col] == 0:
                empty_cells.append([line, col])
    possible_rots = [1,2,3,4,5,6,7,8]

    #level 1 computer that do random move and rotation
    if level == 1:
        coordinates = random.choice(empty_cells)
        row = coordinates[0]
        column = coordinates[1]
        rot = random.choice(possible_rots)
    #level 2 computer... seriously damn hard.....
    # 3 possible ways to move
    # 1)Play move to lead to direct win if it exist
    # 2)Block player if player can direct win the next round
    # 3)Random move
    else:
        #Leads to a direct win if such a move exits
        if turn == 1:
            strs_needed = ['01111', '11110']
            our_num = '1'
        else:
            strs_needed = ['02222', '22220']
            our_num = '2'
        comp_can_win = False
        boards = [board, board.T]
        for current_board in boards:
            for row_idx in range(len(current_board)):
                row_str = [str(number) for number in current_board[row_idx]]
                row_str = ''.join(row_str)
                if strs_needed[0] in row_str:
                    comp_can_win = True
                    start_idx = row_str.index(strs_needed[0])
                    column = start_idx
                    row = row_idx
                    if np.array_equal(current_board, board.T) is True:
                        column = row_idx
                        row = start_idx
                    break
                elif strs_needed[1] in row_str:
                    comp_can_win = True
                    start_idx = row_str.index(strs_needed[1])
                    column = start_idx + len(strs_needed[1]) - 1
                    row = row_idx
                    if np.array_equal(current_board, board.T) is True:
                        column = row_idx
                        row = start_idx + len(strs_needed[1]) - 1
                    break
                # when 110111 or something similar exists
                elif row_str.count(our_num) == 5 and row_str.count('0') == 1:
                    comp_can_win = True
                    column = row_str.index('0')
                    row = row_idx
                    if np.array_equal(current_board, board.T) is True:
                        column = row_idx
                        row = row_str.index('0')
                    break
                else:
                    first_5 = row_str[:5]
                    last_5 = row_str[1:]

                    if first_5.count(our_num) == 4 and '0' in first_5:
                        comp_can_win = True
                        column = first_5.index('0')
                        row = row_idx
                        if np.array_equal(current_board, board.T) is True:
                            column = row_idx
                            row = first_5.index('0')
                        break
                    elif last_5.count(our_num) == 4 and '0' in last_5:
                        comp_can_win = True
                        column = last_5.index('0')+1
                        row = row_idx
                        if np.array_equal(current_board, board.T) is True:
                            column = row_idx
                            row = last_5.index('0')+1
                        break


        if comp_can_win is True:
            return row, column, random.choice(possible_rots)

        #Debug see if can work with diagonals....... (time consuming)
        diagonal_1 = ([0,0], [1,1], [2,2], [3,3], [4,4], [5,5])
        diagonal_2 = ([1,0], [2,1], [3, 2], [4, 3], [5, 4])
        diagonal_3 = ([0, 1], [1, 2], [2, 3], [3, 4], [4, 5])

        diagonal_4 = ([5, 0], [4, 1], [3, 2], [2, 3] ,[1, 4], [0, 5])
        diagonal_5 = ([5,1], [4, 2], [3, 3], [2, 4], [1,5])
        diagonal_6 = ([4, 0], [3, 1], [2, 2], [3, 1], [0, 4])

        diagonals = [diagonal_1, diagonal_2, diagonal_3, diagonal_4, diagonal_5, diagonal_6]
        for diag in diagonals:
            line = []
            for coord in diag:
                number = board[coord[0]][coord[1]]
                line.append(number)
            line = [str(number) for number in line]
            line = ''.join(line)
            first_5 = line[:5]
            last_5 = line[1:]
            if strs_needed[0] in line:
                comp_can_win = True
                start_idx = line.index(strs_needed[0])
                pair = diag[start_idx]
                row = pair[0]
                column = pair[1]
                break
            elif strs_needed[1] in line:
                comp_can_win = True
                start_idx = line.index(strs_needed[1])
                start_idx = start_idx + len(strs_needed[1]) - 1
                pair = diag[start_idx]
                row = pair[0]
                column = pair[1]
                break
            elif len(diag) == 6 and '0' in first_5 and first_5.count(our_num) == 4:
                comp_can_win = True
                target_idx = first_5.index('0')
                pair = diag[target_idx]
                row = pair[0]
                column = pair[1]
                break
            elif len(diag) == 6 and '0' in last_5 and last_5.count(our_num) == 4:
                comp_can_win = True
                target_idx = last_5.index('0')+1
                pair = diag[target_idx]
                row = pair[0]
                column = pair[1]
                break
            elif len(diag) < 6 and '0' in line and line.count(our_num) == 4:
                comp_can_win = True
                target_idx = line.index('0')
                pair = diag[target_idx]
                row = pair[0]
                column = pair[1]
                break
        
        if comp_can_win is True:
            return row, column, random.choice(possible_rots)
        #Prevent player from direct move to win in next round
        #4 3x3 matrixes in 6x6 board game
        one_two_coords = ((0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5))
        three_four_coords = ((3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5))
        five_six_coords = ((3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2))
        senev_eight_coords = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2))

        one_two_rots = (3,4,5,6,7,8)
        three_four_rots = (1,2,5,6,7,8)
        five_six_rots = (1,2,3,4,7,8)
        senev_eight_rots = (1,2,3,4,5,6)

        clever_rots = {one_two_coords: one_two_rots, three_four_coords: three_four_rots, five_six_coords: five_six_rots,
                       senev_eight_coords: senev_eight_rots}
        
        #Same idea as best move for player to win just that in computer move context. i.e. tic tac toe, we block 3 in a row

        if turn == 1:
            strs_needed = ['02222', '22220']
            num_adversary = '2'
        else:
            strs_needed = ['01111', '11110']
            num_adversary = '1'
        for current_board in boards:
            for row_idx in range(len(current_board)):
                row_str = [str(number) for number in current_board[row_idx]]
                row_str = ''.join(row_str)
                if strs_needed[0] in row_str:
                    comp_can_win = True
                    start_idx = row_str.index(strs_needed[0])
                    column = start_idx
                    row = row_idx
                    if np.array_equal(current_board, board.T) is True:
                        column = row_idx
                        row = start_idx
                    break
                elif strs_needed[1] in row_str:
                    comp_can_win = True
                    start_idx = row_str.index(strs_needed[1])
                    column = start_idx + len(strs_needed[1]) - 1
                    row = row_idx
                    if np.array_equal(current_board, board.T) is True:
                        column = row_idx
                        row = start_idx + len(strs_needed[1]) - 1
                    break
                elif row_str.count(num_adversary) == 5 and row_str.count('0') == 1:
                    comp_can_win = True
                    column = row_str.index('0')
                    row = row_idx
                    if np.array_equal(current_board, board.T) is True:
                        column = row_idx
                        row = row_str.index('0')
                    break
                else:
                    first_5 = row_str[:5]
                    last_5 = row_str[1:]

                    if first_5.count(num_adversary) == 4 and '0' in first_5:
                        comp_can_win = True
                        column = first_5.index('0')
                        row = row_idx
                        if np.array_equal(current_board, board.T) is True:
                            column = row_idx
                            row = first_5.index('0')
                        break
                    elif last_5.count(num_adversary) == 4 and '0' in last_5:
                        comp_can_win = True
                        column = last_5.index('0')+1
                        row = row_idx
                        if np.array_equal(current_board, board.T) is True:
                            column = row_idx
                            row = last_5.index('0')+1
                        break

        if comp_can_win is True:
            current_rot = 0
            for key in clever_rots:
                if (row, column) in key:
                    current_rot = random.choice(clever_rots[key])
                    break
            return row, column, current_rot

        for diag in diagonals:
            line = []
            for coord in diag:
                number = board[coord[0]][coord[1]]
                line.append(number)
            line = [str(number) for number in line]
            line = ''.join(line)
            first_5 = line[:5]
            last_5 = line[1:]
            if strs_needed[0] in line:
                comp_can_win = True
                start_idx = line.index(strs_needed[0])
                pair = diag[start_idx]
                row = pair[0]
                column = pair[1]
                break
            elif strs_needed[1] in line:
                comp_can_win = True
                start_idx = line.index(strs_needed[1])
                start_idx = start_idx + len(strs_needed[1]) - 1
                pair = diag[start_idx]
                row = pair[0]
                column = pair[1]
                break
            elif line.count(num_adversary) == 5 and line.count('0') == 1:
                comp_can_win = True
                target_idx = line.index('0')
                pair = diag[target_idx]
                row = pair[0]
                column = pair[1]
                break
            elif len(diag) == 6 and '0' in first_5 and first_5.count(num_adversary) == 4:
                comp_can_win = True
                target_idx = first_5.index('0')
                pair = diag[target_idx]
                row = pair[0]
                column = pair[1]
                break
            elif len(diag) == 6 and '0' in last_5 and last_5.count(num_adversary) == 4:
                comp_can_win = True
                target_idx = last_5.index('0')+1
                pair = diag[target_idx]
                row = pair[0]
                column = pair[1]
                break
            elif len(diag) < 6 and '0' in line and line.count(num_adversary) == 4:
                comp_can_win = True
                target_idx = line.index('0')
                pair = diag[target_idx]
                row = pair[0]
                column = pair[1]
                break

        if comp_can_win is True:
            current_rot = 0
            for key in clever_rots:
                if (row, column) in key:
                    current_rot = random.choice(clever_rots[key])
                    break
            return row, column, current_rot
        else:
            #No direct way to win or for adversery to not win so just make a random (Condition 3)
            coordinates = random.choice(empty_cells)
            row = coordinates[0]
            column = coordinates[1]
            rot = random.choice(possible_rots)



    return row, column, rot


def menu(): 
    game_board = np.zeros((6, 6), dtype=np.int8) #why default is float? Had to trial and error to resolve it
    #Loop until user enter correct values when asked
    while True:
        opponent = input(
            'Do you want to play with human or with computer? Enter 1 for human and 2 for the computer: ')
        #break when lvl1 or 2 ai is entered 
        try:
            opponent = int(opponent)
            if opponent == 1 or opponent == 2:
                break
            else:
                print('You entered neither 1 nor 2. Please, try again.')
                continue
        except:
            print('You entered neither 1 nor 2. Please, try again.')

    #If computer is opponent
    if opponent == 2:
        #Loop until user enter correct values when asked
        while True:
            level = input(
                'Please choose level of computer. Enter 1 easy computer, 2 for medium computer: ')
            try:
                level = int(level)
                if level == 1 or level == 2:
                    break
                else:
                    print('You entered neither 1 nor 2. Please, try again.')
                    continue
            except:
                print('You entered nor 1 or 2. Please, try again.')

    print('-' * 50)
    print('Initial game board has the following appearance: ')
    display_board(game_board)
    players = [1, 2]
    #Counter to change player turn in the next loop.
    counter = 0
    #Make moves and only when a victory or a draw is reached
    while True:
        print('-' * 50)
        #need counter to alternate between number of players hence % number of players
        curr_player = players[counter % len(players)]
        if opponent == 1 or curr_player == 1:
            #Human vs human.
            args = input("It's the {0} player turn now. Please, enter row, column and rotation index separated "
                         "with coma: ".format(curr_player))
            args = args.split(',')
            if len(args) != 3:
                print(
                    'You entered wrong number of arguments. It should be 3: row, column, rotation. Try again, please.')
                continue
        else:
            #Human vs computer
            args = [0, 0, 0]
            print("It's a 2 player (computer) turn now.")
            args[0], args[1], args[2] = computer_move(game_board, curr_player, level)
            print("Computer did the following turn: row {}, col {}, rot {}".format(args[0], args[1], args[2]))
        game_board_old = game_board.copy()  # Store the current board to then compare it with the updated one.
        game_board = apply_move(board=game_board, turn=curr_player, row=args[0], col=args[1], rot=args[2])
        print("The current board's appearance: ")
        display_board(game_board)
        if np.array_equal(game_board, game_board_old) is False:
            counter += 1         
    #menu()


#import numpy as np
#from pentago_final import *

#def test():
#    game_size = 6
#    board = np.zeros((game_size,game_size))
#    turn = 1
    
    # ***************** first test ***************** #
#    if check_move(board,0,0): 
#        print("test 1: OK !")
#    else: 
#        print("test 1: Fail of the check_move function !")
    
    # ***************** second test ***************** #
#    board[1,1] = 1
#    if not check_move(board,1,1): 
#        print("test 2: OK !")
#    else: 
#        print("test 2: Fail of the check_move function !")
        
    # ***************** third test ***************** #
#    board_test3 = [[ 0,0,2,0,0,0], [0,1,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0]]
#    board = apply_move(board,2,0,0,7)
#    if (board_test3 == board).all(): 
#        print("test 3: OK !")
#    else: 
#        print("test 3: Fail of the apply_move function !")
    
    # ***************** fourth test ***************** #
#    if check_victory(board,turn,1) == 0:
#        print("test 4: OK !")
#    else: 
#        print("test 4: Fail of the check_victory function !")
     
    # ***************** fifth test ***************** #
#    turn = 1
#    board = np.array([[1,1,0,2,1,1], [1,0,2,2,1,1], [0,2,1,1,2,2], [2,2,1,1,2,2], [1,1,2,2,1,1], [1,1,0,2,1,1]])
#    move0, move1, _ = computer_move(board,1,1)
#    if (move0, move1) in [(0,2),(1,1),(2,0),(5,2)]:
#        print("test 5: OK !")
#    else: 
#        print("test 5: Fail of the computer_move function !")                

#test()