from screenbase import ScreenBase
from kivy.lang import Builder

class Course_Page(ScreenBase):

    def __init__(self, **kwargs):
        Builder.load_string(kv_string)
        
        super(Course_Page, self).__init__(**kwargs)
        self.dept_fal = self.ids.dept_fal

        #make a text markup template for department and falculty
        template = '[color=#ffffff][b]Department[/b]: {}[/color]\n[color=#ffffcc][b]Faculty[/b]:          {}[/color]'
        self.dept_fal.text = template.format('Computer Science', 'Sciences')

        self.ids.course_code.text = "[size=20dp][color=#ffffff][b]ABS 101[/b][/size]\n[size=15dp]\
                                    [color=#99330088]Intro to Computer Science[/color][/size][/color]"

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


kv_string = '''
<Course_Page>:
    on_back_button: self.manager.go_to_page('home_page')
    on_pre_enter: root.manager.parent.allow_touch_drag= False
    FloatLayout:
        canvas.before:
            Color:
                rgba: get_color_from_hex('#FF9966')
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                size_hint: (1, None)
                height: '80dp'
                IconButton:
                    icon_source: 'arrow_back1.png'
                    pos_hint: {'top': .9}
                    size_hint: (None, 1)
                    width: '40dp'
                    on_release: root.manager.go_to_page('home_page')
                    normal_color: get_color_from_hex('#ff9966')
                Label:
                    id: course_code
                    markup: True
                    text_size: self.size
                    valign: 'middle'
                    halign: 'left'
                IconButton:
                    normal_color: get_color_from_hex('#ff9966')
                    pos_hint: {'top': .9}
                    size_hint: (None, None)
                    size: '40dp', '32dp'
                    icon_source: 'search.png'
                IconButton:
                    normal_color: get_color_from_hex('#ff9966')
                    pos_hint: {'top': .9}
                    size_hint: (None, None)
                    size: '40dp', '32dp'
                    icon_source: 'ic_action_overflow.png'

            FloatLayout:
                size_hint: (1, None)
                height: 40
                Label:
                    size_hint_x: None
                    width: self.parent.width
                    id: dept_fal
                    markup: True
                    font_size: '13dp'
                    text_size: self.size
                    valign: 'middle'
                    halign: 'left'
                    x: '40dp'
                    y: self.parent.y

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
                    text: 'Exam'
                    UniCycle:
                        viewclass: 'Material_btn'
                        id: exam_scroll
                MyTab:
                    text: 'Test'
                    CustScroll:
                        size_hint: (1, 1)
                        size: self.size
                        GridLayout:
                            id: test_scroll
                            cols: 1
                            size_hint: (1, None)
                            height: self.minimum_height
                            Label:
                                text: 'No Material Available'
                                color: (.4, .4, .4, 1)
                MyTab:
                    text: 'Course Material'
                    CustScroll:
                        size_hint: (1, 1)
                        size: self.size
                        GridLayout:
                            id: course_mat_scroll
                            height: self.minimum_height
                            cols: 1
                            size_hint: (1, None)
                            Label:
                                text: 'No Material Available'
                                color: (.4, .4, .4, 1)
                MyTab:
                    text: 'Assignment'
                    CustScroll:
                        size_hint: (1, 1)
                        size: self.size
                        GridLayout:
                            id: ass_scroll
                            cols: 1
                            size_hint: (1, None)
                            height: self.minimum_height
                            Label:
                                text: 'No Material Available'
                                color: (.4, .4, .4, 1)
                MyTab:
                    text: 'Class Note'
                    CustScroll:
                        size_hint: (1, 1)
                        size: self.size
                        GridLayout:
                            id: class_scroll
                            cols: 1
                            size_hint: (1, None)
                            height: self.minimum_height
                            Label:
                                text: 'No Material Available'
                                color: (.4, .4, .4, 1)


        CircleBtn:
            background_color: 0, 0, 0, 0
            size_hint: (None, None)
            size: ('40dp', '40dp')
            pos_hint: {'x': .8,  'y': .05}
            source: 'float.png'
            color: (1, 1, 1, 1)
            on_release: root.manager.go_to_page('add_course_page')
'''