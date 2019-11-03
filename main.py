from kivy.app import App
from kivy.uix.textinput import TextInput  
from kivy.uix.slider import Slider      
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import (Color, Ellipse, Rectangle, Line, Translate, Scale)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.screenmanager import ScreenManager , Screen
from kivy.properties import ListProperty

from kivy.core.window import Window

from random import random
from math import sqrt, sin, cos, tan
color_graph = [0.2, 0.5,0.3,1]
color_lines = [.5, .5, .5, 1]

width = Window.size[0]
height = Window.size[1]
px_point = 40
center_y = int((height)/2)
center_x = int((width*0.8)/2+width*0.2)


def ctg(x):
    return tan(x)**-1
x = -1
defoult_n = int((0.8*width/px_point)/2) 
n = defoult_n
step = 0.1
class BackgroudWidget(Widget):  
    global height, width  
    def __init__(self, **kwargs):
        super(BackgroudWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(.5, .5, .5, 1)
            Rectangle(pos = (0, 0), size = (width , height))

class MenuScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        bl_menu = BoxLayout(orientation = "vertical", spacing = 25, padding = [200, 100])
        btn_graph = Button(text = "Graphic", on_press = self.return_graph, font_size = 40)
        btn_settings = Button(text = "Settings", on_press = self.return_s, font_size = 40)
        bl_menu.add_widget(btn_graph)
        bl_menu.add_widget(btn_eq)
        bl_menu.add_widget(btn_settings)
        self.add_widget(bl_menu)
    def return_graph(self, instance):
        sm.current = "main"
    def return_s(self, instance):
        sm.current = "gr_settings"


class GraphSettingsScreen(Screen, Widget):
    def __init__(self, **kwargs):
        super(GraphSettingsScreen, self).__init__(**kwargs)
        self.sp_n = None
        self.color_graph_nsave = None
        self.color_lines_nsave = None  
        self.beta_step = None
        slider = Slider(orientation='horizontal', max = "1", min = 0.025, step = 0.005)      
        gl = GridLayout(cols = 2)
        lbl1 = Label(text = "You can change color of graphic", font_size = 26)
        bl = BoxLayout(orientation = "vertical")
        bl_btns = BoxLayout(size_hint = (1, 0.3))

        colorpicker_graph = ColorPicker()
        colorpicker_lines = ColorPicker()
        self.lbl_detail = Label(text = "Mid", font_size = 26)
        lbl2 = Label(text = "You can change color of lines ", font_size = 26) 
        btn_save = Button(text = "Save Changes", font_size = 26, on_press = self.save_settings)
        btn_return = Button(text = "Return", font_size = 26, on_press = self.return_main)
        n_input = TextInput(text = "14", multiline = False, font_size = 26)
        n_input.bind(text = self.change_n)
        colorpicker_graph.bind(color = self.on_color_graph)
        colorpicker_lines.bind(color = self.on_color_lines)
        slider.bind(value = self.detail)
        gl.add_widget(lbl1)
        gl.add_widget(colorpicker_graph)
        gl.add_widget(lbl2) 
        gl.add_widget(colorpicker_lines)
        gl.add_widget(Label(text = "Print number of cordanate system", font_size = 26))
        gl.add_widget(n_input)
        gl.add_widget(slider)
        gl.add_widget(self.lbl_detail)
        bl_btns.add_widget(btn_save)
        bl_btns.add_widget(btn_return)
        bl_btns.add_widget(Button())
        bl.add_widget(gl)
        bl.add_widget(bl_btns)        
        self.add_widget(BackgroudWidget())
        self.add_widget(bl) 
    def detail(self, instance, value):
        self.beta_step = round(value, 4)
        if 0.3< self.beta_step <=0.5:
            self.lbl_detail.text = "Low"
        if 0.1<self.beta_step<=0.2:
            self.lbl_detail.text = "Mid"
        if self.beta_step<=0.1:
            self.lbl_detail.text = "High"    

    def change_n(self, instance, value):
        self.sp_n = value
    def on_color_graph(self, instance, value):
        self.color_graph_nsave = value
    def on_color_lines(self, instance, value):
        self.color_lines_nsave = value
    def save_settings(self, instance):
        global color_graph, color_lines, sm , n , px_point, width, step
        if self.color_lines_nsave == None:
            pass
        else:
            color_lines = self.color_lines_nsave
        if self.color_graph_nsave == None:
            pass
        else:
            color_graph = self.color_graph_nsave
        if self.sp_n == None:
            pass
        else:
            n = int(self.sp_n)
        if self.beta_step == None:
            pass
        else:
            step = self.beta_step
        # Config.set("graphics","resizable","0")
    def return_main(self, instance):
        global color_graph, color_lines, sm , b , px_point, step
        self.beta_step = step
        sm.current = "main"
class Canvas(Widget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        global px_point, center_y, center_x, n, color_graph, height, width, step
        with self.canvas:
            Color(color_lines[0], color_lines[1], color_lines[2],1 )
            '''Two main lines;
            Check defoult size or not'''
            self.draw_cord()
    
    def draw_graph(self, f):
        global px_point, center_y, center_x, n, color_graph, color_lines, height, width, step
        with self.canvas:
            Color(color_lines[0], color_lines[1], color_lines[2], 1) 
            
            
            points1 = [] 
            pi = 3.14
            x = -n    
            '''Drawing of segments on a coordinate line'''
            '''Drawing two main lines'''
 

            '''Part of drawing graphic:
                -check diferent x and calc y=f(x), eval do from formul(string) to integer by known arg x
                -apppend coords(x,y) to list(points of graph).
            First cycle for not parsing smallest numbers'''
            for b in range(1,10):
                x -= step*100
                y = eval(f).real
                points1.append(x*px_point+center_x)
                points1.append(y*px_point+center_y)   
            x = -n 
            '''Second cycle for exactly parsing midle(stndart) numbers '''         
            while int(x) in range(-n, n):
                y = eval(f).real
                points1.append(x*px_point+center_x)
                points1.append(y*px_point+center_y)
                x += step
            '''Third cycle for not exactly parsing highest numbers'''
            for b in range(1,10):
                x += step*100
                y = eval(f).real
                points1.append(x*px_point+center_x)
                points1.append(y*px_point+center_y)
            Color(color_graph[0], color_graph[1], color_graph[2],1 )

            Line(points = (points1))#Draw this graph as line with many points
    '''Function for drawing cordinate system'''
    def draw_cord(self):
        global px_point, center_y, center_x, n, color_graph, color_lines, height, width, step
        with self.canvas:
            Color(color_lines[0], color_lines[1], color_lines[2], 1)      
            '''Drawing two main lines'''
            if n == defoult_n:
                Line(points = (center_x, height, center_x, 0))
                Line(points = (width*0.2, center_y, width, center_y))
            else:
                Line(points = (center_x, n*px_point , center_x, -n*px_point))
                Line(points = (-n*px_point, center_y, n*px_point, center_y))    
            '''Small segmaents of lines'''
            for i in range (-n+1, n):
                Line(points = (i*px_point+center_x, center_y-5, i*px_point+center_x, center_y+5 ))
                Line(points = (center_x-5, i*px_point+center_y, center_x+5, i*px_point+center_y ))


        
class MainScreen(Screen, BoxLayout):
    global px_point, center_y, center_x, sm , n
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.formula = None
        bl_panel = BoxLayout(orientation = "vertical")
        self.bl1 = BoxLayout(orientation = "vertical", size_hint = (0.2, 1))
        bl_zoom = BoxLayout(size_hint = (1, 0.4 ))
        self.bl_inputs = BoxLayout(orientation = "vertical")
        btn_draw = Button(text = "Draw", on_press = self.draww, font_size = 36)
        btn_quit = Button(text = "Clear", on_press = self.clear_canvas, font_size = 36)
        btn_settings = Button(text = "Settings", on_press = self.sett, font_size = 36)        
        self.textinput = TextInput(multiline = True , size_hint = (1, 1), font_size = 40, background_color = (.7, .7, .9, 1))
        btn_zoom = Button(text = "+", on_press = self.zoom, font_size = 40)
        btn_unzoom = Button(text = "-", on_press = self.unzoom, font_size = 48)
        btn_update = Button(text = "Update", on_press = self.update, font_size = 36)

        self.input_point = TextInput(multiline = False , size_hint = (1, 1), font_size = 36, background_color = (.7, .7, .9, 1))

        self.scatter = Scatter(do_rotation = False, do_scale = False, do_translation = False, size_hint = (1, 1))
        self.graph = Canvas()
        self.scatter.add_widget(self.graph)
        bl_zoom.add_widget(btn_zoom)
        bl_zoom.add_widget(btn_unzoom)   
        bl_panel.add_widget(bl_zoom)

        self.bl_inputs.add_widget(self.textinput)   
        self.bl1.add_widget(btn_draw)
        self.bl1.add_widget(btn_update)
        self.bl1.add_widget(btn_quit)
        self.bl1.add_widget(bl_panel)
        self.bl1.add_widget(btn_settings)
        self.bl1.add_widget(self.bl_inputs) 

        self.add_widget(self.scatter)
        self.add_widget(self.bl1)

        self.nums()
            
        self.textinput.bind(text = self.functionn) 

        
    '''Function use after changes size screen'''
    def update(self, instance):

        global width, height, center_x, center_y, defoult_n, n

        self.graph.canvas.clear() #clear
        '''Refresh all arguments about screen size'''
        width = Window.size[0]
        height = Window.size[1]
        center_y = int((height)/2)
        center_x = int((width*0.8)/2+width*0.2)
        defoult_n = int((0.8*width/px_point)/2) 
        n = defoult_n
        '''Drawing cord system'''
        self.nums()
        self.graph.draw_cord()
        '''Draw graphic in new size'''
        if not self.formula == None and not self.formula == "":
            self.graph.draw_graph(str(self.formula))
    def zoom(self, instance): 
        self.scatter.scale *= 1.5
    def unzoom(self, instance):
        self.scatter.scale /= 1.5
    def functionn(self, istance, value):
        self.formula = value
    def draww(self, instance):
        '''Refresh all arguments about screen size'''
        global width, height, center_x, center_y, defoult_n, n
        width = Window.size[0]
        height = Window.size[1]
        center_y = int((height)/2)
        center_x = int((width*0.8)/2+width*0.2)
        defoult_n = int((0.8*width/px_point)/2)
        '''Draw graphic and validation '''
        if not self.formula == None and not self.formula == "":
            self.graph.draw_graph(str(self.formula))
    def clear_canvas(self, instance):
        self.graph.canvas.clear()
        self.nums()
        self.graph.draw_cord()
    def sett(self, instance):
        sm.current = "gr_settings"
    def nums(self):
        for i in range (-n+1, n, 1):
            if not i == 0 :
                self.graph.add_widget(Label(text = str(i), pos = (i*px_point+center_x-50, center_y-63)))
                self.graph.add_widget(Label(text = str(i), pos = (center_x-60, i*px_point+center_y-50)))
            else:
                self.graph.add_widget(Label(text = str(i), pos = (i*px_point+center_x-60, center_y-63)))
        
sm = ScreenManager()
sm.add_widget(MainScreen(name = "main"))
sm.add_widget(GraphSettingsScreen(name = "gr_settings"))
sm.current = "main"


class TestApp(App):
    global px_point, center_y, center_x, sm
    def build(self):
        return sm

TestApp().run()
