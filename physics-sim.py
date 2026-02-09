import pyglet
from pyglet import shapes
import random

window = pyglet.window.Window(800, 600, "Collision Physics Simulator")
batch = pyglet.graphics.Batch()

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-100, 100)
        self.vy = random.uniform(0, 200)
        self.radius = radius
        self.circle = shapes.Circle(x, y, radius, color=color, batch=batch)
        
    def update(self, dt):
        # Gravity
        self.vy -= 500 * dt
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Bounce off walls (left/right)
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -0.9
        elif self.x + self.radius > 800:
            self.x = 800 - self.radius
            self.vx *= -0.9
            
        # Bounce off floor
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -0.9
            
        # Update circle position
        self.circle.x = self.x
        self.circle.y = self.y

# Create some balls
balls = [
    Ball(200, 400, 20, (255, 0, 0)),
    Ball(400, 500, 30, (0, 0, 255)),
    Ball(600, 300, 25, (0, 255, 0))
]

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    # Click to add new balls!
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    balls.append(Ball(x, y, random.randint(15, 35), color))

def update(dt):
    for ball in balls:
        ball.update(dt)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
