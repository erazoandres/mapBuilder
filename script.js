let draggedId = null;
let matriz = [];
let lastClickedId = null;
let selectedTileId = null;
let cursorImg = null;
let selectedContainer = null;
let isPainting = false; // Flag for painting mode

// Matriz para almacenar las rotaciones de cada celda
let rotaciones = [];

// Variables para la segunda capa/matriz
let matriz2 = [];
let rotaciones2 = [];
let items = []; // Nueva matriz para almacenar los items de la segunda capa
let activeLayer = 1; // 1 = primera capa, 2 = segunda capa

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

   // --- Add Event Listener for Clear Grid Button ---
  const clearButton = document.getElementById('clear-grid-btn');
  if (clearButton) {
    clearButton.addEventListener('click', clearGrid);
  } else {
    console.error("Clear Grid button not found!"); // Debug log
  }
  // --- End Add Event Listener ---

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

      // --- Apply existing tile data (if any) ---
      const currentTileId = matriz[r] ? matriz[r][c] : 0;
      if (currentTileId !== 0) {
        const sourceImg = document.querySelector(`.tiles img[data-id='${currentTileId}']`);
        if (sourceImg) {
          cell.style.backgroundImage = `url('${sourceImg.src}')`;
          cell.style.backgroundSize = 'cover';
          cell.style.transform = `rotate(${rotaciones[r][c] || 0}deg)`;
          cell.dataset.id = currentTileId; // Set data-id for consistency
        } else {
          console.warn(`Tile ID ${currentTileId} found in matrix at [${r},${c}] but no corresponding image in sidebar.`);
          // Clear the data if the image is missing to avoid broken state
          if (matriz[r]) matriz[r][c] = 0;
          if (rotaciones[r]) rotaciones[r][c] = 0;
        }
      }
      // --- End applying existing tile data ---

      // --- Painting/Placement Logic --- 
      // REMOVED Original 'click' listener
      // cell.addEventListener('click', () => {
      //  if (selectedTileId) {
      //    placeTile(cell, selectedTileId);
      //  }
      // });

      cell.addEventListener('mousedown', (e) => {
        if (e.button === 0) { // Only react to left mouse button
          if (selectedTileId) {
            placeTile(cell, selectedTileId);
            isPainting = true;
            // Prevent default text selection behavior during drag
            e.preventDefault(); 
          }
        }
      });

      cell.addEventListener('mouseenter', (e) => {
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

      // Add event listener for middle-click (wheel button) for deletion
      cell.addEventListener('mousedown', (e) => {
        if (e.button === 1) { // 1 is the middle button
          e.preventDefault(); // Prevent default middle-click behavior (like autoscroll)
          const row = parseInt(cell.dataset.row);
          const col = parseInt(cell.dataset.col);

          // Clear the cell data
          if (matriz[row] && matriz[row][col] !== 0) {
             matriz[row][col] = 0;
          }
          if (rotaciones[row] && rotaciones[row][col] !== 0) {
            rotaciones[row][col] = 0;
          }

          // Clear the visual representation
          cell.style.backgroundImage = '';
          cell.style.transform = ''; // Remove rotation
          cell.dataset.id = 0; // Update data-id attribute

          // console.log(`Deleted tile at [${row}, ${col}]`); // Optional: for debugging
        }
      });

      // Add event listener for double-click to rotate
      cell.addEventListener('dblclick', (e) => {
        e.preventDefault(); // Prevent potential text selection or other default dblclick actions
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);

        // Only rotate if there's a tile in the cell
        if (matriz[row][col] !== 0) {
          // Increment rotation by 90 degrees, wrap around using modulo 360
          rotaciones[row][col] = (rotaciones[row][col] + 90) % 360;
          cell.style.transform = `rotate(${rotaciones[row][col]}deg)`;
          // console.log(`Rotated tile at [${row}, ${col}] to ${rotaciones[row][col]}deg`); // Optional: for debugging
        }
      });

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
      // const currentTileId = matriz[r][c]; // Ya debería ser string ID o 0
      // const currentRotation = rotaciones[r][c];

      // if (currentTileId !== 0) {
      //   const tileImage = document.querySelector(`.tiles img[data-id='${currentTileId}']`);
      //   if (tileImage) {
      //     cell.style.backgroundImage = `url(${tileImage.src})`;
      //     cell.style.backgroundSize = "cover";
      //     cell.dataset.tileId = currentTileId; // Guardar el id
      //     // Habilitar drag solo si hay un tile
      //     cell.draggable = true;
      //     cell.ondragstart = (e) => {
      //         if (cell.dataset.tileId && cell.dataset.tileId !== '0') {
      //            e.dataTransfer.setData("text/plain", cell.dataset.tileId);
      //         } else {
      //             e.preventDefault(); // No arrastrar celdas vacías
      //         }
      //     };
      //   } else {
      //     console.warn(`Tile ID '${currentTileId}' en matriz [${r}][${c}] no encontrado. Limpiando celda.`);
      //     matriz[r][c] = 0; // Marcar como vacío si el tile no existe
      //     cell.style.backgroundImage = '';
      //     delete cell.dataset.tileId;
      //     cell.draggable = false;
      //   }
      // } else {
      //    cell.style.backgroundImage = ''; // Asegurar que esté vacío
      //    delete cell.dataset.tileId;
      //    cell.draggable = false; // No arrastrar celdas vacías
      // }

      // Aplicar rotación
      // cell.style.transform = `rotate(${currentRotation}deg)`;

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

  // Find the source image element in the sidebar using data-id
  const sourceImg = document.querySelector(`.tiles img[data-id='${tileId}']`);

  if (sourceImg) {
    // Update the matrix data
    matriz[row][col] = tileId;
    // We'll keep the existing rotation when placing a tile over another
    // If you want placing a tile to *reset* rotation, uncomment the next line:
    // rotaciones[row][col] = 0;

    // Apply the background image and rotation directly to the cell
    cell.style.backgroundImage = `url('${sourceImg.src}')`;
    cell.style.backgroundSize = 'cover'; // Ensure image fills the cell
    cell.style.transform = `rotate(${rotaciones[row][col] || 0}deg)`; // Apply existing or 0 rotation
    cell.dataset.id = tileId; // Update the cell's data-id
  } else {
    console.error(`Source image not found in sidebar for tileId: ${tileId}`);
    // Optional: Clear the cell if the source image is missing
    // cell.style.backgroundImage = '';
    // cell.style.transform = '';
    // matriz[row][col] = 0;
    // rotaciones[row][col] = 0;
    // cell.dataset.id = 0;
  }
  // Remove the old logic that created an <img> element inside the cell
  // cell.innerHTML = '';
  // const img = document.createElement("img"); ... etc ...
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

  // --- Prepare final rotations ensuring correct dimensions --- 
  let finalRotations = rotaciones;
  if (!(rotaciones.length === rows && rotaciones[0]?.length === cols)) {
      console.warn("Dimensiones de 'rotaciones' no coinciden con la matriz. Exportando rotaciones vacías.");
      finalRotations = Array.from({ length: rows }, () => Array(cols).fill(0));
  }

  // --- Start .txt file generation logic --- 
  // Generate the string for the numeric matrix
  let fileContentString = 'my_map = [\n';
  for (let i = 0; i < matrizNumerica.length; i++) {
    fileContentString += '  [' + matrizNumerica[i].join(',') + ']';
    if (i < matrizNumerica.length - 1) fileContentString += ',\n';
  }
  fileContentString += '\n];\n\n'; // End my_map definition

  // Generate the string for the rotations matrix
  fileContentString += 'my_rotations = [\n';
   for (let i = 0; i < finalRotations.length; i++) {
      // Ensure row exists before joining
      const rowString = finalRotations[i] ? finalRotations[i].join(',') : '';
      fileContentString += '  [' + rowString + ']';
      if (i < finalRotations.length - 1) fileContentString += ',\n';
  }
  fileContentString += '\n];\n\n'; // End my_rotations definition

  // Generate the string for the items matrix
  fileContentString += 'my_items = [\n';
  for (let i = 0; i < items.length; i++) {
    const rowString = items[i] ? items[i].join(',') : '';
    fileContentString += '  [' + rowString + ']';
    if (i < items.length - 1) fileContentString += ',\n';
  }
  fileContentString += '\n];\n\n'; // End my_items definition

  // Add the ID mapping as comments
  fileContentString += '// ID Mapping (Numeric ID: Original ID)\n';
  idMap.forEach((numId, stringId) => {
      // Sanitize stringId in case it contains characters that break comments (like newline)
      const safeStringId = stringId.replace(/\n/g, '\\n').replace(/\r/g, ''); 
      fileContentString += `// ${numId}: ${safeStringId}\n`;
  });
  fileContentString += '// End ID Mapping\n'; // Add an end marker for easier parsing

  // Create a Blob with the text data
  const blob = new Blob([fileContentString], { type: 'text/plain;charset=utf-8' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'mapa_exportado.txt'; // Change file extension back to .txt
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
  // --- End .txt file generation logic ---

  // Guardar la matriz numérica y el mapeo en localStorage como JSON (Keep this part)
  try {
      localStorage.setItem('savedMap', JSON.stringify(matrizNumerica));
      localStorage.setItem('idMap', JSON.stringify(idMapArray));
      // Save the potentially fixed rotations to localStorage as well
      localStorage.setItem('rotaciones', JSON.stringify(finalRotations));
      localStorage.setItem('items', JSON.stringify(items)); // Guardar items en localStorage
  } catch (e) {
      console.error("Error guardando datos en localStorage:", e);
      // Podría ser por exceder el límite de tamaño de localStorage
      alert("Error al guardar el mapa en almacenamiento local. Posiblemente el mapa es demasiado grande.");
      return; // Return if localStorage saving fails
  }

  // --- Remove JSON export logic ---
  // // Create an object containing all data for export
  // const exportData = {
  //   matrixData: matrizNumerica,
  //   idMapping: idMapArray,
  //   rotationData: finalRotations // Use the validated or generated empty rotations
  // };
  
  // // Convert the export object to a JSON string
  // const exportJsonString = JSON.stringify(exportData, null, 2); // null, 2 for pretty printing

  // // Create a Blob with the JSON data
  // const blob = new Blob([exportJsonString], { type: 'application/json;charset=utf-8' });
  // const url = window.URL.createObjectURL(blob);
  // const a = document.createElement('a');
  // a.href = url;
  // a.download = 'mapa_exportado.json'; // Change file extension
  // document.body.appendChild(a);
  // a.click();
  // document.body.removeChild(a);
  // window.URL.revokeObjectURL(url);
  // --- End JSON export logic ---

}

function importarMatriz(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const content = e.target.result;

        // Función auxiliar para extraer y parsear matrices
        function extractMatrix(content, matrixName) {
          const regex = new RegExp(`${matrixName}\\s*=\\s*(\\[\\s*\\[.*?\\]\\s*\\])`, 's');
          const match = content.match(regex);
          if (!match || !match[1]) {
            throw new Error(`No se pudo encontrar la matriz '${matrixName}'`);
          }
          
          // Limpiar y parsear la matriz
          const matrixStr = match[1]
            .replace(/\s+/g, '') // Remover espacios en blanco
            .replace(/\],\[/g, '],[') // Normalizar separadores
            .replace(/objeto(\d+)/g, '"objeto$1"'); // Convertir objetos a strings
            
          try {
            return JSON.parse(matrixStr);
          } catch (parseError) {
            throw new Error(`Error al parsear la matriz ${matrixName}: ${parseError.message}`);
          }
        }

        // Extraer las tres matrices
        const numericMatrix = extractMatrix(content, 'my_map');
        const importedRotations = extractMatrix(content, 'my_rotations');
        const importedItems = extractMatrix(content, 'my_items');

        // Validación de dimensiones
        const rows = numericMatrix.length;
        const cols = numericMatrix[0]?.length || 0;

        if (rows === 0 || cols === 0) {
          throw new Error("La matriz importada está vacía o mal formada");
        }

        // Validar que todas las matrices tengan las mismas dimensiones
        if (!importedRotations.every(row => row.length === cols) || importedRotations.length !== rows) {
          throw new Error("Las dimensiones de la matriz de rotaciones no coinciden");
        }

        if (!importedItems.every(row => row.length === cols) || importedItems.length !== rows) {
          throw new Error("Las dimensiones de la matriz de items no coinciden");
        }

        // Extract ID mapping from comments
        const reverseIdMap = new Map();
        const lines = content.split(/[\r\n]+/);
        let inMappingSection = false;
        const mappingRegex = /^\/\/\s*(\d+):\s*(.*)$/;

        for (const line of lines) {
          const trimmedLine = line.trim();
          if (trimmedLine.startsWith('// ID Mapping')) {
            inMappingSection = true;
            continue;
          }
          if (trimmedLine.startsWith('// End ID Mapping')) {
            inMappingSection = false;
            break;
          }
          if (inMappingSection) {
            const match = trimmedLine.match(mappingRegex);
            if (match) {
              const [, numId, stringId] = match;
              reverseIdMap.set(parseInt(numId, 10), stringId.trim());
            }
          }
        }

        // Convertir matriz numérica a IDs de string
        matriz = numericMatrix.map(row =>
          row.map(numId => {
            if (numId === 0) return 0;
            const stringId = reverseIdMap.get(numId);
            if (!stringId) {
              console.warn(`ID numérico ${numId} no encontrado en el mapeo. Usando 0.`);
              return 0;
            }
            return stringId;
          })
        );

        // Asignar matrices importadas
        rotaciones = importedRotations;
        items = importedItems;

        // Actualizar controles de UI
        document.getElementById('rows').value = rows;
        document.getElementById('cols').value = cols;

        // Guardar en localStorage
        try {
          localStorage.setItem('savedMap', JSON.stringify(numericMatrix));
          localStorage.setItem('idMap', JSON.stringify(Array.from(reverseIdMap.entries()).map(([numId, stringId]) => [stringId, numId])));
          localStorage.setItem('rotaciones', JSON.stringify(rotaciones));
          localStorage.setItem('items', JSON.stringify(items));
        } catch (lsError) {
          console.error("Error al guardar en localStorage:", lsError);
        }

        // Regenerar la grilla
        generarMatriz(true);

      } catch (error) {
        console.error('Error al importar el mapa:', error);
        alert(`Error al importar el mapa: ${error.message}\nVerifique el formato del archivo.`);
      }
    };
    reader.readAsText(file);
  }
  event.target.value = ''; // Reset file input
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

