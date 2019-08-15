from screenbase import ScreenBase
import os
from kivy.lang import Builder

class ThumbChooser(ScreenBase):

    def __init__(self, **kwargs):
        Builder.load_string(kv_string)
        super(ThumbChooser, self).__init__(**kwargs)

    def on_back_button(self):
        previous_dir = os.path.dirname(self.file_chooser.path)
        if os.path.exists(previous_dir):
            self.file_chooser.path =previous_dir


kv_string='''
<ThumbChooser>:
    name: 'file'
    file_chooser: file_chooser
    FloatLayout:
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                size_hint_y: None
                height: '50dp'
                canvas.before:
                    Color:
                        rgba: 1,1,1,1
                    Rectangle:
                        size: self.size
                        pos: self.pos

                IconButton:
                    shape: 'rectangle'
                    normal_color: 1,1,1,1
                    icon_source: atlas_path+'arrow_back'
                    size_hint_x: None
                    width: '50dp'
                    on_release: root.manager.current = 'home'

                Label:
                    rgba: get_color_from_hex('#FF9966')
                    text: 'Select Images'
                    text_size: self.size
                    padding: '8dp', '8dp'
                    halign: 'left'
                    valign: 'center'
                    font_size: '20dp'

                Label:
                    id: count
                    text: '0'
                    size_hint_x: None
                    width: '100dp'
                    rgba: get_color_from_hex('#FF9966')

            FileChooserThumbView:
                id: file_chooser
                filters: ['*.png', '*.jpg', '*.jpeg', '*.gif']
                multiselect: True
                on_selection: count.text = str(len(self.selection))
                progress_cls: 'MyFileProgressCls'
                canvas.before:
                    Color:
                        rgba: .95,.95,.95,1
                    Rectangle:
                        size: self.size
                        pos: self.pos

    CircleBtn:
        background_color: 0, 0, 0, 0
        size_hint: (None, None)
        size: ('40dp', '40dp')
        pos_hint: {'x': .8,  'y': .05}
        source: 'float.png'
        color: (1, 1, 1, 1)
        on_release: root.manager.add_more(file_chooser.selection)
'''