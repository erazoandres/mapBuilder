# MapBuilder - Documentación del Juego

## Descripción General

MapBuilder es un juego de plataformas 2D desarrollado con Pygame Zero que permite a los jugadores explorar mapas personalizables, recolectar items y enfrentarse a enemigos. El juego incluye un sistema de menús, cámara dinámica, física de plataformas y un sistema de configuración flexible.

## Características Principales

- **Sistema de Mapas Dinámicos**: Carga mapas desde archivos de texto
- **Física de Plataformas**: Gravedad, salto doble y colisiones realistas
- **Sistema de Items**: Recolección y contabilización de items
- **Enemigos Inteligentes**: IA básica con movimiento y salto aleatorio
- **Cámara Dinámica**: Seguimiento suave del personaje
- **Menú Principal**: Interfaz de usuario con navegación por teclado
- **Modo Desarrollador**: Herramientas de debug y desarrollo
- **Configuración Flexible**: Parámetros ajustables desde archivo externo

## Estructura del Proyecto

```
MapBuilder/
├── main.py              # Archivo principal del juego
├── mapa.txt             # Archivo de configuración del mapa
├── images/              # Directorio de recursos gráficos
│   ├── personajes/      # Sprites del personaje
│   ├── enemigos/        # Sprites de enemigos
│   ├── terrenos/        # Tiles de terreno
│   ├── items/           # Sprites de items
│   ├── fondos/          # Fondos del juego
│   └── bonus.png        # Imagen para botones
├── sounds/              # Archivos de audio
│   ├── jump.wav         # Sonido de salto
│   └── sonidosalto.wav  # Sonido alternativo de salto
├── index.html           # Archivo HTML (no utilizado)
├── script.js            # Archivo JavaScript (no utilizado)
├── style.css            # Archivo CSS (no utilizado)
└── README.md            # Este archivo de documentación
```

## Instalación y Ejecución

### Requisitos Previos

- Python 3.6 o superior
- Pygame Zero (`pip install pgzero`)

### Ejecutar el Juego

```bash
python main.py
```

## Controles del Juego

### Menú Principal
- **↑/↓**: Navegar entre opciones
- **ENTER/ESPACIO**: Seleccionar opción

### Durante el Juego
- **←/→**: Movimiento horizontal
- **ESPACIO/↑**: Salto (doble salto disponible)
- **E**: Interactuar con items cercanos
- **R**: Recolectar items (alternativo)
- **ESC**: Volver al menú principal
- **F**: Activar/desactivar modo desarrollador
- **U**: Mostrar/ocultar panel detallado de items
- **F5**: Reinicio completo del juego

## Configuración del Juego

El juego se configura a través del archivo `mapa.txt`. Este archivo contiene:

### Estructura del Archivo mapa.txt

```python
# Configuración del mapa
Matrix Size: 10x30

# Configuraciones del juego
configuraciones = {
    'velocidad_personaje': 3,
    'velocidad_salto': 15,
    'gravedad': 0.8,
    'prob_salto_enemigo': 0.02,
    'velocidad_camara': 8,
    'margen_camara': 200,
    'volumen_sonido': 50,
    'pantalla_completa': "No",
    'efectos_visuales': "Básicos",
    'tamaño_hitbox': "Normal"  # "Pequeño", "Normal", "Grande"
}

# Mapeo de IDs a imágenes
# ID Mapping
# 1: (terrenos/tile0.png) : Terreno básico
# 2: (items/tile0.png) : Item coleccionable
# 3: (enemigos/tile0.png) : Enemigo básico
# End ID Mapping

# Matrices del mapa
my_map = [
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    # ... más filas
]

my_items = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    # ... más filas
]

my_rotations = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    # ... más filas
]
```

### Parámetros de Configuración

