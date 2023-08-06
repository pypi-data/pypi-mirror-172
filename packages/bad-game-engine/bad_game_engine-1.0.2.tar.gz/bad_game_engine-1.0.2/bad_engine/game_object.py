from .vector import Vector
from uuid import uuid4

RECT = 'rect'
OVAL = 'oval'
ARC = 'arc'

class Transform:
    """
    the Transform class that holds the position, width, and height of a Game Object
    """

    def __init__(self, x:float, y:float, width:float, height:float):
        self.__position = Vector(x, y)
        self.__width = width
        self.__height = height
    
    def __repr__(self):
        return f"position: {self.__position}, width: {self.__width}, height: {self.__height}"

    def set_position(self, x:float=None, y:float=None) -> None:
        """
        changes position 
        """

        self.__position = Vector(x or self.__position.x, y or self.__position.y)
    
    def set_dimensions(self, width:float=None, height:float=None) -> None:
        """
        changes the width and/or height 
        """

        self.__width = width or self.__width
        self.__height = height or self.__height

    def move_towards(self, speed: float, position: Vector) -> None:
        """
        moves the Game Object that holds the Transform to a a specified positon at the given speed 
        """

        if self.position.x > position.x:
            x = self.position.x - speed
            if x < position.x:
                x = position.x
        else: 
            x = self.position.x + speed
            if x > position.x:
                x = position.x

        if self.position.y > position.y:
            y = self.position.y - speed
            if y < position.y:
                y = position.y
        else:
            y = self.position.y + speed
            if y > position.y:
                y = position.y
        
        self.set_position(x, y)

    @property
    def position(self) -> Vector:
        return self.__position

    @property
    def width(self) -> int | float:
        return self.__width
    
    @property
    def height(self) -> int | float:
        return self.__height
    
    @property
    def center(self) -> float:
        return Vector(self.__position.x + self.__width / 2, self.__position.y + self.__height / 2)

class Game_Object:
    """
    basic Game Object that is part of a scene
    """

    def __init__(self, transform:Transform, tags:list[str]=None, name:str=None, shape=RECT, colour:str="#000000") -> None:
        self.__transform = transform
        self.__colour = colour
        self.__uuid = uuid4()
        self.__tags = tags
        self.__name = name
        self.__shape = shape

    def __repr__(self) -> str:
        return f"{{tags: {self.__tags}, name: {self.__name}, shape: {self.__shape}, colour: {self.__colour}, uuid: {self.__uuid}}}"

    @property
    def transform(self) -> Transform:
        return self.__transform
    
    @property
    def tags(self) -> list[str]:
        return self.__tags
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def shape(self) -> str:
        return self.__shape

    @property
    def colour(self) -> str:
        return self.__colour
    
    @property
    def uuid(self) -> str:
        return self.__uuid
    
    def set_tags(self, tags:list[str]) -> None:
        self.__tags = tags
    
    def set_name(self, name:str) -> None:
        self.__name = name
    
    def set_shape(self, shape) -> None:
        self.__shape = shape
    
    def set_colour(self, colour:str) -> None:
        self.__colour = colour

    def on_destroy(self) -> None:
        pass

    def update(self, delta) -> None:
        pass