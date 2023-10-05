import random

import os

from ImageWork import get_image_bytes, upload_image
from handlers import fallback, make_response

from PIL import Image, ImageDraw, ImageFont

STATE_REQUEST_KEY = 'session'
STATE_RESPONSE_KEY = 'session_state'

filename = __file__.split('/')[-1][:-3]

ru_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

dialog_id, oauth_code = os.environ['dialog_id'], os.environ['oauth_code']


def start_game(event):
    state = event.get('state', {})
    session_state = state.get(STATE_REQUEST_KEY, {})  # Write&Read

    # creating boards for the game
    main_player_board = create_board(board_type='main')
    radar_player_board = create_board(board_type='radar')

    main_AI_board = create_board(board_type='main')
    radar_AI_board = create_board(board_type='radar')

    # adding boards into session_state
    session_state['screen'] = 'sea_battle.start_game'
    session_state['game_info'] = {
        'name': 'sea_battle',
        'status': 'running',
        'main_player_board': main_player_board,
        'radar_player_board': radar_player_board,
        'main_AI_board': main_AI_board,
        'radar_AI_board': radar_AI_board,
    }

    # making boards image for response
    boards_image_id = get_boards_like_images(main_player_board, radar_player_board)

    # making response
    card = {
        "type": "BigImage",
        "image_id": boards_image_id,
        "title": "<sea_battle.handler>",
        "description": "Введите координаты формата `А1`",
    }

    return make_response(text=f'<sea_battle.start_game>', session_state=session_state, card=card)


def help(event):
    return fallback(event, text=f'<{filename}.help>')


def what_is(event):
    return fallback(event, text=f'<{filename}.what_is>')


def which_rules(event):
    return fallback(event, text=f'<{filename}.which_rules>')


def handler(event):
    # getting data from json
    state = event.get('state', {})
    session = event.get(STATE_REQUEST_KEY, {})  # Read Only
    session_state = state.get(STATE_REQUEST_KEY, {})  # Write&Read
    user = state.get('user', {})

    intents = event['request'].get('nlu', {}).get('intents')
    message = str(event.get('request', {})['original_utterance']).lower()

    # getting data for game from session state
    main_player_board, radar_player_board, main_AI_board, radar_AI_board = get_game_boards(session_state)
    player_win = is_player_win(main_player_board, main_AI_board)

    if session_state['game_info']['status'] == 'running':
        if player_win is True:  # the player win
            session_state['game_info']['status'] = True

        elif player_win is False:  # the player lose
            session_state['game_info']['status'] = False

        elif 'SeaBattleMove' in intents:  # game continues
            move_cord = (
                intents['SeaBattleMove']['slots']['x_cord']['value'],
                intents['SeaBattleMove']['slots']['y_cord']['value']
            )

            return make_a_move(session_state, cords=move_cord)

    # if all conditions are False
    return fallback(event, text='<sea_battle.handler>. Это значит не поняла, чел...')


def make_a_move(session_state: dict, cords: tuple):
    """
    :param session_state: dict from skill's json
    :param cords: coordinates for sea battle game like ('а', 1) or ('б', 2)
    :return: dict in skill's response format
    """

    # getting data for game from session state
    main_player_board, radar_player_board, main_AI_board, radar_AI_board = get_game_boards(session_state)

    player_move_cords = parse_coordinates(cords)

    main_AI_board, radar_player_board = make_shot(main_AI_board, radar_player_board, shot_cord=player_move_cords)

    AI_shots = get_bot_shot(radar_AI_board)

    main_player_board, radar_AI_board = make_shot(main_player_board, radar_AI_board, shot_cord=AI_shots)

    # making boards image for response
    boards_image_id = get_boards_like_images(main_player_board, radar_player_board)

    # making response
    card = {
        "type": "BigImage",
        "image_id": boards_image_id,
        "title": "<sea_battle.handler>",
        "description": "Введите координаты формата `А1`",
    }

    return make_response(text=f'<sea_battle.handler>', session_state=session_state, card=card)


def get_game_boards(session_state):
    names = ['main_player_board', 'radar_player_board', 'main_AI_board', 'radar_AI_board']
    if not session_state.get('game_info') is None:
        return [session_state['game_info'].get(name) for name in names]


