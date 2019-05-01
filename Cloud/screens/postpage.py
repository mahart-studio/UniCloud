from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


class PostScreen(Screen):

    def __init__(self, **kwargs):
        Builder.load_string(kv_string)
        super(PostScreen, self).__init__(**kwargs)

    def upload_file(self, filepath):
        if filepath is not None:
            from Cloud.cloud import Uploader
            upload_cls = Uploader(filepath)

            upload_thread = Thread(target=upload_cls.upload)
            upload_thread.start()
        else:
            print('toast no selected file')
            fast_toast('NO file is selected')


kv_string = '''
<PostScreen>:
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    selected_file: None
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                size_hint_y: None
                height: '50dp'
    			shadow: Effects(self).add_shadow()
				IconButton:
					size_hint_x: None
					width: '64dp'
					background_color: 1,1,1,1
					icon_source: 'arrow_back.png'
                    on_release: root.manager.go_to_page('home_page')

                Label:
                    text: 'Post A Material'
                    color: get_color_from_hex('#FF9900')
                    font_size: '18dp'
                    bold: True
                    text_size: self.size
                    valign: 'middle'
                    halign: 'left'
                    padding: '20dp', 0
                NormalButton:
                    text: 'Done'
                    bold: True
                    size_hint_x: None
                    width: '100dp'
                    color: get_color_from_hex('#FF9966')
                    on_release: root.upload_file(root.selected_file)

            ScrollView:
                size_hint: (1, 1)
                size: self.size
                GridLayout:
                    spacing: 1
                    height: self.minimum_height
                    size_hint_y: None
                    cols: 1
                    FloatLayout:
                        size_hint: (1, None)
                        hieght: '60dp'
                        CustLabel1:
                            text: 'Choose A File'
                        IconButton:
                            size_hint: (None, None)
                            size: ('80dp', '40dp')
                            pos_hint: {'center_x': .75, 'center_y': .5}
                            icon_source: 'add1.png'
                            on_release: root.manager.go_to_page('file_chooser')

					Button:
                        background_color: (1,1,1,0) if self.state == 'normal' else (0,0,0,.2)
                        background_normal: ''
						size_hint_y: None
						height: '20dp'
                        BoxLayout:
                            size_hint: None,None
                            size: self.parent.size
                            pos: self.parent.pos
                            Label:
        						text: 'No file selected'
                				id: selected_file
                                color: .5,.5,.5,1
                            Label:
                                size_hint_x: None
                                width: '100dp'
                                id: selected_mb
                                color: .5,.5,.5,1
                                font_size: '13dp'

                    BoxLayout:
                        size_hint: (1, None)
                        hieght: '60dp'
                        padding: '6dp'
                        spacing: '6dp'
                        CustLabel1:
                            text: 'Name Of Material'
                        TextInput:
                            size_hint: (None, None)
                            size: ('200dp', '50dp')
                            pos_hint: {'center_y': .5, 'center_x': .5}
                            text: ''

                    FloatLayout:
                        size_hint: (1, None)
                        hieght: '60dp'
                        CustLabel1:
                            text: 'Course'
                        Spinner:
                            size_hint: (None, None)
                            size: ('120dp', '40dp')
                            pos_hint: {'center_x': .75, 'center_y': .5}
                            text: 'GEG 303'
                            values: 'GEG 303', 'PHY 123', 'GST 101'

                    FloatLayout:
                        size_hint_y: None
                        height: '10dp'
                        Label:
                            size_hint_x: .5
                            pos_hint: {'x': .1, 'y': 0}
                            text: 'If Course Not Found Add To Database'
                            color: (.5, .5, .5, 1)
                            halign: 'left'
                            font_size: '12dp'
                        Button:
                            size_hint: (None, None)
                            size: ('10dp', '10dp')
                            pos_hint: {'x': .75, 'y': 0}
                            size: ('10dp', '10dp')
                            text: '+'
                            background_color: (.7, .7, .7, 1)
                            on_release: root.manager.go_to_page('add_course_page')

                    FloatLayout:
                        size_hint: (1, None)
                        hieght: '60dp'
                        CustLabel1:
                            text: 'Material Type'
                        Spinner:
                            size_hint: (None, None)
                            size: ('120dp', '40dp')
                            pos_hint: {'center_x': .75, 'center_y': .5}
                            text: 'Exam Question'
                            values: 'Exam Question', 'Lecture Note', 'Test', 'Assignment', 'Class Material'


                    FloatLayout:
                        size_hint: (1, None)
                        hieght: '60dp'
                        CustLabel1:
                            text: 'Year'
                        Spinner:
                            size_hint: (None, None)
                            size: ('120dp', '40dp')
                            pos_hint: {'center_x': .75, 'center_y': .5}
                            text: '2018/2019'
                            values: ('2018/2019', '2017/2018', '2016/2017')
'''