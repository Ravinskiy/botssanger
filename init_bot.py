# -*- coding: UTF-8 -*-

import json
import requests
from settings import PAT


def init_facebook() -> None:
    """
    Init configuration for the facebook bot.
    See docs at
    https://developers.facebook.com/docs/messenger-platform/messenger-profile
    """

    print('Start init')
    # Set greeting for the bot
    r = requests.post(
        'https://graph.facebook.com/v2.9/me/thread_settings',
        params={'access_token': PAT},
        data=json.dumps({
            'setting_type': 'greeting',
            'greeting': {
                'text': 'Welcome to FB bot.'
            }
        }),
        headers={'Content-type': 'application/json'}
    )
    print(f'Set greeting result: status {r.status_code}, response {r.text}')

    # Set start button for the bot
    r = requests.post(
        'https://graph.facebook.com/v2.9/me/messenger_profile',
        params={'access_token': PAT},
        data=json.dumps({
            'get_started': {
                'payload': 'GET_STARTED_PAYLOAD'
            }
        }),
        headers={'Content-type': 'application/json'}
    )
    print(f'Set start button result: status {r.status_code}, \
          response {r.text}')

    # Set persistent menu for the bot
    r = requests.post(
        'https://graph.facebook.com/v2.9/me/messenger_profile',
        params={'access_token': PAT},
        data=json.dumps({
            'persistent_menu': [
                {
                    'locale': 'default',
                    'composer_input_disabled': False,
                    'call_to_actions': [
                        {
                            'title': 'Language',
                            'type': 'nested',
                            'call_to_actions': [
                                {
                                    'title': 'English',
                                    'type': 'postback',
                                    'payload': 'ENGLISH_PAYLOAD'
                                },
                                {
                                    'title': 'Русский',
                                    'type': 'postback',
                                    'payload': 'RUSSIAN_PAYLOAD'
                                },
                                {
                                    'title': 'עִברִית',
                                    'type': 'postback',
                                    'payload': 'HEBREW_PAYLOAD'
                                }
                            ]
                        },
                        {
                            'title': 'Update location',
                            'type': 'postback',
                            'payload': 'UPDATE_LOCATION_PAYLOAD'
                        },
                        {
                            'title': 'Contact',
                            'type': 'postback',
                            'payload': 'CONTACT_PAYLOAD'
                        }
                    ]
                },
                {
                    'locale': 'ru_RU',
                    'composer_input_disabled': False,
                    'call_to_actions': [
                        {
                            'title': 'Язык',
                            'type': 'nested',
                            'call_to_actions': [
                                {
                                    'title': 'English',
                                    'type': 'postback',
                                    'payload': 'ENGLISH_PAYLOAD'
                                },
                                {
                                    'title': 'Русский',
                                    'type': 'postback',
                                    'payload': 'RUSSIAN_PAYLOAD'
                                },
                                {
                                    'title': 'עִברִית',
                                    'type': 'postback',
                                    'payload': 'HEBREW_PAYLOAD'
                                }
                            ]
                        },
                        {
                            'title': 'Обновить местоположение',
                            'type': 'postback',
                            'payload': 'UPDATE_LOCATION_PAYLOAD'
                        },
                        {
                            'title': 'Связаться',
                            'type': 'postback',
                            'payload': 'CONTACT_PAYLOAD'
                        }
                    ]
                }
            ]
        }),
        headers={'Content-type': 'application/json'}
    )
    print(f'Set menu result: status {r.status_code}, response {r.text}')
