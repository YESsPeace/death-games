import random

from handlers import fallback, make_response, SessionData

filename = __file__.split('/')[-1][:-3]

# actions, which are needed to create selection chains
actions_consequences = {
    '0.Да': dict(
        text='Вы верите в бога?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=0, next_action_id='0.Да.Да', new_action_id=None,
                              new_text=None),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=-999, next_action_id=None, new_action_id=None,
                              new_text='Казнить его'),
                 hide=False, keyword='не')
        ],
    ),
    '0.Да.Да': dict(
        text='Хорошо, а то если бы вы были атеистом мы бы вас казнили. Вы верите в котов?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=100, next_action_id=None, new_action_id=None,
                              new_text='Вы наш Король'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=-999, next_action_id=None, new_action_id=None,
                              new_text='Казнить его'),
                 hide=False, keyword='не')
        ],
    ),
    '2.Нет': dict(
        text='Из-за фальшивых монет налоги собирать всё сложнее. Может всё-таки отчеканить новые монеты?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=-40, authority=-30, next_action_id=None, new_action_id=None,
                              new_text=None),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=-100, authority=-10, next_action_id=None, new_action_id=None,
                              new_text='Из-за фальшивых монет вся экономика рухнула'),
                 hide=False, keyword='не')
        ],
    ),
    '3.Да': dict(
        text='Наши свиньи обнаружили огромные поля трюфелей! Изволите разделить урожай с крестьянами?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=20, authority=30, next_action_id=None, new_action_id=None,
                              new_text='Крестьяне приветствуют Ваше решение, милорд! Продажа трюфелей принесла хороший доход!'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=40, authority=0, next_action_id=None, new_action_id=None,
                              new_text='Продажа трюфелей принесла хороший доход!'),
                 hide=False, keyword='не')
        ],
    ),
    '4.Нет': dict(
        text='Бросить его в темницу?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=5, next_action_id=None, new_action_id=None,
                              new_text='Ваше блогородие! Яблоки теперь в безопасности'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=-15, authority=-5, next_action_id=None, new_action_id=None,
                              new_text='Ваше блогородие! Яблок на всех не хватит, а воровать теперь повадились каждый день!'),
                 hide=False, keyword='не')
        ],
    ),
    '8.Нет': dict(
        text='Культурное сообщество не довольно вашим решением. С лозунгом "За культуру ты нам ответишь" бунтующие собрались на площади. Обезглавить?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=30, next_action_id=None, new_action_id=None,
                              new_text='Это весьма жестокое решение.'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=0, next_action_id='8.Нет.Нет', new_action_id=None,
                              new_text=''),
                 hide=False, keyword='не')
        ],
    ),
    '8.Нет.Нет': dict(
        text='Посадить?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=-40, next_action_id=None, new_action_id=None,
                              new_text='Они это запомнят'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=0, next_action_id='8.Нет.Нет.Нет', new_action_id=None,
                              new_text=''),
                 hide=False, keyword='не')
        ],
    ),
    '8.Нет.Нет.Нет': dict(
        text='Сделать как они хотят: построить памятник?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=-35, authority=25, next_action_id=None, new_action_id=None,
                              new_text='Наиболее здравое хоть и дорогое решение.'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=-75, authority=-60, next_action_id=None, new_action_id=None,
                              new_text='Пока вы решали бунты закончились, а последствия остались. На восстановление уйдёт много денег.'),
                 hide=False, keyword='не')
        ],
    ),
    '42.Да': dict(
        text='Пи*да',
        card=dict(type='BigImage', image_id='1533899/3ce02377e44322e03fb6', title=None, description=None),
        buttons=[
            dict(title='Продолжить',
                 payload=dict(money=0, authority=0, next_action_id=None, new_action_id=None,
                              new_text=''),
                 hide=False, keyword='продолж'),
        ],
    ),
}

