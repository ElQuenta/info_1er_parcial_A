import math
import arcade
import pymunk
from game_logic import ImpulseVector


class Bird(arcade.Sprite):
    """
    Bird class. This represents an angry bird. All the physics is handled by Pymunk,
    the init method only set some initial properties
    """

    def __init__(
        self,
        image_path: str,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 5,
        radius: float = 12,
        max_impulse: float = 100,
        power_multiplier: float = 50,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
        has_been_clicked: bool = True,
    ):
        super().__init__(image_path, 1)
        # body
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)

        impulse = min(max_impulse, impulse_vector.impulse) * power_multiplier
        self.impulse = impulse_vector
        impulse_pymunk = impulse * pymunk.Vec2d(1, 0)
        # apply impulse
        body.apply_impulse_at_local_point(impulse_pymunk.rotated(impulse_vector.angle))
        # shape
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer

        self.space = space
        space.add(body, shape)

        self.body = body
        self.shape = shape
        self.has_been_clicked = has_been_clicked
        self.childs = []

    def update(self):
        """
        Update the position of the bird sprite based on the physics body position
        """
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle

    def on_click(self):
        pass


class Pig(arcade.Sprite):
    def __init__(
        self,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 0.4,
        collision_layer: int = 0,
    ):
        super().__init__("assets/img/pig_failed.png", 0.1)
        moment = pymunk.moment_for_circle(mass, 0, self.width / 2 - 3)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Circle(body, self.width / 2 - 3)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class PassiveObject(arcade.Sprite):
    """
    Passive object that can interact with other objects.
    """

    def __init__(
        self,
        image_path: str,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)
        moment = pymunk.moment_for_box(mass, (self.width, self.height))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle

class Column(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/column.png", x, y, space)


class StaticObject(arcade.Sprite):
    def __init__(
        self,
        image_path: str,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)


class Blues(Bird):
    def __init__(
        self,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
        has_been_clicked: bool = False,
    ):
        super().__init__(
            "assets/img/blue.png",
            impulse_vector,
            x,
            y,
            space,
            mass=3,
            radius=8,
            max_impulse=80,
            has_been_clicked=has_been_clicked,
        )
        self.scale = 0.1

    def on_click(self):
        if not self.has_been_clicked:
            angle_variation = 0.4
            impulse_variation = 20
            self.has_been_clicked = True
            impulse_Jim = ImpulseVector(
                self.impulse.angle + angle_variation - 0.1,
                self.impulse.impulse - impulse_variation,
            )
            impulse_Jake = ImpulseVector(
                self.impulse.angle - angle_variation,
                self.impulse.impulse - impulse_variation,
            )
            self.childs.append(
                Blues(impulse_Jim, self.center_x, self.center_y, self.space, True)
            )
            self.childs.append(
                Blues(impulse_Jake, self.center_x, self.center_y, self.space, True)
            )


class Terence(Bird):
    def __init__(
        self,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
    ):
        super().__init__(
            "assets\img\Terence.png",
            impulse_vector,
            x,
            y,
            space,
            mass=10,
            radius=20,
            max_impulse=120,
            power_multiplier=60,
        )
        self.scale = 0.06

class Red(Bird):
    def __init__(
        self,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
    ):
        super().__init__(
            "assets/img/red-bird3.png",
            impulse_vector,
            x,
            y,
            space,
        )

class Matilda(Bird):
    def __init__(
        self,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
    ):
        super().__init__(
            "assets\img\Matilda.png",
            impulse_vector,
            x,
            y,
            space,
            mass=6,
            radius=15,
            max_impulse=90,
            power_multiplier=55,
            has_been_clicked=False,
        )
        self.scale = 0.03

    def on_click(self):
        if not self.has_been_clicked:
            self.has_been_clicked = True
            egg = PassiveObject(
                "assets\img\egg.png",
                self.body.position.x,
                self.body.position.y,
                self.space,
            )
            self.childs.append(egg)
class Chuck(Bird):
    def __init__(
        self,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space,
    ):
        super().__init__(
            "assets/img/chuck_1.png",
            impulse_vector,
            x,
            y,
            space,
            max_impulse=200,
            power_multiplier=60,
            has_been_clicked=False,
        )
        self.scale = 0.03

    def on_click(self):
        if not self.has_been_clicked:
            self.has_been_clicked = True
            impulse = 2 * self.body.velocity.length
            impulse_vector = pymunk.Vec2d(impulse, 0).rotated(self.body.angle)
            self.body.apply_impulse_at_local_point(impulse_vector)