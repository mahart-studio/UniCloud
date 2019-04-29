from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
# Eventually write
#  Config.write()
Config.set('graphics', 'height', '630')
Config.set('graphics', 'width', '360')

# Create our Resources
from kivy.resources import resource_add_path
resource_add_path('fonts')
resource_add_path('data/images/common')
resource_add_path('data/images/pdfmaker')
resource_add_path('data/images/cloud')
resource_add_path('data/images/student')
resource_add_path('Cloud')
resource_add_path('Cloud/Pdfmaker')
resource_add_path('student_tools')

# our major imports
from Cloud.main import root

from kivy.storage.jsonstore import JsonStore
from kivy import platform
from kivy.app import App

import os

if platform == 'android':
    from android.runnable import run_on_ui_thread

# from kivy.lang import Builder
# root = Builder.load_file('settings.kv')

class UniCloud(App):
    def build(self):

        self.set_status_color()
        self.creat_local_stores()
        return root

    def creat_local_stores(self):
        self.unicloud_store = JsonStore(os.path.join(self.user_data_dir, 'unicloud_store.json'))

    def on_pause(self):
        return True

    @run_on_ui_thread
    def set_status_color(self, color='holo_orange_light'):
        from jnius import autoclass

        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
        r_color = autoclass('android.R$color')
        color = getattr(r_color, color)

        window = activity.getWindow()
        window.clearFlags(LayoutParams.FLAG_TRANSLUCENT_STATUS)
        window.addFlags(LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(activity.getResources().getColor(color))

    def on_stop(self):
        self.unicloud_store.put('user', first_time=False)

if __name__ == "__main__":
    UniCloud().run()


