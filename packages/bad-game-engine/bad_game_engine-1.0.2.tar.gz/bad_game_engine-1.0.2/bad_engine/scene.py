from __future__ import annotations
from tkinter import Button as bt, Tk, Canvas
from .game_object import Game_Object
from time import sleep, time
from .button import Button
from threading import Thread

class Scene:
    """
    the scene class where the game takes place
    """

    def __init__(self, objects:list[Game_Object]=[], name:str="", width="900", height="600", bg:str="#ffffff") -> None:
        self.__new_objects:list[Game_Object] = []
        self.__active_objects:list[Game_Object] = []
        self.__destroyed_objects:list[Game_Object] = []

        self.__name = name
        self.__width = width
        self.__height = height
        self.__bg = bg

        self.__destroyed = False
      
        for obj in objects:
            self.__new_objects.append(obj)

    def init_game_object(self, *obj:Game_Object) -> None:
        """
        initializes the given Game Objects into the scene
        """

        for object in obj:
            self.__new_objects.append(object)
    
    def destroy_game_object(self, *obj:Game_Object) -> None:
        """
        deletes the given Game Objects from the scene
        """
        for object in obj:
            if object in self.__active_objects: 
                self.__active_objects.remove(object)
            self.__destroyed_objects.append(object)
    
    def get_game_objects(self) -> list[Game_Object]:
        return self.__active_objects

    def destroy(self):
        """
        destroys the scene and closes the window
        """

        self.__destroyed = True

    def switch_scene(self, scene:Scene):
        self.destroy()
        thread = Thread(target=scene.startloop)
        thread.start()

    def startloop(self) -> None:
        """
        starts the main loop of the scene 
        """

        delta = 0

        # creates the window and canvas for the game
        window = Tk()
        window.title(self.__name)
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", self.destroy)

        canvas = Canvas(window, width=self.__width, height=self.__height, bg=self.__bg)
        canvas.pack()

        # a dictionary with references to functions for the shapes 
        shapes = {
            'rect': canvas.create_rectangle,
            'oval': canvas.create_oval,
            'arc': canvas.create_arc
        }

        while True:
            Time = time()
            # taking the objects from __new_objects and puts it in __active_objects
            for _ in range(len(self.__new_objects)):
                obj = self.__new_objects.pop(0)
                self.__active_objects.append(obj)

            # removing the destroyed objects from the scene
            for obj in self.__destroyed_objects:
                canvas.delete(obj.uuid)
                obj.on_destroy()
            
            self.__destroyed_objects.clear()

            # rendering the objects in __active_objects
            for obj in self.__active_objects:
                if type(obj) == Button:
                    if not obj.initialized: canvas.create_window(obj.transform.position.x, obj.transform.position.y, height=obj.transform.height, width=obj.transform.width, window=bt(background=obj.background, foreground=obj.foreground, text=obj.text, command=obj.on_press), tags=obj.uuid)
                    obj.initialized = True
                else:
                    canvas.delete(obj.uuid)
                    shapes[obj.shape](obj.transform.position.x, obj.transform.position.y, obj.transform.width+obj.transform.position.x, obj.transform.position.y+obj.transform.height, fill=obj.colour, outline=obj.colour, tags=obj.uuid)
                
            # calls the update method of every object in __active_objects
            for obj in self.__active_objects:
                try:
                    obj.update(delta)
                except Exception as e:
                    print(e)

                if self.__destroyed:
                    break

            if self.__destroyed:
                window.destroy()
                break

            window.update()
                
            delta = time() - Time
            if delta == 0:
                delta = 0.01
                sleep(0.01)