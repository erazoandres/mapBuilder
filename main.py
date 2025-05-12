import pgzrun
import re

# Constantes
TILE_SIZE = 32

# Dimensiones de la matriz
with open('mapa.txt', 'r') as f:
    content = f.read()
    for line in content.split('\n'):
        if "Matrix Size:" in line:
            dimensions = line.split(':')[1].strip().split('x')
            MATRIZ_ALTO = int(dimensions[0])
            MATRIZ_ANCHO = int(dimensions[1])
            break

WIDTH = MATRIZ_ANCHO * TILE_SIZE
HEIGHT = MATRIZ_ALTO * TILE_SIZE
GRAVEDAD = 0.8
VELOCIDAD_SALTO = -15
VELOCIDAD_MOVIMIENTO = 3  # Nueva constante para la velocidad de movimiento

HITBOX_WIDTH = TILE_SIZE
HITBOX_HEIGHT = TILE_SIZE

TERRENOS = []
ITEMS = []
OBJETOS = []
ENEMIGOS = []


personaje = Actor("personajes/tile0")
personaje.velocidad_y = 0
personaje.velocidad_x = 0  # Nueva variable para velocidad horizontal
personaje.en_suelo = False
personaje.objetos_cerca = []

with open('mapa.txt', 'r') as f:
    content = f.read()
    in_mapping = False
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# ID Mapping'):
            in_mapping = True
            continue
        elif line.startswith('# End ID Mapping'):
            break
        elif in_mapping and line.startswith('#'):
            parts = line[1:].strip().split(':')
            if len(parts) == 2:
                descripcion = parts[1].lower()
                id_val = int(parts[0].strip())
                if 'terreno' in descripcion:
                    TERRENOS.append(id_val)
                if 'items' in descripcion:
                    ITEMS.append(id_val)
                if 'objeto' in descripcion:
                    OBJETOS.append(id_val)

id_to_image = {}

with open('mapa.txt', 'r') as f:
    content = f.read()
    exec(content)

    in_mapping = False
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# ID Mapping'):
            in_mapping = True
            continue
        elif line.startswith('# End ID Mapping'):
            in_mapping = False
            continue
        elif in_mapping and line.startswith('#'):
            parts = line[1:].strip().split(':')
            if len(parts) == 2:
                num_id = int(parts[0].strip())
                image_path = parts[1].strip()
                if '(' in image_path and ')' in image_path:
                    image_path = image_path[image_path.find('(')+1:image_path.find(')')]
                    image_path = re.sub(r'tile0*([0-9]+)\.png', r'tile\1.png', image_path)
                    id_to_image[num_id] = image_path

expanded_map = []
for row in my_map:
    new_row = row + [0] * (30 - len(row))
    expanded_map.append(new_row)
while len(expanded_map) < 10:
    expanded_map.append([0] * 30)
my_map = expanded_map

expanded_items = []
for row in my_items:
    new_row = row + [0] * (30 - len(row))
    expanded_items.append(new_row)
while len(expanded_items) < 10:
    expanded_items.append([0] * 30)
my_items = expanded_items

expanded_rotations = []
for row in my_rotations:
    new_row = row + [0] * (30 - len(row))
    expanded_rotations.append(new_row)
while len(expanded_rotations) < 10:
    expanded_rotations.append([0] * 30)
my_rotations = expanded_rotations

game_over = False
modo_desarrollador = False
personaje_direccion = 0

