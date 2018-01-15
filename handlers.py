# -*- coding: UTF-8 -*- 

import sys
import json
import tornado.web
from tornado import gen
from fb import event_action
from settings import PAT, VERIFY_TOKEN


def get_message_seq(event: dict) -> int:
    seq = 0
    event_type = get_event_type(event)
    if event_type == 'quick_reply':
        seq = int(event['message']['seq'])
    if event_type == 'read':
        seq = int(event['read']['seq'])
    if event_type == 'location':
        seq = int(event['message']['seq'])
    if event_type == 'text':
        seq = int(event['message']['seq'])
    if event_type == 'delivery':
        seq = int(event['delivery']['seq'])
    if event_type == 'echo':
        seq = int(event['message']['seq'])
    return seq


def get_location_data(event: dict) -> dict:
    attachments = event['message']['attachments']
    coordinates = attachments[0]['payload']['coordinates']
    seq = get_message_seq(event)
    data = {
        'type': 'location',
        'seq': seq,
        'sender_id': event['sender']['id'],
        'timestamp': event['timestamp'],
        'lat': coordinates['lat'],
        'lon': coordinates['long']
    }
    return data


def get_quick_reply_data(event: dict) -> dict:
    message = event['message']
    seq = get_message_seq(event)
    data = {
        'type': 'quick_reply',
        'seq': seq,
        'sender_id': event['sender']['id'],
        'timestamp': event['timestamp'],
        'payload': message['quick_reply']['payload'],
        'text': message['text']
    }
    return data


def get_postback_data(event: dict) -> dict:
    seq = get_message_seq(event)
    data = {
        'type': 'postback',
        'seq': seq,
        'sender_id': event['sender']['id'],
        'timestamp': event['timestamp'],
        'payload': event['postback']['payload'],
        'title': event['postback']['title']
    }
    return data


def get_text_data(event: dict) -> dict:
    seq = get_message_seq(event)
    data = {
        'type': 'text',
        'seq': seq,
        'sender_id': event['sender']['id'],
        'timestamp': event['timestamp'],
        'text': event['message']['text']
    }
    return data


def get_echo_data(event: dict) -> dict:
    seq = get_message_seq(event)
    data = {
        'type': 'echo',
        'seq': seq,
        'sender_id': event['sender']['id'],
        'timestamp': event['timestamp'],
        'text': event['message']['text']
    }
    return data


def get_event_type(event: dict) -> str:
    event_type = None
    message = event.get('message', {})
    if 'quick_reply' in message.keys():
        return 'quick_reply'
    if 'is_echo' in message.keys():
        return 'echo'
    if 'read' in event.keys():
        return 'read'
    if message.get('attachments', []):
        if message.get('attachments', [])[0].get('type', '') == 'location':
            return 'location'
    if 'postback' in event.keys():
        return 'postback'
    if 'delivery' in event.keys():
        return 'delivery'
    if 'text' in message.keys():
        return 'text'
    return event_type


# @gen.coroutine
def get_messaging_events(payload):
    """
    Generate tuples of (sender_id, message_text) from the provided payload.
    """
    event_data_funcs = {
        'text': get_text_data,
        'echo': get_echo_data,
        'quick_reply': get_quick_reply_data,
        'location': get_location_data,
        'postback': get_postback_data
    }
    data = json.loads(payload)
    messaging_events = data['entry'][0]['messaging']
    for event in messaging_events:
        event_type = get_event_type(event)
        event_func = event_data_funcs.get(event_type, None)
        if event_func:
            event_data = event_func(event)
        else:
            event_data = {}
        yield (event_data.get('sender_id', ''), event_data)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        sys.stdout.write('Handling Verification.')
        verify_token = self.get_argument(
            'hub.verify_token', default='', strip=False)
        if verify_token == VERIFY_TOKEN:
            challenge = self.get_argument(
                'hub.challenge', default='', strip=False)
            responce = challenge
        else:
            responce = 'Verification fail'
        self.set_status(200)
        self.write(responce)
        self.finish()

    @gen.coroutine
    def post(self):
        payload = self.request.body
        for sender, incoming_message in get_messaging_events(payload):
            yield event_action(PAT, sender, incoming_message)
        self.finish()
