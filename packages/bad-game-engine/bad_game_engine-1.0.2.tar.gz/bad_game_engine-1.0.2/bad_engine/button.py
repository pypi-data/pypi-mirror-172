from .game_object import Transform
from uuid import uuid4

def nothing() -> None:
    pass

class Button():
    """
    a button
    """

    def __init__(self, transform:Transform, bg="#ffffff", fg="#000000", text="", on_press= nothing, tags:list[str]=[], name="") -> None:
        self.__transform = transform
        self.__bg = bg
        self.__fg = fg
        self.__text = text
        self.__on_press = on_press
        self.__uuid = uuid4()
        self.initialized = False

    @property
    def transform(self) -> Transform:
        return self.__transform

    @property
    def background(self) -> str:
        return self.__bg

    @property
    def foreground(self) -> str:
        return self.__fg
    
    @property
    def text(self) -> str:
        return self.__text

    @property
    def on_press(self):
        return self.__on_press 
    
    @property
    def uuid(self) -> str:
        return self.__uuid
    
    def set_background(self, colour:str) -> None:
        self.__bg = colour
    
    def set_foreground(self, colour:str) -> None:
        self.__fg = colour
    
    def set_text(self, text:str) -> None:
        self.__text = text
    
    def on_destroy(self) -> None:
        pass

    def update(self, delta) -> None:
        pass
