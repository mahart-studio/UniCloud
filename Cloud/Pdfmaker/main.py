# kivy and python with pdf
# command to make atlas
#python -m kivy.atlas data/images/images 600 data/images/*

import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.behaviors import DragBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.garden.filechooserthumbview import FileChooserThumbView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
from kivy.resources import resource_add_path
from kivy.clock import Clock

# Mahart Studio Widget
from mahartstudios.widgets.buttons import IconButton, DropButton
from mahartstudios.effects import Effects
from mahartstudios.widgets.alertpopup import AlertPopup

# from mahartstudios.android.api import fast_toast

# from template import Templates, UniCloudPdf
from .crop import ImageCroper

#External Modules
from PIL import Image as PilImage
from PIL import ImageEnhance

# python module
import os, os.path
import shutil
from functools import partial
import time

Builder.load_file('ppdf.kv')


class PageOptions(ModalView):
	choose_pic_btn = ObjectProperty(None)
	custom_button = ObjectProperty(None)
	take_picture = ObjectProperty(None)
		

class PdfImage(DragBehavior, ToggleButton):
	source = StringProperty('')	
	'''source image for display'''
	
	select_color = ListProperty([get_color_from_hex('#FF9966'), get_color_from_hex('#FF996600')])
	'''set of colos to indicate selection'''
	tag_num = StringProperty('')
	
	'''Tag number to indicate page number'''
		

class AddButton(Button):
	type = StringProperty('addbutton')


class PdfScreens(ScreenManager):
	project_name = StringProperty('new')

	def __init__(self, **kwargs):
		super(PdfScreens, self).__init__(**kwargs)
		global root_cls
		root_cls = self

		global float_lay
		global manager
		global pics_grid
		manager = self
		pics_grid = self.ids.pics_grid
		float_lay = self.ids.float_lay
		self.pics_grid = self.ids.pics_grid

		self.selected = None 		# current selected Item

		#add mahart effect
		effect = Effects(self.ids.action_bar1)
		effect.add_shadow()

		self.page_options = PageOptions()	# modal popup
		self.edit_modal = EditModal()	
		self.image_viewer = ImageViewer()
		self.rotate_modal = RotateModal(apply_rotate=self.apply_rotate)
		self.crop_modal = CropModal()

		choose_picture = self.page_options.choose_pic_btn
		choose_picture.bind(on_release=partial(self.go_page, 'file'))

		custum_button = self.page_options.custom_button
		custum_button.bind(on_release=partial(self.go_page, 'template chooser'))		
		
		take_picture = self.page_options.take_picture
		take_picture.bind(on_release=self.take_picture)

		self.addbutton = AddButton()
		self.pics_grid.add_widget(self.addbutton)
		
		self.addbutton.bind(on_release=self.go_file)

		Clock.schedule_once(self.create_store_app_cls)

		#dictianary of real image directory
		self.real_images_dir = {}

		page = self.get_screen('saved page')
		Clock.schedule_once(lambda dt: self.reload_saved_project(page.saved_project_scroll))

		'''
		# Just put some default picture in view
		image_list = os.listdir('/root/Desktop/Podcasts/X-Force/pics')
		image_list =[os.path.join('/root/Desktop/Podcasts/X-Force/pics', image) 
						for image in image_list]

		Clock.schedule_once(lambda dt: self.add_more(image_list))
		'''

	def create_store_app_cls(self, dt):
		global app_cls
		app_cls = kivy.app.App.get_running_app()

 		# Our directories for work
		self.data_dir = app_cls.user_data_dir
		self.create_temps_dir()

		# pdf store
		global pdf_store
		pdf_store = JsonStore(os.path.join(self.data_dir, 'pdf_store.json'))
		global project_store
		project_store = JsonStore(os.path.join(self.data_dir, 'project_store.json'))

	def create_temps_dir(self):
		if os.path.exists(os.path.join(self.data_dir, '.UniCloud')):
			shutil.rmtree(os.path.join(self.data_dir, '.UniCloud'))
		try:
			os.mkdir(os.path.join(self.data_dir, '.UniCloud'))
			os.mkdir(os.path.join(self.data_dir, '.UniCloud/.thumbnails'))
			os.mkdir(os.path.join(self.data_dir, '.UniCloud/.images'))
			os.mkdir(os.path.join(self.data_dir, '.UniCloud/.effect_images'))
			os.mkdir(os.path.join(self.data_dir, '.UniCloud/.effect_tmp'))
			os.mkdir(os.path.join(self.data_dir, '.UniCloud/.templates'))
			os.mkdir(os.path.join(self.data_dir, 'saved project'))
		except Exception as e:
			print('create temp dir',e)
	

	def add_more(self, selections):

		if len(selections) != 0:
			self.current = 'home'

			for file_ in selections:
				file_name = os.path.basename(file_)
				# copy the real image into a TEMP file
				shutil.copy(file_, os.path.join(self.data_dir, '.UniCloud/.images'))
				self.real_images_dir[file_name] = file_
				
				thumbnail_path = self.make_thumbnails(file_)

				# Add to the widget view *note using the thumnail for view instead of real image 
				pdf_image = PdfImage(source=thumbnail_path, tag_num=str(len(self.pics_grid.children)))
				
				self.pics_grid.add_widget(pdf_image, index=1)		
				pdf_image.bind(state=self.selection_made)
		else:
			print('No selection made')

	def make_thumbnails(self, image_file):
		file_dir, file_name = os.path.split(image_file)

		#make tumbnails of the images
		pil_image = PilImage.open(image_file)

		pil_image.thumbnail((128, 128))
		thumbnail_path = os.path.join(os.path.join(self.data_dir, '.UniCloud/.thumbnails'), file_name)
		pil_image.save(thumbnail_path)

		return thumbnail_path

	def go_file(self, *largs):
