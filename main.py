import pgzrun
import re

# Constantes
TILE_SIZE = 32

# Dimensiones de la matriz
# Obtener dimensiones del archivo mapa.txt
with open('mapa.txt', 'r') as f:
    content = f.read()
    # Obtener dimensiones del string "Matrix Size: 10x15"
    for line in content.split('\n'):
        if "Matrix Size:" in line:
            dimensions = line.split(':')[1].strip().split('x')
            MATRIZ_ALTO = int(dimensions[0])
            MATRIZ_ANCHO = int(dimensions[1])
            break

# Dimensiones de la ventana
WIDTH = MATRIZ_ANCHO * TILE_SIZE
HEIGHT = MATRIZ_ALTO * TILE_SIZE
GRAVEDAD = 0.8
VELOCIDAD_SALTO = -15

# Tamaño de la hitbox del personaje
HITBOX_WIDTH = TILE_SIZE * 0.6
HITBOX_HEIGHT = TILE_SIZE * 0.6

# Lista de elementos colisionables
ELEMENTOS_COLISIONABLES = [1]
ITEMS_COLISIONABLES = [5]
OBJETOS_INTERACTIVOS = [4]

personaje = Actor("personajes/tile0")
personaje.velocidad_y = 0
personaje.en_suelo = False
personaje.objetos_cerca = []

# Diccionario para mapear IDs numéricos a rutas de imágenes
id_to_image = {}

# Cargar mapas desde archivo
with open('mapa.txt', 'r') as f:
    content = f.read()
    # Ejecutar el contenido del archivo para cargar las matrices
    exec(content)
    
    # Procesar el mapeo de IDs
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
            # Extraer el ID numérico y la ruta de la imagen
            parts = line[1:].strip().split(':')
            if len(parts) == 2:
                num_id = int(parts[0].strip())
                # Extraer la ruta de la imagen del paréntesis
                image_path = parts[1].strip()
                if '(' in image_path and ')' in image_path:
                    image_path = image_path[image_path.find('(')+1:image_path.find(')')]
                    # Quitar ceros a la izquierda en el nombre del archivo
                    image_path = re.sub(r'tile0*([0-9]+)\.png', r'tile\1.png', image_path)
                    id_to_image[num_id] = image_path

# Expandir el mapa base a 30x10 rellenando con 0s
expanded_map = []
for row in my_map:
    new_row = row + [0] * (30 - len(row))
    expanded_map.append(new_row)
while len(expanded_map) < 10:
    expanded_map.append([0] * 30)
my_map = expanded_map

# Expandir items a 30x10 rellenando con 0s
expanded_items = []
for row in my_items:
    new_row = row + [0] * (30 - len(row))
    expanded_items.append(new_row)
while len(expanded_items) < 10:
    expanded_items.append([0] * 30)
my_items = expanded_items

# Expandir rotaciones a 30x10 rellenando con 0s
expanded_rotations = []
for row in my_rotations:
    new_row = row + [0] * (30 - len(row))
    expanded_rotations.append(new_row)
while len(expanded_rotations) < 10:
    expanded_rotations.append([0] * 30)
my_rotations = expanded_rotations

