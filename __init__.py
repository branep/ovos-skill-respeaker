# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All credits go to domcross (Github https://github.com/domcross)

import time

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import LOG
from mycroft import intent_file_handler

from .pixels import Pixels, pixels

from gpiozero import LED

class ReSpeaker_4mic_hat(MycroftSkill):

    def __init__(self):
        super().__init__()

    def initialize(self):
        #power = LED(5)
        #power.on()
        #pixels.set_brightness(10)
        self.enable()

    def enable(self):
        LOG.debug("initializing")
        pixels.wakeup()
        time.sleep(1)

        self.add_event('recognizer_loop:wakeword',
            self.handle_listener_wakeup)
        self.add_event('recognizer_loop:record_end',
            self.handle_listener_think)

        self.add_event('recognizer_loop:audio_output_start',
            self.handle_listener_speak)
        self.add_event('recognizer_loop:audio_output_end',
            self.handle_listener_off)

        self.add_event('mycroft.ready',
            self.handle_listener_off)

        self.add_event('complete_intent_failure',
            self.handle_listener_off)

        #self.add_event('mycroft.skill.handle.start',
        #    self.handle_listener_think)
        #self.add_event('mycroft.skill.handle.complete',
        #    self.handle_listener_off)

        pixels.off()

    def disable(self):
        LOG.debug("shutdown")
        self.remove_event('recognizer_loop:wakeup')
        self.remove_event('recognizer_loop:record_end')
        self.remove_event('recognizer_loop:audio_output_start')
        self.remove_event('recognizer_loop:audio_output_end')
        #self.remove_event('mycroft.skill.handle.start')
        #self.remove_event('mycroft.skill.handle.complete')

    def shutdown(self):
        pixels.off()

    def handle_listener_wakeup(self, message):
        LOG.debug("wakeup")
        pixels.listen()

    def handle_listener_off(self, message):
        LOG.debug("off")
        pixels.off()

    def handle_listener_think(self, message):
        LOG.debug("think")
        pixels.think()

    def handle_listener_speak(self, message):
        LOG.debug("speak")
        pixels.speak()

    @intent_handler(IntentBuilder("").require("PixelDemo"))
    def handle_pixel_demo(self, message):
        pixels.think()
        time.sleep(3)
        pixels.speak()
        time.sleep(3)
        pixels.off()
        self.speak_dialog("DemoComplete")

    @intent_handler(IntentBuilder("").require("EnablePixelRing"))
    def handle_enable_pixels_intent(self, message):
        self.disable()
        self.enable()
        self.speak_dialog("EnablePixelRing")

    @intent_handler(IntentBuilder("").require("DisablePixelRing"))
    def handle_disable_pixels_intent(self, message):
        self.disable()
        self.speak_dialog("DisablePixelRing")

def create_skill():
    return ReSpeaker_4mic_hat()