// --- New Function to Create Second Layer ---
function createSecondLayer() {
  console.log("Creating second layer matrix...");

  // Obtener las dimensiones de manera segura
  let rows = 10;
  let cols = 15;

  // Intentar obtener las dimensiones de la matriz existente
  if (matriz && matriz.length > 0) {
    rows = matriz.length;
    cols = matriz[0].length;
  } else {
    // Si no hay matriz, intentar obtener los valores de los inputs
    const rowsInput = document.getElementById("rows");
    const colsInput = document.getElementById("cols");
    if (rowsInput) rows = parseInt(rowsInput.value) || rows;
    if (colsInput) cols = parseInt(colsInput.value) || cols;
  }

  // Inicializar las matrices si no existen o si sus dimensiones no coinciden
  if (!matriz2 || matriz2.length !== rows || matriz2[0]?.length !== cols) {
    matriz2 = Array.from({ length: rows }, () => Array(cols).fill(0));
    rotaciones2 = Array.from({ length: rows }, () => Array(cols).fill(0));
    items = Array.from({ length: rows }, () => Array(cols).fill(0));
  }

  // Asegurar que cada fila esté inicializada
  for (let i = 0; i < rows; i++) {
    if (!matriz2[i]) matriz2[i] = Array(cols).fill(0);
    if (!rotaciones2[i]) rotaciones2[i] = Array(cols).fill(0);
    if (!items[i]) items[i] = Array(cols).fill(0);
  }

  activeLayer = 2;

  let layer2Container = document.getElementById("grid-layer2");

  if (!layer2Container) {
    layer2Container = document.createElement("div");
    layer2Container.id = "grid-layer2";
    layer2Container.className = "grid grid-layer2";
    layer2Container.style.position = "absolute";
    layer2Container.style.opacity = "1";
    layer2Container.style.transition = "opacity 0.3s ease";
    layer2Container.style.top = "0";
    layer2Container.style.left = "0";
    layer2Container.style.paddingLeft = "10px";
    layer2Container.style.paddingRight = "10px";
    layer2Container.style.pointerEvents = "auto";
    layer2Container.style.height = "auto";

    const gridContainer = document.getElementById("grid").parentElement;
    gridContainer.style.position = "relative";
    gridContainer.appendChild(layer2Container);
  } else {
    const isVisible = layer2Container.style.opacity === "1";
    layer2Container.style.opacity = isVisible ? "0" : "1";
    layer2Container.style.pointerEvents = isVisible ? "none" : "auto";

    if (!isVisible) {
      redrawSecondLayerTiles(layer2Container);
    }

    if (isVisible) return;
  }

  const firstGrid = document.getElementById("grid");
  layer2Container.style.gridTemplateColumns = firstGrid.style.gridTemplateColumns;
  layer2Container.style.gap = firstGrid.style.gap || "0";
  layer2Container.style.padding = firstGrid.style.padding || "10px";
  layer2Container.innerHTML = '';

  // Redibujar las celdas con los datos guardados
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement("div");
      cell.className = "cell layer2-cell";
      cell.dataset.row = r;
      cell.dataset.col = c;
      cell.style.backgroundColor = "transparent";

      const firstLayerCell = firstGrid.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`);
      if (firstLayerCell) {
        cell.style.width = getComputedStyle(firstLayerCell).width;
        cell.style.height = getComputedStyle(firstLayerCell).height;
      } else {
        cell.style.width = "32px";
        cell.style.height = "32px";
      }

      // Mostrar los tiles ya colocados en la segunda capa (matriz2)
      const tileId = matriz2[r][c];
      const rotation = rotaciones2[r][c];

      if (tileId && tileId !== 0) {
        const sourceImg = document.querySelector(`.tiles img[data-id='${tileId}']`);
        if (sourceImg) {
          cell.style.backgroundImage = `url('${sourceImg.src}')`;
          cell.style.backgroundSize = 'cover';
          cell.dataset.id = tileId;
          cell.style.transform = `rotate(${rotation}deg)`;
        }
      }

      // Si la celda tiene la clase 'custom-cursor', guardarla en la matriz2
      if (cell.classList.contains("custom-cursor")) {
        matriz2[r][c] = 'custom-cursor';  // Guardamos 'custom-cursor' en la matriz2
        console.log(`Celda con custom-cursor en (${r}, ${c})`);
      }

      cell.addEventListener('mousedown', (e) => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);

        if (e.button === 0 && selectedTileId) {
          matriz2[row][col] = selectedTileId;
          items[row][col] = selectedTileId; // Guardar en la matriz items
          const sourceImg = document.querySelector(`.tiles img[data-id='${selectedTileId}']`);
          if (sourceImg) {
            cell.style.backgroundImage = `url('${sourceImg.src}')`;
            cell.style.backgroundSize = 'cover';
            cell.dataset.id = selectedTileId;
          }
          isPainting = true;
          e.preventDefault();
        } else if (e.button === 1) {
          e.preventDefault();
          matriz2[row][col] = 0;
          items[row][col] = 0; // Limpiar en la matriz items
          rotaciones2[row][col] = 0;
          cell.style.backgroundImage = '';
          cell.style.transform = '';
          cell.dataset.id = 0;
        }
      });

      cell.addEventListener('mouseenter', (e) => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);

        if (isPainting && selectedTileId && matriz2[row][col] !== selectedTileId) {
          matriz2[row][col] = selectedTileId;
          items[row][col] = selectedTileId; // Guardar en la matriz items
          const sourceImg = document.querySelector(`.tiles img[data-id='${selectedTileId}']`);
          if (sourceImg) {
            cell.style.backgroundImage = `url('${sourceImg.src}')`;
            cell.style.backgroundSize = 'cover';
            cell.dataset.id = selectedTileId;
          }
        }
      });

      cell.addEventListener('dblclick', (e) => {
        if (e.button === 0) {
          const row = parseInt(cell.dataset.row);
          const col = parseInt(cell.dataset.col);
          if (matriz2[row][col] !== 0) {
            rotaciones2[row][col] = (rotaciones2[row][col] + 90) % 360;
            cell.style.transform = `rotate(${rotaciones2[row][col]}deg)`;
          }
        }
      });

      cell.addEventListener('dragstart', (e) => {
        if (isPainting) e.preventDefault();
      });

      layer2Container.appendChild(cell);
    }
  }

  const firstGridRect = firstGrid.getBoundingClientRect();
  layer2Container.style.width = `${firstGridRect.width}px`;

  console.log("Second layer created with dimensions:", rows, "x", cols);
  return layer2Container;

  function redrawSecondLayerTiles(container) {
    for (let r = 0; r < matriz2.length; r++) {
      for (let c = 0; c < matriz2[0].length; c++) {
        const cell = container.querySelector(`.cell[data-row='${r}'][data-col='${c}']`);
        const tileId = matriz2[r][c];
        const rotation = rotaciones2[r][c];

        if (cell) {
          if (tileId && tileId !== 0) {
            const sourceImg = document.querySelector(`.tiles img[data-id='${tileId}']`);
            if (sourceImg) {
              cell.style.backgroundImage = `url('${sourceImg.src}')`;
              cell.style.backgroundSize = 'cover';
              cell.dataset.id = tileId;
              cell.style.transform = `rotate(${rotation}deg)`;
              items[r][c] = tileId; // Asegurar que items esté sincronizado
            }
          } else {
            cell.style.backgroundImage = '';
            cell.style.transform = '';
            cell.dataset.id = 0;
            items[r][c] = 0; // Asegurar que items esté sincronizado
          }

          // Verificar si la celda tiene la clase 'custom-cursor' y mostrarla en consola
          if (cell.classList.contains("custom-cursor")) {
            console.log(`Celda con custom-cursor en (${r}, ${c})`);
          }
        }
      }
    }
  }
}
