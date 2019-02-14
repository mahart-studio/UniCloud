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
            hint_text: 'example@gmail.com'
        SignLabel:
            text: 'Username:'
        CustomInput:
            size_hint_y: None
            height: '50dp'
            hint_text: 'john123'
        SignLabel:
            text: 'Password:'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            CustomInput:
                hint_text: 'password'
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
        IconButton:
            size_hint_y: None
            height: '50dp'
            icon_source: 'sign_button.png'
            on_release: root.parent.go_to_page('login_page')
            normal_color: get_color_from_hex('#ff9966')
        Label:
            text: '[u][color=3088ff][ref=later]Later[/ref][/color][/u]'
            markup: True
            color: .2,.5,1,1
            on_ref_press: root.parent.go_to_page('home_page')

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
            hint_text: 'john123'
        SignLabel:
            text: 'Password:'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            CustomInput:
                hint_text: 'password'
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
            text: "Don't have an account?  [u][ref=signin][color=#ff3000]Sign in[/color][/ref][/u]"
            on_ref_press: root.parent.go_to_page('sign_in_page')
        Label:
            text: '[u][ref=later]Later[/ref][/u]'
            markup: True
            color: .2,.5,1,1
            on_ref_press: root.parent.go_to_page('home_page')
'''
firstpage_kv = '''
<FirstPage>:
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    Carousel:
        id: caro
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
                color: 1,1,1,1
                font_name: 'comicbd'
            FloatLayout:
                MyCarousel
                    AsyncImage:
                        source: 'data/showcase/Screenshot(1).png'
                    AsyncImage:
                        source: 'data/showcase/Screenshot(2).png'
                    AsyncImage:
                        source: 'data/showcase/Screenshot(7).png'
            FloatLayout:
                size_hint_y: None
                height: '60dp'
                MyCarouselButton
                    text: 'next'
                    on_release: caro.load_next()
            Image:
                source: 'first2.png'
                size_hint_y: None
                height: '60dp'
        BoxLayout:
            orientation: 'vertical'
            Label:
                size_hint_y: None
                height: '60dp'
                text: 'Create fast pdf'
                color: 1,1,1,1
                font_name: 'comicbd'
            FloatLayout:
                center: root.center
                MyCarousel
                    AsyncImage:
                        source: 'data/showcase/Screenshot(4).png'
                    AsyncImage:
                        source: 'data/showcase/Screenshot(5).png'
            FloatLayout:
                size_hint_y: None
                height: '60dp'
                MyCarouselButton
                    text: 'next'
                    on_release: caro.load_next()
            Image:
                source: 'first1.png'
                size_hint_y: None
                height: '60dp'
        BoxLayout:
            orientation: 'vertical'
            Label:
                size_hint_y: None
                height: '60dp'
                text: 'Other tools'
                color: 1,1,1,1
                font_name: 'comicbd'
            FloatLayout:
                MyCarousel
                    AsyncImage:
                        source: 'data/showcase/Screenshot(3).png'
                    AsyncImage:
                        source: 'data/showcase/Screenshot(6).png'
                    AsyncImage:
                        source: 'data/showcase/Screenshot(8).png'
            FloatLayout:
                size_hint_y: None
                height: '60dp'
                MyCarouselButton
                    text: 'sign in'
                    on_release: root.manager.go_to_page('sign_in_page')
            Image:
                source: 'first3.png'
                size_hint_y: None
                height: '60dp'

<MyCarouselButton@NormalButton>:
    size_hint: None,None
    size: '120dp', '48dp'
    center: self.parent.center
    normal_color: .9,.5,0,1
    color: 1,1,1,1

<MyCarousel@AutoCarousel>:
    center: self.parent.center
    size_hint: None, None
    size: '180dp', '300dp'
    canvas.after:
        Color:
            rgba: 1,1,1,1
        Line:
            rectangle: [self.x, self.y, self.width, self.height]
            width: 1.5
'''
