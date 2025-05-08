import pgzrun

# Constantes
TILE_SIZE = 32
WIDTH = 15 * TILE_SIZE
HEIGHT = 10 * TILE_SIZE
GRAVEDAD = 0.8
VELOCIDAD_SALTO = -15
VELOCIDAD_MOVIMIENTO = 5
ACELERACION = 0.5
FRICCION = 0.85

# Tamaño de la hitbox del personaje (más pequeña que el tile)
HITBOX_WIDTH = TILE_SIZE * 0.8
HITBOX_HEIGHT = TILE_SIZE * 0.8

# Lista de elementos colisionables
ELEMENTOS_COLISIONABLES = [2, 3]  # IDs de los tiles con los que colisiona el personaje
ITEMS_COLISIONABLES = [5]  # IDs de los items con los que colisiona el personaje

personaje = Actor("creature", topleft = (200, 100))
personaje.velocidad_y = 0
personaje.velocidad_x = 0
personaje.en_suelo = False

# Mapa base
my_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [2,2,1,1,1,1,1,1,1,1,1,2,1,1,1],
    [2,2,1,1,2,2,1,1,1,1,2,2,2,1,1],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
]

# Ítems sobre el mapa
my_items = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,4,0,5,0,0,0,0,0,0,5,4,0,0],
    [0,0,5,5,5,0,0,4,0,0,0,5,5,0,0],
    [0,0,0,0,0,0,0,5,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

def obtener_tile_en_posicion(x, y):
    columna = int(x // TILE_SIZE)
    fila = int(y // TILE_SIZE)
    
    # Verificar límites del mapa
    if 0 <= fila < len(my_map) and 0 <= columna < len(my_map[0]):
        return my_map[fila][columna], my_items[fila][columna]
    return None, None

def verificar_colision_horizontal(x, y):
    # Ajustar las coordenadas para el punto topleft
    x_centro = x + TILE_SIZE // 2
    y_centro = y + TILE_SIZE // 2
    
    # Solo verificar los puntos laterales
    puntos_colision = [
        (x_centro - HITBOX_WIDTH/2, y_centro),   # Centro izquierda
        (x_centro + HITBOX_WIDTH/2, y_centro),   # Centro derecha
        (x_centro - HITBOX_WIDTH/2, y_centro - HITBOX_HEIGHT/3),  # Izquierda superior
        (x_centro + HITBOX_WIDTH/2, y_centro - HITBOX_HEIGHT/3),  # Derecha superior
        (x_centro - HITBOX_WIDTH/2, y_centro + HITBOX_HEIGHT/3),  # Izquierda inferior
        (x_centro + HITBOX_WIDTH/2, y_centro + HITBOX_HEIGHT/3)   # Derecha inferior
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        # Verificar si el tile o el item está en la lista de elementos colisionables
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def verificar_colision_vertical(x, y):
    # Ajustar las coordenadas para el punto topleft
    x_centro = x + TILE_SIZE // 2
    y_centro = y + TILE_SIZE // 2
    
    # Solo verificar los puntos superior e inferior
    puntos_colision = [
        (x_centro, y_centro - HITBOX_HEIGHT/2),  # Centro superior
        (x_centro, y_centro + HITBOX_HEIGHT/2),  # Centro inferior
        (x_centro - HITBOX_WIDTH/3, y_centro - HITBOX_HEIGHT/2),  # Izquierda superior
        (x_centro + HITBOX_WIDTH/3, y_centro - HITBOX_HEIGHT/2),  # Derecha superior
        (x_centro - HITBOX_WIDTH/3, y_centro + HITBOX_HEIGHT/2),  # Izquierda inferior
        (x_centro + HITBOX_WIDTH/3, y_centro + HITBOX_HEIGHT/2)   # Derecha inferior
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        # Verificar si el tile o el item está en la lista de elementos colisionables
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def update():
    # Aplicar gravedad
    personaje.velocidad_y += GRAVEDAD
    
    # Aplicar fricción horizontal
    personaje.velocidad_x *= FRICCION
    
    # Movimiento horizontal
    if keyboard.left:
        personaje.velocidad_x -= ACELERACION
    if keyboard.right:
        personaje.velocidad_x += ACELERACION
    
    # Limitar velocidad horizontal
    personaje.velocidad_x = max(-VELOCIDAD_MOVIMIENTO, min(VELOCIDAD_MOVIMIENTO, personaje.velocidad_x))
    
    # Intentar mover horizontalmente
    nueva_x = personaje.x + personaje.velocidad_x
    if not verificar_colision_horizontal(nueva_x, personaje.y):
        personaje.x = nueva_x
    
    # Intentar mover verticalmente
    nueva_y = personaje.y + personaje.velocidad_y
    if not verificar_colision_vertical(personaje.x, nueva_y):
        personaje.y = nueva_y
        personaje.en_suelo = False
    else:
        # Si hay colisión, detener el movimiento vertical
        if personaje.velocidad_y > 0:  # Si está cayendo
            personaje.en_suelo = True
        personaje.velocidad_y = 0
    
    # Verificar colisión con el suelo
    if personaje.y >= HEIGHT - TILE_SIZE:
        personaje.y = HEIGHT - TILE_SIZE
        personaje.velocidad_y = 0
        personaje.en_suelo = True
    
    # Mantener al personaje dentro de los límites horizontales
    personaje.x = max(0, min(WIDTH - TILE_SIZE, personaje.x))

def on_key_down(key):
    # Salto
    if key == keys.SPACE and personaje.en_suelo:
        personaje.velocidad_y = VELOCIDAD_SALTO
        personaje.en_suelo = False

def draw():
    screen.clear()

    for fila in range(len(my_map)):
        for columna in range(len(my_map[0])):
            x = columna * TILE_SIZE
            y = fila * TILE_SIZE

            # Dibuja el fondo del mapa (tiles)
            tile_id = my_map[fila][columna]
            tile_name = "tile" + str(tile_id)  # Ajusta el nombre de la imagen
            tile_actor = Actor(tile_name, (x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            tile_actor.draw()

            # Dibuja los ítems sobre el mapa
            item_id = my_items[fila][columna]
            if item_id != 0:  # Si hay un ítem (no es 0)
                item_name = "tile" + str(item_id)  # Usa el mismo formato de nombre
                item_actor = Actor(item_name, (x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                item_actor.draw()

    personaje.draw()
    
    # Dibujar hitbox (para debug)
    # screen.draw.rect(Rect((personaje.x + TILE_SIZE//2 - HITBOX_WIDTH/2, 
    #                       personaje.y + TILE_SIZE//2 - HITBOX_HEIGHT/2), 
    #                      (HITBOX_WIDTH, HITBOX_HEIGHT)), (255, 0, 0))

pgzrun.go()
