import pyglet
from pyglet import shapes
import random
import math



window = pyglet.window.Window(800, 600, "Collision Physics Simulator")
batch = pyglet.graphics.Batch()

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y

        #self.vx = random.uniform(-100, 100)
        #self.vy = random.uniform(0, 200)
        self.vy = (100)
        self.vx = (50)

        self.radius = radius
        self.mass = radius
        self.circle = shapes.Circle(x, y, radius, color=color, batch=batch)
        
    def update(self, dt):
        #gravity
        self.vy -= 500 * dt
        
        #update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        #bounce walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -0.9
        elif self.x + self.radius > 800:
            self.x = 800 - self.radius
            self.vx *= -0.9
            
        #bounce floor
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -0.9
        
        #bounce ceiling - needs fixing
        #elif self.y + self.radius > 600:
        #    self.y = 600 - self.radius
        #    self.vy *= -0.9

        #update circle position
        self.circle.x = self.x
        self.circle.y = self.y

def check_collision(ball1, ball2):
    #calc distance
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.sqrt(dx**2 + dy**2)

    #check if touching
    if distance < ball1.radius + ball2.radius and distance > 0:

        #collision normal
        nx = dx / distance
        ny = dy / distance

        #separate balls
        overlap = (ball1.radius + ball2.radius) - distance
        ball1.x -= nx * overlap * 0.5
        ball1.y -= ny * overlap * 0.5
        ball2.x += nx * overlap * 0.5
        ball2.y += ny * overlap * 0.5

        dvx = ball2.vx - ball1.vx
        dvy = ball2.vy - ball1.vy

        #relative velocity along normal
        dvn = dvx * nx + dvy * ny

        if dvn > 0:
            return
        
        #calc impulse
        restitution = 0.9 #change from 0 to inf 
        impulse = (-(1 + restitution) * dvn) / (1/ball1.mass + 1/ball2.mass)

        #apply impulse
        ball1.vx -= (impulse / ball1.mass) * nx
        ball1.vy -= (impulse / ball1.mass) * ny
        ball2.vx += (impulse / ball2.mass) * nx
        ball2.vy += (impulse / ball2.mass) * ny

#create balls
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
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    balls.append(Ball(x, y, random.randint(15, 35), color))

def update(dt):
    for ball in balls:
        ball.update(dt)

    #check collisions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            check_collision(balls[i], balls[j])

pyglet.clock.schedule_interval(update, 1/600.0)
pyglet.app.run()
