from kivy.lang import Builder

from mahartstudios.widgets.buttons import RetainButton

from screenbase import ScreenBase

class HomePage(ScreenBase):

    def __init__(self, **kwargs):
        Builder.load_string(kv_string)

        super(HomePage, self).__init__(**kwargs)

        self.all_course_scroll = self.ids.all_course_scroll
        self.your_course_scroll = self.ids.your_course_scroll
        self.download_scroll = self.ids.downloads_scroll

        self.load_data()


    def load_data(self,data=3):
        if data is not None:
            recycle_data =[]
            for course in range(10):
                course_code = 'ABS 101'
                course_title = 'Intro to Computer Science......'
                template = "[size=16dp][color=#444444]{}[/color][/size]\n" \
                        "[color=#666666][size=14dp]{}[/size][/color]"
        
                data = {}
                data['title']= course_title
                data['code'] =course_code
                data['code_with_title'] = template.format(course_code, course_title)

                recycle_data.append({'course_data':data})

            self.all_course_scroll.data = recycle_data

        elif data=='load':    #do this if data is loading 
            self.all_course_scroll.viewclass = Image
            self.all_course_scroll.data = [{'source': 'comments-loader.gif'}]
            Clock.schedule_once(lambda dt: self.load_data(data=4), 6)
        else:
            self.all_course_scroll = Label
            self.all_course_scroll.data = [{'text': 'No internet connection'}]




kv_string = '''
#: import Factory kivy.factory.Factory 
<HomePage>:
    on_enter:
        try: root.manager.parent.allow_touch_drag= True
        except Exception: pass
    on_back_button: app.stop()
    FloatLayout:
        BoxLayout:
            id: my_parent
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#FF9966')
                Rectangle:
                    pos: self.pos
                    size: self.size
        #Actiion Bar
            BoxLayout:
                size_hint: (1, None)
                height: '50dp'

                IconButton:
                    normal_color: get_color_from_hex('#ff9966')
                    size_hint_x: None
                    width: '50dp'
                    icon_source: 'menu.png'
                    on_release: root.manager.parent.parent.toggle_state()
                Image:
                    source: 'ic_action_cloudy.png'
                    size: '32dp', '32dp'
                    size_hint_x: None
                Label:
                    text: '[b]UniCloud[/b]'
                    font_size: '22dp'
                    text_size: self.size
                    color: 1,1,1,1
                    markup: True
                IconButton:
                    normal_color: get_color_from_hex('#ff9966')
                    icon_source: 'search.png'
                    size_hint: None, 1
                    size: '40dp', '32dp'
                    on_release: root.manager.go_to_page('search_page')
            Label:
                size_hint_y: None
                height: '10dp'

            AndroidTabs:
                canvas.before:
                    Color:
                        rgba: 1,1,1,1
                    Rectangle:
                        size: self.size
                        pos: self.pos
                MyIconTab:
                    text: 'All Course'
                    image_active: 'All Course.png'
                    image_normal: 'All Course1.png'
                    UniCycle:
                        viewclass: 'Course_btn'
                        id: all_course_scroll
                        # text_effect: FloatScrollEffect(self, 60, color=get_color_from_hex('#ff6600'))
                        viewclass: Factory.Course_btn

                MyIconTab:
                    text: 'Your Courses'
                    image_normal: 'Your Course1.png'
                    image_active: 'Your Course.png'
                    UniCycle:
                        viewclass: 'Course_btn'
                        id: your_course_scroll
                        data: [{'text':'No courses Selected Yet','color': (.7, .7, .7, 1)}]
                        
                MyIconTab:
                    text: 'Uploads'
                    image_active: 'uploads1.png'
                    image_normal: 'uploads.png'
                    BoxLayout:
                        orientation: 'vertical'
                        CustScroll:
                            size_hint: (1, 1)
                            size: self.size
                            GridLayout:
                                id: downloads_scroll
                                height: self.minimum_height
                                cols: 1
                                size_hint: (1, None)

                MyIconTab:
                    text: 'Accounts'
                    image_active: 'Accounts.png'
                    image_normal: 'Accounts1.png'

        CircleBtn:
            background_color: 0, 0, 0, 0
            size_hint: (None, None)
            size: ('40dp', '40dp')
            pos_hint: {'x': .8,  'y': .05}
            source: 'float.png'
            color: (1, 1, 1, 1)
            on_release: root.manager.go_to_page("post_page")
'''