def get_boards_like_images(main_player_board: list, radar_player_board: list):
    main_player_board = board_to_image(
        board=main_player_board,
        font_path='fonts/Roboto-Regular.ttf',
        font_size=24,
        title='Ваши корабли'
    )
    radar_player_board = board_to_image(
        board=radar_player_board,
        font_path='fonts/Roboto-Regular.ttf',
        font_size=24,
        title='Радар'
    )

    boards_image = merge_images(image1=main_player_board, image2=radar_player_board)
    boards_image_id = upload_image(dialog_id, oauth_code, image=get_image_bytes(boards_image))['image']['id']

    return boards_image_id


def is_player_win(main_player_board: list, main_AI_board: list) -> bool:
    if all(cell != 'S' for row in main_AI_board for cell in row):
        return True

    elif all(cell != 'S' for row in main_player_board for cell in row):
        return False


def create_board(board_type: str, ships_cord: list = None, shots_cord: list = None, board_size=10) -> list:
    if ships_cord is None:
        ships_cord = generate_random_ships()

    if shots_cord is None:
        shots_cord = list()

    board = list()

    for y in range(board_size):
        board_line = list()
        for x in range(board_size):
            if ((x, y) in shots_cord) and ((x, y) in ships_cord):
                board_line.append('X')

            elif ((x, y) in ships_cord) and board_type == 'main':
                board_line.append('S')

            elif (x, y) in shots_cord:
                board_line.append('.')

            else:
                board_line.append('~')

        board.append(board_line)

    return board


def generate_random_ships(board_size=10, ship_lengths=None, min_distance=1):
    if ship_lengths is None:
        ship_lengths = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

    num_ships = len(ship_lengths)
    ships_cord = []

    for ship_length in ship_lengths:
        while True:
            orientation = random.choice(["horizontal", "vertical"])
            if orientation == "horizontal":
                x = random.randint(0, board_size - ship_length)
                y = random.randint(0, board_size - 1)
                ship_coords = [(x + i, y) for i in range(ship_length)]
            else:
                x = random.randint(0, board_size - 1)
                y = random.randint(0, board_size - ship_length)
                ship_coords = [(x, y + i) for i in range(ship_length)]

            valid_coords = True
            for coord in ship_coords:
                x, y = coord
                for i in range(-min_distance, min_distance + 1):
                    for j in range(-min_distance, min_distance + 1):
                        if (x + i, y + j) in ships_cord:
                            valid_coords = False
                            break
                    if not valid_coords:
                        break
                if not valid_coords:
                    break

            if valid_coords:
                ships_cord.extend(ship_coords)
                break

    return ships_cord


def is_ship_destroyed(main_board: list, shot_cord: tuple, board_size: int = None) -> bool:
    if board_size is None:
        board_size = len(main_board)

    ship_destroyed = True

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            x = shot_cord[0] + i
            y = shot_cord[1] + j
            if 0 <= x < board_size and 0 <= y < board_size and main_board[x][y] == 'S':
                ship_destroyed = False

    return ship_destroyed


def set_indicates_ship_destroyed(main_board: list, radar_board: list, shot_cord: tuple,
                                 board_size: int = None) -> tuple:
    if board_size is None:
        board_size = len(main_board)

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            x = shot_cord[0] + i
            y = shot_cord[1] + j
            if 0 <= x < board_size and 0 <= y < board_size:
                if main_board[x][y] == 'X':
                    main_board[x][y] = 'o'
                    main_board, radar_board = set_indicates_ship_destroyed(main_board, radar_board, (x, y))

                elif main_board[x][y] == 'o':
                    pass

                else:
                    main_board[x][y] = '.'
                    radar_board[x][y] = '.'

    return main_board, radar_board


def make_shot(main_board: list, radar_board: list, shot_cord: tuple, board_size: int = None) -> tuple:
    if board_size is None:
        board_size = len(main_board)

    shot_cord = shot_cord[::-1]

    if main_board[shot_cord[0]][shot_cord[1]] == '~':
        main_board[shot_cord[0]][shot_cord[1]] = '.'
        radar_board[shot_cord[0]][shot_cord[1]] = '.'

    if main_board[shot_cord[0]][shot_cord[1]] == 'S':
        main_board[shot_cord[0]][shot_cord[1]] = 'X'
        radar_board[shot_cord[0]][shot_cord[1]] = 'X'

        if is_ship_destroyed(main_board, shot_cord):
            # Пометить точками клетки вокруг уничтоженного корабля
            main_board, radar_board = set_indicates_ship_destroyed(main_board, radar_board, shot_cord)

    return main_board, radar_board


