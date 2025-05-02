let draggedId = null;
let matriz = [];
let lastClickedId = null;
let selectedTileId = null;
let cursorImg = null;
let selectedContainer = null;
let isPainting = false; // Flag for painting mode

// Matriz para almacenar las rotaciones de cada celda
let rotaciones = [];

// Cargar mapa al inicio si existe
window.onload = () => {
  // Crear el elemento del cursor personalizado
  cursorImg = document.createElement('img');
  cursorImg.className = 'custom-cursor';
  document.body.appendChild(cursorImg);

  // Agregar manejador de movimiento del mouse
  document.addEventListener('mousemove', (e) => {
    if (selectedTileId && cursorImg) {
      cursorImg.style.left = e.pageX + 'px';
      cursorImg.style.top = e.pageY + 'px';
    }
  });

  // Agregar manejador de clic a las imágenes del sidebar
  document.querySelectorAll('.tiles img').forEach(img => {
    img.addEventListener('click', (e) => {
      // Deseleccionar todas las imágenes primero
      document.querySelectorAll('.tiles img').forEach(i => i.classList.remove('active'));
      // Seleccionar la imagen actual
      e.target.classList.add('active');
      selectedTileId = e.target.dataset.id; // selectedTileId es la string ID
      cursorImg.src = e.target.src;
      cursorImg.style.display = 'block';
      document.querySelectorAll('.cell').forEach(cell => cell.classList.add('cursor-tile'));
      // Evitar que el clic se propague al documento
      e.stopPropagation();
    });
  });

  document.querySelector('.grid').addEventListener('mouseleave', () => {
    if (cursorImg) cursorImg.style.display = 'none';
  });

  document.querySelector('.grid').addEventListener('mouseenter', () => {
    if (selectedTileId && cursorImg) cursorImg.style.display = 'block';
  });

  // --- Lógica de carga modificada ---
  const savedMapJSON = localStorage.getItem('savedMap');
  const savedIdMapJSON = localStorage.getItem('idMap');
  const savedRotationsJSON = localStorage.getItem('rotaciones');

  let loadedSuccessfully = false;
  if (savedMapJSON && savedIdMapJSON && savedRotationsJSON) {
    try {
      const matrizNumerica = JSON.parse(savedMapJSON);
      const idMapArray = JSON.parse(savedIdMapJSON);
      rotaciones = JSON.parse(savedRotationsJSON); // Cargar rotaciones

      // Crear un mapa inverso (numerical ID -> string ID)
      const reverseIdMap = new Map(idMapArray.map(([stringId, numId]) => [numId, stringId]));

      // Reconstruir la matriz global con los string IDs originales
      matriz = matrizNumerica.map(row =>
        row.map(numId => (numId === 0 ? 0 : reverseIdMap.get(numId) || 0)) // Usar 0 si el ID no se encuentra
      );

      // Validar que la matriz cargada y las rotaciones tengan dimensiones consistentes
      if (Array.isArray(matriz) && matriz.length > 0 && Array.isArray(matriz[0]) &&
          Array.isArray(rotaciones) && rotaciones.length === matriz.length &&
          rotaciones[0].length === matriz[0].length)
      {
          document.getElementById('rows').value = matriz.length;
          document.getElementById('cols').value = matriz[0].length;
          generarMatriz(true); // Generar usando la matriz cargada (con string IDs)
          loadedSuccessfully = true;
      } else {
           console.error('Error: Datos cargados inconsistentes (matriz/rotaciones).');
           // Limpiar datos corruptos opcionalmente
           // localStorage.removeItem('savedMap');
           // localStorage.removeItem('idMap');
           // localStorage.removeItem('rotaciones');
      }

    } catch (e) {
      console.error('Error al parsear datos guardados:', e);
      // Limpiar datos corruptos opcionalmente
      // localStorage.removeItem('savedMap');
      // localStorage.removeItem('idMap');
      // localStorage.removeItem('rotaciones');
    }
  }

  if (!loadedSuccessfully) {
    // Si no se cargó, generar matriz por defecto
    matriz = []; // Asegurar que la matriz esté vacía
    rotaciones = []; // Asegurar que las rotaciones estén vacías
    generarMatriz();
  }
   // --- Fin lógica de carga modificada ---

   // --- Add event listener for the new clear button ---
   const clearButton = document.getElementById('clear-grid-btn');
   if (clearButton) {
       clearButton.addEventListener('click', clearGrid);
   }
   // --- End event listener ---

};

