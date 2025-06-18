# MapBuilder - Documentación Técnica

## Índice

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Flujo de Ejecución](#flujo-de-ejecución)
3. [Sistema de Configuración](#sistema-de-configuración)
4. [Sistema de Colisiones](#sistema-de-colisiones)
5. [Sistema de Física](#sistema-de-física)
6. [Sistema de Renderizado](#sistema-de-renderizado)
7. [Sistema de Enemigos](#sistema-de-enemigos)
8. [Sistema de Items](#sistema-de-items)
9. [Sistema de Cámara](#sistema-de-cámara)
10. [Optimizaciones](#optimizaciones)
11. [Guía de Modificación](#guía-de-modificación)

## Arquitectura del Sistema

### Estructura General

El juego sigue una arquitectura basada en eventos de Pygame Zero con las siguientes características:

- **Inicialización**: Carga de configuraciones y recursos al inicio
- **Bucle Principal**: `update()` y `draw()` ejecutándose a 60 FPS
- **Gestión de Estados**: Sistema de estados para menú, juego y extras
- **Sistema de Eventos**: Manejo de entrada de teclado

### Diagrama de Flujo

```
Inicio
  ↓
Cargar mapa.txt
  ↓
Cargar configuraciones
  ↓
Inicializar personaje y enemigos
  ↓
Bucle Principal:
  ├── update() → Lógica del juego
  ├── draw() → Renderizado
  └── Eventos de teclado
```

## Flujo de Ejecución

### 1. Inicialización (Líneas 1-50)

```python
# Carga de dimensiones del mapa
with open('mapa.txt', 'r') as f:
    # Extrae MATRIZ_ALTO y MATRIZ_ANCHO
    
# Configuración de ventana
WINDOW_WIDTH = min(MATRIZ_ANCHO * TILE_SIZE, 750)
WIDTH = min(WINDOW_WIDTH + 400, 750)
```

### 2. Carga de Configuraciones (Líneas 51-120)

```python
def cargar_configuraciones():
    # Lee el diccionario configuraciones del archivo mapa.txt
    # Aplica valores a variables globales
    # Maneja errores de archivo no encontrado
```

### 3. Inicialización de Entidades (Líneas 121-200)

```python
# Creación del personaje
personaje = Actor("personajes/tile0")
# Configuración de hitbox
aplicar_configuracion_hitbox()

# Carga de listas de tipos
TERRENOS = []  # IDs de tiles de terreno
ITEMS = []     # IDs de items coleccionables
ENEMIGOS = []  # IDs de enemigos
```

### 4. Bucle Principal (Líneas 470-607)

```python
def update():
    # Gestión de estados del juego
    if estado_juego == "menu":
        return
    elif estado_juego == "extras":
        return
    elif estado_juego == "jugando":
        # Lógica principal del juego
        # Movimiento del personaje
        # Física y colisiones
        # Actualización de enemigos
```

## Sistema de Configuración

### Estructura del Archivo mapa.txt

El archivo de configuración utiliza una sintaxis híbrida Python/comentarios:

```python
# Sección 1: Dimensiones
Matrix Size: 10x30

# Sección 2: Configuraciones del juego
configuraciones = {
    'velocidad_personaje': 3,
    'velocidad_salto': 15,
    'gravedad': 0.8,
    # ... más configuraciones
}

# Sección 3: Mapeo de IDs
# ID Mapping
# 1: (terrenos/tile0.png) : Terreno básico
# 2: (items/tile0.png) : Item coleccionable
# End ID Mapping

# Sección 4: Matrices del mapa
my_map = [[...]]
my_items = [[...]]
my_rotations = [[...]]
```

### Proceso de Carga

1. **Lectura de Dimensiones**: Busca la línea "Matrix Size:"
2. **Ejecución de Configuraciones**: Usa `exec()` para cargar el diccionario
3. **Aplicación de Valores**: Asigna valores a variables globales
4. **Manejo de Errores**: Fallback a valores por defecto

### Variables Configurables

| Variable | Tipo | Rango | Descripción |
|----------|------|-------|-------------|
| `VELOCIDAD_MOVIMIENTO` | float | > 0 | Velocidad horizontal del personaje |
| `VELOCIDAD_SALTO` | float | < 0 | Fuerza del salto (negativo) |
| `GRAVEDAD` | float | > 0 | Aceleración gravitacional |
| `PROBABILIDAD_SALTO_ENEMIGO` | float | 0.0-1.0 | Probabilidad de salto de enemigos |
| `CAMERA_SPEED` | int | > 0 | Velocidad de seguimiento de cámara |
| `CAMERA_MARGIN` | int | > 0 | Margen para activar movimiento de cámara |

## Sistema de Colisiones

### Arquitectura de Colisiones

El sistema utiliza tres funciones principales:

1. **`verificar_colision_horizontal(x, y)`**: Colisiones laterales
2. **`verificar_colision_vertical(x, y)`**: Colisiones arriba/abajo
3. **`verificar_colision(x, y, es_personaje=False)`**: Función unificada

### Algoritmo de Detección

```python
def verificar_colision_horizontal(x, y):
    if x == personaje.x:  # Si es el personaje
        # Solo verifica colisiones con items
        for offset_y in range(0, personaje.hitbox_height, 5):
            tile_id, item_id = obtener_tile_en_posicion(x, y + offset_y)
            if item_id in ITEMS:
                return True
    else:  # Para enemigos
        # Verifica colisiones con terrenos e items
        for offset_y in [1, TILE_SIZE - 2]:
            for offset_x in [0, TILE_SIZE - 1]:
                tile_id, item_id = obtener_tile_en_posicion(x + offset_x, y + offset_y)
                if (tile_id in TERRENOS) or (item_id in ITEMS):
                    return True
    return False
```

### Optimizaciones de Colisión

- **Hitbox Personalizable**: Tamaño ajustable según configuración
- **Muestreo de Puntos**: Verificación cada 5 píxeles para precisión
- **Diferentes Reglas**: Personaje solo colisiona con items, enemigos con todo

## Sistema de Física

### Implementación de Gravedad

```python
# En update()
if not personaje.en_suelo:
    personaje.velocidad_y += GRAVEDAD
```

### Sistema de Salto

```python
# Salto simple
if personaje.en_suelo:
    personaje.velocidad_y = VELOCIDAD_SALTO
    personaje.en_suelo = False
    personaje.puede_doble_salto = True

# Doble salto
elif personaje.puede_doble_salto and personaje.velocidad_y < 0:
    personaje.velocidad_y = VELOCIDAD_SALTO * 0.8
    personaje.puede_doble_salto = False
```

### Integración de Movimiento

```python
# Calcular nuevas posiciones
nueva_x = personaje.x + personaje.velocidad_x
nueva_y = personaje.y + personaje.velocidad_y

# Verificar colisiones
colision_vertical, colision_horizontal, es_suelo = verificar_colision(nueva_x, nueva_y, True)

# Aplicar movimiento
if not colision_vertical:
    personaje.y = nueva_y
    personaje.en_suelo = False
else:
    if personaje.velocidad_y > 0:
        personaje.velocidad_y = 0
        personaje.en_suelo = es_suelo
```

## Sistema de Renderizado

### Optimización de Culling

```python
# Calcular rango de tiles visibles
start_col = max(0, int(camera_x // TILE_SIZE))
end_col = min(MATRIZ_ANCHO, int((camera_x + WINDOW_WIDTH) // TILE_SIZE) + 1)

# Renderizar solo tiles visibles
for fila in range(len(my_map)):
    for columna in range(start_col, end_col):
        x = columna * TILE_SIZE - camera_x
        y = fila * TILE_SIZE
        # Renderizar tile
```

### Sistema de Capas

1. **Capa de Terreno**: `my_map` - Fondo y plataformas
2. **Capa de Items**: `my_items` - Objetos coleccionables
3. **Capa de Enemigos**: `enemigos_activos` - Entidades móviles
4. **Capa de UI**: Paneles y texto

### Efectos Visuales

- **Bordes de Interacción**: Líneas amarillas en items cercanos
- **Hitbox Debug**: Rectángulos rojos en modo desarrollador
- **Panel de Items**: Fondo semitransparente con información

## Sistema de Enemigos

### Clase Enemigo

```python
class Enemigo:
    def __init__(self, x, y, tipo_id):
        self.x = x
        self.y = y
        self.tipo_id = tipo_id
        self.velocidad_y = 0
        self.velocidad_x = 0
        self.en_suelo = False
        self.direccion = random.choice([-1, 1])
        self.tiempo_cambio_direccion = random.randint(60, 180)
        self.contador = 0
        self.imagen = id_to_image.get(tipo_id, "enemigos/default")
```

### IA de Enemigos

```python
def actualizar(self):
    # Aplicar gravedad
    self.velocidad_y += GRAVEDAD
    
    # Salto aleatorio
    if self.en_suelo and random.random() < PROBABILIDAD_SALTO_ENEMIGO:
        self.velocidad_y = VELOCIDAD_SALTO
        self.en_suelo = False
    
    # Cambio de dirección
    self.contador += 1
    if self.contador >= self.tiempo_cambio_direccion:
        self.direccion *= -1
        self.contador = 0
        self.tiempo_cambio_direccion = random.randint(60, 180)
    
    # Movimiento horizontal
    self.velocidad_x = self.direccion * (VELOCIDAD_MOVIMIENTO * 0.6)
```

### Inicialización de Enemigos

```python
def inicializar_enemigos():
    enemigos_activos.clear()
    for fila in range(len(my_items)):
        for columna in range(len(my_items[0])):
            item_id = my_items[fila][columna]
            if item_id in ENEMIGOS:
                nuevo_enemigo = Enemigo(columna * TILE_SIZE, fila * TILE_SIZE, item_id)
                enemigos_activos.append(nuevo_enemigo)
                my_items[fila][columna] = 0  # Eliminar de la matriz
```

## Sistema de Items

### Detección de Interacción

```python
def verificar_interaccion():
    personaje.objetos_cerca = []
    radio_interaccion = TILE_SIZE * 1.5
    
    centro_x = personaje.x + personaje.hitbox_width / 2
    centro_y = personaje.y + personaje.hitbox_height / 2
    
    inicio_x = max(0, int((centro_x - radio_interaccion) // TILE_SIZE))
    fin_x = min(len(my_map[0]), int((centro_x + radio_interaccion) // TILE_SIZE) + 1)
    # ... verificar items en el rango
```

### Recolección de Items

```python
if keyboard.E and personaje.objetos_cerca:
    x, y, item_id = personaje.objetos_cerca[0]
    if item_id not in items_recolectados:
        items_recolectados[item_id] = 1
    else:
        items_recolectados[item_id] += 1
    my_items[y][x] = 0
    personaje.objetos_cerca.remove((x, y, item_id))
```

## Sistema de Cámara

### Algoritmo de Seguimiento

```python
def update_camera():
    center_x = WINDOW_WIDTH // 2
    dist_x = personaje.x - (center_x + camera_x)
    
    if abs(dist_x) > CAMERA_MARGIN:
        if dist_x > 0:
            camera_x += CAMERA_SPEED
        else:
            camera_x -= CAMERA_SPEED
    
    # Limitar cámara a bordes del mapa
    max_camera_x = MATRIZ_ANCHO * TILE_SIZE - WINDOW_WIDTH
    camera_x = max(0, min(camera_x, max_camera_x))
```

### Características

- **Seguimiento Suave**: Movimiento gradual hacia el personaje
- **Margen de Activación**: Solo se mueve cuando el personaje se aleja
- **Límites del Mapa**: No sale de los bordes del nivel
- **Velocidad Configurable**: Ajustable desde configuración

## Optimizaciones

### Renderizado

1. **Culling de Tiles**: Solo renderiza tiles visibles
2. **Cálculo de Rango**: Optimiza el bucle de renderizado
3. **Límite de Ventana**: Respeta límites de Pygame Zero

### Memoria

1. **Enemigos Dinámicos**: Se crean solo cuando es necesario
2. **Listas Optimizadas**: Uso eficiente de estructuras de datos
3. **Carga Lazy**: Configuraciones se cargan solo al inicio

### Rendimiento

1. **Muestreo de Colisiones**: Verificación cada 5 píxeles
2. **Cálculos Reducidos**: Minimiza operaciones matemáticas
3. **Estructuras Eficientes**: Uso de diccionarios para búsquedas rápidas

## Guía de Modificación

### Agregar Nuevos Tipos de Items

1. **Actualizar mapeo de IDs**:
```python
# En mapa.txt
# 10: (items/nuevo_item.png) : Nuevo item
```

2. **Agregar a la lista de tipos**:
```python
# En main.py
if 'nuevo_item' in descripcion:
    ITEMS.append(id_val)
```

3. **Implementar lógica específica**:
```python
# En la función de interacción
if item_id == 10:  # Nuevo item
    # Lógica específica
```

### Modificar Física del Personaje

1. **Ajustar constantes**:
```python
VELOCIDAD_MOVIMIENTO = 4  # Más rápido
VELOCIDAD_SALTO = -18     # Salto más alto
GRAVEDAD = 0.9            # Gravedad más fuerte
```

2. **Modificar lógica de salto**:
```python
# En update()
if keyboard.SPACE and personaje.en_suelo:
    personaje.velocidad_y = VELOCIDAD_SALTO
    # Agregar efectos adicionales
```

### Agregar Nuevos Estados de Juego

1. **Definir nuevo estado**:
```python
estado_juego = "menu"  # Agregar "nuevo_estado"
```

2. **Implementar lógica**:
```python
def update():
    if estado_juego == "nuevo_estado":
        # Lógica del nuevo estado
        return
```

3. **Agregar renderizado**:
```python
def draw():
    if estado_juego == "nuevo_estado":
        # Renderizado del nuevo estado
        return
```

### Optimizar Rendimiento

1. **Reducir cálculos de colisión**:
```python
# Aumentar el paso de muestreo
for offset_y in range(0, personaje.hitbox_height, 10):  # Cada 10 píxeles
```

2. **Optimizar renderizado**:
```python
# Cachear cálculos frecuentes
camera_offset_x = camera_x // TILE_SIZE
```

3. **Reducir memoria**:
```python
# Usar generadores en lugar de listas
def obtener_items_cercanos():
    for item in items_recolectados.items():
        yield item
```

### Debugging

1. **Modo Desarrollador**:
```python
if modo_desarrollador:
    screen.draw.text(f"FPS: {clock.get_fps()}", (10, 90))
    screen.draw.text(f"Enemigos: {len(enemigos_activos)}", (10, 110))
```

2. **Logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def verificar_colision(x, y):
    logger.debug(f"Verificando colisión en ({x}, {y})")
```

3. **Profiling**:
```python
import time

def update():
    start_time = time.time()
    # ... lógica del juego
    end_time = time.time()
    if modo_desarrollador:
        screen.draw.text(f"Update: {(end_time - start_time)*1000:.2f}ms", (10, 130))
```

## Consideraciones de Seguridad

### Uso de exec()

El código usa `exec()` para cargar configuraciones, lo cual puede ser peligroso:

```python
# ❌ Peligroso
exec(config_section, {}, config_dict)

# ✅ Más seguro (alternativa)
import ast
config_dict = ast.literal_eval(config_section)
```

### Validación de Entrada

```python
def validar_configuracion(config):
    valores_permitidos = {
        'velocidad_personaje': (0.1, 10.0),
        'velocidad_salto': (1.0, 30.0),
        'gravedad': (0.1, 2.0),
    }
    
    for key, (min_val, max_val) in valores_permitidos.items():
        if key in config:
            if not (min_val <= config[key] <= max_val):
                raise ValueError(f"Valor inválido para {key}")
```

## Conclusión

El sistema está diseñado para ser modular y extensible. Las principales áreas de mejora incluyen:

1. **Seguridad**: Reemplazar `exec()` con métodos más seguros
2. **Rendimiento**: Implementar spatial partitioning para colisiones
3. **Modularidad**: Separar sistemas en módulos independientes
4. **Testing**: Agregar tests unitarios y de integración
5. **Documentación**: Documentar APIs internas con docstrings 