# Estado del juego
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
    x_centro = x + TILE_SIZE - 10
    y_centro = y + TILE_SIZE
    
    puntos_colision = [
        (x_centro - HITBOX_WIDTH, y_centro - HITBOX_HEIGHT/2),    # Punto superior izquierdo medio
        (x_centro, y_centro - HITBOX_HEIGHT/2),                   # Punto superior derecho medio
        (x_centro - HITBOX_WIDTH, y_centro - HITBOX_HEIGHT),      # Punto superior izquierdo
        (x_centro, y_centro - HITBOX_HEIGHT),                     # Punto superior derecho
        (x_centro - HITBOX_WIDTH, y_centro),                      # Punto inferior izquierdo
        (x_centro, y_centro)                                      # Punto inferior derecho
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def verificar_colision_vertical(x, y):
    x_centro = x + TILE_SIZE
    y_centro = y + TILE_SIZE
    
    puntos_colision = [
        (x_centro - HITBOX_WIDTH/2, y_centro - HITBOX_HEIGHT),
        (x_centro - HITBOX_WIDTH/2, y_centro),
        (x_centro - HITBOX_WIDTH, y_centro - HITBOX_HEIGHT),
        (x_centro, y_centro - HITBOX_HEIGHT),
        (x_centro - HITBOX_WIDTH, y_centro),
        (x_centro, y_centro)
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
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
            
            if item_id in OBJETOS_INTERACTIVOS:
                dist_x = (x * TILE_SIZE + TILE_SIZE/2) - (personaje.x + TILE_SIZE/2)
                dist_y = (y * TILE_SIZE + TILE_SIZE/2) - (personaje.y + TILE_SIZE/2)
                distancia = (dist_x**2 + dist_y**2)**0.5
                
                if distancia <= radio_interaccion:
                    personaje.objetos_cerca.append((x, y, item_id))

def update():
    global game_over
    
    if game_over:
        return
        
    personaje.velocidad_y += GRAVEDAD
    
    nueva_y = personaje.y + personaje.velocidad_y
    if not verificar_colision_vertical(personaje.x, nueva_y):
        personaje.y = nueva_y
        personaje.en_suelo = False
    else:
        if personaje.velocidad_y > 0:
            personaje.en_suelo = True
        personaje.velocidad_y = 0
    
    if personaje.y >= HEIGHT - TILE_SIZE:
        personaje.y = HEIGHT - TILE_SIZE
        personaje.velocidad_y = 0
        personaje.en_suelo = True
    
    personaje.x = max(0, min(WIDTH - TILE_SIZE, personaje.x))
    
    verificar_interaccion()

def on_key_down(key):
    global game_over, modo_desarrollador, personaje_direccion
    
    if game_over:
        if key == keys.R:
            game_over = False
            personaje.x = 0
            personaje.y = 0
            personaje.velocidad_x = 0
            personaje.velocidad_y = 0
            return
    
    if key == keys.F:
        modo_desarrollador = not modo_desarrollador
            
    if key == keys.SPACE and personaje.en_suelo:
        personaje.velocidad_y = VELOCIDAD_SALTO
        personaje.en_suelo = False
    
    if key == keys.LEFT:
        nueva_x = personaje.x - TILE_SIZE
        if nueva_x >= 0 and not verificar_colision_horizontal(nueva_x, personaje.y):
            personaje.x = nueva_x
        personaje.image = "personajes/tile1"
        personaje_direccion = -1
    if key == keys.RIGHT:
        nueva_x = personaje.x + TILE_SIZE
        if nueva_x <= WIDTH - TILE_SIZE and not verificar_colision_horizontal(nueva_x, personaje.y):
            personaje.x = nueva_x
        personaje.image = "personajes/tile0"
        personaje_direccion = 1
    
    if key == keys.E and personaje.objetos_cerca:
        x, y, item_id = personaje.objetos_cerca[0]
        my_items[y][x] = 0
        personaje.objetos_cerca.remove((x, y, item_id))

def draw():
    screen.clear()

    for fila in range(len(my_map)):
        for columna in range(len(my_map[0])):
            x = columna * TILE_SIZE
            y = fila * TILE_SIZE

            # Dibujar tile del mapa base
            tile_id = my_map[fila][columna]
            if tile_id != 0 and tile_id in id_to_image:
                tile_actor = Actor(id_to_image[tile_id], topleft=(x, y))
                tile_actor.draw()

            # Dibujar item
            item_id = my_items[fila][columna]
            if item_id != 0 and item_id in id_to_image:
                item_actor = Actor(id_to_image[item_id], topleft=(x, y))
                item_actor.draw()
                
                if item_id in OBJETOS_INTERACTIVOS and any(x == columna and y == fila for x, y, _ in personaje.objetos_cerca):
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
        screen.draw.rect(
            Rect(
                personaje.x,
                personaje.y,
                TILE_SIZE,
                TILE_SIZE
            ),
            (255, 0, 0)
        )

        screen.draw.text("Modo Desarrollador: ON", (10, 30), color="yellow")

pgzrun.go()