function generarMatriz(useExisting = false) {
  const rows = parseInt(document.getElementById("rows").value) || 10;
  const cols = parseInt(document.getElementById("cols").value) || 15;
  const grid = document.getElementById("grid");

  // Guardar estado anterior solo si no estamos cargando desde localStorage
  const matrizAnterior = useExisting ? [] : [...matriz];
  const rotacionesAnteriores = useExisting ? [] : (rotaciones.length ? [...rotaciones] : []);

  grid.style.gridTemplateColumns = `repeat(${cols}, 32px)`;
  grid.innerHTML = '';

  // Si no estamos usando datos existentes (cargados de localStorage),
  // inicializamos o redimensionamos matriz y rotaciones.
  if (!useExisting) {
    const nuevaMatriz = Array.from({ length: rows }, (_, r) =>
      Array.from({ length: cols }, (_, c) =>
        (matrizAnterior.length > r && matrizAnterior[0]?.length > c) ? matrizAnterior[r][c] : 0
      )
    );
    matriz = nuevaMatriz; // Actualizar la matriz global

    const nuevasRotaciones = Array.from({ length: rows }, (_, r) =>
      Array.from({ length: cols }, (_, c) =>
        (rotacionesAnteriores.length > r && rotacionesAnteriores[0]?.length > c) ? rotacionesAnteriores[r][c] : 0
      )
    );
    rotaciones = nuevasRotaciones; // Actualizar rotaciones global
  }
  // Si useExisting es true, la matriz global y rotaciones ya fueron
  // cargadas en window.onload

  // Generar celdas y aplicar datos (ya sea nuevos/redimensionados o cargados)
  for (let r = 0; r < rows; r++) {
    // Asegurarse que la fila exista en rotaciones
     if (!rotaciones[r]) {
        rotaciones[r] = Array(cols).fill(0);
     }
     // Asegurarse que la fila exista en la matriz
     if (!matriz[r]) {
        matriz[r] = Array(cols).fill(0);
     }

    for (let c = 0; c < cols; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = r;
      cell.dataset.col = c;

      // Asegurarse que la celda exista en rotaciones
      if (rotaciones[r][c] === undefined) {
        rotaciones[r][c] = 0;
      }

      // --- Painting/Placement Logic --- 
      // REMOVED Original 'click' listener
      // cell.addEventListener('click', () => {
      //  if (selectedTileId) {
      //    placeTile(cell, selectedTileId);
      //  }
      // });

      cell.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return; // Only react to left mouse button
        if (selectedTileId) {
          placeTile(cell, selectedTileId);
          isPainting = true;
          // Prevent default text selection behavior during drag
          e.preventDefault(); 
        }
      });

      cell.addEventListener('mouseover', () => {
        if (isPainting && selectedTileId) {
          // Check if the tile is different before placing to avoid unnecessary updates
          const currentRow = parseInt(cell.dataset.row);
          const currentCol = parseInt(cell.dataset.col);
          if (matriz[currentRow][currentCol] !== selectedTileId) {
              placeTile(cell, selectedTileId);
          }
        }
      });
      
      // Prevent drag start interfering with painting
      cell.addEventListener('dragstart', (e) => {
          if (isPainting) {
              e.preventDefault();
          }
      });

      // --- End Painting/Placement Logic ---

      // Eventos drag/drop
      cell.ondragover = (e) => {
        e.preventDefault(); // Necesario para permitir drop
      };
      cell.ondrop = (e) => {
          e.preventDefault();
          const tileId = e.dataTransfer.getData("text/plain");
          if (tileId) {
              // Validar si tileId es un ID válido del sidebar antes de colocar
              const tileExists = document.querySelector(`.tiles img[data-id='${tileId}']`);
              if (tileExists) {
                 placeTile(cell, tileId);
              } else {
                 console.warn("Intento de drop con ID inválido:", tileId);
              }
          }
      };

       // Evento doble click para rotar (código existente)
       cell.addEventListener('dblclick', handleDoubleClick);

      // Aplicar el tile y la rotación existente (cargado o redimensionado)
      const currentTileId = matriz[r][c]; // Ya debería ser string ID o 0
      const currentRotation = rotaciones[r][c];

      if (currentTileId !== 0) {
        const tileImage = document.querySelector(`.tiles img[data-id='${currentTileId}']`);
        if (tileImage) {
          cell.style.backgroundImage = `url(${tileImage.src})`;
          cell.style.backgroundSize = "cover";
          cell.dataset.tileId = currentTileId; // Guardar el id
          // Habilitar drag solo si hay un tile
          cell.draggable = true;
          cell.ondragstart = (e) => {
              if (cell.dataset.tileId && cell.dataset.tileId !== '0') {
                 e.dataTransfer.setData("text/plain", cell.dataset.tileId);
              } else {
                  e.preventDefault(); // No arrastrar celdas vacías
              }
          };
        } else {
          console.warn(`Tile ID '${currentTileId}' en matriz [${r}][${c}] no encontrado. Limpiando celda.`);
          matriz[r][c] = 0; // Marcar como vacío si el tile no existe
          cell.style.backgroundImage = '';
          delete cell.dataset.tileId;
          cell.draggable = false;
        }
      } else {
         cell.style.backgroundImage = ''; // Asegurar que esté vacío
         delete cell.dataset.tileId;
         cell.draggable = false; // No arrastrar celdas vacías
      }

      // Aplicar rotación
      cell.style.transform = `rotate(${currentRotation}deg)`;

      grid.appendChild(cell);
    }
  }
}