"""
just actions list
next_action means that the action will immediately after the current
new_action_id means that the action will just add in queue
"""
actions = {
    '0': dict(
        text='Вас хочет допросить инквизиция. Согласитесь?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=0, next_action_id='0.Да', new_action_id=None,
                              new_text=None),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=-50, next_action_id=None, new_action_id=None,
                              new_text='Правильно, с какой ещё стати вас должны проверять. Вот только жители не в восторге'),
                 hide=False, keyword='не')
        ],
    ),
    '1': dict(
        text='Милорд! Один из жителей наших земель убил свою жену! Обезглавить его?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=-30, authority=20, next_action_id=None, new_action_id=None,
                              new_text='Народ собрался на площади. Это зрелище не из дешевых, но Вы стали еще влиятельнее!'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=-30, next_action_id=None, new_action_id=None,
                              new_text='Да уж, казнь это зрелище не из дешевых, но зато Вы не потеряли деньги.'),
                 hide=False, keyword='не')
        ],
    ),
    '2': dict(
        text='Ваше благородие! Кто-то подделывает монеты в наших землях! Распорядитесь отчеканить новые?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=-30, authority=20, next_action_id=None, new_action_id=None,
                              new_text='Да уж, дело не из дешевых, но зато экономический крах нам не грозит.'),
                 hide=False, keyword='не'),
            dict(title='Нет',
                 payload=dict(money=0, authority=0, next_action_id=None, new_action_id='2.Нет',
                              new_text='Фальшивые монеты приобретают всё большее распространение! Налоги собирать стало сложнее. Зато у населения стало чуть больше денег в карманах!'),
                 hide=False, keyword='да'),

        ],
    ),
    '3': dict(
        text='Иностранный исследователь утверждает, будто наши края богаты дорогими трюфелями! Изволите отправить наших свиней на поиски этих грибов?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=0, next_action_id='3.Да', new_action_id=None,
                              new_text=''),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=0, next_action_id=None, new_action_id=None,
                              new_text=''),
                 hide=False, keyword='не')
        ],
    ),
    '4': dict(
        text='Ваша светлость! Один селянин всё время ворует яблоки из Вашего сада! Прикажете казнить его?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=-30, next_action_id=None, new_action_id=None,
                              new_text='Народу не по нраву ваше жесткое решение'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=0, next_action_id='4.Нет', new_action_id=None,
                              new_text=''),
                 hide=False, keyword='не')
        ],
    ),
    '5': dict(
        text='Милорд! Содержание Вашего поместья требует всё больших трат. Может быть повысим налоги?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=-15, next_action_id=None, new_action_id=None,
                              new_text='Народу не по нраву ваше решение'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=-15, authority=0, next_action_id=None, new_action_id=None,
                              new_text='Ваше благородие! Нам придётся изыскать средства из казны, иначе Ваше поместье быстро обветшает.'),
                 hide=False, keyword='не')
        ],
    ),
    '6': dict(
        text='Граф Уиглисли предлагает вам построить в деревне таверну. Изволите принять коммерческое предложение?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=-30, authority=50, next_action_id=None, new_action_id=None,
                              new_text='Благородный поступок, Ваша светлость! Крестьяне очень Вам благодарны! Но теперь Ваши слуги превратились в пьяниц и на полях некому работать.'),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=-30, next_action_id=None, new_action_id=None,
                              new_text='Народу не по нраву ваше решение. Зато вы не потратили ни монеты'),
                 hide=False, keyword='не')
        ],
    ),
    '7': dict(
        text='Ваша светлость! Служанка случайно испортила гобелен в Ваших покоях! Прикажете сшить новый?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=-10, authority=0, next_action_id=None, new_action_id=None,
                              new_text='Это вышло в кругленькую сумму'),
                 hide=False, keyword='да'),
            random.choice([dict(title='Нет',
                                payload=dict(money=0, authority=-10, next_action_id=None, new_action_id=None,
                                             new_text='Слуга застал Вас за шитьём, милорд! Боюсь, что он не применёт разболтать об этом кому-то ещё!'),
                                hide=False, keyword='не'),
                           dict(title='Нет',
                                payload=dict(money=0, authority=0, next_action_id=None, new_action_id=None,
                                             new_text=''),
                                hide=False, keyword='не'),
                           ]),
        ],
    ),
    '8': dict(
        text='Народ желает установить огромную статую из золота в честь выдающегося культурного деятеля вашего государства! Распорядитесь создать скульптуру?',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=-30, authority=30, next_action_id=None, new_action_id=None,
                              new_text='Это вышло в кругленькую сумму. Зато подняло ваше величие в глазах народа'),
                 hide=False, keyword='да'),
            random.choice([dict(title='Нет',
                                payload=dict(money=0, authority=-10, next_action_id=None, new_action_id=None,
                                             new_text='Культурное сообщество не довольно вашим решением. С их слов: "За культуру ты нам ответишь". Как бы это не вылилось в конфликт'),
                                hide=False, keyword='не'),
                           dict(title='Нет',
                                payload=dict(money=0, authority=0, next_action_id='8.Нет', new_action_id=None,
                                             new_text=''),
                                hide=False, keyword='не'),
                           dict(title='Нет',
                                payload=dict(money=0, authority=0, next_action_id=None, new_action_id=None,
                                             new_text=''),
                                hide=False, keyword='не')
                           ]),
        ],
    ),
    '10': dict(
        text='42',
        card=dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=None, description=None),
        buttons=[
            dict(title='Да',
                 payload=dict(money=0, authority=0, next_action_id='42.Да', new_action_id=None,
                              new_text=''),
                 hide=False, keyword='да'),
            dict(title='Нет',
                 payload=dict(money=0, authority=0, next_action_id=None, new_action_id=None,
                              new_text='Как скажете.'),
                 hide=False, keyword='не')
        ],
    ),
}


