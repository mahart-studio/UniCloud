
import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.utils import get_color_from_hex
from kivy.garden.androidtabs import AndroidTabsBase
from kivy.uix.recycleview import RecycleView
from kivy.storage.jsonstore import JsonStore
from kivy.resources import resource_add_path
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

#python
from functools import  partial
import time
import os, os.path

# Mahart Studio Widget
from mahartstudios.widgets.buttons import IconButton, RetainButton, NormalButton
from mahartstudios.widgets.autocarousel import AutoCarousel
from .Pdfmaker.main import PdfMaker

# student tools screen
# from student_tools.tools import get_screens
# external_pages = get_screens()

class MyTab(BoxLayout, AndroidTabsBase):
    pass

class UniCycle(RecycleView):
    pass
    # def __init__(self, **kwargs):
    #     super(UniCycle, self).__init__(**kwargs)


class HomePage(Screen):

    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)

        self.all_course_scroll = self.ids.all_course_scroll
        self.your_course_scroll = self.ids.your_course_scroll
        self.download_scroll = self.ids.downloads_scroll

        self.load_data()


    def load_data(self,data=3):
        if data is not None:
            recycle_data =[]
            for course in range(100):
                course_code = 'ABS 101'
                course_title = 'Intro to Computer Science......'
                template = "[size=16dp][font=comic][color=#444444]{}[/color][/font][/size]\n" \
                        "[color=#666666][size=14dp]{}[/size][/color]"
        
                data = {}
                data['title']= course_title
                data['code'] =course_code
                data['code_with_title'] = template.format(course_code, course_title)

                recycle_data.append({'course_data':data})

                # self.all_course_scroll.add_widget(self.course)

            self.all_course_scroll.viewclass = Course_btn
            self.all_course_scroll.data = recycle_data

        elif data=='load':    #do this if data is loading 
            self.all_course_scroll.viewclass = Image
            self.all_course_scroll.data = [{'source': 'comments-loader.gif'}]
            Clock.schedule_once(lambda dt: self.load_data(data=4), 6)
        else:
            self.all_course_scroll = Label
            self.all_course_scroll.data = [{'text': 'No internet connection'}]
            


class Add_Course(Screen):
    selected_file =  StringProperty('')

    def __init__(self, **kwargs):
        super(Add_Course, self).__init__(**kwargs)


class PostScreen(Screen):

    def __init__(self, **kwargs):
        super(PostScreen, self).__init__(**kwargs)
        self.ids.form_scroll.bind(minimum_height=self.ids.form_scroll.setter('height'))


    def upload_file(self, filepath):
        if filepath is not None:
            from Cloud.cloud import Uploader
            upload_cls = Uploader(filepath)

            upload_thread = Thread(target=upload_cls.upload)
            upload_thread.start()
        else:
            print('toast no selected file')



class Course_Page(Screen):

    def __init__(self, **kwargs):
        super(Course_Page, self).__init__(**kwargs)
        self.test_scroll = self.ids.test_scroll
        self.ass_scroll = self.ids.ass_scroll
        self.course_mat_scroll = self.ids.course_mat_scroll
        self.class_scroll = self.ids.class_scroll


        self.test_scroll.bind(minimum_height=self.test_scroll.setter('height'))
        self.ass_scroll.bind(minimum_height=self.ass_scroll.setter('height'))
        self.course_mat_scroll.bind(minimum_height=self.course_mat_scroll.setter('height'))
        self.class_scroll.bind(minimum_height=self.class_scroll.setter('height'))

        self.dept_fal = self.ids.dept_fal

        #make a text markup template for department and falculty
        template = '[color=#ffffff][b]Department[/b]: {}[/color]\n[color=#ffffcc][b]Faculty[/b]:          {}[/color]'

        self.dept_fal.text = template.format('Computer Science', 'Sciences')

        recycle_data=[]

        for i in range(20):            
            material_data ={}
            material_data['name'] = '2012/2013 Past Question'
            material_data['user']= 'Posted By Avour'
            material_data['size'] = '4.6mb'
            material_data['google_id'] = '19_naVrwu6f1xgHfgB54qo_IL5eU_xk1_'
            material_data['filename'] = 'donwload_test.jpg'

            recycle_data.append({'material_data':material_data})

        self.ids.exam_scroll.data = recycle_data

    def on_enter(self):
        Window.bind(on_key_down=self.key_pressed)

    def on_leave(self):
        Window.unbind(on_key_down=self.key_pressed)

    def key_pressed(self, *largs, **kwargs):        
        if largs[1] ==27:
            print('the escape key was pressed')
            print('Now do shit')
            print(self.modal.stop_escape)
            if not self.modal.stop_escape:
                screens.go_to_page('home_page')


class Course_btn(RecycleDataViewBehavior, RetainButton):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def on_touched(self, *largs):
        if self.parent.multiselect:
            self.parent.select_node(self.index)            
            self.selected = True
        else:
            # do what you would normaly do
            screens.go_to_page ('course_page')

    
    def on_retain_touch(self, *largs):
        ''' Add selection on touch down '''
        if self.selectable:
            self.parent.select_node(self.index)
            self.selected = True
            self.parent.multiselect = True
            self.parent.touch_multiselect = True
        


class Material_btn(RetainButton):

    def on_retain_touch(self, *largs):
        print(largs)
        mat_modal = MaterialOptions()
        mat_modal.open()
        mat_modal.material_data = self.material_data

    def on_touched(self, *largs):
        print(largs)
        mat_modal = MaterialOptions()
        mat_modal.open()
        mat_modal.material_data = self.material_data



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
        download_page = screens.get_screen('download page')
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
        else:
            unicloud_store.put(data['name'], data=data)
            page = screens.get_screen('download page')
            grid = page.ids.download_later
            grid.data.append({'material_data': data})
            grid.refresh_from_data()
    
    def downloading_done(self,filepath):
        print('Toast downloading done',filepath)
        if hasattr(self, 'downloading_btn'):
            download_page = screens.get_screen('download page')
            grid = download_page.ids.downloading_grid
            grid.remove_widget(self.downloading_btn)


class LoginPage(Screen):
    pass

class SignInPage(Screen):
    pass

class DownloadPage(Screen):
    pass

class DownloadingButton(NormalButton):
    download_cls = ObjectProperty()

class SelectFile(Screen):
    pass

class SearchPage(Screen):
    pass

class FirstPage(Screen):
    pass


class Manager(ScreenManager):

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        global screens 
        screens = self

        self.home_page =  HomePage(name='home_page')
        self.add_widget(self.home_page)   # default first page

        Clock.schedule_once(self.make_screen_obj)

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

    def go_to_page(self, name):
        page = getattr(self, name)

        try:
            self.add_widget(page)
        except:
            pass

        self.current = name

    def go_to_external_page(self, name):
        page = list(filter(lambda page: page.name==name, external_pages))[0]
        try:
            self.add_widget(page)
        except:
            pass
        self.current = name

root = Builder.load_file('cloud.kv')


class Student_db_(App):
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


if __name__ == '__main__':
    Student_db_().run()
