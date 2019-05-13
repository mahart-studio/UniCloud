# my kivy side import

import kivy 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.garden.androidtabs import AndroidTabsBase
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.properties import StringProperty, ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.factory import Factory

#python side import
import time
from functools import partial
from io import open
import os, os.path

from mahartstudios.widgets.buttons import DropButton

student_store = JsonStore('student_store.json')
gp_store = JsonStore('gp_store.json')

# defualt password
global password
password = '0000'

if student_store.exists('password_on'):
    password_on = [student_store.get('password_on')]
else:
    password_on = [True]

Builder.load_file('student_tools.kv')



class MyTab1(BoxLayout, AndroidTabsBase):
    pass

class CalculatorPage(Screen):
    def __init__(self, **kwargs):
        super(CalculatorPage, self).__init__(**kwargs)
        manager = ScreenManager()
        self.add_widget(manager)
        manager.add_widget(CalculatorHome())
        manager.add_widget(Result_list())
        manager.add_widget(Result_view())
        manager.add_widget(GpCalculator())


class CalculatorHome(Screen):
    def __init__(self, **kwargs):
        super(CalculatorHome, self).__init__(**kwargs)

        self.result_btn = self.ids.result_btn
        self.password_pop = PasswordPop()    #password popup modalview
        self.password_pop.screen_guy = self
        self.result_btn.bind(on_release=self.password_dicide)

    def password_dicide(self,  value):
        print([password_on[0]])
        if password_on[0]:
            self.password_pop.open(self)
        else:
            self.manger.current =  'result_list_page'


