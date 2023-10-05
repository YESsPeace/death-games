from Exceptions import GetStateError, ImportGameModuleError
from handlers import fallback, make_response, SessionData
import importlib

STATE_REQUEST_KEY = 'session'
STATE_RESPONSE_KEY = 'session_state'


def handler(event, context):
    session_data = SessionData(event)

    if session_data.is_new is True:
        return main_welcome(session_state=session_data.session_state)

    elif 'quit_skill' in session_data.intents:
        return make_response(text='Ещё увидимся.', end_session=True)

    elif 'restart' in session_data.intents:
        if 'GameName' in session_data.intents['restart']['slots']:
            game_name = session_data.intents['restart']['slots']['GameName']['value']

            return start_game_function(event,
                                       session_state=session_data.session_state,
                                       game_name=game_name,
                                       func_name='start_game')

        else:
            return main_welcome(session_state=None)

    elif 'what_is' in session_data.intents:
        if 'GameName' in session_data.intents['what_is']['slots']:
            game_name = session_data.intents['what_is']['slots']['GameName']['value']

            return start_game_function(event,
                                       session_state=session_data.session_state,
                                       game_name=game_name,
                                       func_name='what_is')

        else:
            return fallback(event,
                            text='<main.handler>. '
                                 'Что это за навык')

    elif 'which_rules' in session_data.intents:
        if 'GameName' in session_data.intents['which_rules']['slots']:
            game_name = session_data.intents['which_rules']['slots']['GameName']['value']

        else:
            game_name = 'some_game'

        return start_game_function(event,
                                   session_state=session_data.session_state,
                                   game_name=game_name,
                                   func_name='which_rules')



    elif 'help' in session_data.intents:
        if 'GameName' in session_data.intents['help']['slots']:
            game_name = session_data.intents['help']['slots']['GameName']['value']

            return start_game_function(event,
                                       session_state=session_data.session_state,
                                       game_name=game_name,
                                       func_name='help')

        else:
            return fallback(event,
                            text='<main.handler>. Помощь. Если нужна справка в игре, то скажите "Помощь в морском бое"')

    elif session_data.session_state['screen'] == 'main_welcome':
        if 'start_game' in session_data.intents:
            if 'GameName' in session_data.intents['start_game']['slots']:
                game_name = session_data.intents['start_game']['slots']['GameName']['value']

                # if game_name in ['sea_battle', 'mafia']:
                return start_game_function(event,
                                           session_state=session_data.session_state,
                                           game_name=game_name,
                                           func_name='start_game')

            return fallback(event, text='Извините, мы не можем сыграть в это сейчас. Только морской бой или мафия.')

    elif not session_data.game_info.get('name') is None:
        game_name = session_data.game_info['name']

        if session_data.game_info.get('status') == 'running':
            return start_game_function(event,
                                       session_state=session_data.session_state,
                                       game_name=game_name,
                                       func_name='handler')

        elif game_name == 'sea_battle':
            if session_data.game_info.get('status') == 1:
                pass

            elif session_data.game_info.get('status') == 0:
                pass

        elif game_name == 'mafia':
            if session_data.game_info.get('status') == 1:
                pass

            elif session_data.game_info.get('status') == 0:
                pass

        elif game_name == 'amphibian':
            if session_data.game_info.get('status') == 1:
                pass

            elif session_data.game_info.get('status') == 0:
                pass

        elif game_name in ['dictator_regular', 'dictator_amphibian', 'find_yourself', 'gangstar_in_heaven']:
            if session_data.game_info.get('status') in [1, 0]:
                pass

    # if all conditions are False
    return fallback(event, text='<main.handler>. Извините, не поняла.')


def main_welcome(session_state: dict = None):
    text = 'Добро пожаловать в мою обитель, прекрасный муж иль дева, не желаете сыграть в игру, в которой ставкой будет ваша жизнь?'

    buttons = [
        dict(title='Морской бой', hide=False),
        dict(title='Мафия', hide=False),
    ]

    if session_state is None:
        session_state = dict()

    session_state['screen'] = 'main_welcome'

    return make_response(text, session_state=session_state, buttons=buttons)


def start_game_function(event, session_state: dict, game_name: str, func_name: str):
    try:
        if game_name == 'some_game':
            if not session_state.get('game_info') is None:
                game_name = session_state['game_info']['name']

            else:
                return fallback(event, text='Кажется никакая игра сейчас не запущена')

        game_module = importlib.import_module(f'games.{game_name}')

        return getattr(game_module, func_name)(event)

    except AttributeError as e:
        raise GetStateError('Failed getting data from event') from e

    except ImportError as e:
        raise ImportGameModuleError('Failed import game module') from e
