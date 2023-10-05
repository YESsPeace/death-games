from handlers import fallback, make_response, SessionData

filename = __file__.split('/')[-1][:-3]

actions = {
    'start': dict(
        text='Тебе нужно убить лягушка бургер',
        buttons=[dict(title='Сделать это ножом', payload='1', hide=False, keyword='нож'),
                 dict(title='Сделать это своими зубами', payload='2', hide=False, keyword='зуб')],
        card=dict(type='BigImage', image_id='1540737/47407655cdbca32c8f99', title=None, description=None)
    ),
    'start.1': dict(
        text='Теперь ты можешь его съесть или выбросить его труп',
        buttons=[dict(title='Съесть', payload='1', hide=False, keyword='съе'),
                 dict(title='Выбросить труп', payload='2', hide=False, keyword='выбро')],
        card=dict(type='BigImage', image_id='1533899/bbab3afe193454a01829', title=None, description=None)
    ),
    'start.2': dict(
        text='О, нет! Он достал нож. Теперь тебе нужно сбежать от лягушка бургер',
        buttons=[dict(title='Попытаться съесть его', payload='1', hide=False, keyword='съе'),
                 dict(title='Отдать ему деньги', payload='2', hide=False, keyword='ден'),
                 dict(title='Выбежать из вкусно и .', payload='3', hide=False, keyword='выбе'), ],
        card=dict(type='BigImage', image_id='1540737/6afe99e3e28de304367b', title=None, description=None)
    ),
    'start.1.1': dict(
        text='Вы отравились и сдохли',
        card=dict(type='BigImage', image_id='997614/3eba7ac0bf6027c88cbf', title=None, description=None)
    ),
    'start.1.2': dict(
        text='Вы избавили мир от лягушка бургер',
        card=dict(type='BigImage', image_id='1533899/bbab3afe193454a01829', title=None, description=None)
    ),
    'start.2.1': dict(
        text='Чел... При попытки съесть вооружённый лягушка бургер вы умерли. Вам посмертно присуждена умственная отсталость.',
        card=dict(type='BigImage', image_id='997614/3eba7ac0bf6027c88cbf', title=None, description=None)
    ),
    'start.2.2': dict(
        text='Лягушка бургер съел деньги. Ему понравились деньги. Он ограбил вас, а потом стал бизнесфрогам и ограбил всех. Вам присуждено банкротство.',
        card=dict(type='BigImage', image_id='1533899/34d7d38d49ebbf3c2ef7', title=None, description=None)
    ),
    'start.2.3': dict(
        text='Вы избежали смерти. Мир погружен в постапокалиптический хаос. Лягушка бургер теперь диктатор',
        card=dict(type='BigImage', image_id='965417/99ff64618ab884c7b921', title=None, description=None)
    ),
}


def start_game(event):
    session_data = SessionData(event)

    session_data.game_info = {
        'name': f'{filename}',
        'status': 'running',
        'action_key': 'start',
    }

    session_data.session_state['game_info'] = session_data.game_info

    session_data.session_state['screen'] = f'{filename}.start_game'

    new_action_dict = actions[session_data.game_info["action_key"]]

    text = new_action_dict.get("text")

    buttons = new_action_dict.get("buttons")

    card = new_action_dict.get('card', {})
    card['title'] = f'<{filename}.start_game>'

    return make_response(
        text=text,
        session_state=session_data.session_state,
        card=card,
        buttons=buttons
    )


def help(event):
    return fallback(event, text=f'<{filename}.help>')


def what_is(event):
    return fallback(event, text=f'<{filename}.what_is>')


def which_rules(event):
    return fallback(event, text=f'<{filename}.which_rules>')


def handler(event):
    session_data = SessionData(event)

    if session_data.game_info.get('status') == 'running':
        new_key = ''
        card_title = f'<{filename}.handler>'
        message = session_data.message

        if 'deselect' in session_data.intents:
            session_data.game_info['action_key'] = '.'.join(session_data.game_info['action_key'].split('.')[:-1])
            card_title = 'Изменить выбор'

        else:
            if event['request']['type'] == 'ButtonPressed':
                if 'payload' in event['request']:
                    new_key = '.' + str(session_data.payload_data)
                    for button in session_data.session_state.get('last_buttons'):
                        if button['title'].lower() == message:
                            card_title = button['title']

            elif event['request']['type'] == 'SimpleUtterance':
                for button in session_data.last_buttons:
                    if not button.get('keyword') is None:
                        if all([keyword in message for keyword in button['keyword'].lower().split()]):
                            if not button.get('payload') is None:
                                card_title = button['title']
                                new_key = '.' + button['payload']
                                break

                else:  # if didn't find the right button
                    card_title = 'Что-то я вас не поняла. Давайте ещё раз и лучше используйте кнопки.'

            session_data.game_info['action_key'] = session_data.game_info['action_key'] + new_key

        new_action_dict = actions[session_data.game_info["action_key"]]

        text = new_action_dict.get("text")

        card = new_action_dict.get('card', {})
        card['title'] = f'Ваш ответ: {card_title}'

        return make_response(
            text=text,
            session_state=session_data.session_state,
            card=card,
            buttons=new_action_dict.get('buttons')
        )

    # if all conditions are False
    return fallback(event, text=f'<{filename}.handler>')