| Parámetro | Descripción | Valores | Default |
|-----------|-------------|---------|---------|
| `velocidad_personaje` | Velocidad de movimiento horizontal | Número positivo | 3 |
| `velocidad_salto` | Fuerza del salto | Número positivo | 15 |
| `gravedad` | Fuerza de la gravedad | Número positivo | 0.8 |
| `prob_salto_enemigo` | Probabilidad de salto de enemigos | 0.0-1.0 | 0.02 |
| `velocidad_camara` | Velocidad de seguimiento de la cámara | Número positivo | 8 |
| `margen_camara` | Margen para activar el movimiento de cámara | Píxeles | 200 |
| `volumen_sonido` | Volumen del audio | 0-100 | 50 |
| `pantalla_completa` | Modo pantalla completa | "Sí"/"No" | "No" |
| `efectos_visuales` | Nivel de efectos visuales | "Básicos"/"Avanzados" | "Básicos" |
| `tamaño_hitbox` | Tamaño de la caja de colisión | "Pequeño"/"Normal"/"Grande" | "Normal" |

## Arquitectura del Código

### Constantes y Configuración

```python
TILE_SIZE = 36                    # Tamaño de cada tile en píxeles
PROBABILIDAD_SALTO_ENEMIGO = 0.02 # Probabilidad de salto de enemigos
GRAVEDAD = 0.8                    # Fuerza de la gravedad
VELOCIDAD_SALTO = -15             # Velocidad inicial del salto
VELOCIDAD_MOVIMIENTO = 3          # Velocidad de movimiento horizontal
```

### Variables Globales Importantes

- `estado_juego`: Controla el estado actual ("menu", "jugando", "extras")
- `camera_x, camera_y`: Posición de la cámara
- `items_recolectados`: Diccionario con items recolectados y sus cantidades
- `enemigos_activos`: Lista de enemigos activos en el juego

### Clases Principales

#### Clase Enemigo

```python
class Enemigo:
    def __init__(self, x, y, tipo_id):
        # Inicialización del enemigo
    
    def actualizar(self):
        # Lógica de movimiento y comportamiento del enemigo
```

**Atributos:**
- `x, y`: Posición del enemigo
- `tipo_id`: ID del tipo de enemigo
- `velocidad_x, velocidad_y`: Velocidades de movimiento
- `en_suelo`: Estado de contacto con el suelo
- `direccion`: Dirección de movimiento (-1: izquierda, 1: derecha)

### Funciones Principales

#### Gestión de Configuración

```python
def cargar_configuraciones():
    """Carga las configuraciones desde mapa.txt"""
    
def aplicar_configuracion_hitbox():
    """Aplica la configuración de tamaño de hitbox al personaje"""
```

#### Sistema de Colisiones

```python
def verificar_colision_horizontal(x, y):
    """Verifica colisiones horizontales"""
    
def verificar_colision_vertical(x, y):
    """Verifica colisiones verticales"""
    
def verificar_colision(x, y, es_personaje=False):
    """Función unificada para verificar colisiones"""
```

#### Sistema de Interacción

```python
def verificar_interaccion():
    """Verifica items cercanos al personaje para interacción"""
    
def obtener_tile_en_posicion(x, y):
    """Obtiene el tile y item en una posición específica"""
```

#### Gestión de Enemigos

```python
def inicializar_enemigos():
    """Inicializa los enemigos desde el mapa de items"""
```

#### Sistema de Cámara

```python
def update_camera():
    """Actualiza la posición de la cámara para seguir al personaje"""
```

#### Funciones de Renderizado

```python
def dibujar_panel_detallado_items():
    """Dibuja el panel detallado de items recolectados"""
    
def dibujar_menu_principal():
    """Dibuja el menú principal del juego"""
```

#### Funciones de Pygame Zero

```python
def update():
    """Función principal de actualización del juego"""
    
def draw():
    """Función principal de renderizado"""
    
def on_key_down(key):
    """Maneja eventos de teclas presionadas"""
    
def on_key_up(key):
    """Maneja eventos de teclas liberadas"""
```

## Sistema de Física

### Gravedad y Salto

- **Gravedad**: Se aplica constantemente cuando el personaje no está en el suelo
- **Salto Simple**: Presionar ESPACIO o ↑ cuando está en el suelo
- **Doble Salto**: Disponible cuando el personaje está en el aire y no ha usado el segundo salto

### Colisiones

