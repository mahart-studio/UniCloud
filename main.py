from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
# Eventually write
#  Config.write()
Config.set('graphics', 'height', '630')
Config.set('graphics', 'width', '360')

import sys
sys.path=['libs',]+sys.path

# Create our Resources
from kivy.resources import resource_add_path
resource_add_path('data/fonts')
resource_add_path('data/images/common')
resource_add_path('data/images/pdfmaker')
resource_add_path('data/images/cloud')
resource_add_path('data/images/student')
resource_add_path('Cloud')
resource_add_path('Cloud/pdfmaker')
resource_add_path('student_tools')

# our major imports
from Cloud.main import root

from kivy.storage.jsonstore import JsonStore
from kivy import platform
from kivy.app import App

import os

if platform == 'android':
    from mahartstudios.android.api import set_status_color

# from kivy.lang import Builder
# root = Builder.load_file('settings.kv')

class UniCloud(App):
    def build(self):

        # set_status_color('holo_orange_dark')
        # self.start_app_service()
        self.creat_local_stores()
        return root

    def creat_local_stores(self):
        self.unicloud_store = JsonStore(os.path.join(self.user_data_dir, 'unicloud_store.json'))

    def on_pause(self):
        return True

    def start_app_service(self):
        from jnius import autoclass
        service = autoclass('org.unicloud.unicloud.ServiceUniservice')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.start(activity, 'unicloud')

    def restart_service(self):
        service = autoclass('org.kivy.android.PythonService').mService
        service.setAutoRestartService(True)

    def on_start(self):
        pass

    def on_stop(self):
        self.unicloud_store.put('user', first_time=False)

if __name__ == "__main__":
    UniCloud().run()