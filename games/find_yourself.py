from handlers import fallback, make_response, SessionData

filename = __file__.split('/')[-1][:-3]


def start_game(event):
    session_data = SessionData(event)

    session_data.game_info = {
        'name': f'{filename}',
        'status': 'running',
    }

    session_data.session_state['game_info'] = session_data.game_info

    session_data.session_state['screen'] = f'{filename}.start_game'

    return make_response(text=f'<{filename}.start_game>', session_state=session_data.session_state)


def help(event):
    return fallback(event, text=f'<{filename}.help>')


def what_is(event):
    return fallback(event, text=f'<{filename}.what_is>')


def which_rules(event):
    return fallback(event, text=f'<{filename}.which_rules>')


def handler(event):
    # if all conditions are False
    return fallback(event, text=f'<{filename}.handler>')
