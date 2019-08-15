from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from screenbase import ScreenBase

class DownloadPage(ScreenBase):
    def __init__(self, **kwargs):
        Builder.load_string(kv_string)

        super(DownloadPage, self).__init__(**kwargs)


kv_string = '''
<DownloadPage>:
    on_pre_enter: root.manager.parent.allow_touch_drag= True
    on_leave: android_tab.default_tab = 0
    on_back_button: app.root.toggle_state()
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        AndroidTabs:
            id: android_tab
            anim_threshold: 0
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos

            MyTab:
                text: 'Downloading'
                CustScroll:
                    size_hint: (1, 1)
                    size: self.size
                    GridLayout
                        id: downloading_grid
                        cols: 1
                        size_hint: (1, None)
                        height: self.minimum_height
                        # Label:
                        #     text: 'No Downloads'
                        #     color: (.4, .4, .4, 1)
                        #     size_hint_y: None
                        DownloadingButton:

            MyTab:
                text: 'Downloads'
                CustScroll:
                    size_hint: (1, 1)
                    size: self.size
                    GridLayout:
                        cols: 1
                        size_hint: (1, None)
                        height: self.minimum_height
                        # Label:
                        #     text: 'No Downloads'
                        #     color: (.4, .4, .4, 1)
                        #     size_hint_y: None
                        DownloadButton:
                        DownloadButton:
            MyTab:
                text: 'Download Later'
                UniCycle:
                    viewclass: 'Material_btn'
                    id: download_later
'''