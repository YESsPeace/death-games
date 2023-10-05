STATE_REQUEST_KEY = 'session'
STATE_RESPONSE_KEY = 'session_state'


def make_response(text, *, tts: str = None, card: dict = None, buttons: list = None,
                  session_state: dict = None, user_state: dict = None, end_session: bool = False):
    response = {
        'text': text,
        'tts': tts if tts is not None else text,
        "end_session": end_session,
    }

    if card is not None:
        if card.get('description') is None:
            card['description'] = text

        if card.get('title') is None:
            card['title'] = 'card title is empty'

        response['card'] = card
        session_state['last_card'] = card

    if buttons is not None:
        response['buttons'] = buttons

    session_state['last_buttons'] = buttons

    webhook_response = {
        'response': response,
        'version': '1.0'
    }

    if session_state is not None:
        webhook_response[STATE_RESPONSE_KEY] = session_state

    if user_state is not None:
        webhook_response['user_state_update'] = user_state

    return webhook_response


def fallback(event, text='Извините, я вас не поняла.', tts=None):
    session_data = SessionData(event)

    if not session_data.last_card is None:
        card_title = text if len(text) < 128 else 'card title too long'

        if session_data.last_card['type'] == 'BigImage':
            session_data.last_card['title'] = card_title

        elif session_data.last_card['type'] == 'ItemsList':
            session_data.last_card['header']['text'] = card_title

    return make_response(text, tts=tts, card=session_data.last_card, buttons=session_data.last_buttons,
                         session_state=session_data.session_state, user_state=session_data.user_state)


class SessionData:
    def __init__(self, event):
        # Session's ids and new or not session
        self.session = event.get(STATE_REQUEST_KEY, {})  # Read Only
        self.session_id = self.session['session_id']
        self.skill_id = self.session['skill_id']
        self.user_id = self.session['user_id']
        self.is_new = self.session['new']

        # some session's states
        self.state = event.get('state', {})
        self.user_state = self.state.get('user', {})  # Write&Read
        self.session_state = self.state.get(STATE_REQUEST_KEY, {})  # Write&Read

        # my own values in session's state
        self.last_buttons = self.session_state.get('last_buttons')
        self.last_card = self.session_state.get('last_card')
        self.game_info = self.session_state.get('game_info', {})

        # intents
        self.intents = event['request']['nlu']['intents']

        # message and buttons' data
        self.message = None
        if event['request']['type'] == 'SimpleUtterance':
            self.message = event['request']['original_utterance'].lower()

        self.payload_data = None  # it's only for buttons, which under a message
        if event['request']['type'] == 'ButtonPressed':
            self.message = ' '.join(event['request']['nlu']['tokens']).lower()
            self.payload_data = event['request'].get('payload')
