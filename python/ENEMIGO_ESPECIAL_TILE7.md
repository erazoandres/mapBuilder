# Enemigo Especial - Tile7

## Descripción General

El enemigo que usa la imagen `tile7.png` es un enemigo especial con comportamientos únicos y avanzados que lo diferencian de los enemigos normales del juego.

## Configuración del Mapeo

### ID Mapping
En el archivo `mapa.txt`, el enemigo especial está configurado con el siguiente mapeo:
```
# 2: 142 (enemigos/tile7.png)
```

Esto significa que:
- **ID 2** en el mapa corresponde al **ID 142** (tile7.png)
- El enemigo especial se crea cuando se encuentra un enemigo con ID 2 en la matriz `my_items`

### Inicialización
El sistema automáticamente:
1. Detecta enemigos con ID 2 en la matriz
2. Los mapea al ID 142 (tile7.png)
3. Crea instancias de la clase `EnemigoEspecial`
4. Los agrega a la lista `enemigos_activos`

## Características Especiales

### Estados de Comportamiento

El enemigo especial tiene tres estados principales:

1. **Patrulla**: Estado normal donde el enemigo patrulla el área
2. **Ataque**: Estado agresivo cuando detecta al jugador
3. **Retirada**: Estado defensivo cuando está en desventaja

### Atributos Únicos

- **Vida**: 3 puntos de vida (configurable)
- **Velocidad**: 20% más rápido que enemigos normales
- **Rango de Detección**: 150 píxeles
- **Rango de Ataque**: 80 píxeles
- **Invulnerabilidad**: 1 segundo después de recibir daño

## Comportamientos Específicos

### Movimiento de Patrulla
- Se mueve de un lado a otro en el área asignada
- Detecta automáticamente al jugador cuando está dentro del rango
- Cambia a estado de ataque cuando detecta al jugador

### Movimiento de Ataque
- Se mueve rápidamente hacia el jugador
- Realiza saltos de ataque cuando está cerca
- Mantiene el estado de ataque por hasta 3 segundos
- Cambia a retirada si el jugador está muy alto o muy bajo

### Movimiento de Retirada
- Se aleja del jugador
- Realiza saltos de escape
- Vuelve a patrulla después de un tiempo

## Interacción con el Jugador

### Daño al Enemigo
- El jugador puede dañar al enemigo saltando sobre él
- Cada salto exitoso reduce 1 punto de vida
- El enemigo se vuelve invulnerable por 1 segundo después de recibir daño
- Cuando la vida llega a 0, el enemigo es eliminado

### Daño al Jugador
- Si el jugador toca al enemigo sin saltar sobre él, recibe daño
- El enemigo es más peligroso que los enemigos normales

## Efectos Visuales

### Estados Visuales
- **Normal**: Apariencia estándar (tile7.png)
- **Ataque**: Borde rojo alrededor del enemigo
- **Invulnerable**: Parpadeo amarillo

### Barra de Vida
- Se muestra una barra de vida cuando el enemigo ha recibido daño
- Barra roja (vida perdida) y verde (vida restante)

### Modo Desarrollador
- Muestra información adicional como estado actual y vida
- Hitbox visible para debugging

## Configuración

Las características del enemigo especial se pueden configurar en el diccionario `CONFIG_JUEGO`:

```python
'ENEMIGO_ESPECIAL_VIDA': 3,                    # Puntos de vida
'ENEMIGO_ESPECIAL_VELOCIDAD': 1.2,            # Multiplicador de velocidad
'ENEMIGO_ESPECIAL_RANGO_DETECCION': 150,      # Rango de detección en píxeles
'ENEMIGO_ESPECIAL_RANGO_ATAQUE': 80,          # Rango de ataque en píxeles
'ENEMIGO_ESPECIAL_TIEMPO_INVULNERABLE': 60,   # Frames de invulnerabilidad
```

## Implementación Técnica

### Clase EnemigoEspecial
- Implementa lógica de estados avanzada
- Maneja colisiones y física de manera específica
- Usa la imagen `enemigos/tile7.png` en todos los estados

### Función de Mapeo
```python
def obtener_id_real_enemigo(item_id):
    mapeo_ids = {
        2: 142,  # ID 2 mapeado a tile7.png (ID 142)
    }
    return mapeo_ids.get(item_id, item_id)
```

### Inicialización
```python
def inicializar_enemigos():
    for fila in range(len(my_items)):
        for columna in range(len(my_items[0])):
            item_id = my_items[fila][columna]
            if item_id in ENEMIGOS:
                id_real = obtener_id_real_enemigo(item_id)
                if id_real == 142:  # tile7.png
                    nuevo_enemigo = EnemigoEspecial(columna * TILE_SIZE, fila * TILE_SIZE, id_real)
```

## Diferencias con Enemigos Normales

| Característica | Enemigo Normal | Enemigo Especial |
|----------------|----------------|------------------|
| Vida | 1 | 3 |
| Velocidad | Base | +20% |
| Estados | 1 (comportamiento fijo) | 3 (patrulla/ataque/retirada) |
| Detección | No | Sí (150px) |
| Invulnerabilidad | No | Sí (1 segundo) |
| Efectos Visuales | Básicos | Avanzados |
| Interacción | Simple | Compleja |
| Imagen | Variable | Siempre tile7.png |

## Uso en el Juego

Para usar este enemigo especial en el editor web:
1. Selecciona la imagen `tile7.png` en la sección de enemigos
2. Colócala en el mapa donde desees que aparezca
3. El enemigo se inicializará automáticamente con comportamiento especial

## Debug y Verificación

El sistema incluye mensajes de debug que muestran:
- Enemigos encontrados en el mapa
- Creación de enemigos especiales vs normales
- Posiciones de inicialización
- Total de enemigos creados

Ejemplo de salida:
```
Encontrado enemigo: ID=2, ID_real=142, Posición=(2,2)
✅ Creado EnemigoEspecial (tile7) en posición (64, 64)
Total de enemigos inicializados: 6
  Enemigo 1: Especial en (64, 64)
```

El enemigo especial añade un nivel de desafío adicional al juego, requiriendo estrategia y timing por parte del jugador para derrotarlo de manera segura. 