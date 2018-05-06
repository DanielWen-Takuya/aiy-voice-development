#!/usr/bin/env python3

"""
AiyAssistant class can reponse to questions by Google Cloud, react to
button, control the led on the button

Available to Rasperry Pi 2/3

by Zoutao WEN
"""

import logging
import platform
import sys
import threading

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType

from postgre_server import PostgreServer

from random import randint

import datetime

import subprocess

# need to be used for postgresql
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


class ActionButton(object):
    def __init__(self):
        self.action_time = datetime.datetime.now()
        self.question = None
        self.answer = None
        self.success_read = False
        self.success_answer = False

    def set_question(self, question):
        self.question = question
        self.success_read = True

    def set_answer(self, answer):
        self.answer = answer
        self.success_answer = True


class AiyAssistant(object):
    def __init__(self, pwd):
        self._task = threading.Thread(target=self._run_task)
        self._can_start_conversation = False
        self._assistant = None
        self.music_process = None
        self.server = PostgreServer(pwd)
        self.action_button = None

    def start(self):
        self._task.start()

    def _run_task(self):

        credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
        with Assistant(credentials) as assistant:
            self._assistant = assistant
            self.server.connect()
            try:
                for event in assistant.start():
                    self._process_event(event)
            finally:
                self.server.close()


    def _process_event(self, event):
        status_ui = aiy.voicehat.get_status_ui()
        status_ui.set_trigger_sound_wave('listening.wav');

        if event.type == EventType.ON_START_FINISHED:
            status_ui.status('ready')
            self.action_button = ActionButton()
            self._can_start_conversation = True
            # Start the voicehat button trigger.
            aiy.voicehat.get_button().on_press(self._on_button_pressed)
            if sys.stdout.isatty():
                print('Say "OK, Google" or press the button, then speak. '
                      'Press Ctrl+C to quit...')

        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self._can_start_conversation = False
            status_ui.status('listening')

        elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            print('You said:', event.args['text'])
            text = event.args['text'].lower()
            self.action_button.set_question(text)
            # do some reaction
            if text == 'testing':
                self._assistant.stop_conversation()
                self.testing()
            elif text == 'play music':
                self._assistant.stop_conversation()
                self.play_music()
            elif text == 'record':
                self._assistant.stop_conversation()
                self.record_sth()

        elif event.type == EventType.ON_END_OF_UTTERANCE:
            status_ui.status('thinking')

        elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
              or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
              or event.type == EventType.ON_NO_RESPONSE):
            # status_ui.status('ready')
            # save action in server
            action = self.action_button
            print('%s: %s => %s' % (action.action_time, action.question, action.answer))
            self._can_start_conversation = True

        elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
            sys.exit(1)


    def _on_button_pressed(self):
        # Check if we can start a conversation. 'self._can_start_conversation'
        # is False when either:
        # 1. The assistant library is not yet ready; OR
        # 2. The assistant library is already in a conversation.
        if self._can_start_conversation:
            self._assistant.start_conversation()
        if self.music_process is not None:
            self.music_process.kill()
            self.music_process = None


    def testing(self):
        print('Testing!')
        led = aiy.voicehat.get_led()
        # led.set_state(aiy.voicehat.LED.ON)
        # led.set_state(aiy.voicehat.LED.BLINK)
        # led.set_state(aiy.voicehat.LED.BLINK_3)
        # led.set_state(aiy.voicehat.LED.BEACON)
        # led.set_state(aiy.voicehat.LED.BEACON_4)
        # led.set_state(aiy.voicehat.LED.BEACON_DARK)
        # led.set_state(aiy.voicehat.LED.DECAY)
        # led.set_state(aiy.voicehat.LED.PULSE_SLOW)
        # led.set_state(aiy.voicehat.LED.PULSE_QUICK)

    def play_music(self):  # can use pkill -f mplayer to kill the process or use the process?
        # use server
        (success, list) = self.server.read_music_list()
        if success == 'Ok':
            nb = len(list)
            print(nb)
            index = randint(0, nb-1)
            choice = list[index]
            print(choice)
            file_path = choice[3]
            file_name = choice[1]
            extension = choice[2]
            complete = file_path + '/' + file_name + '.' + extension
            print('Going to play ' + complete)
            self.music_process = subprocess.Popen(['mplayer', complete],start_new_session=True)

    def record_sth(self):  # need test
        import aiy.assistant.grpc
        assistant = aiy.assistant.grpc.get_assistant()
        print('Recording')
        with aiy.audio.get_recorder():
            text, audio = assistant.recognize()
            if text:
                print('You said "', text, '"')

            if audio:
                aiy.audio.play_audio(audio)


# test
def main():
    if platform.machine() == 'armv6l':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)
    AiyAssistant('qwertyuiop').start()


if __name__ == '__main__':
    main()