// Global listener to stop painting when mouse button is released anywhere
document.addEventListener('mouseup', () => {
  if (isPainting) {
    isPainting = false;
  }
});

function handleDoubleClick(ev) {
  ev.preventDefault();
  const cell = ev.currentTarget;
  const row = parseInt(cell.dataset.row);
  const col = parseInt(cell.dataset.col);
  
  if (matriz[row][col] !== 0) {
    const img = cell.querySelector('img');
    if (img) {
      // Inicializar rotación si no existe
      if (!rotaciones[row]) rotaciones[row] = [];
      if (typeof rotaciones[row][col] === 'undefined') rotaciones[row][col] = 0;
      
      // Rotar la imagen
      rotaciones[row][col] = ((rotaciones[row][col] || 0) + 1) % 4;
      
      // Remover clases de rotación anteriores
      img.classList.remove('rotate-90', 'rotate-180', 'rotate-270');
      
      // Agregar nueva clase de rotación si no es 0
      if (rotaciones[row][col] > 0) {
        img.classList.add(`rotate-${rotaciones[row][col] * 90}`);
      }
      
      // Guardar el estado actual
      localStorage.setItem('rotaciones', JSON.stringify(rotaciones));
    }
  }
}

function handleMouseClick(ev) {
  if (ev.button === 1) {
    ev.preventDefault();
    const cell = ev.currentTarget;
    const row = parseInt(cell.dataset.row);
    const col = parseInt(cell.dataset.col);
    cell.innerHTML = '';
    matriz[row][col] = 0;
    rotaciones[row][col] = 0;
  }
}

function placeTile(cell, tileId) {
  const row = parseInt(cell.dataset.row);
  const col = parseInt(cell.dataset.col);
  
  cell.innerHTML = '';
  const img = document.createElement("img");
  const imgId = tileId;
  img.src = imgId.startsWith('fondo') 
    ? `./tiles/${imgId}.png` 
    : `./tiles/img${imgId}.png`;
  img.draggable = true;
  
  // Aplicar rotación si existe
  if (rotaciones[row][col] > 0) {
    img.classList.add(`rotate-${rotaciones[row][col] * 90}`);
  }
  
  img.ondragstart = (e) => {
    draggedId = selectedTileId || matriz[row][col].toString();
    matriz[row][col] = 0;
    rotaciones[row][col] = 0;
    setTimeout(() => e.target.parentElement.innerHTML = '', 0);
  };
  cell.appendChild(img);
  matriz[row][col] = tileId;
}

function drag(ev) {
  draggedId = ev.target.dataset.id;
  deselectTile();
}

function drop(ev) {
  ev.preventDefault();
  const cell = ev.currentTarget;
  placeTile(cell, draggedId);
}

