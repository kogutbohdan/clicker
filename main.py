from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen,TransitionBase
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.utils import platform
from random import choice

animation=Animation(size_hint_y=0.7,duration=0.1,background_color=(1,0,0,1)) + Animation(size_hint_y=1,duration=0.1,background_color=(1,1,1,1))

class ButtonMenuLevels(Button):
    switch_to_level=None

class Zombi(Button):
    pass

class MenuScreen(Screen):
    pass
class Levels(MenuScreen):
    def __init__(self,sm, **kwargs):
        super().__init__(**kwargs)
        ButtonMenuLevels.switch_to_level=self.switch_to_level
        self.sm=sm


    def switch_to_level(self,instance):
        self.sm.current=instance.text

class GameScreen(Screen):
    def __init__(self,level,**kwargs):
        super().__init__(**kwargs)
        self.__init(level)

    def __init(self,level):
        box=BoxLayout(orientation="vertical",padding=(10,10))
        level.setParentWindow(self)
        level.setParrent(box)
        for child in level.children():
            box.add_widget(child)
        self.add_widget(box)

class Level:
    def __init__(self,maxNumbers,imgs,sm):
        self.number=0
        self.imgs=imgs
        self.maxNumbers=maxNumbers
        self.text=Label(text=f"Number click {self.number}")
        img=choice(imgs)
        self.zombi=Zombi(text="1", on_press=lambda elem:self.increment(elem), background_normal=img, background_down=img)
        self.lbl=Label(text="You winner")
        self.btnR=Button(text="Return menu",on_press=lambda inst:self.returnMenu())
        self.btnNextLevel=Button(text="Next level",on_press=lambda inst:self.nextLevel(inst))
        self.maxNumber=choice(maxNumbers)
        self.sm=sm

    def setParentWindow(self,parentWindow):
        self.parentWindow=parentWindow
    def setParrent(self,parent):
        self.parent=parent
    def children(self):
        return [self.text, self.zombi]

    def nextLevel(self,instance):
        self.returnMenu()
        if(self.parentWindow.name=="Level1"):
            self.sm.current="Level2"
        if(self.parentWindow.name=="Level2"):
            self.sm.current="Level3"
        if(self.parentWindow.name=="Level3"):
            self.sm.current="Level4"
        if(self.parentWindow.name=="Level4"):
            self.sm.current="Level1"

    def returnMenu(self):
        self.number=0
        self.maxNumber=choice(self.maxNumbers)
        img=choice(self.imgs)
        self.zombi.background_normal=img
        self.zombi.background_down=img
        self.parent.add_widget(self.text)
        self.parent.add_widget(self.zombi)
        self.parent.remove_widget(self.lbl)
        self.parent.remove_widget(self.btnR)
        self.parent.remove_widget(self.btnNextLevel)
        self.sm.current="menu"
    def increment(self,instance):
        animation.start(instance)
        self.number+=1
        if self.number>self.maxNumber:
            self.parent.add_widget(self.lbl)
            self.parent.add_widget(self.btnR)
            self.parent.remove_widget(self.text)
            self.parent.remove_widget(self.zombi)
            self.parent.add_widget(self.btnNextLevel)
        self.text.text=f"Number click {self.number}"

class MenuGame(MenuScreen):
    def __init__(self,sm,**kwargs):
        super().__init__(**kwargs)
        self.sm=sm

    def to_game(self):
        self.sm.current="menu"
class MainApp(App):
    def build(self):
        sm=ScreenManager()

        sm.add_widget(MenuGame(sm=sm))
        sm.add_widget(Levels(name="menu", sm=sm))
        sm.add_widget(GameScreen(name="Level1", level=Level(range(4, 10),
                                                            ['./imgs/pngwing.com.png', "./imgs/pngwing.com (3).png"],
                                                            sm=sm)))
        sm.add_widget(GameScreen(name="Level2", level=Level(range(10, 20), ["./imgs/pngwing.com (4).png",
                                                                            "./imgs/pngwing.com (5).png"], sm=sm)))
        sm.add_widget(GameScreen(name="Level3", level=Level(range(20, 60), ["./imgs/pngwing.com (6).png"], sm=sm)))
        sm.add_widget(GameScreen(name="Level4", level=Level(range(60, 100), ["./imgs/pngwing.com (2).png",
                                                                             "./imgs/pngwing.com (8).png"], sm=sm)))

        if platform != "android":
            Window.size=(400,800)
            Window.left=500
            Window.top=100
        return sm
MainApp().run()