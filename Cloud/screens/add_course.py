from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder

class Add_Course(Screen):
    selected_file =  StringProperty('')

    def __init__(self, **kwargs):
        Builder.load_string(kv_string)
        
        super(Add_Course, self).__init__(**kwargs)


kv_string = '''
<Add_Course>:
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    FloatLayout:
        id: my_parent
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                size_hint_y: None
                height: '50dp'
				IconButton:
					size_hint_x: None
					width: '64dp'
					background_color: 1,1,1,1
					icon_source: 'arrow_back.png'
                    on_release: root.manager.go_to_page('post_page')


                Label:
                    text: 'Add Course'
                    color: get_color_from_hex('#FF9900')
                    font_size: '18dp'
                    bold: True
                    text_size: self.size
                    valign: 'middle'
                    halign: 'left'
                    padding: '20dp', 0
                Button:
                    text: 'Add'
                    bold: True
                    size_hint_x: None
                    width: '100dp'
                    color: get_color_from_hex('#FF9966')
                    background_color: 1,1,1,1
                    background_normal: ''
                    background_down: ''
                    background_color: (1,1,1,0) if self.state == 'normal' else (0,0,0,.2)

            FloatLayout:
                size_hint: (1, 1)
                CustLabel1:
                    text: 'Course Code'
                TextInput:
                    size_hint: (None, None)
                    size: ('150dp', '50dp')
                    pos_hint: {'center_x': .75, 'center_y': .5}
                    text: 'GEG 303'
                    multiline: False

            FloatLayout:
                size_hint: (1, 1)
                CustLabel1:
                    text: 'Course Title'
                TextInput:
                    size_hint: (None, None)
                    size: ('200dp', '50dp')
                    pos_hint: {'center_x': .75, 'center_y': .5}
                    text: 'Intro To Engineering Statistics'
                    multiline: False

            FloatLayout:
                size_hint: (1, 1)
                CustLabel1:
                    text: 'Department'
                Spinner:
                    size_hint: (None, None)
                    size: ('180dp', '40dp')
                    pos_hint: {'center_x': .75, 'center_y': .5}
                    text: 'Mechanical Engineering'
                    values: ('Mechanical Engineering', 'Chemical', 'Systems')

            FloatLayout:
                size_hint: (1, 1)
                CustLabel1:
                    text: 'Falculty'
                Spinner:
                    size_hint: (None, None)
                    size: ('180dp', '40dp')
                    pos_hint: {'center_x': .75, 'center_y': .5}
                    text: 'Engineering'
                    values: ('Medicine', 'Law')
'''