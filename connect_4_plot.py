import constants


def get_state_from_message(message):
    message = message.split('\n')
    current_turn = message[0].split("'")[0].strip()
    current_board = [[y for y in x] for x in message[3:3 + constants.board_height]]
    return current_turn, current_board


def get_next_state(state, move):
    current_turn, current_board = state
    current_board = [list(i) for i in zip(*current_board)]
    if current_board[move - 1][0] != constants.blank:
        return state, ['Invalid move!']
    else:
        i = 0
        while i < constants.board_height and current_board[move - 1][i] == constants.blank:
            i += 1
        current_board[move - 1][i - 1] = current_turn

    score = find_score([list(i) for i in zip(*current_board)])
    messages = []
    messages += [constants.player_1 + "'s score: " + str(score[constants.player_1])]
    messages += [constants.player_2 + "'s score: " + str(score[constants.player_2])]
    if score['match_finished']:
        messages += [('Match finished!, ' + "It's a tie!" if score[constants.player_1] == score[constants.player_2] else (constants.player_1 if score[constants.player_1] > score[constants.player_2] else constants.player_2 + ' won!'))]
        messages += ['Start a new match by using command /new_game']

    return (constants.player_1 if current_turn == constants.player_2 else constants.player_2,
            [list(i) for i in zip(*current_board)]), messages


def get_next_message(state, messages):
    next_turn, next_board = state
    next_message = next_turn + \
                   "'s turn!\n\n" + \
                   "1⃣2⃣3⃣4⃣5⃣6⃣7⃣\n" + '\n'.join([''.join(x) for x in next_board]) + '\n\n' + \
                   '\n'.join(messages)

    return next_message.strip()


def find_score(board):
    score = {
        constants.player_1: 0,
        constants.player_2: 0,
        'match_finished': True
    }

    # vertical
    for i in range(constants.board_height - constants.connect_length + 1):
        for j in range(constants.board_width):
            if board[i][j] == constants.player_1 and board[i+1][j] == constants.player_1 and board[i+2][j] == constants.player_1 and board[i+3][j] == constants.player_1 :
                score[constants.player_1] += 1
            elif board[i][j] == constants.player_2 and board[i+1][j] == constants.player_2 and board[i+2][j] == constants.player_2 and board[i+3][j] == constants.player_2 :
                score[constants.player_2] += 1

    # horizontal
    for i in range(constants.board_height):
        for j in range(constants.board_width - constants.connect_length + 1):
            if board[i][j] == constants.player_1 and board[i][j+1] == constants.player_1 and board[i][j+2] == constants.player_1 and board[i][j+3] == constants.player_1 :
                score[constants.player_1] += 1
            elif board[i][j] == constants.player_2 and board[i][j+1] == constants.player_2 and board[i][j+2] == constants.player_2 and board[i][j+3] == constants.player_2 :
                score[constants.player_2] += 1

    # axis \
    for i in range(constants.board_height - constants.connect_length + 1):
        for j in range(constants.board_width - constants.connect_length + 1):
            if board[i][j] == constants.player_1 and board[i+1][j+1] == constants.player_1 and board[i+2][j+2] == constants.player_1 and board[i+3][j+3] == constants.player_1 :
                score[constants.player_1] += 1
            elif board[i][j] == constants.player_2 and board[i+1][j+1] == constants.player_2 and board[i+2][j+2] == constants.player_2 and board[i+3][j+3] == constants.player_2 :
                score[constants.player_2] += 1

    # axis /
    for i in range(constants.connect_length - 1, constants.board_height):
        for j in range(constants.board_width - constants.connect_length + 1):
            if board[i][j] == constants.player_1 and board[i-1][j+1] == constants.player_1 and board[i-2][j+2] == constants.player_1 and board[i-3][j+3] == constants.player_1 :
                score[constants.player_1] += 1
            elif board[i][j] == constants.player_2 and board[i-1][j+1] == constants.player_2 and board[i-2][j+2] == constants.player_2 and board[i-3][j+3] == constants.player_2 :
                score[constants.player_2] += 1

    # finished
    for i in range(constants.board_height):
        for j in range(constants.board_width):
            if board[i][j] == constants.blank:
                score['match_finished'] = False
                break

    return score


def make_move(current_message, move):
    next_state, messages = get_next_state(get_state_from_message(current_message), int(move))
    return get_next_message(next_state, messages)


def main():
    print(make_move("🔵's turn!\n\n1⃣2⃣3⃣4⃣5⃣6⃣7⃣\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪\n⚪⚪⚪⚪⚪⚪⚪", "3"))

    # message = "🔵's turn!\n\n🔴🔵⚪🔵🔴🔴🔵\n🔵🔴🔴🔴🔴🔵🔴\n🔵🔵🔵🔵🔵🔵🔵\n🔵🔴🔴🔴🔴🔴🔴\n🔴🔵🔵🔵🔴🔴🔵\n🔵🔵🔴🔴🔵🔵🔴"
    # next_state, messages = get_next_state(get_state_from_message(message), 3)
    # print(get_next_message(next_state, messages))

    # turn, board = get_state_from_message(message)
    # for x in board:
    #     print(''.join(x))
    # print(find_score(board))


if __name__ == '__main__':
    main()
