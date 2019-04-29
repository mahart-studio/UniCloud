
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.vector import Vector

from PIL import Image as PilImg

Builder.load_string('''
#: import Vector kivy.vector.Vector

<Drager@Label>:
    size_hint: None, None
    size: '38dp', '18dp'
    
    canvas.after:
        Color:
            rgba: 1,1,0,1
        RoundedRectangle:
            size: self.size
            pos: self.pos

<Drager1@Label>:
    size_hint: None, None
    size: '18dp', '38dp'
    canvas.after:
        Color:
            rgba: 1,1,0,1
        RoundedRectangle:
            size: self.size
            pos: self.pos


<ImageCroper>:
    BoxLayout:
        size_hint_y: None
        height: '40dp'
        Button:
            text: 'Cancel'
        Button:
            text: 'Crop'
            on_release: root.crop_image('croped.png')


<Croper>:
    orientation: 'vertical'
    source: root.source
    line_width: 1.5
    image_cls: crop_image

    CustImage:
        id: crop_image
        source: root.source
        size_hint: (None,None)
        pad: 20
        size: root.width-self.pad, root.height-self.pad
        pos_hint: {'center_x': .5, 'center_y': .5}
        canvas.after:
            Color:
                rgba: 1,1,0,.6
            Line:
                points: root.h1_points   
                width: root.line_width
            Line:
                points: root.h2_points   
                width: root.line_width
            Line:
                points: root.v2_points   
                width: root.line_width
            Line:
                points: root.v1_points   
                width: root.line_width
        
            Color:
                rgba: 1,1,0,.2
            Rectangle:
                pos: root.v2_points[0], root.v2_points[1]
                size: (Vector(root.v2_points[:2]).distance(root.v2_points[2:]), Vector(root.h2_points[:2]).distance(root.h2_points[2:]))


    Drager:
        name: 'v1'
        id: drag1
        center: crop_image.texture_center[0], crop_image.texture_pos[1]+crop_image.texture_size[1]

    Drager:
        name: 'v2'
        id: drag2
        center: crop_image.texture_center[0], crop_image.texture_pos[1]

    Drager1:
        name: 'h1'
        id: drag3
        center: crop_image.texture_pos[0], crop_image.texture_center[1]

    Drager1:
        name: 'h2'
        id: drag4
        center: crop_image.texture_pos[0]+crop_image.texture_size[0], crop_image.texture_center[1]
    
    Label:
        name:''
        id: restriction_widget
        size_hint: None,None
        pos_hint: {'center_x': .5, 'center_y': .5}
        size: crop_image.texture_size
    Label:
        id: restriction_widget1
        pos: root.v2_points[0], root.v2_points[1]
        size_hint: None,None
        size: (Vector(root.v2_points[:2]).distance(root.v2_points[2:]), Vector(root.h2_points[:2]).distance(root.h2_points[2:]))

<CropImage>:
    canvas:
        Color:
            rgb: (1, 1, 1)
        Rectangle:
            texture: self.texture
            size: self.size
            pos: self.pos


<CustImage>:
    texture_pos: (abs(self.center_x-(self.texture_size[0]/2)), abs(self.center_y-(self.texture_size[1]/2)))

    texture_center: (abs(self.texture_pos[0]+self.texture_size[0]/2), abs(self.texture_pos[1]+self.texture_size[1]/2))

    texture_size: self.norm_image_size

    canvas.after:   
        Color:
            rgba: 1,1,0,0
        Rectangle:
            size: self.norm_image_size
            pos: self.texture_pos


''')

class CustImage(Image):
    texture_pos =  ListProperty([0,0])
    'the position of the actual image on the widget'

    texture_center =  ListProperty([0,0])
    'center position of the widget'


class CropImage(Image):
    pass

