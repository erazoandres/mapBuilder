
import pgzrun

WIDTH = 512
HEIGHT = 256

# Animaciones y frames por tipo
animations = {
    "idle": [f"idle{i}" for i in range(8)],
    "walk": [f"walk{i}" for i in range(8)],
    "jump": [f"jump{i}" for i in range(8)],
    "attack": [f"attack{i}" for i in range(8)],
}

# Configuración inicial
current_animation = "idle"
frame_index = 0
frame_delay = 6
frame_timer = 0

def update():
    global frame_index, frame_timer
    frame_timer += 1
    if frame_timer >= frame_delay:
        frame_timer = 0
        frame_index = (frame_index + 1) % len(animations[current_animation])

def draw():
    screen.clear()
    frame_name = animations[current_animation][frame_index]
    screen.blit(frame_name, (WIDTH // 2 - 32, HEIGHT // 2 - 32))

def on_key_down(key):
    global current_animation
    if key == keys.RIGHT:
        current_animation = "walk"
    elif key == keys.UP:
        current_animation = "jump"
    elif key == keys.SPACE:
        current_animation = "attack"
    elif key == keys.DOWN:
        current_animation = "idle"



pgzrun.go()