function exportarMatriz() {
  // Crear un mapa de conversión de IDs (string ID -> numerical ID)
  const idMap = new Map();
  let nextId = 1;
  // Asegurarse que matriz[0] exista antes de acceder a su longitud
  const rows = matriz.length;
  const cols = (rows > 0 && matriz[0]) ? matriz[0].length : 0;
  if (rows === 0 || cols === 0) {
    console.warn("Exportando matriz vacía.");
    // Opcional: manejar este caso, quizás no guardar nada o guardar vacío
    localStorage.setItem('savedMap', JSON.stringify([]));
    localStorage.setItem('idMap', JSON.stringify([]));
    localStorage.setItem('rotaciones', JSON.stringify([]));
    return; // Salir si la matriz está vacía o mal formada
  }

  const matrizNumerica = Array.from({ length: rows }, () => Array(cols).fill(0));

  // Construir el mapa de IDs y la matriz numérica
  for (let i = 0; i < rows; i++) {
    // Asegurarse que la fila exista
    if (!matriz[i] || matriz[i].length !== cols) {
        console.error(`Fila ${i} inválida o con longitud incorrecta. Saltando fila en exportación.`);
        // Rellenar la fila numérica con 0s si hay inconsistencia
        matrizNumerica[i] = Array(cols).fill(0);
        continue;
    }
    for (let j = 0; j < cols; j++) {
      const valor = matriz[i][j]; // valor should be the string ID or 0
      if (valor !== 0) {
        // Validar que 'valor' sea un string ID esperado o manejar si no lo es
        if (typeof valor !== 'string'){
            console.warn(`Valor inesperado en [${i}][${j}]: ${valor}. Tratando como 0.`);
            matrizNumerica[i][j] = 0;
            continue;
        }
        if (!idMap.has(valor)) {
          idMap.set(valor, nextId++);
        }
        matrizNumerica[i][j] = idMap.get(valor);
      } else {
        matrizNumerica[i][j] = 0;
      }
    }
  }

  // Convertir el mapa a un array para guardarlo en JSON (stringID, numID)
  const idMapArray = Array.from(idMap.entries());

  // Guardar la matriz numérica y el mapeo en localStorage como JSON
  try {
      localStorage.setItem('savedMap', JSON.stringify(matrizNumerica));
      localStorage.setItem('idMap', JSON.stringify(idMapArray));
      // Asegurarse que 'rotaciones' tenga las dimensiones correctas antes de guardar
      if (rotaciones.length === rows && rotaciones[0]?.length === cols) {
         localStorage.setItem('rotaciones', JSON.stringify(rotaciones));
      } else {
         console.warn("Dimensiones de 'rotaciones' no coinciden con la matriz. Guardando rotaciones vacías.");
         // Generar rotaciones vacías si hay inconsistencia
         const rotacionesVacias = Array.from({ length: rows }, () => Array(cols).fill(0));
         localStorage.setItem('rotaciones', JSON.stringify(rotacionesVacias));
      }
  } catch (e) {
      console.error("Error guardando datos en localStorage:", e);
      // Podría ser por exceder el límite de tamaño de localStorage
      alert("Error al guardar el mapa. Posiblemente el mapa es demasiado grande.");
      return;
  }


  // Generar la cadena para el archivo descargado (formato my_map = [...])
  let matrizStringParaArchivo = 'my_map = [\n';
  for (let i = 0; i < matrizNumerica.length; i++) {
    matrizStringParaArchivo += '  [' + matrizNumerica[i].join(',') + ']';
    if (i < matrizNumerica.length - 1) matrizStringParaArchivo += ',\n';
  }
  matrizStringParaArchivo += '\n];\n\n'; // Añadir punto y coma y salto de línea

  // Añadir el mapeo de IDs como comentario en el archivo
  matrizStringParaArchivo += '// ID Mapping (Numeric ID: Original ID)\n';
  idMap.forEach((numId, stringId) => {
      matrizStringParaArchivo += `// ${numId}: ${stringId}\n`;
  });


  const blob = new Blob([matrizStringParaArchivo], { type: 'text/plain;charset=utf-8' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'matriz_mapa.txt'; // Cambiar nombre de archivo si se desea
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

function importarMatriz(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const content = e.target.result;
        const mapData = eval(content.replace('my_map = ', ''));
        if (Array.isArray(mapData)) {
          // Recuperar el mapeo de IDs
          const idMapString = localStorage.getItem('idMap');
          const idMap = idMapString ? new Map(JSON.parse(idMapString)) : null;

          // Si tenemos el mapeo, convertir los números de vuelta a los IDs originales
          if (idMap) {
            matriz = mapData.map(row => 
              row.map(val => val === 0 ? 0 : (idMap.get(val) || val.toString()))
            );
          } else {
            matriz = mapData;
          }

          // Reiniciar rotaciones al importar nuevo mapa
          rotaciones = Array.from({ length: matriz.length }, () => 
            Array.from({ length: matriz[0].length }, () => 0)
          );

          document.getElementById('rows').value = matriz.length;
          document.getElementById('cols').value = matriz[0].length;
          localStorage.setItem('savedMap', content);
          localStorage.setItem('rotaciones', JSON.stringify(rotaciones));
          generarMatriz(true);
        }
      } catch (error) {
        console.error('Error al importar el mapa:', error);
        alert('Error al importar el mapa. Asegúrate de que el formato sea correcto.');
      }
    };
    reader.readAsText(file);
  }
  event.target.value = '';
}