class Croper(FloatLayout):
    
    source = StringProperty('')

    v1_points = ListProperty([])  # give it a defualt value to avoid an IndexError
    v2_points = ListProperty([1,1,1,1])
    h1_points = ListProperty([])
    h2_points = ListProperty([1,1,1,1])

    v1 = ObjectProperty()
    v2 = ObjectProperty()
    h1 = ObjectProperty()
    h2 = ObjectProperty()

    crop_image = ObjectProperty()

    def __init__(self, **kwargs):   
        super(Croper, self).__init__(**kwargs)
        self.crop_image = self.ids.crop_image
        self.v1 = self.ids.drag1
        self.v2 = self.ids.drag2
        self.h1 = self.ids.drag3
        self.h2 = self.ids.drag4


        self.start = False
        self.touched_child = None
        self.start_pos = None

        Clock.schedule_once(self.set_init_value)

    def on_source(self, *a):
        Clock.schedule_once(self.set_init_value)

    def set_init_value(self, dt):
        size = self.crop_image.texture_size
        center = self.crop_image.texture_center
        pos = self.crop_image.texture_pos

        # Defualts points value

        self.v1_points = [pos[0], pos[1]+size[1],
                            pos[0]+size[0], pos[1]+size[1]]

        self.v2_points = [pos[0], pos[1],
                            pos[0]+size[0], pos[1]]


        self.h1_points = [pos[0], pos[1],
                            pos[0], pos[1]+size[1]]

        self.h2_points = [pos[0]+size[0], pos[1],
                            pos[0]+size[0], pos[1]+size[1]]

    def on_touch_down(self, touch):
       #super(CropImage, self).on_touch_down(touch)
        for child in self.children[:]:
            if child.collide_point(*touch.pos):
                if not hasattr(child, 'source'):
                    self.start = True
                    self.touched_child = child
                    self.start_pos = child.pos

        return super(Croper, self).on_touch_down(touch)


    def on_touch_move(self, touch):

        if self.start:
            restrictions = not self.ids.restriction_widget.collide_point(*touch.pos)
            if restrictions:
                return True 
            if self.ids.restriction_widget1.height < 60 and self.ids.restriction_widget1.collide_point(*touch.pos):
                print('height')
                return True 
            if self.ids.restriction_widget1.width < 60 and self.ids.restriction_widget1.collide_point(*touch.pos):
                print('width')
                return True


            v_center = self.crop_image.x+(Vector((self.crop_image.x, self.v1_points[1])).distance((self.v1_points[0], self.v1_points[1])) +
                ((Vector((self.v1_points[0], self.v1_points[1])).distance((self.v1_points[2], self.v1_points[3])))/2))

            self.v1.center_x = v_center
            self.v2.center_x = v_center

            h_center = self.crop_image.y+(Vector((self.h1_points[0], self.crop_image.y)).distance((self.h1_points[0], self.h1_points[1])) +
                ((Vector((self.h1_points[0], self.h1_points[1])).distance((self.h1_points[2], self.h1_points[3])))/2))

            self.h1.center_y = h_center
            self.h2.center_y = h_center


            if self.touched_child.name == 'h1':

                formal_points = self.h1_points
                self.v1_points[0] = self.touched_child.center_x
                self.v2_points[0] = self.touched_child.center_x

                self.h1_points = [self.touched_child.center_x, formal_points[1],
                                    self.touched_child.center_x, formal_points[3]]

                self.touched_child.center_x = touch.pos[0]   


            elif self.touched_child.name == 'h2':
                formal_points = self.h2_points
                self.v1_points[2] = self.touched_child.center_x
                self.v2_points[2] = self.touched_child.center_x
                
                self.h2_points = [self.touched_child.center_x, formal_points[1],
                                    self.touched_child.center_x, formal_points[3]]

                self.touched_child.center_x = touch.pos[0]   


            elif self.touched_child.name == 'v1':
                formal_points = self.v1_points      # save formal points 
                self.h1_points[3] = self.touched_child.center_y
                self.h2_points[3] = self.touched_child.center_y
                
                self.v1_points = [formal_points[0], self.touched_child.center_y,
                                    formal_points[2], self.touched_child.center_y]

                self.touched_child.center_y = touch.pos[1]           

 
            elif self.touched_child.name == 'v2':
                formal_points = self.v2_points
                self.h1_points[1] = self.touched_child.center_y
                self.h2_points[1] = self.touched_child.center_y

                self.v2_points = [formal_points[0], self.touched_child.center_y,
                            formal_points[2], self.touched_child.center_y]

                self.touched_child.center_y = touch.pos[1]           

        return super(Croper, self).on_touch_down(touch)

    def on_touch_up(self, touch):   
        self.start = False
        #self.catch_restriction()
        return super(Croper, self).on_touch_down(touch)

    def catch_restriction(self):
        size = self.crop_image.texture_size
        center = self.crop_image.texture_center
        pos = self.crop_image.texture_pos

        # Defualts points value

        if self.h1.center_x < self.crop_image.texture_pos[0] or self.h1.x+self.h1.width > self.h2.x-60:
            self.h1_points[0] = pos[0]
            self.h1_points[2] = pos[0]
            self.touched_child.center_x = self.crop_image.texture_pos[0]        
            self.v1_points[0] = self.touched_child.center_x
            self.v2_points[0] = self.touched_child.center_x

        if (self.h2.center_x) > (self.crop_image.texture_pos[0]+ self.crop_image.texture_size[0]):
            self.touched_child.center_x = (self.crop_image.texture_pos[0]+ self.crop_image.texture_size[0])
            self.v1_points[2] = self.touched_child.center_x
            self.v2_points[2] = self.touched_child.center_x
            self.h2_points[0] = self.touched_child.center_x
            self.h2_points[2] = self.touched_child.center_x


        if (self.v1.center_y) > (self.crop_image.texture_pos[1] + self.crop_image.texture_size[1]):
            self.v1.center_y = (self.crop_image.texture_pos[1] + self.crop_image.texture_size[1])
            self.h1_points[3] = self.touched_child.center_y
            self.h2_points[3] = self.touched_child.center_y
            self.v1_points[1] = self.touched_child.center_y
            self.v1_points[3] = self.touched_child.center_y

        if (self.v2.center_y) < (self.crop_image.texture_pos[1]):
            self.v2.center_y = (self.crop_image.texture_pos[1])
            self.h1_points[1] = self.touched_child.center_y
            self.h2_points[1] = self.touched_child.center_y
            self.v2_points[1] = self.touched_child.center_y
            self.v2_points[3] = self.touched_child.center_y


    def get_box(self):
        '''function to calculate the box region to be croped in the image,
            Its returns the format of the Pil Module ('left', 'upper', 'right', 'lower')
            returns a tupple of the box region and the pil image object that has
            been open'''

        upper_point = (self.crop_image.texture_pos[0], 
                        self.crop_image.texture_pos[1] + self.crop_image.texture_size[1])
        
        upper_point2 = (self.crop_image.texture_pos[0]+ self.crop_image.texture_size[0], 
                        self.crop_image.texture_pos[1] + self.crop_image.texture_size[1])
        lower_point = (self.crop_image.texture_pos[0], 
                        self.crop_image.texture_pos[1])

        left = Vector(upper_point).distance((self.crop_image.texture_pos[0], self.v1_points[1]))
        upper = Vector(upper_point).distance((self.v1_points[0], upper_point[1]))

        lower = Vector(self.v2_points[:2]).distance(self.v2_points[2:])
        rigth = Vector(self.h2_points[:2]).distance(self.h2_points[2:])

        lower = Vector(self.h2_points[0], self.crop_image.texture_pos[1]).distance(lower_point)
        rigth = Vector(upper_point2).distance((upper_point2[0], self.h2_points[1]))

        # use pil to get the original size        
        img = PilImg.open(self.crop_image.source)
        orig_size = img.size
        norm_size = self.crop_image.texture_size

        # calculate the real values of the box
        left = (left * orig_size[1])/ norm_size[1] 
        upper = (upper * orig_size[0])/ norm_size[0]

        lower = (lower * orig_size[0])/ norm_size[0]
        rigth = (rigth * orig_size[1])/ norm_size[1]

        print(upper, left, lower, rigth)
        print(orig_size)

        return (upper, left, lower, rigth), img
        

class ImageCroper(BoxLayout):
    source = StringProperty('/root/ed_artwork.jpg')

    def __init__(self, **k):
        super(ImageCroper, self).__init__(**k)
        self.orientation =  'vertical'
        Clock.schedule_once(self.add_croper)
        
    def add_croper(self, dt):
        self.croper = Croper(source=self.source)
        self.bind(source=self.croper.setter('source'))
        self.add_widget(self.croper)

    def on_source(self, *a):
        self.croper.image_cls.reload()

    def crop_image(self, path):
        box, img = self.croper.get_box()
        img_crop = img.crop(box)
        img_crop.save(path)




if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.uix.button import Button
    from kivy.uix.modalview import ModalView
    mv = ModalView()
    box = BoxLayout()
    box.add_widget(ImageCroper())
   
    btn = Button()
    btn.bind(on_release=lambda *a: mv.open())
    runTouchApp(box)