def start_game(event):
    session_data = SessionData(event)

    # session states
    session_data.game_info = {
        'name': f'{filename}',
        'status': 'running',
        'actions_happened': [],
        'actions_queue': [],
        'money': 100,
        'authority': 100,
    }

    session_data.session_state['screen'] = f'{filename}.start_game'

    # getting action data
    new_action_key = random.choice(list(actions.keys()))
    new_action = actions[new_action_key]

    card = new_action.get('card', {})
    card['title'] = f'<{filename}.start_game>'

    session_data.game_info['actions_happened'].append(new_action_key)

    session_data.session_state['game_info'] = session_data.game_info

    return make_response(
        text=new_action.get('text', ''),
        session_state=session_data.session_state,
        card=card,
        buttons=new_action.get('buttons')
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
        card_title, button_data = get_data_from_pressed_button(event, session_data)

        # getting next action, which will immediately after the current
        next_action: dict = actions_consequences.get(button_data.get('next_action_id'))

        if not next_action is None:
            session_data.game_info['actions_queue'].insert(0, next_action)

        # getting new action, which will just add in queue
        new_action: dict = actions_consequences.get(button_data.get('new_action_id'))

        if not new_action is None:
            session_data.game_info['actions_queue'].insert(2, new_action)

        # creating text
        text_list = list(filter(lambda s: s not in [None, ''], [button_data.get('new_text', 'button.text'),
                                                                get_game_resources_text(session_data,
                                                                                        button_data)]))

        # update resources data in game_info
        new_money = session_data.game_info['money'] + button_data['money']
        session_data.game_info['money'] = new_money if new_money >= 0 else 0

        new_authority = session_data.game_info['authority'] + button_data['authority']
        session_data.game_info['authority'] = new_authority if new_authority >= 0 else 0

        if (session_data.game_info['money'] and session_data.game_info['authority']) == 0:
            return game_failed(event, text_list)

        # getting new random actions
        if len(session_data.game_info['actions_happened']) < len(actions):
            new_random_action_key = get_new_random_action(session_data)

            if not new_random_action_key is None:
                new_random_action = actions[new_random_action_key]

                session_data.game_info['actions_queue'].append(new_random_action)
                session_data.game_info['actions_happened'].append(new_random_action_key)

        elif len(session_data.game_info['actions_queue']) == 0:
            return game_passed(event, text_list)

        # getting current action
        action: dict = session_data.game_info['actions_queue'][0]

        # deleting current action from queue and put it in list of happened
        del session_data.game_info['actions_queue'][0]

        text_list.append(action.get('text', 'action.text'))
        text = '\n'.join(text_list)

        # update game_info in session state
        session_data.session_state['game_info'] = session_data.game_info

        # get card
        card = action.get('card', {})
        card['title'] = f'Ваш ответ: {card_title}'

        # get buttons
        buttons = action.get('buttons')

        return make_response(
            text=text,
            session_state=session_data.session_state,
            card=card,
            buttons=buttons
        )

    # if all conditions are False
    return fallback(event, text=f'<{filename}.handler>')


def game_passed(event, text_list):
    session_data = SessionData(event)

    session_data.session_state['game_info'] = {
        'name': f'{filename}',
        'status': 1,
    }

    text_list.append('Игра окончена! Поздравляем вы выиграли! (события закончились)')

    card = dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=f'<{filename}.game_passed>',
                description=None)
    buttons = [dict(title='Поставить оценку', hide=False, url='https://i.imgur.com/e6yb607.png')]

    return make_response(
        text='\n'.join(text_list),
        session_state=session_data.session_state,
        card=card,
        buttons=buttons
    )


