import pgzrun
import re
import random
import time

# Diccionario global de configuración del juego
CONFIG_JUEGO = {
    'TILE_SIZE': 32,
    'ENEMIGO_SIZE': 32,
    'PROBABILIDAD_SALTO_ENEMIGO': 0.000000000000002,
    'GRAVEDAD': 0.8,
    'VELOCIDAD_SALTO': -15,
    'VELOCIDAD_MOVIMIENTO': 3,
    'CAMERA_SPEED': 8,
    'CAMERA_MARGIN': 100,  # Valor por defecto, se ajusta después
    'VOLUMEN_SONIDO': 50,
    'PANTALLA_COMPLETA': False,
    'EFECTOS_VISUALES': 'Básicos',
    'TAMANO_CUADRO_COLOCACION': 24,
    'LIMITE_CUADROS_COLOCACION': 10,
    'PERSEGUIDOR_RANGO_X': 200,
    'PERSEGUIDOR_RANGO_Y': 40,
    'SALTADOR_RANGO_X': 100,
    'SALTADOR_PROB_SALTO': 0.02,
    'ALEATORIO_MIN_FRAMES': 60,
    'ALEATORIO_MAX_FRAMES': 180,
    'PATRULLA_VELOCIDAD': 0.7,
    'SALTADOR_VELOCIDAD': 0.5,
    'PERSEGUIDOR_VELOCIDAD': 0.9,
    'ALEATORIO_VEL_MIN': 0.3,
    'ALEATORIO_VEL_MAX': 1.0,
}

# Reemplazar todas las variables directas por CONFIG_JUEGO['NOMBRE'] en el código relevante
TILE_SIZE = CONFIG_JUEGO['TILE_SIZE']
ENEMIGO_SIZE = CONFIG_JUEGO['ENEMIGO_SIZE']
PROBABILIDAD_SALTO_ENEMIGO = CONFIG_JUEGO['PROBABILIDAD_SALTO_ENEMIGO']
GRAVEDAD = CONFIG_JUEGO['GRAVEDAD']
VELOCIDAD_SALTO = CONFIG_JUEGO['VELOCIDAD_SALTO']
VELOCIDAD_MOVIMIENTO = CONFIG_JUEGO['VELOCIDAD_MOVIMIENTO']
CAMERA_SPEED = CONFIG_JUEGO['CAMERA_SPEED']
CAMERA_MARGIN = CONFIG_JUEGO['CAMERA_MARGIN']
VOLUMEN_SONIDO = CONFIG_JUEGO['VOLUMEN_SONIDO']
PANTALLA_COMPLETA = CONFIG_JUEGO['PANTALLA_COMPLETA']
EFECTOS_VISUALES = CONFIG_JUEGO['EFECTOS_VISUALES']
TAMANO_CUADRO_COLOCACION = CONFIG_JUEGO['TAMANO_CUADRO_COLOCACION']
LIMITE_CUADROS_COLOCACION = CONFIG_JUEGO['LIMITE_CUADROS_COLOCACION']