def get_board_print(board: list) -> str:
    board_size = len(board)
    s = list()

    s.append("  " + " ".join(str(i) for i in range(board_size)))

    for index, row in enumerate(board):
        s.append(str(index) + " " + " ".join(row))

    s = '\n'.join(s)

    return s


def get_bot_shot(radar_AI_board: list) -> tuple:
    board_size = len(radar_AI_board)

    while True:
        x = random.randint(0, board_size - 1)
        y = random.randint(0, board_size - 1)

        if radar_AI_board[x][y] not in ['X', '.' 'o']:
            return x, y


def board_to_image(board: list, cell_size: int = 50, line_color: tuple = (255, 255, 255), fill_colors: dict = None,
                   text_color: tuple = (255, 255, 255), font_path: str = None, font_size: int = 40,
                   title: str = ' ', background_color=(0, 75, 125)) -> Image:
    if fill_colors is None:
        fill_colors = {
            '~': (0, 150, 225),  # Вода
            'S': (255, 255, 255),  # Корабль
            'X': (255, 0, 0),  # Уничтоженная часть корабля
            '.': (128, 128, 128),  # Промах
            'o': (255, 0, 0)  # Пометка полностью уничтоженного корабля
        }

    width = len(board[0]) * cell_size
    height = len(board) * cell_size

    # Добавляем высоту для заголовка и нумерации строк
    enlarged_width = width + cell_size
    enlarged_height = height + cell_size + font_size * 3
    image = Image.new("RGB", (enlarged_width, enlarged_height))
    draw = ImageDraw.Draw(image)

    # Заполняем фон синим цветом
    image.paste(background_color, [0, 0, image.width, image.height])

    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            left = x * cell_size + cell_size
            top = y * cell_size + cell_size + font_size * 3
            right = (x + 1) * cell_size + cell_size
            bottom = (y + 1) * cell_size + cell_size + font_size * 3

            fill_color = fill_colors.get(cell, (255, 255, 255))
            draw.rectangle((left, top, right, bottom), fill=fill_color, outline=line_color)

    # Создаем объект шрифта
    title_font, num_font = None, None

    if font_path is not None:
        title_font = ImageFont.truetype(font_path, size=int(font_size * 1.5))
        num_font = ImageFont.truetype(font_path, size=font_size)

    # Нумерация строк слева
    for y, row in enumerate(board):
        number_x = 10
        number_y = (y + 2) * cell_size + cell_size // 2 + font_size // 2
        draw.text((number_x, number_y), str(y + 1), fill=text_color, font=num_font)

    # Нумерация столбцов сверху
    russian_letters = list(ru_letters)
    for x in range(len(board[0])):
        number_x = 10 + (x + 1) * cell_size + cell_size // 2 - font_size // 2
        number_y = 10 + font_size * 3
        draw.text((number_x, number_y), russian_letters[x], fill=text_color, font=num_font)

    # Определяем ограничивающий прямоугольник текста заголовка
    title_bbox = draw.textbbox((0, 0), title, font=title_font)

    # Определяем размеры текста заголовка
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]

    # Определяем координаты для размещения заголовка
    title_x = 10 + title_width // len(title)
    title_y = font_size

    # Размещаем заголовок
    draw.text((title_x, title_y), title, fill=text_color, font=title_font)

    # Изменяем размер изображения на 388x172
    resized_image = image.resize((388, 172))

    return resized_image


def merge_images(image1: Image, image2: Image) -> Image:
    # Изменяем размер изображений на 388x172
    resized_image1 = image1.resize((194, 172))
    resized_image2 = image2.resize((194, 172))

    # Создаем новое изображение для объединения
    merged_image = Image.new("RGB", (388, 172))

    # Размещаем resized_image1 слева от resized_image2
    merged_image.paste(resized_image1, (0, 0))
    merged_image.paste(resized_image2, (194, 0))

    return merged_image


def parse_coordinates(input_coordinates: tuple):
    letter = input_coordinates[0].upper()
    number = int(input_coordinates[1]) - 1
    column = ru_letters.index(letter)
    return column, number
