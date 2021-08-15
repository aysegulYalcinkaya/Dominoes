import random


def get_player_move():
    try:
        next_move = int(input())
    except ValueError:
        next_move = 9999999
    while next_move < -len(player_pieces) or next_move > len(player_pieces):
        print("Invalid input. Please try again.")
        try:
            next_move = int(input())
        except ValueError:
            next_move = 99999
    return next_move


def get_computer_move():
    total_list = domino_snake.copy()
    total_list.extend(computer_pieces)

    number_counts = {x: sum(element.count(x) for element in total_list) for x in range(7)}
    computer_pieces_scores = [number_counts.get(x) + number_counts.get(y) if x != y else number_counts.get(x) for (x, y)
                              in computer_pieces]

    candidate_list = computer_pieces.copy()
    while len(candidate_list) > 0:
        max_score = max(computer_pieces_scores)
        index = computer_pieces_scores.index(max_score)
        domino_max = candidate_list[index]
        if do_move(computer_pieces.index(domino_max) + 1, computer_pieces) or do_move(
                -computer_pieces.index(domino_max) - 1, computer_pieces):
            break;
        computer_pieces_scores.remove(max_score)
        candidate_list.remove(domino_max)
    else:
        do_move(0, computer_pieces)


def print_snake(domino_snake):
    snake_str = ""
    if len(domino_snake) > 6:
        for domino in domino_snake[0:3]:
            snake_str += str(domino)
        snake_str += "..."
        for domino in domino_snake[len(domino_snake) - 3:len(domino_snake)]:
            snake_str += str(domino)
    else:
        for domino in domino_snake:
            snake_str += str(domino)
    print(snake_str)


def do_move(move, pieces):
    global gameover
    if move > 0:
        domino_checked = check_right(pieces[abs(move) - 1])
        if domino_checked:
            domino_snake.append(domino_checked)
            pieces.remove(pieces[abs(move) - 1])
            return True
        else:
            return False
    elif move < 0:
        domino_checked = check_left(pieces[abs(move) - 1])
        if domino_checked:
            domino_snake.insert(0, domino_checked)
            pieces.remove(pieces[abs(move) - 1])
            return True
        else:
            return False
    else:
        stock = random.randint(0, len(stock_pieces) - 1)
        pop_domino = stock_pieces.pop(stock)
        pieces.append(pop_domino)
        return True


def check_right(domino):
    if domino_snake[-1][1] == domino[0]:
        return domino
    if domino_snake[-1][1] == domino[1]:
        return [domino[1], domino[0]]
    else:
        return []


def check_left(domino):
    if domino_snake[0][0] == domino[1]:
        return domino
    if domino_snake[0][0] == domino[0]:
        return [domino[1], domino[0]]
    else:
        return []


domino_set = []
for i in range(7):
    for j in range(i, 7, 1):
        domino_set.append([i, j])

max_computer = []
max_player = []
while len(max_computer) == 0 and len(max_player) == 0:
    computer_pieces = random.sample(domino_set, 7)
    stock_pieces = list.copy(domino_set)
    for domino in computer_pieces:
        stock_pieces.remove(domino)

    player_pieces = random.sample(stock_pieces, 7)
    for domino in player_pieces:
        stock_pieces.remove(domino)

    max_computer = [domino for domino in computer_pieces if
                    domino[0] == domino[1] and domino[0] in max(computer_pieces)]
    max_player = [domino for domino in player_pieces if domino[0] == domino[1] and domino[0] in max(player_pieces)]

if max_computer > max_player:
    status = "player"
    domino_snake = max_computer
    computer_pieces.remove(max_computer[0])
else:
    status = "computer"
    domino_snake = max_player
    player_pieces.remove(max_player[0])

gameover = False

while True:
    print("======================================================================")
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer_pieces)}\n")

    print_snake(domino_snake)
    print("\nYour pieces:")
    i = 1
    for domino in player_pieces:
        print(f"{i}:{domino}")
        i += 1
    if gameover:
        break
    if status == "player":
        print("\nStatus: It's your turn to make a move. Enter your command.")

        move = get_player_move()
        while not do_move(move, player_pieces):
            print("Illegal move. Please try again.")
            move = get_player_move()

        status = "computer"
    else:
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
        move = input()
        move = random.randint(-len(computer_pieces), len(computer_pieces))
        get_computer_move()
        # while not do_move(move, computer_pieces):
        #    move = random.randint(-len(computer_pieces), len(computer_pieces))
        status = "player"
    if len(player_pieces) == 0 or len(computer_pieces) == 0 or len(stock_pieces) == 0:
        gameover = True

if len(player_pieces) == 0:
    print("\nStatus: The game is over. You won!")
elif len(computer_pieces) == 0:
    print("\nStatus: The game is over. The computer won!")
else:
    print("\nStatus: The game is over. It's a draw!")
