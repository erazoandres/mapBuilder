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
VELOCIDAD_ENEMIGO = 2

# Tamaño de la hitbox del personaje (más pequeña que el tile)
HITBOX_WIDTH = TILE_SIZE * 0.8
HITBOX_HEIGHT = TILE_SIZE * 0.8

# Tamaño de la hitbox de los enemigos
ENEMY_HITBOX_WIDTH = TILE_SIZE * 0.8
ENEMY_HITBOX_HEIGHT = TILE_SIZE * 0.9  # Aumentamos la altura para que se detenga más arriba

# Lista de elementos colisionables
ELEMENTOS_COLISIONABLES = [2, 3]  # IDs de los tiles con los que colisiona el personaje
ITEMS_COLISIONABLES = [5]  # IDs de los items con los que colisiona el personaje
OBJETOS_INTERACTIVOS = [4]  # IDs de los objetos con los que se puede interactuar

# Lista de enemigos [x, y, velocidad_x, velocidad_y, dirección, en_suelo]
enemigos = [
    [200, 180, 0, 0, -1, False],  # x, y, vel_x, vel_y, dirección, en_suelo
    [200, 180, 0, 0, 1, False],
    [200, 100, 0, 0, 1, False]
]

personaje = Actor("creature", topleft = (200, 100))
personaje.velocidad_y = 0
personaje.velocidad_x = 0
personaje.en_suelo = False
personaje.objetos_cerca = []  # Lista para almacenar objetos cercanos

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