# Dimensiones de la matriz
with open('mapa.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    for line in content.split('\n'):
        if "Matrix Size:" in line:
            dimensions = line.split(':')[1].strip().split('x')
            MATRIZ_ALTO = int(dimensions[0])
            MATRIZ_ANCHO = int(dimensions[1])
            break

# Tamaño de la ventana del juego
WINDOW_WIDTH = min(MATRIZ_ANCHO * TILE_SIZE, 750)  # Ancho basado en el mapa, máximo 750px
WINDOW_HEIGHT = MATRIZ_ALTO * TILE_SIZE  # Alto basado en el mapa

# Ajustar el tamaño de la ventana - hacerla más ancha pero respetando el límite de 750px
WIDTH = min(WINDOW_WIDTH + 400, 750)  # Agregar 400 píxeles extra de ancho, máximo 750px
HEIGHT = WINDOW_HEIGHT

# Variables globales para configuraciones adicionales
VOLUMEN_SONIDO = 50
PANTALLA_COMPLETA = False
EFECTOS_VISUALES = "Básicos"

# Variables de la cámara
camera_x = 0
camera_y = 0

# Variables para el sistema de menú
estado_juego = "menu"  # "menu", "jugando", "extras"
boton_seleccionado = 0  # 0: Jugar, 1: Extras

# Variable para mostrar panel detallado de items
mostrar_panel_detallado = False

# Variables para el modo de colocación de terreno
modo_colocacion_terreno = False
posicion_terreno_x = 0
posicion_terreno_y = 0
tipo_terreno_actual = 1  # ID del terreno a colocar (por defecto 1)

TERRENOS = []
ITEMS = []
ENEMIGOS = []

# Lista para almacenar los items recolectados
items_recolectados = {}  # Cambiado de lista a diccionario para contar items

print(ITEMS)

cuadros_colocados = 0  # Contador de cuadros colocados

# Diccionario de tipos de comportamiento de enemigos
TIPOS_COMPORTAMIENTO_ENEMIGO = {
    'saltador': {
        'nombre': 'Saltador',
        'descripcion': 'Enemigo que salta periódicamente o cuando detecta al jugador cerca.'
    },
    'patrulla': {
        'nombre': 'Patrulla',
        'descripcion': 'Enemigo que se mueve de un lado a otro en una zona fija.'
    },
    'perseguidor': {
        'nombre': 'Perseguidor',
        'descripcion': 'Enemigo que persigue al jugador si entra en su rango de visión.'
    },
    'aleatorio': {
        'nombre': 'Errático',
        'descripcion': 'Enemigo que se mueve de forma aleatoria, cambiando de dirección y velocidad.'
    }
}

# Ejemplo de cómo asociar un tipo de comportamiento a un enemigo:
# enemigo.tipo_comportamiento = 'saltador'
# Luego, en la lógica de actualización del enemigo, se puede usar TIPOS_COMPORTAMIENTO_ENEMIGO[enemigo.tipo_comportamiento]

# Leer configuraciones del archivo mapa.txt
def cargar_configuraciones():
    global GRAVEDAD, VELOCIDAD_SALTO, VELOCIDAD_MOVIMIENTO, PROBABILIDAD_SALTO_ENEMIGO, CAMERA_SPEED, CAMERA_MARGIN, VOLUMEN_SONIDO, PANTALLA_COMPLETA, EFECTOS_VISUALES
    
    try:
        with open('mapa.txt', 'r') as f:
            content = f.read()
            
            # Buscar el diccionario de configuraciones
            if 'configuraciones = {' in content:
                # Extraer la sección de configuraciones
                start = content.find('configuraciones = {')
                end = content.find('}', start) + 1
                config_section = content[start:end]
                
                # Ejecutar el diccionario para obtener las configuraciones
                config_dict = {}
                exec(config_section, {}, config_dict)
                
                # Aplicar las configuraciones
                if 'configuraciones' in config_dict:
                    config = config_dict['configuraciones']
                    
                    # Aplicar valores numéricos
                    if 'velocidad_personaje' in config:
                        VELOCIDAD_MOVIMIENTO = config['velocidad_personaje']
                    if 'velocidad_salto' in config:
                        VELOCIDAD_SALTO = -config['velocidad_salto']  # Negativo para que sea hacia arriba
                    if 'gravedad' in config:
                        GRAVEDAD = config['gravedad']
                    if 'prob_salto_enemigo' in config:
                        PROBABILIDAD_SALTO_ENEMIGO = config['prob_salto_enemigo']
                    if 'velocidad_camara' in config:
                        CAMERA_SPEED = config['velocidad_camara']
                    if 'margen_camara' in config:
                        CAMERA_MARGIN = config['margen_camara']
                    if 'volumen_sonido' in config:
                        VOLUMEN_SONIDO = config['volumen_sonido']
                    if 'pantalla_completa' in config:
                        PANTALLA_COMPLETA = config['pantalla_completa'] == "Sí"
                    if 'efectos_visuales' in config:
                        EFECTOS_VISUALES = config['efectos_visuales']
                    
                    print("✅ Configuraciones cargadas desde mapa.txt")
                    print(f"   Velocidad: {VELOCIDAD_MOVIMIENTO}")
                    print(f"   Salto: {abs(VELOCIDAD_SALTO)}")
                    print(f"   Gravedad: {GRAVEDAD}")
                    print(f"   Cámara: {CAMERA_SPEED}")
                    print(f"   Margen: {CAMERA_MARGIN}")
                    print(f"   Volumen de sonido: {VOLUMEN_SONIDO}")
                    print(f"   Pantalla completa: {PANTALLA_COMPLETA}")
                    print(f"   Efectos visuales: {EFECTOS_VISUALES}")
                else:
                    print("⚠️ No se encontró el diccionario de configuraciones en mapa.txt")
            else:
                print("⚠️ No se encontró la sección de configuraciones en mapa.txt")
                
    except FileNotFoundError:
        print("⚠️ Archivo mapa.txt no encontrado. Usando configuraciones por defecto.")
    except Exception as e:
        print(f"⚠️ Error al cargar configuraciones: {e}. Usando configuraciones por defecto.")

# Cargar configuraciones antes de crear el personaje
cargar_configuraciones()

personaje = Actor("personajes/tile0")
personaje.velocidad_y = 0
personaje.velocidad_x = 0  # Nueva variable para velocidad horizontal
personaje.en_suelo = False
personaje.objetos_cerca = []
personaje.puede_doble_salto = False  # Nueva variable para el doble salto
# Obtener el tamaño real de la imagen del personaje
personaje.hitbox_width = personaje.width
personaje.hitbox_height = personaje.height

# Aplicar configuración de tamaño de hitbox después de crear el personaje
def aplicar_configuracion_hitbox():
    global personaje
    try:
        with open('mapa.txt', 'r') as f:
            content = f.read()
            if 'configuraciones = {' in content:
                start = content.find('configuraciones = {')
                end = content.find('}', start) + 1
                config_section = content[start:end]
                config_dict = {}
                exec(config_section, {}, config_dict)
                
                if 'configuraciones' in config_dict:
                    config = config_dict['configuraciones']
                    if 'tamaño_hitbox' in config:
                        if config['tamaño_hitbox'] == "Pequeño":
                            personaje.hitbox_width = personaje.width * 0.7
                            personaje.hitbox_height = personaje.height * 0.7
                        elif config['tamaño_hitbox'] == "Grande":
                            personaje.hitbox_width = personaje.width * 1.3
                            personaje.hitbox_height = personaje.height * 1.3
                        else:  # Normal
                            personaje.hitbox_width = personaje.width
                            personaje.hitbox_height = personaje.height
                        print(f"   Hitbox: {config['tamaño_hitbox']}")
    except:
        pass

aplicar_configuracion_hitbox()

# Lista para almacenar los enemigos activos
enemigos_activos = []

# --- FUNCIONES DE MOVIMIENTO PARA CADA COMPORTAMIENTO ---
def movimiento_saltador(enemigo, jugador):
    # Salta periódicamente o si el jugador está cerca, y se mueve horizontalmente
    if enemigo.en_suelo:
        if random.random() < 0.02 or abs(enemigo.x - jugador.x) < 100:
            enemigo.velocidad_y = VELOCIDAD_SALTO
            enemigo.en_suelo = False
        # Elegir dirección hacia el jugador si está cerca
        if abs(enemigo.x - jugador.x) < 100:
            enemigo.direccion = 1 if jugador.x > enemigo.x else -1
    # Movimiento horizontal fluido
    enemigo.velocidad_x = enemigo.direccion * (VELOCIDAD_MOVIMIENTO * 0.5)

def movimiento_patrulla(enemigo, jugador):
    # Se mueve de un lado a otro, cambia de dirección solo al llegar a los bordes o colisión
    enemigo.velocidad_x = enemigo.direccion * (VELOCIDAD_MOVIMIENTO * 0.7)
    # Si está cerca del borde, cambia de dirección
    if enemigo.x <= 0 or enemigo.x >= WIDTH - TILE_SIZE:
        enemigo.direccion *= -1
    # Si hay colisión horizontal, cambiar dirección (esto ya se maneja en actualizar)

def movimiento_perseguidor(enemigo, jugador):
    # Persigue al jugador suavemente si está cerca en X y Y
    distancia_x = jugador.x - enemigo.x
    distancia_y = abs(jugador.y - enemigo.y)
    if abs(distancia_x) < 200 and distancia_y < 40:
        velocidad_objetivo = VELOCIDAD_MOVIMIENTO * 0.9 if distancia_x > 0 else -VELOCIDAD_MOVIMIENTO * 0.9
        # Interpolación suave
        enemigo.velocidad_x += (velocidad_objetivo - enemigo.velocidad_x) * 0.1
    else:
        # Detenerse completamente
        enemigo.velocidad_x = 0

def movimiento_aleatorio(enemigo, jugador):
    # Mantiene dirección por más tiempo, cambia menos abruptamente
    if not hasattr(enemigo, 'frames_direccion'):
        enemigo.frames_direccion = random.randint(60, 180)
    enemigo.frames_direccion -= 1
    if enemigo.frames_direccion <= 0:
        enemigo.direccion = random.choice([-1, 0, 1])
        enemigo.velocidad_x = enemigo.direccion * (VELOCIDAD_MOVIMIENTO * random.uniform(0.3, 1.0))
        enemigo.frames_direccion = random.randint(60, 180)
    # Si está cerca del borde, cambia de dirección
    if enemigo.x <= 0 or enemigo.x >= WIDTH - TILE_SIZE:
        enemigo.direccion *= -1
        enemigo.velocidad_x = enemigo.direccion * (VELOCIDAD_MOVIMIENTO * random.uniform(0.3, 1.0))

# --- CLASE ENEMIGO MODIFICADA ---
class Enemigo:
    def __init__(self, x, y, tipo_id):
        self.x = x
        self.y = y
        self.tipo_id = tipo_id
        self.velocidad_y = 0
        self.velocidad_x = 0
        self.en_suelo = False
        self.direccion = random.choice([-1, 1])  # -1 izquierda, 1 derecha
        self.tiempo_cambio_direccion = random.randint(60, 180)  # frames hasta cambiar dirección
        self.contador = 0
        self.imagen_base = id_to_image.get(tipo_id, "enemigos/default")
        # Asignar comportamiento aleatorio
        self.tipo_comportamiento = random.choice(list(TIPOS_COMPORTAMIENTO_ENEMIGO.keys()))
    
    def obtener_imagen_actual(self):
        if self.direccion == -1:
            return "enemigos/tile6.png"
        else:
            return "enemigos/tile4.png"
    
    def actualizar(self, jugador=None):
        # Aplicar gravedad
        self.velocidad_y += GRAVEDAD
        # Lógica de movimiento según comportamiento
        if self.tipo_comportamiento == 'saltador':
            movimiento_saltador(self, jugador)
        elif self.tipo_comportamiento == 'patrulla':
            movimiento_patrulla(self, jugador)
        elif self.tipo_comportamiento == 'perseguidor':
            movimiento_perseguidor(self, jugador)
        elif self.tipo_comportamiento == 'aleatorio':
            movimiento_aleatorio(self, jugador)
        # Actualizar posición vertical
        nueva_y = self.y + self.velocidad_y
        if not verificar_colision_vertical(self.x, nueva_y):
            self.y = nueva_y
            self.en_suelo = False
        else:
            if self.velocidad_y > 0:
                self.en_suelo = True
            self.velocidad_y = 0
        # Actualizar posición horizontal
        nueva_x = self.x + self.velocidad_x
        if not verificar_colision_horizontal(nueva_x, self.y):
            self.x = nueva_x
        else:
            self.direccion *= -1
            self.velocidad_x = 0
        # Mantener al enemigo dentro de los límites
        self.x = max(0, min(WIDTH - TILE_SIZE, self.x))
        if self.y >= HEIGHT - TILE_SIZE:
            self.y = HEIGHT - TILE_SIZE
            self.velocidad_y = 0
            self.en_suelo = True

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
                if 'enemigo' in descripcion:
                    ENEMIGOS.append(id_val)



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
    # Para el personaje, solo verificamos colisiones con items, no con terrenos
    if x == personaje.x:  # Si es el personaje
        for offset_y in range(0, personaje.hitbox_height, 5):
            # Borde izquierdo
            tile_id, item_id = obtener_tile_en_posicion(x, y + offset_y)
            if item_id in ITEMS:  # Solo verificamos items
                return True
            # Borde derecho
            tile_id, item_id = obtener_tile_en_posicion(x + personaje.hitbox_width, y + offset_y)
            if item_id in ITEMS:  # Solo verificamos items
                return True
        return False
    else:  # Para enemigos u otros objetos, mantener la lógica original
        for offset_y in [1, TILE_SIZE - 2]:
            for offset_x in [0, TILE_SIZE - 1]:
                tile_id, item_id = obtener_tile_en_posicion(x + offset_x, y + offset_y)
                if (tile_id in TERRENOS) or (item_id in ITEMS):
                    return True
        return False

def verificar_colision_vertical(x, y):
    # Para el personaje, solo verificamos colisiones con items y terrenos en la parte inferior
    if x == personaje.x:  # Si es el personaje
        # Solo verificamos colisión en la parte inferior cuando está cayendo
        if personaje.velocidad_y > 0:
            for offset_x in range(0, personaje.hitbox_width, TILE_SIZE):
                tile_id, item_id = obtener_tile_en_posicion(x + offset_x, y + personaje.hitbox_height)
                if (tile_id in TERRENOS) or (item_id in ITEMS):  # Verificamos terrenos para detectar suelo
                    personaje.en_suelo = True
                    return True
        # Verificamos colisión en la parte superior solo cuando está saltando
        elif personaje.velocidad_y < 0:  # Si está saltando
            for offset_x in range(0, personaje.hitbox_width, TILE_SIZE):
                tile_id, item_id = obtener_tile_en_posicion(x + offset_x, y)
                if (tile_id in TERRENOS) or (item_id in ITEMS):  # Mantenemos colisión con terrenos al saltar
                    return True
        return False
    else:  # Para enemigos u otros objetos, mantener la lógica original
        for offset_x in [1, TILE_SIZE - 2]:
            for offset_y in [0, TILE_SIZE - 1]:
                tile_id, item_id = obtener_tile_en_posicion(x + offset_x, y + offset_y)
                if (tile_id in TERRENOS) or (item_id in ITEMS):
                    return True
        return False

def verificar_interaccion():
    personaje.objetos_cerca = []
    radio_interaccion = TILE_SIZE * 1.5
    
    # Calcular el centro del personaje basado en su hitbox real
    centro_x = personaje.x + personaje.hitbox_width / 2
    centro_y = personaje.y + personaje.hitbox_height / 2
    
    inicio_x = max(0, int((centro_x - radio_interaccion) // TILE_SIZE))
    fin_x = min(len(my_map[0]), int((centro_x + radio_interaccion) // TILE_SIZE) + 1)
    inicio_y = max(0, int((centro_y - radio_interaccion) // TILE_SIZE))
    fin_y = min(len(my_map), int((centro_y + radio_interaccion) // TILE_SIZE) + 1)

    for y in range(inicio_y, fin_y):
        for x in range(inicio_x, fin_x):
            tile_id, item_id = my_map[y][x], my_items[y][x]
            if item_id in ITEMS:
                dist_x = (x * TILE_SIZE + TILE_SIZE/2) - centro_x
                dist_y = (y * TILE_SIZE + TILE_SIZE/2) - centro_y
                distancia = (dist_x**2 + dist_y**2)**0.5
                if distancia <= radio_interaccion:
                    personaje.objetos_cerca.append((x, y, item_id))

# Función para inicializar enemigos desde el mapa
def inicializar_enemigos():
    enemigos_activos.clear()
    for fila in range(len(my_items)):
        for columna in range(len(my_items[0])):
            item_id = my_items[fila][columna]
            if item_id in ENEMIGOS:
                # Crear un nuevo enemigo y agregarlo a la lista
                nuevo_enemigo = Enemigo(columna * TILE_SIZE, fila * TILE_SIZE, item_id)
                enemigos_activos.append(nuevo_enemigo)
                # Eliminar el enemigo de la matriz para que no se dibuje estático
                my_items[fila][columna] = 0

def verificar_colision(x, y, es_personaje=False):
    """
    Función unificada para verificar colisiones.
    Retorna: (colision_vertical, colision_horizontal, es_suelo)
    """
    colision_vertical = False
    colision_horizontal = False
    es_suelo = False

    # Obtener las coordenadas de los tiles que podrían colisionar
    tile_x_izq = int(x // TILE_SIZE)
    tile_x_der = int((x + personaje.hitbox_width) // TILE_SIZE)
    tile_y_arriba = int(y // TILE_SIZE)
    tile_y_abajo = int((y + personaje.hitbox_height) // TILE_SIZE)

    # Verificar colisiones verticales
    if es_personaje:
        # Verificar suelo solo cuando está cayendo
        if personaje.velocidad_y > 0:
            for tile_x in range(tile_x_izq, tile_x_der + 1):
                if 0 <= tile_x < len(my_map[0]) and 0 <= tile_y_abajo < len(my_map):
                    tile_id = my_map[tile_y_abajo][tile_x]
                    if tile_id in TERRENOS:
                        colision_vertical = True
                        es_suelo = True
                        break
        # Verificar techo solo cuando está saltando
        elif personaje.velocidad_y < 0:
            for tile_x in range(tile_x_izq, tile_x_der + 1):
                if 0 <= tile_x < len(my_map[0]) and 0 <= tile_y_arriba < len(my_map):
                    tile_id = my_map[tile_y_arriba][tile_x]
                    if tile_id in TERRENOS:
                        colision_vertical = True
                        break

    # Verificar colisiones horizontales
    if es_personaje:
        # Solo verificar items para el personaje
        for tile_y in range(tile_y_arriba, tile_y_abajo + 1):
            if 0 <= tile_y < len(my_map):
                # Verificar borde izquierdo
                if 0 <= tile_x_izq < len(my_map[0]):
                    item_id = my_items[tile_y][tile_x_izq]
                    if item_id in ITEMS:
                        colision_horizontal = True
                        break
                # Verificar borde derecho
                if 0 <= tile_x_der < len(my_map[0]):
                    item_id = my_items[tile_y][tile_x_der]
                    if item_id in ITEMS:
                        colision_horizontal = True
                        break

    return colision_vertical, colision_horizontal, es_suelo

def update():
    global game_over, modo_desarrollador, mostrar_panel_detallado, estado_juego, boton_seleccionado, modo_colocacion_terreno, posicion_terreno_x, posicion_terreno_y, tipo_terreno_actual, cuadros_colocados, LIMITE_CUADROS_COLOCACION
    
    # Si estamos en el menú principal
    if estado_juego == "menu":
        # Los controles del menú se manejan en on_key_down()
        return
    
    # Si estamos en extras
    elif estado_juego == "extras":
        # Los controles de extras se manejan en on_key_down()
        return
    
    # Si estamos jugando
    elif estado_juego == "jugando":
        # Volver al menú con ESC
        if keyboard.ESCAPE:
            estado_juego = "menu"
            return
        
        if game_over:
            if keyboard.R:
                game_over = False
                personaje.x = 0
                personaje.y = 0
                personaje.velocidad_y = 0
                personaje.velocidad_x = 0
                personaje.puede_doble_salto = False
                # No reiniciar la colección de items para mantener el progreso
                return

        if keyboard.F:
            modo_desarrollador = not modo_desarrollador
        
        # Mostrar/ocultar panel detallado de items
        if keyboard.U:
            mostrar_panel_detallado = not mostrar_panel_detallado
        
        # Activar/desactivar modo de colocación de terreno
        if keyboard.Y:
            modo_colocacion_terreno = not modo_colocacion_terreno
            if modo_colocacion_terreno:
                # Inicializar posición del terreno en la posición del personaje
                posicion_terreno_x = int(personaje.x // TILE_SIZE) * TILE_SIZE
                posicion_terreno_y = int(personaje.y // TILE_SIZE) * TILE_SIZE
                # Al inicio, asegúrate de que tipo_terreno_actual esté en TERRENOS si la lista no está vacía
                if TERRENOS:
                    tipo_terreno_actual = TERRENOS[0]
                else:
                    tipo_terreno_actual = 1
            else:
                # Salir del modo de colocación
                pass
        
        # Reinicio completo del juego (incluyendo colección)
        if keyboard.F5:
            game_over = False
            personaje.x = 0
            personaje.y = 0
            personaje.velocidad_y = 0
            personaje.velocidad_x = 0
            personaje.puede_doble_salto = False
            items_recolectados.clear()  # Limpiar la colección
            # Reinicializar el mapa de items
            inicializar_enemigos()
            return

        # Lógica de salto mejorada - controles fluidos
        if (keyboard.SPACE or keyboard.UP):
            if personaje.en_suelo:
                personaje.velocidad_y = VELOCIDAD_SALTO
                personaje.en_suelo = False
                personaje.puede_doble_salto = True
            elif personaje.puede_doble_salto and personaje.velocidad_y < 0:  # Solo permitir doble salto cuando está cayendo
                personaje.velocidad_y = VELOCIDAD_SALTO * 0.8  # El segundo salto es ligeramente más débil
                personaje.puede_doble_salto = False
                # Nota: El volumen del sonido se puede ajustar editando el archivo de audio directamente
                # sounds.jump.play()  # Sonido de salto (volumen controlado por el archivo de audio)

        # Interacción con items - controles fluidos
        if keyboard.E and personaje.objetos_cerca:
            x, y, item_id = personaje.objetos_cerca[0]
            # Agregar el item a la colección si no está ya recolectado
            if item_id not in items_recolectados:
                items_recolectados[item_id] = 1
            else:
                items_recolectados[item_id] += 1
            my_items[y][x] = 0
            personaje.objetos_cerca.remove((x, y, item_id))

        # Movimiento horizontal - controles fluidos
        if not modo_colocacion_terreno:  # Solo permitir movimiento si no está en modo colocación
            if keyboard.LEFT:
                personaje.velocidad_x = -VELOCIDAD_MOVIMIENTO
            elif keyboard.RIGHT:
                personaje.velocidad_x = VELOCIDAD_MOVIMIENTO
            else:
                personaje.velocidad_x = 0
        else:
            # En modo colocación, detener el movimiento del personaje
            personaje.velocidad_x = 0

        # Aplicar gravedad solo si no está en el suelo
        if not personaje.en_suelo:
            personaje.velocidad_y += GRAVEDAD

        # Calcular nuevas posiciones
        nueva_x = personaje.x + personaje.velocidad_x
        nueva_y = personaje.y + personaje.velocidad_y

        # Verificar colisiones
        colision_vertical, colision_horizontal, es_suelo = verificar_colision(nueva_x, nueva_y, True)

        # Actualizar posición vertical
        if not colision_vertical:
            personaje.y = nueva_y
            personaje.en_suelo = False
        else:
            if personaje.velocidad_y > 0:
                personaje.velocidad_y = 0
                personaje.en_suelo = es_suelo
                if es_suelo:
                    personaje.puede_doble_salto = False  # Resetear el doble salto al tocar el suelo
            else:
                personaje.velocidad_y = 0

        # Actualizar posición horizontal
        if not colision_horizontal:
            personaje.x = nueva_x

        # Mantener al personaje dentro de los límites del mapa
        personaje.x = max(0, min(MATRIZ_ANCHO * TILE_SIZE - personaje.hitbox_width, personaje.x))
        if personaje.y >= HEIGHT - personaje.hitbox_height:
            personaje.y = HEIGHT - personaje.hitbox_height
            personaje.velocidad_y = 0
            personaje.en_suelo = True
            personaje.puede_doble_salto = False  # Resetear el doble salto al tocar el suelo

        # Actualizar dirección del personaje
        if personaje.velocidad_x > 0:
            personaje.image = "personajes/tile0"
        elif personaje.velocidad_x < 0:
            personaje.image = "personajes/tile1"

        verificar_interaccion()
        
        # Actualizar enemigos
        for enemigo in enemigos_activos:
            enemigo.actualizar(personaje)
            
            # Comprobar colisión con el personaje usando el hitbox real
            if (personaje.x < enemigo.x + ENEMIGO_SIZE and
                personaje.x + personaje.hitbox_width > enemigo.x and
                personaje.y < enemigo.y + ENEMIGO_SIZE and
                personaje.y + personaje.hitbox_height > enemigo.y):
                # Implementar lógica de daño o juego terminado
                pass

def on_key_down(key):
    global game_over, modo_desarrollador, mostrar_panel_detallado, estado_juego, boton_seleccionado, modo_colocacion_terreno, posicion_terreno_x, posicion_terreno_y, cuadros_colocados, LIMITE_CUADROS_COLOCACION, tipo_terreno_actual

    # Si estamos en el menú principal
    if estado_juego == "menu":
        if key == keys.UP:
            boton_seleccionado = (boton_seleccionado - 1) % 2
        elif key == keys.DOWN:
            boton_seleccionado = (boton_seleccionado + 1) % 2
        elif key == keys.RETURN or key == keys.SPACE:
            # Seleccionar botón
            if boton_seleccionado == 0:  # Jugar
                estado_juego = "jugando"
            elif boton_seleccionado == 1:  # Extras
                estado_juego = "extras"
        return
    
    # Si estamos en extras
    elif estado_juego == "extras":
        if key == keys.ESCAPE or key == keys.BACKSPACE: # type: ignore
            estado_juego = "menu"
        return
    
    # Si estamos jugando
    elif estado_juego == "jugando":
        # Volver al menú con ESC
        if key == keys.ESCAPE: # type: ignore
            estado_juego = "menu"
            return

        if game_over:
            if key == keys.R:
                game_over = False
                personaje.x = 0
                personaje.y = 0
                personaje.velocidad_y = 0
                personaje.velocidad_x = 0
                # No reiniciar la colección de items para mantener el progreso
                return

        if key == keys.F: # type: ignore
            modo_desarrollador = not modo_desarrollador
        
        # Mostrar/ocultar panel detallado de items
        if key == keys.U:
            mostrar_panel_detallado = not mostrar_panel_detallado
        
        # Activar/desactivar modo de colocación de terreno
        if key == keys.Y:
            modo_colocacion_terreno = not modo_colocacion_terreno
            if modo_colocacion_terreno:
                # Inicializar posición del terreno en la posición del personaje
                posicion_terreno_x = int(personaje.x // TILE_SIZE) * TILE_SIZE
                posicion_terreno_y = int(personaje.y // TILE_SIZE) * TILE_SIZE
            else:
                # Salir del modo de colocación
                pass
        
        # Reinicio completo del juego (incluyendo colección)
        if key == keys.F5:
            game_over = False
            personaje.x = 0
            personaje.y = 0
            personaje.velocidad_y = 0
            personaje.velocidad_x = 0
            personaje.puede_doble_salto = False
            items_recolectados.clear()  # Limpiar la colección
            # Reinicializar el mapa de items
            inicializar_enemigos()
            return

        if key == keys.SPACE and personaje.en_suelo:
            personaje.velocidad_y = VELOCIDAD_SALTO
            personaje.en_suelo = False

        if key == keys.R and personaje.objetos_cerca:
            x, y, item_id = personaje.objetos_cerca[0]
            # Agregar el item a la colección si no está ya recolectado
            if item_id not in items_recolectados:
                items_recolectados[item_id] = 1
            else:
                items_recolectados[item_id] += 1
            my_items[y][x] = 0
            personaje.objetos_cerca.remove((x, y, item_id))

        # Lógica del modo de colocación de terreno
        if modo_colocacion_terreno:
            # Mover el cuadro de colocación con las flechas
            if key == keys.LEFT:
                posicion_terreno_x = max(0, posicion_terreno_x - TILE_SIZE)
            elif key == keys.RIGHT:
                posicion_terreno_x = min((MATRIZ_ANCHO - 1) * TILE_SIZE, posicion_terreno_x + TILE_SIZE)
            elif key == keys.UP:
                posicion_terreno_y = max(0, posicion_terreno_y - TILE_SIZE)
            elif key == keys.DOWN:
                posicion_terreno_y = min((MATRIZ_ALTO - 1) * TILE_SIZE, posicion_terreno_y + TILE_SIZE)
            elif key == keys.TAB:
                # Cambiar el tipo de terreno a colocar
                if TERRENOS:
                    idx = TERRENOS.index(tipo_terreno_actual) if tipo_terreno_actual in TERRENOS else 0
                    tipo_terreno_actual = TERRENOS[(idx + 1) % len(TERRENOS)]

            elif key == keys.T:  # Confirmar colocación con la tecla T
                if cuadros_colocados < LIMITE_CUADROS_COLOCACION:
                    columna = int(posicion_terreno_x // TILE_SIZE)
                    fila = int(posicion_terreno_y // TILE_SIZE)
                    if 0 <= fila < len(my_map) and 0 <= columna < len(my_map[0]):
                        my_map[fila][columna] = tipo_terreno_actual
                        cuadros_colocados += 1
                        print(f"Terreno colocado con tecla T en posición ({fila}, {columna}) - Total colocados: {cuadros_colocados}")
                else:
                    print("¡Límite de cuadros de colocación alcanzado!")

def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        personaje.velocidad_x = 0

def update_camera():
    global camera_x, camera_y
    
    # Calcular el centro de la pantalla
    center_x = WINDOW_WIDTH // 2
    
    # Calcular la distancia del personaje al centro de la pantalla
    dist_x = personaje.x - (center_x + camera_x)
    
    # Mover la cámara horizontalmente
    if abs(dist_x) > CAMERA_MARGIN:
        if dist_x > 0:
            camera_x += CAMERA_SPEED
        else:
            camera_x -= CAMERA_SPEED
    
    # Limitar la cámara a los bordes del mapa
    max_camera_x = MATRIZ_ANCHO * TILE_SIZE - WINDOW_WIDTH
    camera_x = max(0, min(camera_x, max_camera_x))

def dibujar_panel_detallado_items():
    """Dibuja un panel detallado con información de los items recolectados"""
    if not items_recolectados or not mostrar_panel_detallado:
        return
    
    # Configuración del panel - ajustado para ventana más ancha
    panel_x = WIDTH - 160  # Ajustado para la nueva ventana
    panel_y = 10
    item_size = 20
    line_height = 25
    padding = 10
    
    # Calcular el alto necesario basado en el número de items únicos
    panel_height = len(items_recolectados) * line_height + padding * 2
    
    # Dibujar fondo del panel
    screen.draw.filled_rect(Rect(panel_x, panel_y, 150, panel_height), (0, 0, 0, 120))
    screen.draw.rect(Rect(panel_x, panel_y, 150, panel_height), (255, 255, 255, 150))
    
    # Dibujar título
    screen.draw.text("Items Recolectados:", (panel_x + 5, panel_y + 5), color="white", fontsize=14)
    
    # Dibujar cada item con su información
    for i, (item_id, cantidad) in enumerate(items_recolectados.items()):
        if item_id in id_to_image:
            y_pos = panel_y + padding + 20 + i * line_height
            
            # Dibujar el item
            item_actor = Actor(id_to_image[item_id], topleft=(panel_x + 5, y_pos - 7))
            item_actor.scale = 0.5
            item_actor.draw()
            
            # Dibujar el nombre del item (basado en el ID)
            item_name = f"Item {item_id}"
            screen.draw.text(item_name, (panel_x + 30, y_pos - 2), color="white", fontsize=12)
            
            # Dibujar la cantidad real
            cantidad_texto = f"x{cantidad}"
            screen.draw.text(cantidad_texto, (panel_x + 125, y_pos - 2), color="yellow", fontsize=12)

def dibujar_menu_principal():
    """Dibuja el menú principal con los 3 botones"""
    global boton_seleccionado
    
    # Configuración del menú - ajustado para ventana más ancha
    boton_width = 250  # Botones más anchos
    boton_height = 70  # Botones más altos
    espaciado = 30     # Más espacio entre botones
    centro_x = WIDTH // 2  # Centrar en la nueva ventana
    centro_y = HEIGHT // 2
    
    # Posiciones de los botones (en columna)
    botones = [
        (centro_x - boton_width // 2, centro_y - boton_height // 2),  # Jugar
        (centro_x - boton_width // 2, centro_y + boton_height // 2 + espaciado)   # Extras
    ]
    
    # Textos de los botones
    textos = ["JUGAR", "EXTRAS"]
    
    # Dibujar fondo degradado
    for y in range(HEIGHT):
        # Crear un degradado de azul oscuro a azul claro
        intensidad = int(20 + (y / HEIGHT) * 40)
        color = (intensidad, intensidad, intensidad + 20)
        screen.draw.line((0, y), (WIDTH, y), color)
    
    # Dibujar patrón de estrellas en el fondo
    for i in range(50):
        x = (i * 37) % WIDTH
        y = (i * 23) % HEIGHT
        if (x + y) % 2 == 0:
            screen.draw.circle((x, y), 1, (255, 255, 255, 100))
    
    # Dibujar cada botón
    for i, (x, y) in enumerate(botones):
        # Color del botón (resaltado si está seleccionado)
        if i == boton_seleccionado:
            # Botón seleccionado con efecto de brillo
            color_boton = (255, 215, 0)
            color_borde = (255, 255, 255)
            color_texto = (0, 0, 0)
            # Efecto de sombra para botón seleccionado
            screen.draw.filled_rect(Rect(x + 3, y + 3, boton_width, boton_height), (100, 100, 0, 100))
        else:
            # Botón normal
            color_boton = (100, 100, 100, 150)
            color_borde = (150, 150, 150)
            color_texto = (255, 255, 255)
        
        # Intentar usar la imagen bonus.png si existe
        try:
            boton_actor = Actor("bonus", topleft=(x, y))
            boton_actor.scale = boton_width / boton_actor.width
            boton_actor.draw()
        except:
            # Si no existe la imagen, dibujar un rectángulo con efectos
            screen.draw.filled_rect(Rect(x, y, boton_width, boton_height), color_boton)
            screen.draw.rect(Rect(x, y, boton_width, boton_height), color_borde, 3)
            
            # Efecto de brillo en la parte superior del botón
            if i == boton_seleccionado:
                screen.draw.line((x, y), (x + boton_width, y), (255, 255, 255, 100))
        
        # Dibujar el texto del botón
        texto_x = x + boton_width // 2
        texto_y = y + boton_height // 2
        screen.draw.text(textos[i], center=(texto_x, texto_y), color=color_texto, fontsize=24)
    
    # Dibujar título del juego con efectos
    # Sombra del título
    screen.draw.text("MAP BUILDER", center=(centro_x + 2, 30), color=(0, 0, 0, 100), fontsize=48)
    # Título principal
    screen.draw.text("MAP BUILDER", center=(centro_x, 32), color=(255, 215, 0), fontsize=48)
    
    # Línea decorativa bajo el título
    screen.draw.line((centro_x - 150, 50), (centro_x + 150, 50), (255, 215, 0))
    
    # Instrucciones con mejor diseño
    instrucciones_bg = Rect(centro_x - 200, HEIGHT - 80, 400, 40)
    screen.draw.filled_rect(instrucciones_bg, (0, 0, 0, 100))
    screen.draw.rect(instrucciones_bg, (255, 215, 0))
    screen.draw.text("Usa ↑↓ para navegar, ENTER para seleccionar", center=(centro_x, HEIGHT - 60), color="white", fontsize=18)

def dibujar_cuadro_colocacion_terreno():
    """Dibuja solo el borde entrelineado del cuadro de colocación de terreno, sin imagen de tile"""
    if not modo_colocacion_terreno:
        return
    
    # Calcular posición en pantalla (considerando la cámara)
    x = posicion_terreno_x - camera_x
    y = posicion_terreno_y
    
    # Solo dibujar si está en pantalla
    if -TILE_SIZE <= x <= WINDOW_WIDTH and 0 <= y <= HEIGHT:
        # Calcular el área del cuadro pequeño
        cuadro_x = x + (TILE_SIZE - TAMANO_CUADRO_COLOCACION)//2
        cuadro_y = y + (TILE_SIZE - TAMANO_CUADRO_COLOCACION)//2
        # Dibujar borde entrelineado (líneas discontinuas)
        color_borde = (255, 255, 0)
        dash = 4
        length = TAMANO_CUADRO_COLOCACION
        # Lados horizontales
        for i in range(0, length, dash*2):
            screen.draw.line((cuadro_x + i, cuadro_y), (cuadro_x + min(i+dash, length-1), cuadro_y), color_borde)
            screen.draw.line((cuadro_x + i, cuadro_y + length-1), (cuadro_x + min(i+dash, length-1), cuadro_y + length-1), color_borde)
        # Lados verticales
        for i in range(0, length, dash*2):
            screen.draw.line((cuadro_x, cuadro_y + i), (cuadro_x, cuadro_y + min(i+dash, length-1)), color_borde)
            screen.draw.line((cuadro_x + length-1, cuadro_y + i), (cuadro_x + length-1, cuadro_y + min(i+dash, length-1)), color_borde)
        # Dibujar texto indicativo
        texto_x = x + TILE_SIZE // 2
        texto_y = y - 25
        screen.draw.text("TERRENO", center=(texto_x, texto_y), color="yellow", fontsize=12)
        # Mostrar el tipo de terreno seleccionado
        screen.draw.text(f"ID: {tipo_terreno_actual}", center=(texto_x, texto_y - 15), color="orange", fontsize=10)
        if cuadros_colocados < LIMITE_CUADROS_COLOCACION:
            screen.draw.text(f"Presiona T para colocar ({LIMITE_CUADROS_COLOCACION - cuadros_colocados} restantes)", center=(texto_x, texto_y + 15), color="white", fontsize=10)
        else:
            screen.draw.text("¡Límite alcanzado!", center=(texto_x, texto_y + 15), color="red", fontsize=12)

def on_mouse_down(pos, button):
    global modo_colocacion_terreno, posicion_terreno_x, posicion_terreno_y
    if estado_juego == "jugando" and modo_colocacion_terreno and button == mouse.LEFT:
        # Calcular la posición del cuadro de colocación en pantalla
        x = posicion_terreno_x - camera_x
        y = posicion_terreno_y
        # Calcular el área del cuadro pequeño
        cuadro_x = x + (TILE_SIZE - TAMANO_CUADRO_COLOCACION)//2
        cuadro_y = y + (TILE_SIZE - TAMANO_CUADRO_COLOCACION)//2
        cuadro_rect = Rect(cuadro_x, cuadro_y, TAMANO_CUADRO_COLOCACION, TAMANO_CUADRO_COLOCACION)
        # Verificar si el clic está dentro del cuadro
        if cuadro_rect.collidepoint(pos):
            columna = int(posicion_terreno_x // TILE_SIZE)
            fila = int(posicion_terreno_y // TILE_SIZE)
            if 0 <= fila < len(my_map) and 0 <= columna < len(my_map[0]):
                my_map[fila][columna] = tipo_terreno_actual
                print(f"Terreno colocado con clic en posición ({fila}, {columna}) - Tipo: {tipo_terreno_actual}")

def draw():
    screen.clear()
    
    # Si estamos en el menú principal
    if estado_juego == "menu":
        dibujar_menu_principal()
        return
    
    # Si estamos en extras
    elif estado_juego == "extras":
        # Fondo
        screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0))
        # Título
        screen.draw.text("EXTRAS", center=(WIDTH//2, 120), color="white", fontsize=48)
        # Contenido (placeholder)
        screen.draw.text("Contenido extra del juego", center=(WIDTH//2, HEIGHT//2), color="white", fontsize=28)
        screen.draw.text("Presiona ESC para volver", center=(WIDTH//2, HEIGHT - 60), color="white", fontsize=18)
        return
    
    # Si estamos jugando
    elif estado_juego == "jugando":
        # Actualizar la posición de la cámara
        update_camera()

        # Calcular el rango de tiles visibles
        start_col = max(0, int(camera_x // TILE_SIZE))
        end_col = min(MATRIZ_ANCHO, int((camera_x + WINDOW_WIDTH) // TILE_SIZE) + 1)

        # Dibujar solo los tiles visibles
        for fila in range(len(my_map)):
            for columna in range(start_col, end_col):
                x = columna * TILE_SIZE - camera_x
                y = fila * TILE_SIZE

                tile_id = my_map[fila][columna]
                if tile_id != 0 and tile_id in id_to_image:
                    tile_actor = Actor(id_to_image[tile_id], topleft=(x, y))
                    tile_actor.width = TILE_SIZE
                    tile_actor.height = TILE_SIZE
                    tile_actor.draw()

                item_id = my_items[fila][columna]
                if item_id != 0 and item_id in id_to_image:
                    item_actor = Actor(id_to_image[item_id], topleft=(x, y))
                    item_actor.draw()

                    # Dibujar borde amarillo si el item está cerca del personaje
                    if item_id in ITEMS and any(x == columna and y == fila for x, y, _ in personaje.objetos_cerca):
                        # Dibujar borde amarillo
                        for i in range(4):
                            screen.draw.line((x + i, y + i), (x + TILE_SIZE - i, y + i), (255, 255, 0))
                            screen.draw.line((x + i, y + i), (x + i, y + TILE_SIZE - i), (255, 255, 0))
                            screen.draw.line((x + TILE_SIZE - i, y + i), (x + TILE_SIZE - i, y + TILE_SIZE - i), (255, 255, 0))
                            screen.draw.line((x + i, y + TILE_SIZE - i), (x + TILE_SIZE - i, y + TILE_SIZE - i), (255, 255, 0))
        
        # Dibujar los enemigos activos que están en pantalla
        for enemigo in enemigos_activos:
            x = enemigo.x - camera_x
            if 0 <= x <= WINDOW_WIDTH:
                enemigo_actor = Actor(enemigo.obtener_imagen_actual(), topleft=(x, enemigo.y))
                enemigo_actor.scale = ENEMIGO_SIZE / TILE_SIZE  # Calcular escala automáticamente
                enemigo_actor.draw()
                
                if modo_desarrollador:
                    screen.draw.rect(Rect(x, enemigo.y, ENEMIGO_SIZE, ENEMIGO_SIZE), (0, 255, 0))

        # Dibujar personaje
        x = personaje.x - camera_x
        personaje_actor = Actor(personaje.image, topleft=(x, personaje.y))
        personaje_actor.draw()

        # Dibujar texto de interacción si hay items cerca
        if personaje.objetos_cerca:
            texto_x = x + personaje.hitbox_width / 2
            texto_y = personaje.y - 20
            screen.draw.text("Presiona R para tomar", center=(texto_x, texto_y), color="white", fontsize=20)

        if game_over:
            screen.draw.text("¡Has perdido!", center=(WINDOW_WIDTH//2, HEIGHT//2), fontsize=60, color="red")
            screen.draw.text("Presiona R para reiniciar", center=(WINDOW_WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")

        if modo_desarrollador:
            # Mostrar hitbox real del personaje
            screen.draw.rect(Rect(x, personaje.y, personaje.hitbox_width, personaje.hitbox_height), (255, 0, 0))
            screen.draw.text("Modo Desarrollador: ON", (10, 30), color="yellow", fontsize=14)
            # Mostrar controles adicionales
            screen.draw.text("F5: Reinicio completo", (10, 50), color="yellow", fontsize=14)
            screen.draw.text("U: Panel detallado de items", (10, 70), color="yellow", fontsize=14)
            screen.draw.text("Y: Modo colocación terreno", (10, 90), color="yellow", fontsize=14)
            
            # Mostrar información del modo de colocación si está activo
            if modo_colocacion_terreno:
                screen.draw.text("MODO COLOCACIÓN ACTIVO", (10, 110), color="red", fontsize=16)
                screen.draw.text("Flechas: Mover cuadro", (10, 130), color="yellow", fontsize=14)
                screen.draw.text("T: Colocar terreno", (10, 150), color="yellow", fontsize=14)

        # Dibujar el panel detallado de items
        dibujar_panel_detallado_items()

        # Dibujar el cuadro de colocación de terreno
        dibujar_cuadro_colocacion_terreno()

# Inicializar enemigos al cargar el juego
inicializar_enemigos()

pgzrun.go()
