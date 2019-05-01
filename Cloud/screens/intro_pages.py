from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


class LoginPage(Screen):
    def __init__(self, **kwargs):
        Builder.load_string(login_kv)
        super(LoginPage, self).__init__(**kwargs)

class SignInPage(Screen):
    def __init__(self, **kwargs):
        Builder.load_string(signin_kv)
        super(SignInPage, self).__init__(**kwargs)

class FirstPage(Screen):
    def __init__(self, **kwargs):
        Builder.load_string(firstpage_kv)
        super(FirstPage, self).__init__(**kwargs)



signin_kv = '''
<SignInPage>:
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#FF9966')
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint_y: None
            height: '80dp'
            Image:
                source: 'ic_action_cloudy.png'
                size_hint_x: None
                width: '80dp'
            Label:
                color: 1,1,1,1
                font_size: '18dp'
                bold: True
                text_size: self.size
                valign: 'middle'
                halign: 'left'
                padding: '30dp', 0
                text: 'Sign In'
        Image:
            source: 'line.png'
            size_hint_y: None
            height: '30dp'
        SignLabel:
            text: 'Email:'
        CustomInput:
            size_hint_y: None
            height: '50dp'
            hint_text: 'example@email.comm'
            text: 'Email'
        SignLabel:
            text: 'Username:'
        CustomInput:
            size_hint_y: None
            height: '50dp'
            hint_text: 'Username'
            text: 'Username'
        SignLabel:
            text: 'Password:'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            CustomInput:
                hint_text: 'password'
                text: 'Password'
                password: True
                id: password
            IconToggle:
                size_hint_x: None
                width: '50dp'
                down_source: 'eye.png'
                normal_source: 'eye_closed.png'
                pos_hint: {'center_x':.5, 'center_y':.5}
                on_state:
                    if self.state == 'down': password.password=False
                    else: password.password=True
        SignLabel:
            text: 'Re entert Password'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            CustomInput:
                hint_text: 'password'
                text: 'Password'
                password: True
                id: re_enter
            IconToggle:
                size_hint_x: None
                width: '50dp'
                down_source: 'eye.png'
                normal_source: 'eye_closed.png'
                pos_hint: {'center_x':.5, 'center_y':.5}
                on_state:
                    if self.state == 'down': re_enter.password=False
                    else: re_enter.password=True
        Label:
            text: '[color=#ff0000]Warning[/color]'
            markup: True
            id: warnig
        IconButton:
            size_hint_y: None
            height: '50dp'
            icon_source: 'sign_button.png'
            on_release: root.parent.go_to_page('login_page')
            normal_color: get_color_from_hex('#ff9966')
'''

login_kv = '''
<LoginPage>:
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#FF9966')
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint_y: None
            height: '80dp'
            Image:
                source: 'ic_action_cloudy.png'
                size_hint_x: None
                width: '80dp'
            Label:
                color: 1,1,1,1
                font_size: '18dp'
                bold: True
                text_size: self.size
                valign: 'middle'
                halign: 'left'
                padding: '30dp', 0
                text: 'Login'
        Image:
            source: 'line.png'
            size_hint_y: None
            height: '20dp'
        Label:
        SignLabel:
            text: 'Username:'
        CustomInput:
            size_hint_y: None
            height: '50dp'
            hint_text: 'Username'
            text: 'Username'
        SignLabel:
            text: 'Password:'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            CustomInput:
                hint_text: 'password'
                text: 'Password'
                password: True
                id: password
            IconToggle:
                size_hint_x: None
                width: '50dp'
                down_source: 'eye.png'
                normal_source: 'eye_closed.png'
                pos_hint: {'center_x':.5, 'center_y':.5}
                on_state:
                    if self.state == 'down': password.password=False
                    else: password.password=True
        Label:
        IconButton:
            size_hint_y: None
            height: '50dp'
            icon_source: 'login_button.png'
            normal_color: get_color_from_hex('#ff9966')
        Label:
        Label:
            size_hint_y: None
            height: self.texture_size[1]+8
            normal_color: get_color_from_hex('#FF9966')
            text: '[ref=forgot][color=#ff0000]forgot password[/color][/ref]'
            markup: True
            on_ref_press:
        Label:
            size_hint_y: None
            height: self.texture_size[1] +10
            markup: True
            text: "Don't you have an account  [ref=signin][color=#ff0000]Sign in[/color][/ref]"
            on_ref_press: root.parent.go_to_page('sign_in_page')
'''
firstpage_kv = '''
<FirstPage>:
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    Carousel:
        canvas.before:
            Color:
                rgba: get_color_from_hex('#ff9966')
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            orientation: 'vertical'
            Label:
                size_hint_y: None
                height: '60dp'
                text: 'Upload and store material on the cloud'
                color: get_color_from_hex('#ff6600')
            AutoCarousel:
                AsyncImage:
                AsyncImage:
                AsyncImage:
            Image:
                source: 'first2.png'
                size_hint_y: None
                height: '60dp'
        BoxLayout:
            orientation: 'vertical'
            Label:
                size_hint_y: None
                height: '60dp'
                text: 'Upload and store material on the cloud'
                color: get_color_from_hex('#ff6600')
            AutoCarousel:
                AsyncImage:
                AsyncImage:
                AsyncImage:
            Image:
                source: 'first1.png'
                size_hint_y: None
                height: '60dp'
        BoxLayout:
            orientation: 'vertical'
            Label:
                size_hint_y: None
                height: '60dp'
                text: 'Upload and store material on the cloud'
                color: get_color_from_hex('#ff6600')
            AutoCarousel:
                AsyncImage:
                AsyncImage:
                AsyncImage:
            Image:
                source: 'first3.png'
                size_hint_y: None
                height: '60dp'
'''