#		self.current='file'			
		self.page_options.open()


	def go_page(self, page, *largs):
		if page == 'template chooser':
			self.get_screen('templates').mode ='new'
		elif page == 'home_page':
			self.parent.manager.go_to_page(page)
			return

		self.current = page				#go to page and dismiss the popup
		self.page_options.dismiss()
		
		

	def my_filter(self, directory, filename):
		exts = ['.png', '.jpg', 'jpeg', '.gif']
		if os.path.isdir(os.path.join(directory, filename)):

			if len(os.listdir(directory)) != 0:
				return True
							#if the Extention were looking for is in folder
			else:
				return False
		else:
			_, ext = os.path.splitext(filename)
			if ext in exts:
				return True
			else: 
				return False

	def delete_pic(self):
		

		if self.selected is None:
			print('[Error  ]  No valid selection')

		elif self.selected is not None and len(self.pics_grid.children) != 1:
			if self.selected.type == 'pdf_image':

				index = self.pics_grid.children.index(self.selected)

				self.pics_grid.remove_widget(self.selected)

				#remove real image
				os.remove(self.get_real_image(self.selected.source))
				# remove thumbnail
				os.remove(self.selected.source)
				
				selected = self.pics_grid.children[index-1]
				selected.state = 'down'
				if index == 1:
					self.selected = None
			else:
				index = self.pics_grid.children.index(self.selected)
				self.pics_grid.remove_widget(self.selected)

				num = self.selected.id_num
				image_name = '.UniCloud/.templates/template{}.png'.format(num)
				os.remove(os.path.join(self.data_dir, image_name))

				selected = self.pics_grid.children[index-1]
				selected.state = 'down'
				if index == 1:
					self.selected = None
		
		else:
			print('Toast noting to delete')
			# fast_toast(msg='Noting to delete')
	

	def export_pdf(self, modal, file_name, author_name, material_name):
		# store author name for later
		pdf_store.put('author_name', name=author_name)

		children =  self.pics_grid.children[:]
		children.reverse()

		pdf = UniCloudPdf()

		template = Templates(pdf_cls=pdf)

		for child in children:
			if child.type =='pdf_image':
				pdf.add_page()
				real_image = self.get_real_image(child.source)
				pdf.image(real_image, 0, 0, 210, 290)
			
			elif child.type[:8] == 'template':
				template_func = getattr(template, child.template_func)
				template_func(*child.data_list)


		pdf.output(os.path.join(os.path.dirname(__file__),"{}".format(file_name)), "F")
		
		modal.dismiss()		#close The popup
		self.current = 'saved_pdf'	# move to next page
		self.ids.saved_file_name.text = file_name +'.pdf'
		self.clear_all_widget()
		

	def apply_rotate(self, image, type):
		'rotate an image it takes type temp or real'

		if type == 'temp':
			pil_image = PilImage.open(image)

			filename = os.path.basename(image)
			save_path = os.path.join(os.path.join(self.data_dir, '.UniCloud/.effect_tmp'), filename)
			pil_image.transpose(PilImage.ROTATE_90).save(save_path)

			self.rotate_modal.source_image = save_path
			self.rotate_modal.source_image_cls.reload()

		else:
			shutil.copy(image, os.path.join(self.data_dir, '.UniCloud/.images'))
			real_image = self.get_real_image(image)

			thumbnail_path = self.make_thumbnails(real_image)

			#then load the image
			self.selected.source = thumbnail_path
			self.selected.image_cls.reload()
			self.edit_modal.dismiss()

		
	def edit_manager(self):
		if self.selected is None:
			print('[Error  ]  No valid selection')

		elif self.selected is not None and len(self.pics_grid.children) != 1:
			if self.selected.type == 'pdf_image':
				effect_list = self.get_effect_list(self.selected.source)

				if effect_list is not None:
					self.edit_modal.open()		
					real_image = self.get_real_image(self.selected.source)

					# add the original thumbnail
					effect_list = [self.selected.source] + effect_list	
			
					self.edit_modal.source_image = real_image
					self.edit_modal.effect_images = effect_list
					
					# Then reload all the images
					for button in self.edit_modal.edit_grid.children[:]:
						button.image_cls.reload()
				else:
					print('toast can\'t edit image the image type')

			else:
				self.current = 'templates'
				screener = self.get_screen('templates')
				screener.currrent_working_data = self.selected.data_list
				screener.current= self.selected.template_func
		else:
			print('Toast noting to edit')
			# fast_toast(msg='Noting to edit')

	def rotate_manager(self):
		if self.selected is None:
			print('[Error  ]  No valid selection')
		else:
			if self.selected.type == 'pdf_image':
				self.rotate_modal.open()		
				real_image = self.get_real_image(self.selected.source)
				self.rotate_modal.source_image = real_image
				self.rotate_modal.source_image_cls.reload()
			else:
				print('Toast can\'t rotate a custom page')


	def image_viewer_manager(self):
		if self.selected is None:
			print('[Error  ]  Not a valid selection')
		else:
			if self.selected.type == 'pdf_image':
				self.image_viewer.open()
				real_image = self.get_real_image(self.selected.source)
				self.image_viewer.source = real_image
				self.image_viewer.image_cls.reload() 
			else:
				self.image_viewer.open()
				num = self.selected.id_num
				image_name = '.UniCloud/.templates/template{}.png'.format(num)
				self.image_viewer.source = os.path.join(self.data_dir, image_name)
				self.image_viewer.image_cls.reload() 
				

	def selection_made(self, instance, state):
		if state =='down':
			self.selected = instance
		
	def get_real_image(self, image):
		# get the real image 
		__, file_name =os.path.split(image)
		real_image = os.path.join(os.path.join(self.data_dir, '.UniCloud/.images'), file_name)

		return real_image

	def get_thumb_image(self, image):
		# get the thumbnail of  image
		__, file_name =os.path.split(image)
		thumbnail_path = os.path.join(os.path.join(self.data_dir, '.UniCloud/.thumbnails'), file_name)

		return thumbnail_path

	def get_effect_list(self, image_path):
		'''fucn takes an image and make defferent effect with then'''

		# first remember to clear the effect_image folder
		image = PilImage.open(image_path)

		__, file_name =os.path.split(image_path)
		save_path = os.path.join(os.path.join(self.data_dir, '.UniCloud/.effect_images'), file_name)
		print(save_path)
		color = ImageEnhance.Color(image)
		contrast = ImageEnhance.Contrast(image)
		bright = ImageEnhance.Brightness(image)

		ext = os.path.splitext(os.path.basename(image_path))[1]
		try:
			color.enhance(0).save(os.path.join(self.data_dir, '.UniCloud/.effect_images/effect1.{}'.format(ext)))
			color.enhance(0.5).save(os.path.join(self.data_dir, '.UniCloud/.effect_images/effect2.{}'.format(ext)))
			color.enhance(2).save(os.path.join(self.data_dir, '.UniCloud/.effect_images/effect3.{}'.format(ext)))

			bright.enhance(0.5).save(os.path.join(self.data_dir, '.UniCloud/.effect_images/effect4.{}'.format(ext)))
			bright.enhance(2).save(os.path.join(self.data_dir, '.UniCloud/.effect_images/effect5.{}'.format(ext)))

			contrast.enhance(0.5).save(os.path.join(self.data_dir, '.UniCloud/.effect_images/effect6.{}'.format(ext)))
		except Exception as e:
			print(e)
			return None

		else:
			effect_list = [os.path.join(os.path.join(self.data_dir, '.UniCloud/.effect_images', file))
					for file in os.listdir(os.path.join(self.data_dir, '.UniCloud/.effect_images'))]

			# sort the list before returning
			effect_list.sort()

			return effect_list

	def apply_temp_effect(self, state, index):
		if state == 'down':
			image_source = self.edit_modal.source_image

			# we always open the real image
			real_image = self.get_real_image(image_source)
			image = PilImage.open(real_image)

			color = ImageEnhance.Color(image)
			contrast = ImageEnhance.Contrast(image)
			bright = ImageEnhance.Brightness(image)

			__, filename = os.path.split(image_source)
			save_path = os.path.join(os.path.join(self.data_dir, '.UniCloud/.effect_tmp'), filename)

			if index == 0:
				save_path = self.get_real_image(image_source)
			elif index == 1:
				color.enhance(0).save(save_path)
			elif index == 2:
				color.enhance(0.5).save(save_path)
			elif index == 3:
				color.enhance(2).save(save_path)
			elif index == 4:
				bright.enhance(0.5).save(save_path)
			elif index == 5:
				bright.enhance(2).save(save_path)
			elif index == 6:
				contrast.enhance(0.5).save(save_path)

			#then load the image
			self.edit_modal.source_image = save_path
			self.edit_modal.source_image_cls.reload()

	def apply_effect(self, index):

		image_source = self.edit_modal.source_image

		# we allways open the real image
		real_image = self.get_real_image(image_source)
		image = PilImage.open(real_image)

		color = ImageEnhance.Color(image)
		contrast = ImageEnhance.Contrast(image)
		bright = ImageEnhance.Brightness(image)

		__, filename = os.path.split(image_source)
		save_path = os.path.join(os.path.join(self.data_dir, '.UniCloud/.images'), filename)

		if index == 1:
			color.enhance(0).save(save_path)
		elif index == 2:
			color.enhance(0.5).save(save_path)
		elif index == 3:
			color.enhance(2).save(save_path)
		elif index == 4:
			bright.enhance(0.5).save(save_path)
		elif index == 5:
			bright.enhance(2).save(save_path)
		elif index == 6:
			contrast.enhance(0.5).save(save_path)
		
		thumbnail_path = self.make_thumbnails(save_path)

		#then load the image
		self.selected.source = thumbnail_path
		self.selected.image_cls.reload()
		self.edit_modal.dismiss()

	def set_template_data(self, data_layout, data):
		if data is not None:

			arg = lambda child: hasattr(child, 'text')
			text_widget = list(filter(arg, data_layout.walk()))
			for index, wid in enumerate(text_widget):
				wid.text = data[index]
		else:
			arg = lambda child: hasattr(child, 'text')
			text_widget = list(filter(arg, data_layout.walk()))
			for index, wid in enumerate(text_widget):
				wid.text =''


	def template_manager(self, layout):
		# export image as png
		num = len(os.listdir(os.path.join(self.data_dir,'.UniCloud/.templates'))) + 1

		name = '.UniCloud/.templates/template{}.png'.format(num)
		full_path=os.path.join(self.data_dir, name)
		layout.export_to_png(full_path)

		pdf_wid = PdfImage(tag_num=str(len(self.pics_grid.children)),source=full_path)
		pdf_wid.type = layout.template_type
		pdf_wid.template_func = layout.template_func
		pdf_wid.id_num = num
	
		# set template data
		arg = lambda child: hasattr(child, 'text')

		data_list = list(map(lambda data: data.text, list(filter(arg, layout.walk()))))
		pdf_wid.data_list = data_list
		pdf_wid.bind(state=self.selection_made)

		self.current = 'home'
		self.pics_grid.add_widget(pdf_wid, index=1)
		
	def clear_all_widget(self):
		'clean all the widget avialable except addbutton and clear dirs'
		for child in self.pics_grid.children[:]:
			if child.type != 'addbutton':
					self.pics_grid.remove_widget(child)
		
		# shutil.rmtree(os.path.join(self.data_dir, '.UniCloud'))
		
		def delete_pic(arg, dir, files):
			for file in files:
				full_path = os.path.join(dir, file)
				if os.path.isfile(full_path):
					os.remove(full_path)

		# os.path.walk(os.path.join(self.data_dir, '.UniCloud'), delete_pic, 0)


	def save_project(self, project_name):
		# method to save is to pickle all the widget and move the .image and .template and .thumnail folder
		save_data=[]
		for child in self.pics_grid.children[:]:
			if child.type =='pdf_image':
				data={}
				data['source']= child.source
				data['type']= child.type
				save_data.append(data)

			elif child.type[:8] == 'template':
				data={}
				data['source']= child.source
				data['type']= child.type	
				data['template_func']= child.template_func	
				data['data_list']= child.data_list
				data['id_num']= child.id_num
				save_data.append(data)
		save_data.reverse()

		project_dir = os.path.join(self.data_dir, 'saved project/{}'.format(project_name))

		try:
			os.mkdir(project_dir)
		except OSError:
			pass
			print('Overiding')

		if len(save_data)!=0:
			# our button pics
			shutil.copy(save_data[0]['source'], project_dir)

		self.handle_copy(os.path.join(self.data_dir, '.UniCloud/.images'), project_dir,mode=1)
		self.handle_copy(os.path.join(self.data_dir, '.UniCloud/.templates'), project_dir,mode=1)
		self.handle_copy(os.path.join(self.data_dir, '.UniCloud/.thumbnails'), project_dir,mode=1)
		# self.create_temps_dir()
		# except Exception as e:
		# 	raise e
		# 	self.create_temps_dir()
		# 	# print('an error occured 1', e)
		# 	return

		#then store
		if not project_store.exists(project_name) or self.project_name==project_name:
			# create widget btn
			btn = SavedProjectButton(load=partial(self.load_project, project_name), delete = partial(self.delete_project,project_name))
			btn.project_name = project_name
			btn.created_time = time.ctime()

			source = os.path.join(project_dir, os.path.basename(save_data[0]['source']))
			btn.project_source = source 

			project_store.put(project_name, saved_data=save_data, source=source, created_time=time.ctime())
			
			page = self.get_screen('saved page')
			self.current = 'saved page'
			if self.project_name!=project_name:
				page.saved_project_scroll.add_widget(btn)

		else:
			print('warn that you would override an exsiting project')
			return

	def load_project(self, project_name):
		project_dir = os.path.join(self.data_dir, 'saved project/{}'.format(project_name))

		# try:
		self.create_temps_dir()
		self.handle_copy(os.path.join(project_dir, '.images'), os.path.join(self.data_dir, '.UniCloud/.images'))
		self.handle_copy(os.path.join(project_dir, '.templates'), os.path.join(self.data_dir, '.UniCloud/.templates'))
		self.handle_copy(os.path.join(project_dir, '.thumbnails'), os.path.join(self.data_dir, '.UniCloud/.thumbnails'))
		# except Exception as e:
		# 	raise e
		# 	# print('an error occured 2',e)
		# 	self.create_temps_dir()
		# 	return

		if project_store.exists(project_name):
			saved_data = project_store.get(project_name)['saved_data']

			self.clear_all_widget()
			for data in saved_data:
				if data['type'] =='pdf_image':
					pdf= PdfImage(source=data['source'],tag_num=str(len(self.pics_grid.children)))
				else:
					pdf= PdfImage(source=data['source'],tag_num=str(len(self.pics_grid.children)))
					pdf.template_func = data['template_func']
					pdf.data_list = data['data_list']
					pdf.id_num = data['id_num']

				pdf.type =data['type']
				pdf.bind(state=self.selection_made)
				self.pics_grid.add_widget(pdf,index=1)
	
		else:
			print('Toast: cant find project')
			return

		self.project_name =project_name
		self.current = 'home'
		
	
	def handle_copy(self, dir, dis,mode=0):
		if mode ==0:
			for file in os.listdir(dir):
				shutil.copy(os.path.join(dir,file), dis)
		elif mode ==1:
			base=os.path.basename(dir)
			dis_fold = os.path.join(dis,base)
			if os.path.exists(dis_fold):
				shutil.rmtree(dis_fold)
				os.mkdir(dis_fold)
			else:
				os.mkdir(dis_fold)
			for file in os.listdir(dir):
				shutil.copy(os.path.join(dir,file), dis_fold)


	def delete_project(self,project_name):
		print('deleted {}'.format(project_name))
		project_dir = os.path.join(self.data_dir, 'saved project/{}'.format(project_name))

		if os.path.exists(project_dir):
			shutil.rmtree(project_dir)
		if project_store.exists(project_name):
			project_store.delete(project_name)

		page = self.get_screen('saved page')
		layout = page.saved_project_scroll

		widget = list(filter((lambda child: getattr(child,'project_name')==project_name),layout.children))[0]
		layout.remove_widget(widget)

	def reload_saved_project(self,layout):
		layout.clear_widgets()
		for key in project_store.keys():
			data=project_store.get(key)

			created_time = data['created_time']
			source = data['source']
			name =key
			btn = SavedProjectButton(load=partial(self.load_project,name))
			btn.delete = partial(self.delete_project,name)
			btn.project_name = name
			btn.created_time = created_time
			btn.project_source = source

			layout.add_widget(btn)

	def take_picture(self, *largs):
		from Mahart.android.camera import TakePicture
		picture = TakePicture(self.pic_taken,'')
		picture.take_picture()

	def pic_taken(self, fn, *args):
		self.add_more([fn])

	def crop_manager(self):

		if self.selected is None:
			print('[Error  ]  No valid selection')
		else:
			if self.selected.type == 'pdf_image':
				self.crop_modal.open()
				self.crop_modal.croper.source= self.get_real_image(self.selected.source)

			else:
				print('Toast can\'t rotate a custom page')



