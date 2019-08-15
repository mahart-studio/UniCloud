from kivy.lang import Builder
from kivy.properties import ObjectProperty

from screenbase import ScreenBase
import os

class SelectFile(ScreenBase):
    file_chooser = ObjectProperty(None)

    def __init__(self, **kwargs):
        Builder.load_string(kv_string)
        super(SelectFile, self).__init__(**kwargs)

    def on_back_button(self):
        previous_dir = os.path.dirname(self.file_chooser.path)
        if os.path.exists(previous_dir):
            self.file_chooser.path =previous_dir


kv_string = '''
<SelectFile>:
    file_chooser: file_chooser
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    canvas.before:
        Color:
            rgba: .9,.9,.9,1
        Rectangle:
            size: self.size
            pos: self.pos
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            IconButton:
                normal_color: .9,.9,.9,1
                icon_source: 'arrow_back.png'
                size_hint_x: None
                width: '50dp'
                on_release: root.manager.go_to_page('post_page')

            Label:
                color: get_color_from_hex('#FF9900')
                text: 'Select File'
                text_size: self.size
                padding: '40dp', '40dp'
                halign: 'left'
                valign: 'center'
                font_size: '22dp'
                markup: True

            NormalButton:
                text: 'Select'
                bold: True
                size_hint_x: None
                width: '100dp'
                color: get_color_from_hex('#FF9900')
                background_color: .9,.9,.9,1
                post_page: None
                on_release:
                    root.manager.go_to_page('post_page');
                    self.post_page =root.manager.get_screen('post_page')
                    self.post_page.ids.selected_file.text = os.path.split(file_chooser.selection[0])[1]
                    self.post_page.ids.selected_mb.text = str(file_chooser.get_nice_size(file_chooser.selection[0]));
                    self.post_page.selected_file=file_chooser.selection[0]

        FileChooserListView:
            progress_cls: 'MyFileProgressCls'
            id: file_chooser
            on_submit:
                root.manager.get_screen('post_page').ids.selected_file.text = os.path.split(self.selection[0])[1];
                root.manager.go_to_page('post_page');
                root.manager.get_screen('post_page').ids.selected_mb.text = str(self.get_nice_size(self.selection[0]));
                root.manager.get_screen('post_page').selected_file=self.selection[0]

'''
