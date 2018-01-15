# -*- coding: UTF-8 -*-

import json
import requests
from tornado import gen
import dal
from settings import API_URL


def add_text_to_message(text: str, message: dict = {}) -> dict:
    """
    Text is used when sending a text message, must be UTF-8 and
    has a 640 character limit.
    See docs at
    https://developers.facebook.com/docs/messenger-platform/send-api-reference
    """
    if message.get('text', ''):
        prev_text = message.get('text', '')
        message['text'] = f'{prev_text}\n{text}'
    else:
        message['text'] = text
    return message


def add_quick_replies_to_message(reply: dict, message: dict = {}) -> dict:
    '''
    See docs at
    https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies
    '''
    quick_replies = message.get('quick_replies', [])
    quick_replies.append(reply)
    message['quick_replies'] = quick_replies
    return message


def add_buttons_to_message(
        buttons: list,
        text: str,
        message: dict = {}
) -> dict:
    '''
    See docs at
    https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template
    '''
    attachment = {
        'type': 'template',
        'payload': {
            'text': text,
            'template_type': 'button',
            'buttons': buttons
        }
    }
    message['attachment'] = attachment
    return message


def send_message(
        token: str,
        user_id: str,
        message: dict = {}
) -> None:
    """
    Send the message text to user with id.
    See docs at
    https://developers.facebook.com/docs/messenger-platform/send-api-reference
    and
    https://developers.facebook.com/docs/messenger-platform/product-overview/conversation#send_messages
    """
    r = requests.post(
        API_URL,
        params={'access_token': token},
        data=json.dumps({
            'recipient': {'id': user_id},
            'message': message
        }),
        headers={'Content-type': 'application/json'}
    )


def do_on_text_data(
        token: str,
        user_id: str,
        incoming_event: dict = {}
) -> dict:
    text = 'ололо текст'
    message = add_text_to_message(text)
    send_message(token, user_id, message)
    report = {'status': 'ok'}
    return report


def do_on_echo_data(
        token: str,
        user_id: str,
        incoming_event: dict = {}
) -> dict:
    text = 'ололо эхо'
    message = add_text_to_message(text)
    send_message(token, user_id, message)
    report = {'status': 'ok'}

    return report


def do_on_quick_reply_data(
        token: str,
        user_id: str,
        incoming_event: dict = {}
) -> dict:
    text = 'ололо кр'
    message = add_text_to_message(text)
    send_message(token, user_id, message)
    report = {'status': 'ok'}

    return report


def do_on_location_data(
        token: str,
        user_id: str,
        incoming_event: dict = {}
) -> dict:
    text = 'ололо локация'
    message = add_text_to_message(text)
    send_message(token, user_id, message)
    report = {'status': 'ok'}

    return report


def do_on_postback_data(
        token: str,
        user_id: str,
        incoming_event: dict = {}
) -> dict:
    text = 'ололо постбэк'
    message = add_text_to_message(text)
    send_message(token, user_id, message)
    report = {'status': 'ok'}

    return report


@gen.coroutine
def event_action(
        token: str,
        user_id: str,
        incoming_event: dict = {}
) -> None:
    """
    Raise some action for incoming event
    """
    event_action_funcs = {
        'text': do_on_text_data,
        'echo': do_on_echo_data,
        'quick_reply': do_on_quick_reply_data,
        'location': do_on_location_data,
        'postback': do_on_postback_data
    }
    user_info = dal.redis_get(user_id)
    action_func = event_action_funcs.get(incoming_event['type'], None)
    result = action_func(token, user_id, incoming_event)