- **Colisiones Verticales**: Detectan suelo y techo
- **Colisiones Horizontales**: Detectan paredes y obstáculos
- **Hitbox Personalizable**: Tamaño ajustable según configuración

## Sistema de Items

### Tipos de Items

- **Items Coleccionables**: Se pueden recolectar con E o R
- **Items de Terreno**: Bloquean el movimiento
- **Items de Enemigos**: Se convierten en enemigos activos

### Interacción

- **Radio de Interacción**: 1.5 tiles alrededor del personaje
- **Indicador Visual**: Borde amarillo en items cercanos
- **Panel de Inventario**: Muestra items recolectados y cantidades

## Sistema de Enemigos

### Comportamiento

- **Movimiento Automático**: Cambian dirección aleatoriamente
- **Salto Aleatorio**: Probabilidad configurable de salto
- **Colisiones**: Detectan obstáculos y cambian dirección
- **Velocidad Reducida**: 60% de la velocidad del personaje

### IA Básica

- **Patrullaje**: Movimiento de lado a lado
- **Detección de Obstáculos**: Cambio de dirección al colisionar
- **Límites del Mapa**: Se mantienen dentro de los bordes

## Optimización y Rendimiento

### Renderizado Optimizado

- **Culling de Tiles**: Solo se renderizan los tiles visibles
- **Cálculo de Rango**: Se calcula el rango de tiles visibles basado en la cámara
- **Límite de Ventana**: Máximo 750px de ancho para compatibilidad

### Gestión de Memoria

- **Enemigos Dinámicos**: Se crean solo cuando es necesario
- **Listas Optimizadas**: Uso eficiente de estructuras de datos
- **Carga Lazy**: Configuraciones se cargan solo al inicio

## Modo Desarrollador

### Características

- **Hitbox Visible**: Muestra las cajas de colisión
- **Información de Debug**: Muestra estado del juego
- **Controles Adicionales**: Acceso a funciones de desarrollo
- **Panel Detallado**: Información completa de items

### Activación

Presionar **F** durante el juego para activar/desactivar el modo desarrollador.

## Personalización

### Crear Nuevos Mapas

1. Crear un archivo `mapa.txt` con la estructura especificada
2. Definir las matrices `my_map`, `my_items` y `my_rotations`
3. Configurar el mapeo de IDs a imágenes
4. Ajustar las configuraciones según sea necesario

### Agregar Nuevos Sprites

1. Colocar las imágenes en el directorio `images/` correspondiente
2. Actualizar el mapeo de IDs en `mapa.txt`
3. Asignar los IDs en las matrices del mapa

### Modificar Configuraciones

Editar el diccionario `configuraciones` en `mapa.txt` para ajustar:
- Física del juego
- Comportamiento de enemigos
- Configuración de la cámara
- Efectos visuales y audio

## Solución de Problemas

### Problemas Comunes

1. **Error de archivo no encontrado**: Verificar que `mapa.txt` existe
2. **Imágenes no cargan**: Verificar rutas en el mapeo de IDs
3. **Colisiones incorrectas**: Ajustar configuración de hitbox
4. **Rendimiento lento**: Reducir tamaño del mapa o optimizar sprites

### Debug

- Usar modo desarrollador (F) para ver información de debug
- Verificar la consola para mensajes de error
- Comprobar que todas las imágenes referenciadas existen

## Limitaciones Conocidas

- **Tamaño de Ventana**: Máximo 750px de ancho por limitaciones de Pygame Zero
- **Audio**: Volumen controlado por archivos de audio externos
- **Resolución**: Optimizado para tiles de 36x36 píxeles
- **Enemigos**: IA básica sin pathfinding avanzado

## Futuras Mejoras

- [ ] Sistema de niveles múltiples
- [ ] Guardado de progreso
- [ ] Efectos de sonido mejorados
- [ ] Animaciones de sprites
- [ ] Sistema de puntuación
- [ ] Power-ups y habilidades especiales
- [ ] Editor de mapas integrado
- [ ] Modo multijugador local

## Créditos

Desarrollado como proyecto de juego de plataformas 2D con Pygame Zero.

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal. 