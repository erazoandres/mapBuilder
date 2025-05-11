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

# Tamaño de la hitbox del personaje (más pequeña que el tile)
HITBOX_WIDTH = TILE_SIZE 
HITBOX_HEIGHT = TILE_SIZE

# Tamaño de la hitbox de los enemigos
ENEMY_HITBOX_WIDTH = TILE_SIZE * 0.8
ENEMY_HITBOX_HEIGHT = TILE_SIZE * 0.8  # Reducimos la altura para que se detecte mejor el suelo

# Lista de elementos colisionables
ELEMENTOS_COLISIONABLES = [1]  # IDs de los tiles con los que colisiona el personaje
ITEMS_COLISIONABLES = [5]  # IDs de los items con los que colisiona el personaje
OBJETOS_INTERACTIVOS = [4]  # IDs de los objetos con los que se puede interactuar

# Lista de enemigos [x, y, velocidad_x, velocidad_y, dirección, en_suelo]
enemigos = [
    [200, 0, 0, 0, 1, False],  # x, y, vel_x, vel_y, dirección, en_suelo
    [200, 190, 0, 0, 1, False],
    [250, 100, 0, 0, 1, False]
]

personaje = Actor("creature")
personaje.velocidad_y = 0  # Solo mantenemos la velocidad vertical para la gravedad
personaje.en_suelo = False
personaje.objetos_cerca = []

# Mapa base
my_map = [
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0],
  [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
];

my_rotations = [
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
];

# Ítems sobre el mapa
my_items = [
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
];
# Estado del juego
game_over = False
modo_desarrollador = False  # Nueva variable para el modo desarrollador
personaje_moviendose = False  # Nueva variable para controlar el movimiento
personaje_direccion = 0  # 0: quieto, -1: izquierda, 1: derecha