def verificar_interaccion():
    # Limpiar lista de objetos cercanos
    personaje.objetos_cerca = []
    
    # Verificar en un área alrededor del personaje
    radio_interaccion = TILE_SIZE * 1.5  # Radio de interacción
    
    # Obtener el rango de tiles a verificar
    inicio_x = max(0, int((personaje.x - radio_interaccion) // TILE_SIZE))
    fin_x = min(len(my_map[0]), int((personaje.x + radio_interaccion) // TILE_SIZE) + 1)
    inicio_y = max(0, int((personaje.y - radio_interaccion) // TILE_SIZE))
    fin_y = min(len(my_map), int((personaje.y + radio_interaccion) // TILE_SIZE) + 1)
    
    # Verificar cada tile en el rango
    for y in range(inicio_y, fin_y):
        for x in range(inicio_x, fin_x):
            tile_id, item_id = my_map[y][x], my_items[y][x]
            
            # Si hay un objeto interactivo, agregarlo a la lista
            if item_id in OBJETOS_INTERACTIVOS:
                # Calcular distancia al personaje
                dist_x = (x * TILE_SIZE + TILE_SIZE/2) - (personaje.x + TILE_SIZE/2)
                dist_y = (y * TILE_SIZE + TILE_SIZE/2) - (personaje.y + TILE_SIZE/2)
                distancia = (dist_x**2 + dist_y**2)**0.5
                
                if distancia <= radio_interaccion:
                    personaje.objetos_cerca.append((x, y, item_id))

def verificar_colision_vertical_enemigo(x, y):
    # Ajustar las coordenadas para el punto topleft
    x_centro = x + TILE_SIZE // 2
    y_centro = y + TILE_SIZE // 2
    
    # Solo verificar los puntos superior e inferior
    puntos_colision = [
        (x_centro, y_centro - ENEMY_HITBOX_HEIGHT/2),  # Centro superior
        (x_centro, y_centro + ENEMY_HITBOX_HEIGHT/2 + 9),  # Centro inferior (ajustado más arriba)
        (x_centro - ENEMY_HITBOX_WIDTH/3, y_centro - ENEMY_HITBOX_HEIGHT/2),  # Izquierda superior
        (x_centro + ENEMY_HITBOX_WIDTH/3, y_centro - ENEMY_HITBOX_HEIGHT/2),  # Derecha superior
        (x_centro - ENEMY_HITBOX_WIDTH/3, y_centro + ENEMY_HITBOX_HEIGHT/2 - 5),  # Izquierda inferior (ajustado)
        (x_centro + ENEMY_HITBOX_WIDTH/3, y_centro + ENEMY_HITBOX_HEIGHT/2 - 5)   # Derecha inferior (ajustado)
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def verificar_colision_horizontal_enemigo(x, y):
    # Ajustar las coordenadas para el punto topleft
    x_centro = x + TILE_SIZE // 2
    y_centro = y + TILE_SIZE // 2
    
    # Solo verificar los puntos laterales
    puntos_colision = [
        (x_centro - ENEMY_HITBOX_WIDTH/2, y_centro),   # Centro izquierda
        (x_centro + ENEMY_HITBOX_WIDTH/2, y_centro),   # Centro derecha
        (x_centro - ENEMY_HITBOX_WIDTH/2, y_centro - ENEMY_HITBOX_HEIGHT/3),  # Izquierda superior
        (x_centro + ENEMY_HITBOX_WIDTH/2, y_centro - ENEMY_HITBOX_HEIGHT/3),  # Derecha superior
        (x_centro - ENEMY_HITBOX_WIDTH/2, y_centro + ENEMY_HITBOX_HEIGHT/3),  # Izquierda inferior
        (x_centro + ENEMY_HITBOX_WIDTH/2, y_centro + ENEMY_HITBOX_HEIGHT/3)   # Derecha inferior
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
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
    
    # Verificar objetos interactivos cercanos
    verificar_interaccion()

    # Actualizar enemigos
    for enemigo in enemigos:
        # Aplicar gravedad
        enemigo[3] += GRAVEDAD
        
        # Aplicar velocidad horizontal
        enemigo[2] = VELOCIDAD_ENEMIGO * enemigo[4]
        
        # Intentar mover horizontalmente
        nueva_x = enemigo[0] + enemigo[2]
        if not verificar_colision_horizontal_enemigo(nueva_x, enemigo[1]):
            enemigo[0] = nueva_x
        else:
            enemigo[4] *= -1  # Cambiar dirección
        
        # Intentar mover verticalmente
        nueva_y = enemigo[1] + enemigo[3]
        if not verificar_colision_vertical_enemigo(enemigo[0], nueva_y):
            enemigo[1] = nueva_y
            enemigo[5] = False
        else:
            if enemigo[3] > 0:  # Si está cayendo
                enemigo[5] = True
            enemigo[3] = 0
        
        # Verificar colisión con el suelo
        if enemigo[1] >= HEIGHT - TILE_SIZE:
            enemigo[1] = HEIGHT - TILE_SIZE
            enemigo[3] = 0
            enemigo[5] = True
        
        # Mantener dentro de los límites horizontales
        enemigo[0] = max(0, min(WIDTH - TILE_SIZE, enemigo[0]))

def on_key_down(key):
    # Salto
    if key == keys.SPACE and personaje.en_suelo:
        personaje.velocidad_y = VELOCIDAD_SALTO
        personaje.en_suelo = False
    
    # Interacción con objetos
    if key == keys.E and personaje.objetos_cerca:
        # Interactuar con el objeto más cercano
        x, y, item_id = personaje.objetos_cerca[0]
        print(f"Interactuando con objeto {item_id} en posición ({x}, {y})")
        # Eliminar el objeto del mapa de items
        my_items[y][x] = 0
        # Eliminar el objeto de la lista de objetos cercanos
        personaje.objetos_cerca.remove((x, y, item_id))
        # Aquí puedes agregar la lógica específica para cada tipo de objeto
        if item_id == 4:
            print("¡Has interactuado con el objeto 4!")

def draw():
    screen.clear()

    for fila in range(len(my_map)):
        for columna in range(len(my_map[0])):
            x = columna * TILE_SIZE
            y = fila * TILE_SIZE

            # Dibuja el fondo del mapa (tiles)
            tile_id = my_map[fila][columna]
            tile_name = "tile" + str(tile_id)
            tile_actor = Actor(tile_name, (x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            tile_actor.draw()

            # Dibuja los ítems sobre el mapa
            item_id = my_items[fila][columna]
            if item_id != 0:
                item_name = "tile" + str(item_id)
                item_actor = Actor(item_name, (x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                item_actor.draw()
                
                # Resaltar objetos interactivos cercanos
                if item_id in OBJETOS_INTERACTIVOS and any(x == columna and y == fila for x, y, _ in personaje.objetos_cerca):
                    screen.draw.rect(Rect((x, y), (TILE_SIZE, TILE_SIZE)), (255, 255, 0))

    personaje.draw()
    
    # Mostrar mensaje de interacción si hay objetos cercanos
    if personaje.objetos_cerca:
        screen.draw.text("Presiona E para interactuar", (10, 10), color="white")

    # Dibujar enemigos
    for enemigo in enemigos:
        enemy_actor = Actor("enemy1", topleft=(enemigo[0], enemigo[1]))
        enemy_actor.draw()

pgzrun.go()
