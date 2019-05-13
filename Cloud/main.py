
import kivy
from kivy import platform

# kivy widgets
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.recycleview import RecycleView

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty

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
    pass


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

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def on_touched(self, *largs):
        if self.parent.multiselect:
            self.parent.select_node(self.index)            
            self.selected = True
        else:
            # do what you would normaly do
            screens.go_to_page('course_page')

    
    def on_retain_touch(self, *largs):
        ''' Add selection on touch down '''
        if self.selectable:
            self.parent.select_node(self.index)
            self.selected = True
            self.parent.multiselect = True
            self.parent.touch_multiselect = True


class MaterialOptions(ModalView):
    
    download_manager = ObjectProperty()
    screen_name = StringProperty('', allow_none=True)
    pb_value = NumericProperty(20)

    def __init__(self, **kwargs):
        super(MaterialOptions, self).__init__(**kwargs)
        self.done = False
        self.status = 0
        self.download_manager = self.ids._manager_
        self.download_cls = None


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

        self.download_cls = Downloader(google_id, filepath, self.ids.pb, self.ids._manager_, self.downloading_done)
        self.download_cls.start()

    def take_to_download_page(self):
        download_page = screens.get_screen('download_page')
        grid = download_page.ids.downloading_grid

        self.downloading_btn = DownloadingButton()
        self.downloading_btn.download_cls = self.downloading_cls

    #    pause download and start with another progress bar
        self.download_cls.pause()
        self.download_cls.progress_bar = self.downloading_btn.ids.pb
        self.download_cls.countinue()

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
    
    def downloading_done(self,filepath):
        print('Toast downloading done',filepath)
        fast_toast('downloading done')
        if hasattr(self, 'downloading_btn'):
            download_page = screens.get_screen('download_page')
            grid = download_page.ids.downloading_grid
            grid.remove_widget(self.downloading_btn)



class DownloadingButton(NormalButton):
    download_cls = ObjectProperty()


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

    def go_to_page(self, name):
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
                Clock.schedule_once(lambda dt: setattr(self, 'current', 'home_page'), 6)
            else:
                # self.current= 'pdf maker'
                pass


root = Builder.load_file('cloud.kv')


class Student_db_():
    def build(self):
        self.title = 'UniCloud'
        return 

    def on_stop(self):
        unicloud_store.put('user', first_time=False)
        def delete_pic(arg, dir, files):
            for file in files:
                full_path = os.path.join(dir, file)
                if os.path.isfile(full_path):
                    os.remove(full_path)

        os.path.walk (os.path.join(self.user_data_dir, '.UniCloud'), delete_pic, 0)