def obtener_tile_en_posicion(x, y):
    columna = int(x // TILE_SIZE)
    fila = int(y // TILE_SIZE)
    
    # Verificar límites del mapa
    if 0 <= fila < len(my_map) and 0 <= columna < len(my_map[0]):
        return my_map[fila][columna], my_items[fila][columna]
    return None, None

def verificar_colision_horizontal(x, y):
    # Ajustar las coordenadas para el punto bottomright
    x_centro = x + TILE_SIZE  # Ahora x es la esquina inferior derecha
    y_centro = y + TILE_SIZE  # Ahora y es la esquina inferior derecha
    
    # Solo verificar los puntos laterales con un margen más pequeño
    margen = 2  # Reducimos el margen para hacer la colisión menos sensible
    puntos_colision = [
        (x_centro - TILE_SIZE, y_centro - TILE_SIZE/2),  # Izquierda centro
        (x_centro, y_centro - TILE_SIZE/2),  # Derecha centro
        (x_centro - TILE_SIZE, y_centro - TILE_SIZE + margen),  # Izquierda inferior
        (x_centro, y_centro - TILE_SIZE + margen),  # Derecha inferior
        (x_centro - TILE_SIZE, y_centro - TILE_SIZE/4),  # Izquierda superior
        (x_centro, y_centro - TILE_SIZE/4)  # Derecha superior
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        # Verificar si el tile o el item está en la lista de elementos colisionables
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def verificar_colision_vertical(x, y):
    # Ajustar las coordenadas para el punto bottomright
    x_centro = x + TILE_SIZE
    y_centro = y + TILE_SIZE
    
    # Solo verificar los puntos superior e inferior
    margen = 2
    puntos_colision = [
        (x_centro - TILE_SIZE/2, y_centro - TILE_SIZE),  # Centro superior
        (x_centro - TILE_SIZE/2, y_centro),  # Centro inferior
        (x_centro - TILE_SIZE + margen, y_centro - TILE_SIZE),  # Izquierda superior
        (x_centro - margen, y_centro - TILE_SIZE),  # Derecha superior
        (x_centro - TILE_SIZE + margen, y_centro),  # Izquierda inferior
        (x_centro - margen, y_centro)  # Derecha inferior
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
        (x_centro, y_centro + ENEMY_HITBOX_HEIGHT/2),  # Centro inferior (ajustado más abajo)
        (x_centro - ENEMY_HITBOX_WIDTH/3, y_centro - ENEMY_HITBOX_HEIGHT/2),  # Izquierda superior
        (x_centro + ENEMY_HITBOX_WIDTH/3, y_centro - ENEMY_HITBOX_HEIGHT/2),  # Derecha superior
        (x_centro - ENEMY_HITBOX_WIDTH/3, y_centro + ENEMY_HITBOX_HEIGHT/2),  # Izquierda inferior (ajustado más abajo)
        (x_centro + ENEMY_HITBOX_WIDTH/3, y_centro + ENEMY_HITBOX_HEIGHT/2)   # Derecha inferior (ajustado más abajo)
    ]
    
    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def verificar_colision_horizontal_enemigo(x, y):
    x_centro = x + TILE_SIZE // 2
    y_centro = y + TILE_SIZE // 2

    margen = 2  # Puedes probar con 2, 3 o más
    puntos_colision = [
        (x_centro - ENEMY_HITBOX_WIDTH/2 - margen, y_centro),   # Centro izquierda
        (x_centro + ENEMY_HITBOX_WIDTH/2 + margen, y_centro),   # Centro derecha
        (x_centro - ENEMY_HITBOX_WIDTH/2 - margen, y_centro - ENEMY_HITBOX_HEIGHT/3),
        (x_centro + ENEMY_HITBOX_WIDTH/2 + margen, y_centro - ENEMY_HITBOX_HEIGHT/3),
        (x_centro - ENEMY_HITBOX_WIDTH/2 - margen, y_centro + ENEMY_HITBOX_HEIGHT/3),
        (x_centro + ENEMY_HITBOX_WIDTH/2 + margen, y_centro + ENEMY_HITBOX_HEIGHT/3)
    ]

    for punto_x, punto_y in puntos_colision:
        tile_id, item_id = obtener_tile_en_posicion(punto_x, punto_y)
        if tile_id in ELEMENTOS_COLISIONABLES or item_id in ITEMS_COLISIONABLES:
            return True
    return False

def verificar_colision_con_enemigo():
    # Obtener el centro del personaje
    personaje_centro_x = personaje.x + TILE_SIZE/2
    personaje_centro_y = personaje.y + TILE_SIZE/2
    
    # Calcular los límites de la hitbox del personaje
    personaje_izq = personaje_centro_x - HITBOX_WIDTH/2
    personaje_der = personaje_centro_x + HITBOX_WIDTH/2
    personaje_arriba = personaje_centro_y - HITBOX_HEIGHT/2
    personaje_abajo = personaje_centro_y + HITBOX_HEIGHT/2
    
    # Verificar colisión con cada enemigo
    for enemigo in enemigos:
        # Obtener el centro del enemigo
        enemigo_centro_x = enemigo[0] + TILE_SIZE/2
        enemigo_centro_y = enemigo[1] + TILE_SIZE/2
        
        # Calcular los límites de la hitbox del enemigo
        enemigo_izq = enemigo_centro_x - ENEMY_HITBOX_WIDTH/2
        enemigo_der = enemigo_centro_x + ENEMY_HITBOX_WIDTH/2
        enemigo_arriba = enemigo_centro_y - ENEMY_HITBOX_HEIGHT/2
        enemigo_abajo = enemigo_centro_y + ENEMY_HITBOX_HEIGHT/2
        
        # Verificar si hay colisión
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
        
    # Aplicar gravedad
    personaje.velocidad_y += GRAVEDAD
    
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
        
        # Verificar límites de la ventana
        if nueva_x <= 0 or nueva_x >= WIDTH - TILE_SIZE:
            enemigo[4] *= -1  # Cambiar dirección
        elif not verificar_colision_horizontal_enemigo(nueva_x, enemigo[1]):
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

    # Verificar colisión con enemigos
    if verificar_colision_con_enemigo():
        game_over = True

def on_key_down(key):
    global game_over, modo_desarrollador, personaje_moviendose, personaje_direccion
    
    if game_over:
        if key == keys.R:
            # Reiniciar el juego
            game_over = False
            personaje.x = 0
            personaje.y = 0
            personaje.velocidad_x = 0
            personaje.velocidad_y = 0
            return
    
    # Activar/desactivar modo desarrollador
    if key == keys.F:
        modo_desarrollador = not modo_desarrollador
            
    # Salto
    if key == keys.SPACE and personaje.en_suelo:
        personaje.velocidad_y = VELOCIDAD_SALTO
        personaje.en_suelo = False
    
    # Movimiento horizontal por celdas (ahora funciona en el aire también)
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
            tile_actor = Actor(tile_name, topleft=(x, y))
            tile_actor.draw()

            # Dibuja los ítems sobre el mapa
            item_id = my_items[fila][columna]
            if item_id != 0:
                item_name = "tile" + str(item_id)
                item_actor = Actor(item_name, topleft=(x, y))
                item_actor.draw()
                
                # Resaltar objetos interactivos cercanos
                if item_id in OBJETOS_INTERACTIVOS and any(x == columna and y == fila for x, y, _ in personaje.objetos_cerca):
                    # Dibujar un borde amarillo alrededor del objeto
                    for i in range(4):  # Grosor del borde
                        screen.draw.line((x + i, y + i), (x + TILE_SIZE - i, y + i), (255, 255, 0))  # Línea superior
                        screen.draw.line((x + i, y + i), (x + i, y + TILE_SIZE - i), (255, 255, 0))  # Línea izquierda
                        screen.draw.line((x + TILE_SIZE - i, y + i), (x + TILE_SIZE - i, y + TILE_SIZE - i), (255, 255, 0))  # Línea derecha
                        screen.draw.line((x + i, y + TILE_SIZE - i), (x + TILE_SIZE - i, y + TILE_SIZE - i), (255, 255, 0))  # Línea inferior

    # Dibujar el personaje
    personaje_actor = Actor(personaje.image, bottomright=(personaje.x + TILE_SIZE, personaje.y + TILE_SIZE))
    personaje_actor.draw()
    
    # Mostrar mensaje de interacción si hay objetos cercanos
    if personaje.objetos_cerca:
        screen.draw.text("Presiona E para interactuar", (10, 10), color="white")

    # Dibujar enemigos
    for enemigo in enemigos:
        enemy_actor = Actor("enemy1", bottomright=(enemigo[0] + TILE_SIZE, enemigo[1] + TILE_SIZE))
        enemy_actor.draw()
        
    # Mostrar mensaje de game over
    if game_over:
        screen.draw.text("¡Has perdido!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
        screen.draw.text("Presiona R para reiniciar", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")

    # Modo desarrollador: mostrar hitboxes
    if modo_desarrollador:
        # Hitbox del personaje
        screen.draw.rect(
            Rect(
                personaje.x,  # x desde la esquina inferior derecha
                personaje.y, # y desde la esquina inferior derecha
                TILE_SIZE,
                TILE_SIZE
            ),
            (255, 0, 0)  # Color rojo para el personaje
        )

        # Hitboxes de los enemigos
        for enemigo in enemigos:
            screen.draw.rect(
                Rect(
                    enemigo[0],  # x desde la esquina inferior derecha
                    enemigo[1], # y desde la esquina inferior derecha
                    TILE_SIZE,
                    TILE_SIZE
                ),
                (0, 255, 0)  # Color verde para los enemigos
            )

        # Mostrar mensaje de modo desarrollador
        screen.draw.text("Modo Desarrollador: ON", (10, 30), color="yellow")

pgzrun.go()
