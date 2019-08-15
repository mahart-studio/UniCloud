from screenbase import ScreenBase

from kivy.lang import Builder

class SearchPage(ScreenBase):

    def __init__(self, **kwargs):
        Builder.load_string(kv_string)
        super(SearchPage, self).__init__(**kwargs)


kv_string = '''
<SearchPage>:
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    # on_enter: search_input.focus = True
    on_back_button: self.manager.go_to_page('home_page')
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 1,1,1,1
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            canvas.before:
                Color:
                    rgba: get_color_from_hex('#FF9966')
                Rectangle:
                    size: self.size
                    pos: self.pos
            IconButton:
                icon_source: 'arrow_back1.png'
                size_hint_x: None
                width: '50dp'
                on_release: root.manager.go_to_page('home_page')
                normal_color: get_color_from_hex('#ff9966')

            CustomInput:
                id: search_input
                background_active: ''
                background_normal: ''
                background_color: get_color_from_hex('#FF9966')
                hint_text: 'Search'
                multiline: False
                foreground_color: .3,.3,.3,1
                padding: '20dp','18dp'

            IconButton:
                icon_source: 'search.png'
                size_hint_x: None
                width: '50dp'
                normal_color: get_color_from_hex('#ff9966')


        AndroidTabs:
            anim_threshold: 0
            default_tab: 2
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos

            MyTab:
                text: 'Courses'
                CustScroll:
                    size_hint: (1, 1)
                    size: self.size
                    GridLayout:
                        id: course_scroll
                        cols: 1
                        size_hint: (1, None)
                        Label:
                            text: 'Search for course'
                            color: (.4, .4, .4, 1)
            MyTab:
                text: 'Materials'
                CustScroll:
                    size_hint: (1, 1)
                    size: self.size
                    GridLayout
                        id: material_scroll
                        cols: 1
                        size_hint: (1, None)
                        Label:
                            text: 'Search for Materials'
                            color: (.4, .4, .4, 1)
'''