def obtener_tile_en_posicion(x, y):
    columna = int(x // TILE_SIZE)
    fila = int(y // TILE_SIZE)
    if 0 <= fila < len(my_map) and 0 <= columna < len(my_map[0]):
        return my_map[fila][columna], my_items[fila][columna]
    return None, None

def verificar_colision_horizontal(x, y):
    for offset_y in [1, TILE_SIZE - 2]:
        for offset_x in [0, TILE_SIZE - 1]:
            tile_id, item_id = obtener_tile_en_posicion(x + offset_x, y + offset_y)
            if (tile_id in TERRENOS) or (item_id in ITEMS):
                return True
    return False

def verificar_colision_vertical(x, y):
    for offset_x in [1, TILE_SIZE - 2]:
        for offset_y in [0, TILE_SIZE - 1]:
            tile_id, item_id = obtener_tile_en_posicion(x + offset_x, y + offset_y)
            if (tile_id in TERRENOS) or (item_id in ITEMS):
                return True
    return False

def verificar_interaccion():
    personaje.objetos_cerca = []
    radio_interaccion = TILE_SIZE * 1.5
    inicio_x = max(0, int((personaje.x - radio_interaccion) // TILE_SIZE))
    fin_x = min(len(my_map[0]), int((personaje.x + radio_interaccion) // TILE_SIZE) + 1)
    inicio_y = max(0, int((personaje.y - radio_interaccion) // TILE_SIZE))
    fin_y = min(len(my_map), int((personaje.y + radio_interaccion) // TILE_SIZE) + 1)

    for y in range(inicio_y, fin_y):
        for x in range(inicio_x, fin_x):
            tile_id, item_id = my_map[y][x], my_items[y][x]
            if item_id in OBJETOS:
                dist_x = (x * TILE_SIZE + TILE_SIZE/2) - (personaje.x + TILE_SIZE/2)
                dist_y = (y * TILE_SIZE + TILE_SIZE/2) - (personaje.y + TILE_SIZE/2)
                distancia = (dist_x**2 + dist_y**2)**0.5
                if distancia <= radio_interaccion:
                    personaje.objetos_cerca.append((x, y, item_id))

def update():
    global game_over
    if game_over:
        return

    # Aplicar gravedad
    personaje.velocidad_y += GRAVEDAD
    
    # Actualizar posición vertical
    nueva_y = personaje.y + personaje.velocidad_y
    if not verificar_colision_vertical(personaje.x, nueva_y):
        personaje.y = nueva_y
        personaje.en_suelo = False
    else:
        if personaje.velocidad_y > 0:
            personaje.en_suelo = True
        personaje.velocidad_y = 0

    # Actualizar posición horizontal
    nueva_x = personaje.x + personaje.velocidad_x
    if not verificar_colision_horizontal(nueva_x, personaje.y):
        personaje.x = nueva_x
    else:
        personaje.velocidad_x = 0

    # Mantener al personaje dentro de los límites
    personaje.x = max(0, min(WIDTH - TILE_SIZE, personaje.x))
    if personaje.y >= HEIGHT - TILE_SIZE:
        personaje.y = HEIGHT - TILE_SIZE
        personaje.velocidad_y = 0
        personaje.en_suelo = True

    # Actualizar dirección del personaje
    if personaje.velocidad_x > 0:
        personaje.image = "personajes/tile0"
    elif personaje.velocidad_x < 0:
        personaje.image = "personajes/tile1"

    verificar_interaccion()

def on_key_down(key):
    global game_over, modo_desarrollador

    if game_over:
        if key == keys.R:
            game_over = False
            personaje.x = 0
            personaje.y = 0
            personaje.velocidad_y = 0
            personaje.velocidad_x = 0
            return

    if key == keys.F:
        modo_desarrollador = not modo_desarrollador

    if key == keys.SPACE and personaje.en_suelo:
        personaje.velocidad_y = VELOCIDAD_SALTO
        personaje.en_suelo = False

    if key == keys.E and personaje.objetos_cerca:
        x, y, item_id = personaje.objetos_cerca[0]
        my_items[y][x] = 0
        personaje.objetos_cerca.remove((x, y, item_id))

    # Movimiento horizontal
    if key == keys.LEFT:
        personaje.velocidad_x = -VELOCIDAD_MOVIMIENTO
    elif key == keys.RIGHT:
        personaje.velocidad_x = VELOCIDAD_MOVIMIENTO

def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        personaje.velocidad_x = 0

def draw():
    screen.clear()

    for fila in range(len(my_map)):
        for columna in range(len(my_map[0])):
            x = columna * TILE_SIZE
            y = fila * TILE_SIZE

            tile_id = my_map[fila][columna]
            if tile_id != 0 and tile_id in id_to_image:
                tile_actor = Actor(id_to_image[tile_id], topleft=(x, y))
                tile_actor.draw()

            item_id = my_items[fila][columna]
            if item_id != 0 and item_id in id_to_image:
                item_actor = Actor(id_to_image[item_id], topleft=(x, y))
                item_actor.draw()

                if item_id in OBJETOS and any(x == columna and y == fila for x, y, _ in personaje.objetos_cerca):
                    for i in range(4):
                        screen.draw.line((x + i, y + i), (x + TILE_SIZE - i, y + i), (255, 255, 0))
                        screen.draw.line((x + i, y + i), (x + i, y + TILE_SIZE - i), (255, 255, 0))
                        screen.draw.line((x + TILE_SIZE - i, y + i), (x + TILE_SIZE - i, y + TILE_SIZE - i), (255, 255, 0))
                        screen.draw.line((x + i, y + TILE_SIZE - i), (x + TILE_SIZE - i, y + TILE_SIZE - i), (255, 255, 0))

    personaje_actor = Actor(personaje.image, bottomright=(personaje.x + TILE_SIZE, personaje.y + TILE_SIZE))
    personaje_actor.draw()

    if personaje.objetos_cerca:
        screen.draw.text("Presiona E para interactuar", (10, 10), color="white")

    if game_over:
        screen.draw.text("¡Has perdido!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
        screen.draw.text("Presiona R para reiniciar", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")

    if modo_desarrollador:
        screen.draw.rect(Rect(personaje.x, personaje.y, TILE_SIZE, TILE_SIZE), (255, 0, 0))
        screen.draw.text("Modo Desarrollador: ON", (10, 30), color="yellow")

pgzrun.go()
