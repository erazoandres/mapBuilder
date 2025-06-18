# Editor de Mapas Web - MapBuilder

## Descripción

Esta carpeta contiene el editor de mapas web para el juego MapBuilder. El editor permite crear y editar mapas de manera visual mediante una interfaz web intuitiva.

## Archivos

- **`index.html`**: Página principal del editor
- **`css/style.css`**: Estilos y diseño de la interfaz
- **`js/script.js`**: Lógica y funcionalidad del editor

## Características del Editor

### Funcionalidades Principales

- **Editor Visual**: Interfaz drag & drop para crear mapas
- **Múltiples Capas**: Soporte para terrenos, items y enemigos
- **Configuración del Juego**: Ajustes de física y comportamiento
- **Importar/Exportar**: Carga y guarda mapas en formato .txt
- **Previsualización**: Vista previa de tiles y sprites

### Controles

- **Drag & Drop**: Arrastra tiles desde la barra lateral al mapa
- **Click**: Selecciona y coloca tiles en el mapa
- **Botones de Control**: Generar, exportar, importar y limpiar
- **Configuración**: Ajusta parámetros del juego

### Estructura de Carpetas

```
web/
├── index.html       # Página principal
├── css/
│   └── style.css    # Estilos CSS
├── js/
│   └── script.js    # JavaScript
└── README.md        # Este archivo
```

## Uso

1. Abre `index.html` en tu navegador web
2. Configura las dimensiones del mapa
3. Arrastra tiles desde la barra lateral al mapa
4. Ajusta la configuración del juego según necesites
5. Exporta el mapa para usarlo en el juego

## Compatibilidad

- Navegadores modernos (Chrome, Firefox, Safari, Edge)
- Requiere JavaScript habilitado
- Funciona mejor con pantallas de 1024px o más de ancho

## Integración con el Juego

El editor genera archivos `mapa.txt` que son compatibles directamente con el juego principal (`main.py`). Los mapas creados aquí se pueden usar inmediatamente en MapBuilder.

## Desarrollo

Para modificar el editor:

- **Estilos**: Edita `css/style.css`
- **Funcionalidad**: Modifica `js/script.js`
- **Estructura**: Actualiza `index.html`

## Notas

- El editor es independiente del juego principal
- Los archivos generados son compatibles con el formato de `mapa.txt`
- Se recomienda usar imágenes de 36x36 píxeles para mejor compatibilidad 