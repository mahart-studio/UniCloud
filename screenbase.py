from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


class UniScreen(Screen):

    __events__ = ('on_back_button',)

    def on_pre_enter(self):
        Window.bind(on_key_down=self.listen_for_key)

    def on_pre_leave(self):
        Window.unbind(on_key_down=self.listen_for_key)

    def listen_for_key(self, keyboard, keycode, text, *modifiers):
        if keycode == 27:
            self.dispatch('on_back_button')

    def on_back_button(self):
        ''' event fired when the back button is pressed'''