def game_failed(event, text_list):
    session_data = SessionData(event)

    session_data.session_state['game_info'] = {
        'name': f'{filename}',
        'status': 0,
    }

    if session_data.game_info['money'] == 0:
        text_list.append(
            'Милорд! Мне очень жаль, но Вы потеряли всё Ваше богатство! Король собирается казнить Вас за растраты!')

    if session_data.game_info['authority'] == 0:
        text_list.append('Милорд! Мне очень жаль, но Вы потеряли всё Ваше влияния! Народ собирается Вас казнить!')

    card = dict(type='BigImage', image_id='1030494/12b6a5d1ea04e3317f9a', title=f'<{filename}.game_failed>',
                description=None)
    buttons = [dict(title='Поставить оценку', hide=False, url='https://i.imgur.com/e6yb607.png')]

    return make_response(
        text='\n'.join(text_list),
        session_state=session_data.session_state,
        card=card,
        buttons=buttons
    )


def get_data_from_pressed_button(event, session_data):
    card_title = f'<{filename}.handler>'  # basic card title
    message = session_data.message
    button_data = {}

    # find out which button was pressed and getting button data
    if event['request']['type'] == 'ButtonPressed':  # if user pressed a button
        if 'payload' in event['request']:
            for button in session_data.session_state.get('last_buttons'):
                if button['title'].lower() == message:
                    card_title = button['title']
                    button_data = button['payload']

    elif event['request']['type'] == 'SimpleUtterance':  # if user just send a message
        for button in session_data.last_buttons:
            if not button.get('keyword') is None:
                if all([keyword in message for keyword in button['keyword'].lower().split()]):
                    card_title = button['title']
                    button_data = button['payload']
                    break

        else:  # if didn't find the right button
            card_title = 'Что-то я вас не поняла. Давайте ещё раз и лучше используйте кнопки.'

    return card_title, button_data


def get_new_random_action(session_data):
    actions_keys = set(list(actions.keys()))
    actions_happened = set(session_data.game_info['actions_happened'])

    new_actions_keys = actions_keys - actions_happened
    new_action_key = random.choice(list(new_actions_keys))

    return new_action_key


def get_game_resources_text(session_data, button_data) -> str:
    text_list = []

    if button_data['money'] < 0:
        new_money = session_data.game_info["money"] + button_data["money"]
        new_money = new_money if new_money >= 0 else 0

        text_list.append(f'Ваше богатство упало до {new_money}.')

        if 0 < new_money < 25:
            text_list.append('Будьте осторожны, если у вас не останется денег, то вы проиграете.')

    elif button_data['money'] > 0:
        text_list.append(f'Ваше богатство выросло до {session_data.game_info["money"] + button_data["money"]}.')

    if button_data['authority'] < 0:
        new_authority = session_data.game_info["authority"] + button_data["authority"]
        new_authority = new_authority if new_authority >= 0 else 0

        text_list.append(f'Ваше влияние упало до {new_authority}.')

        if 0 < new_authority < 25:
            text_list.append('Будьте осторожны, если у вас не останется влияния, то вы проиграете.')

    if button_data['authority'] > 0:
        text_list.append(f'Ваше влияние выросло до {session_data.game_info["authority"] + button_data["authority"]}.')

    return '\n'.join(text_list)
