import kivy
from kivy import platform

# kivy widgets
from kivy.uix.screenmanager import ScreenManager, ScreenManagerException
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.recycleview import RecycleView

from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.properties import (StringProperty, ObjectProperty,
                            NumericProperty, BooleanProperty,
                            ListProperty)
from kivy.core.window import Window

# kivy garden
from kivy.garden.androidtabs import AndroidTabsBase
from kivy.garden.navigationdrawer import NavigationDrawer

#python
import os
from threading import Thread

# Mahart Studio Widget
from mahartstudios.widgets.buttons import IconButton, RetainButton, NormalButton
from mahartstudios.widgets.autocarousel import AutoCarousel

if platform == 'android':
    from mahartstudios.android.notification import fast_toast



class MyTab(BoxLayout, AndroidTabsBase):
    pass


class UniCycle(RecycleView):
    
    multiselect = BooleanProperty(False)
    selected_list = ListProperty([])

    def on_multiselect(self, *a):
        if self.multiselect:
            Window.bind(on_key_down=self.listen_for_key)
        else:
            Window.unbind(on_key_down=self.listen_for_key)
            for child in self.selected_list:
                child.selected=False
            self.selected_list=[]

    def listen_for_key(self, keyboard, keycode, text, *modifiers):
        if keycode == 27:
            self.multiselect=False
            return True

    def select_me(self, me):
        if me not in self.selected_list:
            self.selected_list.append(me)
        else:
            me.selected=False
            self.selected_list.remove(me)


class Material_btn(RetainButton):

    def on_retain_touch(self, *largs):
        mat_modal = MaterialOptions()
        mat_modal.open()
        mat_modal.material_data = self.material_data

    def on_touched(self, *largs):
        mat_modal = MaterialOptions()
        mat_modal.open()
        mat_modal.material_data = self.material_data


class Course_btn(RetainButton):

    selected = BooleanProperty(False)

    def on_touched(self, *largs):
        if self.parent.parent.multiselect:
            self.selected = True
            self.parent.parent.select_me(self)
        else:
            # do what you would normaly do
            screens.go_to_page('course_page')

    
    def on_retain_touch(self, *largs):
        ''' Add selection on touch down '''
        self.selected = True
        self.parent.parent.multiselect=True
        self.parent.parent.select_me(self)


class MaterialOptions(ModalView):
    
    download_manager = ObjectProperty()
    screen_name = StringProperty('', allow_none=True)
    pb_value = NumericProperty(20)

    def __init__(self, **kwargs):
        super(MaterialOptions, self).__init__(**kwargs)
        self.done = False
        self.status = 0
        self.download_manager = self.ids._manager_
        self.downloader_cls = None


    def ccc(self):
        Clock.schedule_once(self.download, 0)

    def download(self, dt):
        self.status += 1
        self.pb_value = int(self.status)
        if self.status < 100:
            Clock.schedule_once(self.download, 0.5)

    def download_file(self):
        from cloud_handler.cloud import Downloader

        filepath = 'Unicloud/downloads' + self.material_data['filename']
        google_id = self.material_data['google_id']

        self.downloader_cls = Downloader(google_id, filepath, self.ids.pb, self.downloading_done)
        self.downloader_cls.start()
        self.download_manager.current='downloading'

    def take_to_download_page(self):
        download_page = screens.get_screen('download_page')
        grid = download_page.ids.downloading_grid

        self.downloading_btn = DownloadingButton()
        self.downloading_btn.downloader_cls = self.downloading_cls

        # change the progress bar of the downloader cls
        self.downloader_cls.progress_bar = self.downloading_btn.ids.pb
        grid.add_widget(self.downloading_btn)

    def download_later(self, data):
        if unicloud_store.exists(data['name']):
            print('Toast: already saved')
            fast_toast('Already saved')
        else:
            unicloud_store.put(data['name'], data=data)
            page = screens.get_screen('download_page')
            grid = page.ids.download_later
            grid.data.append({'material_data': data})
            grid.refresh_from_data()

    @mainthread
    def downloading_done(self,filepath):
        print('Toast downloading done',filepath)
        fast_toast('{} donwloader'.format(filepath))
        if hasattr(self, 'downloading_btn'):
            download_page = screens.get_screen('download_page')
            grid = download_page.ids.downloading_grid
            grid.remove_widget(self.downloading_btn)



class DownloadingButton(NormalButton):
    downloader_cls = ObjectProperty()


class Manager(ScreenManager):

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        global screens 
        screens = self

        from .screens.home_page import HomePage
        self.home_page =  HomePage(name='home_page')
        self.add_widget(self.home_page)   # default first page
        
        # thread the import for speed
        Thread(target=self.thread_import).start()

        Clock.schedule_once(self.create_store)
        Clock.schedule_once(lambda dt: self.set_first_page())

    def make_screen_obj(self,dt):
        self.first_page = FirstPage(name='first_page')
        self.file_chooser = SelectFile(name = 'file_chooser')
        self.pdf_maker =  PdfMaker(name='pdf_maker')
        self.search_page = SearchPage(name= 'search_page')
        self.course_page = Course_Page(name='course_page')
        self.post_page = PostScreen(name='post_page')
        self.add_course_page = Add_Course(name='add_course_page')
        self.login_page = LoginPage(name='login_page')
        self.sign_in_page = SignInPage(name='sign_in_page')
        self.download_page = DownloadPage(name='download_page')
    
    # overiding
    def get_screen(self, name):
        try:
            return super(Manager, self).get_screen(name)
        except ScreenManagerException:
            self.go_to_page(name, go_to_screen=False)
            return super(Manager, self).get_screen(name)
            

    def go_to_page(self, name, go_to_screen=True):
        if hasattr(self, name):
            page = getattr(self, name)
            self.current = name
        else:
            try:
                # importer = __import__('Cloud.screens', fromlist='Cloud')
                Screen_obj = getattr(self.cloud_screens_module, name)
            except AttributeError:
                # importer = __import__('Cloud.pdfmaker', fromlist='Cloud')
                Screen_obj = getattr(self.pdfmaker_module, name)

            page = Screen_obj(name=name)
            setattr(self, name, page)
            self.add_widget(page)

            if go_to_screen:
                self.current = name


    def go_to_external_page(self, name):
        if hasattr(self, name):
            page = getattr(self, name)
            self.current = name
        else:
            # importer = __import__('student_tools')
            Screen_obj = getattr(self.student_tools_module, name)
            page = Screen_obj(name=name)
            setattr(self, name, page)
            self.add_widget(page)
            self.current = name

    def thread_import(self):
        self.student_tools_module = __import__('student_tools')
        self.cloud_screens_module = __import__('Cloud.screens', fromlist='Cloud')
        self.pdfmaker_module = __import__('Cloud.pdfmaker', fromlist='Cloud')

    def create_store(self, dt):
        global unicloud_store
        global user_data_dir

        app_cls = kivy.app.App.get_running_app()
        user_data_dir = app_cls.user_data_dir
        print(user_data_dir)

        unicloud_store = JsonStore(os.path.join(user_data_dir, 'unicloud_store.json'))
        if not unicloud_store.exists('user'):
            unicloud_store.put('user', first_time=True)


    def set_first_page(self):
        if unicloud_store.exists('user'):
            if unicloud_store.get('user')['first_time']:
                self.go_to_page('first_page')
            else:
                # self.current= 'pdf maker'
                pass

root = Builder.load_file('cloud.kv')