class SavedProjectButton(DropButton):
	load = ObjectProperty()
	delete = ObjectProperty()


class PdfLayout(GridLayout):
	
	def on_touch_down(self, touch):
		super(PdfLayout, self).on_touch_down(touch)
		if self.collide_point(*touch.pos):
			for child in self.children[:]:
				if child.collide_point(*touch.pos) and child.type!='addbutton':
					touch.grab(self)
					touch.ud['touched_child'] = child

					pdf_mimic = PdfImage(source=child.source, group='mimic',
							tag_num=str(child.tag_num),size_hint=(None,None))
					touch.ud['pdf_mimic'] = pdf_mimic
					pos = self.parent.to_parent(*child.pos)
					pdf_mimic.pos = pos
					pdf_mimic.size = child.size
					float_lay.add_widget(pdf_mimic)

					return True

	def on_touch_move(self, touch):
		super(PdfLayout, self).on_touch_move(touch)
		if self.collide_point(*touch.pos):
			if touch.grab_current is self:
				touched_child = touch.ud['touched_child']

				child = list(filter(lambda child: child.collide_widget(touched_child), self.children[:]))
				if len(child) >= 1:
					child = child[0]
					self.parent.scroll_to(child,padding=30)

				pdf_mimic = touch.ud['pdf_mimic']
				pos = self.parent.to_parent(*touched_child.pos)
				pdf_mimic.pos = pos

				return True


	def on_touch_up(self, touch):
		super(PdfLayout, self).on_touch_up(touch)
		if touch.grab_current is self:
			touch.ungrab(self)
			for child in self.children[:]:
				touched_child = touch.ud['touched_child']
				if child.collide_point(*touched_child.center) and child != touched_child:
					index = self.children[:].index(child)
					self.remove_widget(touched_child)
					self.add_widget(touched_child, index=index)

					# delete mimic widget
					pdf_mimic = touch.ud['pdf_mimic']
					float_lay.remove_widget(pdf_mimic)
					self.recompute_tag()
					del pdf_mimic
					break
			else:
				index = self.children[:].index(touched_child)
				self.remove_widget(touched_child)
				self.add_widget(touched_child, index=index)

				# delete mimic widget
				pdf_mimic = touch.ud['pdf_mimic']
				float_lay.remove_widget(pdf_mimic)
				del pdf_mimic
			return True

	def recompute_tag(self):
		children = self.children[:]
		children.reverse()
		for index, child in enumerate(children):
			if child.type != 'addbutton':
				child.tag_num =str(index+1)


	