class GpCalculator(Screen):
    
    def __init__(self, **kwargs):
        super(GpCalculator, self).__init__(**kwargs)

        self.grid_guy = self.ids.grid_guy
        self.calc_option = self.ids.calc_option

        self.course_num = 6
        self.Gp_values1=[]        

        #my drop down custom
        self.options = Factory.MyDropDown(auto_width=False, width='150dp')
        self.resest_btn = Button(text='Reset', size_hint=(1, None),
                                 height='50dp', background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))

        self.resest_btn.bind(on_release = lambda btn: self.reset_values())

        self.delete_btn = Button(text='Delete', size_hint=(1, None),
                                 height='50dp', background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))

        self.delete_btn.bind(on_release= lambda btn: self.delete_course())
        #add course to dropdown
        self.options.add_widget(self.resest_btn)
        self.options.add_widget(self.delete_btn)
        
        self.calc_option.bind(on_release=self.options.open)
        Clock.schedule_once(lambda dt: self.set_values())


    def set_values(self):
        self.grid_guy.clear_widgets()
        for i in range(5): #add 5 courses to the gridlayout
            self.course_text = 'Course {}'
            self.grid_guy.add_widget(Label(text=self.course_text.format(i+1), size_hint_y=None, height='38dp',
                                        color=(.1, .1, .1, 1)))
            
            self.grid_guy.add_widget(Factory.Spinner(text='2', values=('1', '2', '3', '4', '5')))

            self.grid_guy.add_widget(Factory.Spinner(text='B', values=('A', 'B', 'C', 'D', 'E', 'F')))


    def delete_course(self): # remove 3 widget from the grid
        self.grid_list = self.grid_guy.children

        for j in range(3):
            if len(self.grid_list) <= 3:
                self.course_num = 2
            else:
                self.grid_guy.remove_widget(self.grid_list[0])   
        if len(self.grid_list) != 3:
            self.course_num -= 1


    def reset_values(self):
        self.set_values()

    def add_btn(self):  #add a new button to the gridlayout
        self.course_text = 'Course {}'
        self.grid_guy.add_widget(Label(text=self.course_text.format(self.course_num), size_hint_y=None, height='38dp', color=(.1, .1,.1, 1)))

        self.grid_guy.add_widget(Factory.Spinner(text='2', values=('1', '2', '3', '4', '5')))

        self.grid_guy.add_widget(Factory.Spinner(text='B', values=('A', 'B', 'C', 'D', 'E', 'F')))
        
        self.course_num += 1


    def open_drop(self):
        self.options.open(self.calc_option)
        
    def calculate_gp(self, grades, units):
        grade_values = []
        cal_grade = []
        sum_of_unit = 0
        sum_of_grade = 0

        for i in grades:
            
            if i == 'E':
                grade_values.append('1')
            if i == 'D':
                grade_values.append('2')
            if i == 'C':
                grade_values.append('3')
            if i == 'B':
                grade_values.append('4')
            if i == 'A':
                grade_values.append('5')
            if i == 'F':
                grade_values.append('0') 
        
        for i in range(len(grade_values)):
            multi = int(units[i]) * int(grade_values[i])
            cal_grade.append(multi)
            print((units[i], grades[i]))
            
        for i in units:
            sum_of_unit += int(i)

        for i in cal_grade:
            sum_of_grade += i            

        gp = sum_of_grade/sum_of_unit
        gp = str(gp)

        return [gp, sum_of_unit]


    def get_values(self):
        list_value = self.grid_guy.children
        course_list = []
        grade_list = []
        unit_list = []
        
        j = 2 # get the course list
        for i in range((len(list_value)//3)):
            course = list_value[j]
            course = course.text
            course_list.append(course)
            j += 3
        courses = len(course_list)
        
        j = 1 #get the unit list
        for i in range((len(list_value)//3)):
            unit = list_value[j]
            unit = unit.text
            unit_list.append(unit)
            j += 3

        j = 0# get the grade list
        for grade in range((len(list_value)//3)):
            grade = list_value[j].text
            grade_list.append(grade)
            j += 3

        #then we send values to the calculator func
        gp, sum_of_unit = self.calculate_gp(grade_list, unit_list)
        print(gp)
        
        # if screens.previous() == 'result_view_page':
        #     pass

        course_values = [course_list, unit_list, grade_list]

        # then we store
        gp_store.put(time.ctime(), gp=gp, sum_of_unit=sum_of_unit, course_values=course_values)

        self.parent.current = 'result_view_page'
        self.parent.get_screen('result_view_page').set_values(gp, sum_of_unit, course_values)


class Result_view(Screen):
    def __init__(self, **kwargs):
        super(Result_view, self).__init__(**kwargs)        
        self.gp_view = self.ids.gp_view
        self.total_unit = self.ids.total_unit
        self.grid_lay = self.ids.grid_lay
        self.result_list_option = self.ids.result_list_option


    def set_values(self, gp, sum_of_unit, course_values):
        'function called when we get to set values for page'

        self.grid_lay.clear_widgets()

        for course, unit, grade in zip(course_values[0], course_values[1], course_values[2]):
            course_label = Label(text='ssg4', color=(.1, .1,.1, 1), size_hint_y=None, height=40)
      
            unit_spin = Factory.MySpinner(text='2', values=('1', '2', '3', '4', '5'))

            grade_spin = Factory.MySpinner(text='B', values=('A', 'B', 'C', 'D', 'E', 'F'))
        
            course_label.text = course
            unit_spin.text = unit
            grade_spin.text = grade 

            #then add to the gridlayout
            self.grid_lay.add_widget(course_label)
            self.grid_lay.add_widget(unit_spin)
            self.grid_lay.add_widget(grade_spin)

            self.gp_view.text = 'Grade Point: {}'.format(gp)
            self.total_unit.text = 'Sum of Unit: {}'.format(sum_of_unit)
            self.ids.num_of_course.text = 'Total Number Of Courses: {}'.format(str(len(course_values[0])))


class Result_list(Screen):
    def __init__(self, **kwargs):
        super(Result_list, self).__init__(**kwargs)
        self.result_scroll = self.ids.result_scroll
        self.result_scroll.bind(minimum_height=self.result_scroll.setter('height'))
        
    def on_enter(self):
        self.set_values()

    def set_values(self):
        self.result_scroll.clear_widgets()

        if len(gp_store.keys()) < 1:
            self.error_msg = Label(text='Sorry no Result were found', color=(.3,.3, .3, 1) )
            self.result_scroll.add_widget(self.error_msg)
            return

        for gp in gp_store.keys():
            result_btn = Result_Button()
            result_btn.time = '{}'.format(gp)
            result_btn.gp =  'Gp: {}   Sum of unit: {}'.format(gp_store.get(gp)['gp'], gp_store.get(gp)['sum_of_unit'])
            result_btn.gp_values = gp_store.get(gp)['course_values']
            self.result_scroll.add_widget(result_btn)
            result_btn.load=partial(self.load_data, result_btn.time)
            result_btn.delete=partial(self.delete_data, result_btn.time)

    def load_data(self, time):
        self.manager.current = 'result_view_page'
        gp = gp_store.get(time)['gp']
        sum_of_unit = gp_store.get(time)['sum_of_unit']
        course_values = gp_store.get(time)['course_values']
        self.manager.get_screen('result_view_page').set_values(gp, sum_of_unit, course_values)

    def delete_data(self, time):
        child = list(filter(lambda child: child.time == time, self.result_scroll.children))[0]
        self.result_scroll.remove_widget(child)
        gp_store.delete(child.time)


    def delete_all(self):
        pass

    def refresh_list(self):
        self.set_values()

    def on_result_press(self, pos):
        Gp_values2 = Gp_values_list[pos]
        self.manager.current = 'result_view_page'


class PasswordPop(ModalView):
    screen_guy = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PasswordPop, self).__init__(**kwargs)  
        self.password_state = self.ids.password_state
        self.pass_btn = self.ids.pass_btn
        self.password_value = self.ids.password_value

    def on_open(self):
        if password == '0000':  # set the text if the user hasnt change the default password
            self.password_value.text = '0000'

    def comfirm_pass(self):
        if self.password_value.text == password:
            self.dismiss()
            self.screen_guy.manager.current = 'result_list_page'

        else:
            self.password_value.text = ''
            self.password_state.color = (1, .2, .2, 1)
            self.password_state.text = 'Incorrect Password'


class Settings_password(Screen):
    def __init__(self, **kwargs):
        super(Settings_password, self).__init__(**kwargs)
        self.warning = self.ids.warning
        self.old_password = self.ids.old_password
        self.new_password = self.ids.new_password
        self.comfirm_pass = self.ids.comfirm_password
        self.password_switch = self.ids.password_switch
        

        if password == '0000': # set the text if the user hasnt change the default password
            self.old_password.text = '0000'
            

    def set_warning(self): #this func is being called on_text event 
        if self.new_password.text != self.comfirm_pass.text:
            if len(self.comfirm_pass.text) >= len(self.new_password.text):
                self.warning.text = "Password Does Not Macth"
        else:
            self.warning.text =  ''

    def  set_password(self):
        if self.old_password.text == password:
            password = self.new_password.text
            self.old_password.text = self.new_password.text
        else:
            pass
        print((self.password1))

    def on_leave(self):
        #turm password on/off
        if self.password_switch.active:
            password_on[0]  = True
        else:
            password_on[0] = False

        print((password_on[0]))       
            

class Settings(Screen):
    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)

    def go_back(self): #go back to previous page cause you might have being coming from any page
        previous = self.manager.previous()
        self.manager.current = previous


class Home_page(Screen):
    def __init__(self, **kwargs):
        super(Home_page, self).__init__(**kwargs)


class TimeTableButton(DropButton):
    pass


class Lecture_time_table(Screen):
    
    def display(self):
        days = ['Monday', 'Tuesday', 'Wenesday', 'Thusday', 'Friday']
        codes = ['GEG 101', 'Phy 111', 'SSG 201', 'EEG 301']
        times = ['8:00-10:00AM', '12:00-2:00PM', '2:00-4:00pPM', '4:00-6:00PM']
        venues = ['Elt', 'Room 201', 'Room 211', 'Room 101']

        for day in days:    
            drop_btn = TimeTableButton(day=day)

            for time, code, venue in zip(times, codes, venues):
                box = BoxLayout(size_hint_y=None, height='60dp')
                box.add_widget(Label(color=(0,0,0,1), text=time))
                box.add_widget(Label(color=(0,0,0,1), text=code))
                box.add_widget(Label(color=(0,0,0,1), text=venue))

                drop_btn.drop_container.add_widget(box)

            self.ids.grid.add_widget(drop_btn)

    def on_enter(self):
        self.ids.grid.clear_widgets()
        self.display()


class Exam_time_table(Screen):
    def __init__(self, **kwargs):
        super(Exam_time_table, self).__init__(**kwargs)        


class Box_guy(BoxLayout):
    pass

class Matrix_detector(Screen):  #detector side of app

    def __init__(self, **kwargs):
        super(Matrix_detector, self).__init__(**kwargs)

        file = open('data/unilag_courses.txt', 'r')

        self.courses = {}
        file_lines = file.readlines()
        temp = []
        temp_fal = ''
        first = True
        # print(file_lines)

        for line in file_lines:
            line = line.strip('\n')
            if line == '':
                pass
            else:
                if line[0] == '*':
                    if first:
                        temp_fal = line
                    else:
                        self.courses[temp_fal[1:]] = temp
                        temp = []
                        temp_fal = line
                    # print('-----------------------')
                    # print('FACULTY OF ', line[1:])
                    # print('-----------------------')
                    first = False
                else:
                    first = False
                    temp.append(line)
                    # print(line)

    def go_back(self): #go back to previous page cause you might have being coming from any page
        previous = self.manager.previous()
        manager.current = previous

    def get_year(self, matrix):
    
        self.year = matrix[0:2]
        self.current_year = time.ctime()

        self.year = int('20' + self.year)
        self.current_year = int(self.current_year[20:24])
    
        self.year_dif = self.current_year - self.year
    
        self.level = str(self.year_dif) + '00'
    
        self.year_of_entry = (str(self.year) + '/' + str(self.year + 1))
         
        return [self.level, self.year_of_entry]
    


    def get_falculty(self, matrix):
        
        self.list_falculty = list(self.courses)
        self.list_falculty.sort()
        print((self.list_falculty))

        if matrix[2] == '0':
            self.falc_no = int(matrix[3])-1
            self.falculty = self.list_falculty[self.falc_no]
        else:
            self.falc_no = int(matrix[2:4])-1
            self.falculty = self.list_falculty[self.falc_no]

        self.return_val = self.falculty

        return self.return_val


    def get_department(self, matrix):

        self.falculty = self.get_falculty(matrix)
        # self.falc_no = self.falculty[1]
        print((self.falculty))
        
        if matrix[4] == '0':
            self.dept_no = int(matrix[5])-1
            print((self.dept_no))
            print((self.courses[self.falculty]))
            self.department = self.courses[self.falculty][self.dept_no]
        else:
            self.dept_no =  int(matrix[4:6])
            self.department = self.courses[self.falculty][self.dept_no]


        return self.department


    def get_position(self, matrix):

        if matrix[7] == '0' and matrix[6] == '0':
            self.position = matrix[8]
        elif matrix[6] == '0':
            self.position = matrix[7:9]
        else:
            self.position = matrix[6:9]

        return self.position
    
    def set_info(self, matrix):
        self.box_guy = Box_guy()
        self.year_display = self.ids.year_display
        self.level_display = self.ids.level_display
        self.department_display = self.ids.department_display
        self.falculty_display = self.ids.falculty_display
        self.position_display = self.ids.position_display


        self.matrix = int(matrix)
        self.year_level = self.get_year(matrix)
        self.year = str(self.year_level[1])
        self.level = str(self.year_level[0])
        
        self.department = str(self.get_department(matrix))
        self.falculty = str(self.get_falculty(matrix))
        self.position = str(self.get_position(matrix))

        self.year_display.text = self.year
        self.level_display.text = self.level
        self.department_display.text = self.department
        self.falculty_display.text = self.falculty
        self.position_display.text = self.position

class Result_Button(DropButton):
    pass
