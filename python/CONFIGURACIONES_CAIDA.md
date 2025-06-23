# Configuraciones de Caída - MapBuilder

## Descripción General

Las configuraciones de caída controlan cómo se comporta el personaje y los enemigos cuando caen del mapa. Estas configuraciones están sincronizadas para evitar conflictos lógicos.

## Configuraciones Disponibles

### 1. `CAIDA_SIN_LIMITE` (Prioridad Máxima)
- **Descripción**: Permite que el personaje/enemigo caiga sin límite más allá del mapa dibujado
- **Valor por defecto**: `False`
- **Tecla de acceso rápido**: `C` (modo desarrollador)
- **Comportamiento**: Si está activo, desactiva automáticamente `LIMITE_INFERIOR`

### 2. `PERDER_POR_CAIDA`
- **Descripción**: El personaje pierde el juego al caerse del mapa
- **Valor por defecto**: `False`
- **Tecla de acceso rápido**: `P` (modo desarrollador)
- **Comportamiento**: Si está activo, desactiva automáticamente `REGRESAR_POSICION_INICIAL`

### 3. `REGRESAR_POSICION_INICIAL`
- **Descripción**: El personaje/enemigo regresa a su posición inicial al caerse
- **Valor por defecto**: `False`
- **Tecla de acceso rápido**: `G` (modo desarrollador)
- **Comportamiento**: Si está activo, desactiva automáticamente `PERDER_POR_CAIDA`

## Jerarquía de Prioridades

1. **CAIDA_SIN_LIMITE** (máxima prioridad)
2. **PERDER_POR_CAIDA**
3. **REGRESAR_POSICION_INICIAL**

## Configuraciones Recomendadas

### Modo Normal (Recomendado)
```python
'CAIDA_SIN_LIMITE': False,
'PERDER_POR_CAIDA': False,
'REGRESAR_POSICION_INICIAL': True,
```

### Modo Difícil
```python
'CAIDA_SIN_LIMITE': False,
'PERDER_POR_CAIDA': True,
'REGRESAR_POSICION_INICIAL': False,
```

### Modo Sandbox
```python
'CAIDA_SIN_LIMITE': True,
'PERDER_POR_CAIDA': False,
'REGRESAR_POSICION_INICIAL': False,
```

## Uso en Modo Desarrollador

1. Presiona `F` para activar el modo desarrollador
2. Usa las siguientes teclas para cambiar configuraciones en tiempo real:
   - `C`: Cambiar CAIDA_SIN_LIMITE
   - `P`: Cambiar PERDER_POR_CAIDA
   - `G`: Cambiar REGRESAR_POSICION_INICIAL

## Archivos de Configuración

### En `main.py`
Las configuraciones se definen en el diccionario `CONFIG_JUEGO`:
```python
CONFIG_JUEGO = {
    'PERDER_POR_CAIDA': False,
    'REGRESAR_POSICION_INICIAL': False,
    'CAIDA_SIN_LIMITE': False,
}
```

### En `mapa.txt`
Las configuraciones se pueden cargar desde el archivo de mapa:
```python
configuraciones = {
    "perder_por_caida": False,
    "regresar_posicion_inicial": False,
    "caida_sin_limite": False
}
```

## Validación Automática

El sistema incluye una función `validar_configuraciones_caida()` que:
- Detecta conflictos entre configuraciones
- Ajusta automáticamente las configuraciones conflictivas
- Muestra mensajes informativos sobre los cambios realizados
- Se ejecuta automáticamente al cargar el juego y al cambiar configuraciones

## Mensajes del Sistema

- `⚠️ PERDER_POR_CAIDA activo: REGRESAR_POSICION_INICIAL desactivado automáticamente`
- `⚠️ REGRESAR_POSICION_INICIAL activo: PERDER_POR_CAIDA desactivado automáticamente`
- `✅ Configuración de caída sincronizada`
- `💀 Game Over: Personaje se cayó del mapa`
- `🔄 Personaje regresado a posición inicial`
- `💀 Enemigo eliminado por caída`
- `🔄 Enemigo regresado a posición inicial` 