class EditModal(ModalView):
	source_image = StringProperty('')
	'''path to the image to be edited'''

	effect_images = ListProperty(['','','','','','',''])
	'''effect version of the images'''

	current_index = NumericProperty(0)

	def __init__(self, **kwargs):
		super(EditModal, self).__init__(**kwargs)
		self.edit_grid = self.ids.edit_grid
		
		self.edit_grid.bind(minimum_width=self.edit_grid.setter('width'))
		
	def apply_temp_effect(self, state, index):	
		root_cls.apply_temp_effect(state, index)

	def apply_effect(self):
		if self.current_index != 0:
			root_cls.apply_effect(self.current_index)
		else:
			print('toast:  No Effect Selected')


class RotateModal(ModalView):
	source_image = StringProperty('')
	apply_rotate = ObjectProperty()

class CropModal(ModalView):

	croper = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(CropModal, self).__init__(**kwargs)
		self.croper =  ImageCroper()
		Clock.schedule_once(self.add_image_croper,1)
		
	def add_image_croper(self, *a):
		self.add_widget(self.croper)




class SaveModal(ModalView):
	activate = ObjectProperty()
	saved_author_name = StringProperty('')

	def on_open(self):
		if pdf_store.exists('author_name'):
			self.saved_author_name = pdf_store.get('author_name')['name']
		else:
			pdf_store.put('author_name', name='')


class ImageViewer(ModalView):
	source = StringProperty('')
				

class PdfMaker(Screen):

	def __init__(self, **kwargs):
		super(PdfMaker, self).__init__(**kwargs)
		self.pdf_screens = PdfScreens()
		self.add_widget(self.pdf_screens)
		
		self.alert = AlertPopup(title='Alert', message='Are you sure you want to exsit you \
				will loose you current walking project', front_text='Yes')

	def on_pre_leave(self):
		self.pdf_screens.clear_all_widget()

class PdfApp(App):

	def build(self):
		return PdfScreens()

	def on_pause(self):
		return True


if __name__ == '__main__':
	PdfApp().run()