document.addEventListener('DOMContentLoaded', () => {
  // Agregar el cubo de fondo
  const cube = document.createElement('div');
  cube.className = 'background-cube';
  document.body.appendChild(cube);

  // Agregar evento de clic al documento para deseleccionar al hacer clic fuera
  document.addEventListener('click', (e) => {
    // Si el clic no fue dentro de la matriz (grid) ni en el sidebar ni en los controles
    if (!e.target.closest('.grid') && !e.target.closest('.sidebar') && !e.target.closest('.matrix-controls')) {
      deselectTile();
      // Deseleccionar también el grupo seleccionado
      document.querySelectorAll('.tile-group').forEach(g => g.classList.remove('selected'));
      selectedContainer = null;
    }
  });

  // Minimizar todos los grupos excepto los dos primeros
  document.querySelectorAll('.tile-group').forEach((group, index) => {
    if (index >= 2) {
      group.classList.add('minimized');
    }
  });

  // Agregar eventos para minimizar/expandir grupos
  document.querySelectorAll('.tile-group h3').forEach(header => {
    header.addEventListener('click', (e) => {
      const group = e.target.closest('.tile-group');
      group.classList.toggle('minimized');
      e.stopPropagation(); // Evitar que el clic se propague al grupo
    });
  });

  // Agregar evento de clic a las imágenes del sidebar
  document.querySelectorAll('.tiles img').forEach(img => {
    img.addEventListener('click', (e) => {
      // Deseleccionar todas las imágenes primero
      document.querySelectorAll('.tiles img').forEach(i => i.classList.remove('active'));
      // Seleccionar la imagen actual
      e.target.classList.add('active');
      selectedTileId = e.target.dataset.id;
      cursorImg.src = e.target.src;
      cursorImg.style.display = 'block';
      document.querySelectorAll('.cell').forEach(cell => cell.classList.add('cursor-tile'));
      // Evitar que el clic se propague al documento
      e.stopPropagation();
    });
  });

  document.querySelectorAll('.tile-group').forEach(group => {
    group.addEventListener('click', (e) => {
      // Solo si el click fue directamente en el contenedor o en su título
      if (e.target === group || e.target.tagName === 'H3') {
        if (group.classList.contains('selected')) {
          // Si ya está seleccionado, lo deseleccionamos
          group.classList.remove('selected');
          selectedContainer = null;
        } else {
          // Si no está seleccionado, deseleccionamos otros y seleccionamos este
          document.querySelectorAll('.tile-group').forEach(g => g.classList.remove('selected'));
          group.classList.add('selected');
          selectedContainer = group;
        }
        // Evitar que el clic se propague al documento
        e.stopPropagation();
      }
    });
  });

  // Evitar que los clics dentro del sidebar y los controles se propaguen al documento
  document.querySelector('.sidebar').addEventListener('click', e => e.stopPropagation());
  document.querySelector('.matrix-controls').addEventListener('click', e => e.stopPropagation());
});

function deselectTile() {
  selectedTileId = null;
  document.querySelectorAll('.tiles img').forEach(i => i.classList.remove('active'));
  if (cursorImg) cursorImg.style.display = 'none';
  document.querySelectorAll('.cell').forEach(cell => cell.classList.remove('cursor-tile'));
}

function moveContainerUp() {
  const container = document.querySelector('.tile-group.selected');
  if (container) {
    const prev = container.previousElementSibling;
    if (prev && prev.classList.contains('tile-group')) {
      container.parentNode.insertBefore(container, prev);
    }
  }
}

function moveContainerDown() {
  const container = document.querySelector('.tile-group.selected');
  if (container) {
    const next = container.nextElementSibling;
    if (next && next.classList.contains('tile-group')) {
      container.parentNode.insertBefore(next, container);
    }
  }
}

// --- New Function to Clear Grid --- 
function clearGrid() {
    console.log("clearGrid function called."); // Debug log
    const rows = matriz.length;
    const cols = (rows > 0 && matriz[0]) ? matriz[0].length : 0;

    if (rows === 0 || cols === 0) {
        console.log("Grid is already empty or not initialized.");
        return; // Nothing to clear
    }

    // Reset the data arrays
    matriz = Array.from({ length: rows }, () => Array(cols).fill(0));
    rotaciones = Array.from({ length: rows }, () => Array(cols).fill(0));

    // Regenerate the grid using the now empty data
    console.log("Regenerating grid to clear visuals...");
    generarMatriz(false); // Call generarMatriz to redraw with empty data

    console.log("Grid cleared by regenerating.");
    // Optional: Save the cleared state to localStorage immediately? 
    // exportarMatriz(); // Uncomment if you want clearing to persist on refresh
}
// --- End Clear Grid Function ---
