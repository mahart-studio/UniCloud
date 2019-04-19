from kivy.gesture import Gesture, GestureDatabase
from kivy.uix.floatlayout import FloatLayout
from kivy.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.effects.scroll import ScrollEffect

gesture_string = '''eNqlWNtSHDcQfZ8fMS+h+t7qH8CvqfIHpLC9hSk7sAXrJP779Eja2Zkw400y8LBwODqS+nSrJW4evz7+8eP24fB6+v5yGN73zyMMN5+POHx493T/++HdcKT8MT94eP3w7vX08vz18Jq/ynDz7ajDzarIh0objjZKeY4/Pj8+ncZhZRwWG8N+HVnDEdsKxiX8yCFIwx3cqlKgKygwYMG6mr/Gv/Jw9wvcgngpzsQhbEZAw+vH+5/PInUWHR76BDnIRIQLqAXa8Prw/7XrxtHP2uJIRYpiWAk115k4h5OAFmNXDi3XxUsVj0mccyx6gOfqzefSakJCGkVyC4xXpalGnnCSJmJQMkAmopzyok0unlECS2HV4nJdnKo4n8W5hGmKllx5Rpfm4pxRUSpA6XoG77p2NZMmM9kQSsoCszHwPCiImDtiALP8Ef6Fm1TdpMnN1NSAyHBn1PPnLp7agBBEGZJgcHLw69rVTJrMzCS3HJxLZCHLzc/Eg1SVGSMwlPR6xLnayZOdtExD26Vd3eTJTULJ7wgpmS4RNls4MrOjaVGizMixtK6JVzt5shODnTkzWA0y5LOIowsWj5IHQ9aA2PXy4eomT25mvEnkXCsGfhEnVADhTJjCnkV2Xbu6yZObKFkfo2Z+R7jtkJbqpUxeQvHMXy6kBQlQYk+8pZopk5mwTJSyy0ypZspkJkjmYWZ3r3HUXeLVTZnchH+kYdklXu2Ubmc9mMxcskwcRJEM96hrdVTxop49TtQtz1YNySNgV9i1eqp8kXe17DDEKkji5rvUq6mqk3p2CI88+SCzBSFPxlmuZ38gMC6IWWgwGn5NvbqqflFXp2IZmwxO9gOd2UphxpYHjonm4e7Xz1ytturF1rxPuGf/zW4DhWOPtlVT7WJqXhewiLJmlWN++i716qldPM0ukeeHhmfnMVbcE3SrltrF0mxkEpBZkSmTGVNsl3q11C6Wcp4DlHEhzELKLew4G60aahdDeZmMuivVvVrqF0t5mYzzY/2/XwC8WuoXS/NaFByZjXmCheH86nLuI4IZvCjXm7RXS/1iaTZLzUtP5l1kogNduxeNV/5PL4fD03SBz93mDT5z9eYuy+YWhrvsD/lxOnoZ7megNjAWoFSwwALEBuIChAbSHFRrIDeQGsgNlAZyBaUtqWgDpYFtSZnHc7BP5A3UCrI3sO/IGthn7zvyBjbNgAXYdhQ4B6ktKfqOSgNbQKLtKKCBfXjbUbQdYZ+o7Sjyt/lXeqjQtWyLIRGN4duMFsxoGw97yyh9HXFmxPzLR0aLaKZQo/hbikun4DYFO4U2KeadwtuUs4psbijzZzFMKl+3+eft2SZFuFN8k9KTKV8pm17wWaWHuuarMDUUYYH2RSFuzkh9RqRtCi8xq3ze5GNZCR3Kz/htCdvRxTU30DaTDXFtyb6ZENBzBnvco4YPYE2lxp2gFiWPgX5DIZhTxpp+S8EFpXtKNEe9x4V4tqhs6x2VBbq2YdI55VwXZAu01xz5Au0FQmUrZKzn1cU2RVdcY9jmrwWTcctl7md83jG3EidvKJ3CWwXFEmurlFkdjZSmogt0zVi22fHMvbcg9+hSQ3tZco9ubWP5kF1bRywo3UKBWWPg3mzygbNAaUVOaEFZSxrhBaUvVWSO9qaVF9cFamsz2oKiazP2JttSj7qp+cq6b1eNL4fHhy+n8Z96+ea6oxrThP98/Hz6MqL5YsoJGnh6/nZ4uX/6dKh/wPraHvF+Efrt+PL8+funKpYvoTu69XD34uL5Zrbx8fPx9m/EgCKj'''


class GestureBox(FloatLayout):
    def __init__(self,**kwargs):
        super(Box, self).__init__(**kwargs)
        self.gdb = GestureDatabase()
        top_to_button = self.gdb.str_to_gesture(gesture_string)
        self.gdb.add_gesture(top_to_button)
        self.register_event_type('on_top_to_button')

    def on_touch_down(self,touch):
        super(Box, self).on_touch_down(touch)
        # print('vbar',self.scroll.vbar)
        if self.scroll.vbar[0] >0.79 and self.collide_point(*touch.pos):
            touch.grab(self)
            touch.ud['data points'] = [(touch.x,touch.y)]
    
    def on_touch_move(self,touch):
        super(Box, self).on_touch_move(touch)
        if touch.grab_current is self:
            touch.ud['data points'] += [(touch.x,touch.y)]

    def on_touch_up(self,touch):
        super(Box, self).on_touch_up(touch)
        if touch.grab_current is self:
            gesture = Gesture()
            gesture.add_stroke(touch.ud['data points'])
            gesture.normalize()
            
            match = self.gdb.find(gesture, minscore=0.8)
            if match:
                # print(match[0])
                self.dispatch('on_top_to_button')
                
            touch.ungrab(self)

    def on_top_to_button(self):
        print('My event happend')
    
    def add_widget(self,widget):
        if len(self.children) == 0:
            super(Box,self).add_widget(widget)
            self.scroll = widget
        else:
            print("Can't add more than one widget")

grid = BoxLayout(orientation='vertical',size_hint_y=None)
grid.bind(minimum_height=grid.setter('height'))

for i in range(30):
    grid.add_widget(Button(size_hint_y=None,text=str(i)))

scroll = ScrollView(effect_cls=ScrollEffect)
scroll.add_widget(grid)
b = GestureBox()
b.add_widget(scroll)

from kivy.base import runTouchApp
runTouchApp(b)
