import pgzrun

# Constantes
TILE_SIZE = 32

# Dimensiones de la matriz
MATRIZ_ANCHO = 30
MATRIZ_ALTO = 10

# Dimensiones de la ventana
WIDTH = MATRIZ_ANCHO * TILE_SIZE
HEIGHT = MATRIZ_ALTO * TILE_SIZE
GRAVEDAD = 0.8
VELOCIDAD_SALTO = -15
VELOCIDAD_ENEMIGO = 2

# Tamaño de la hitbox del personaje
HITBOX_WIDTH = TILE_SIZE * 0.6
HITBOX_HEIGHT = TILE_SIZE * 0.6

# Tamaño de la hitbox de los enemigos
ENEMY_HITBOX_WIDTH = TILE_SIZE * 0.6
ENEMY_HITBOX_HEIGHT = TILE_SIZE * 0.6

# Lista de elementos colisionables
ELEMENTOS_COLISIONABLES = [1]
ITEMS_COLISIONABLES = [5]
OBJETOS_INTERACTIVOS = [4]

# Lista de enemigos [x, y, velocidad_x, velocidad_y, dirección, en_suelo]
enemigos = [
    [200, 0, 0, 0, 1, False],
    [200, 190, 0, 0, 1, False],
    [250, 100, 0, 0, 1, False]
]

personaje = Actor("creature")
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

def verificar_colision_horizontal_enemigo(x, y):
    x_centro = x + TILE_SIZE
    y_centro = y + TILE_SIZE

    puntos_colision = [
        (x_centro - ENEMY_HITBOX_WIDTH/2, y_centro),
        (x_centro + ENEMY_HITBOX_WIDTH/2, y_centro),
        (x_centro - ENEMY_HITBOX_WIDTH/2, y_centro - ENEMY_HITBOX_HEIGHT/3),
        (x_centro + ENEMY_HITBOX_WIDTH/2, y_centro - ENEMY_HITBOX_HEIGHT/3),
        (x_centro - ENEMY_HITBOX_WIDTH/2, y_centro + ENEMY_HITBOX_HEIGHT/3),
        (x_centro + ENEMY_HITBOX_WIDTH/2, y_centro + ENEMY_HITBOX_HEIGHT/3)
    ]

    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def verificar_colision_vertical_enemigo(x, y):
    x_centro = x + TILE_SIZE
    y_centro = y + TILE_SIZE
    
    puntos_colision = [
        (x_centro, y_centro - ENEMY_HITBOX_HEIGHT/2),
        (x_centro, y_centro + ENEMY_HITBOX_HEIGHT/2),
        (x_centro - ENEMY_HITBOX_WIDTH/3, y_centro - ENEMY_HITBOX_HEIGHT/2),
        (x_centro + ENEMY_HITBOX_WIDTH/3, y_centro - ENEMY_HITBOX_HEIGHT/2),
        (x_centro - ENEMY_HITBOX_WIDTH/3, y_centro + ENEMY_HITBOX_HEIGHT/2),
        (x_centro + ENEMY_HITBOX_WIDTH/3, y_centro + ENEMY_HITBOX_HEIGHT/2)
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def verificar_colision_con_enemigo():
    personaje_centro_x = personaje.x + TILE_SIZE/2
    personaje_centro_y = personaje.y + TILE_SIZE/2
    
    personaje_izq = personaje_centro_x - HITBOX_WIDTH/2
    personaje_der = personaje_centro_x + HITBOX_WIDTH/2
    personaje_arriba = personaje_centro_y - HITBOX_HEIGHT/2
    personaje_abajo = personaje_centro_y + HITBOX_HEIGHT/2
    
    for enemigo in enemigos:
        enemigo_centro_x = enemigo[0] + TILE_SIZE/2
        enemigo_centro_y = enemigo[1] + TILE_SIZE/2
        
        enemigo_izq = enemigo_centro_x - ENEMY_HITBOX_WIDTH/2
        enemigo_der = enemigo_centro_x + ENEMY_HITBOX_WIDTH/2
        enemigo_arriba = enemigo_centro_y - ENEMY_HITBOX_HEIGHT/2
        enemigo_abajo = enemigo_centro_y + ENEMY_HITBOX_HEIGHT/2
        
        if (personaje_der > enemigo_izq and 
            personaje_izq < enemigo_der and 
            personaje_abajo > enemigo_arriba and 
            personaje_arriba < enemigo_abajo):
            return True
    return False

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

    for enemigo in enemigos:
        enemigo[3] += GRAVEDAD
        enemigo[2] = VELOCIDAD_ENEMIGO * enemigo[4]
        
        nueva_x = enemigo[0] + enemigo[2]
        
        if nueva_x <= 0 or nueva_x >= WIDTH - TILE_SIZE:
            enemigo[4] *= -1
        elif not verificar_colision_horizontal_enemigo(nueva_x, enemigo[1]):
            enemigo[0] = nueva_x
        else:
            enemigo[4] *= -1
        
        nueva_y = enemigo[1] + enemigo[3]
        if not verificar_colision_vertical_enemigo(enemigo[0], nueva_y):
            enemigo[1] = nueva_y
            enemigo[5] = False
        else:
            if enemigo[3] > 0:
                enemigo[5] = True
            enemigo[3] = 0
        
        if enemigo[1] >= HEIGHT - TILE_SIZE:
            enemigo[1] = HEIGHT - TILE_SIZE
            enemigo[3] = 0
            enemigo[5] = True

    if verificar_colision_con_enemigo():
        game_over = True

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
        personaje.image = "creature_left"
        personaje_direccion = -1
    if key == keys.RIGHT:
        nueva_x = personaje.x + TILE_SIZE
        if nueva_x <= WIDTH - TILE_SIZE and not verificar_colision_horizontal(nueva_x, personaje.y):
            personaje.x = nueva_x
        personaje.image = "creature"
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

    for enemigo in enemigos:
        enemy_actor = Actor("enemy1", bottomright=(enemigo[0] + TILE_SIZE, enemigo[1] + TILE_SIZE))
        enemy_actor.draw()
        
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

        for enemigo in enemigos:
            screen.draw.rect(
                Rect(
                    enemigo[0],
                    enemigo[1],
                    TILE_SIZE,
                    TILE_SIZE
                ),
                (0, 255, 0)
            )

        screen.draw.text("Modo Desarrollador: ON", (10, 30), color="yellow")

pgzrun.go()