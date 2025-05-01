let draggedId = null;
let matriz = [];
let lastClickedId = null;
let selectedTileId = null; // Para mantener el ID del tile seleccionado

// Cargar mapa al inicio si existe
window.onload = () => {
  // Agregar manejador de clic a las imágenes del sidebar
  document.querySelectorAll('.tiles img').forEach(img => {
    img.addEventListener('click', (e) => {
      // Remover la clase active de todas las imágenes
      document.querySelectorAll('.tiles img').forEach(i => i.classList.remove('active'));
      // Agregar la clase active a la imagen seleccionada
      e.target.classList.add('active');
      // Guardar el ID del tile seleccionado
      selectedTileId = e.target.dataset.id;
    });
  });

  if (localStorage.getItem('savedMap')) {
    try {
      const savedMap = localStorage.getItem('savedMap');
      const mapData = eval(savedMap);
      if (Array.isArray(mapData)) {
        matriz = mapData;
        document.getElementById('rows').value = matriz.length;
        document.getElementById('cols').value = matriz[0].length;
        generarMatriz(true);
        return;
      }
    } catch (e) {
      console.error('Error al cargar el mapa:', e);
    }
  }
  generarMatriz();
};

function generarMatriz(useExisting = false) {
  const rows = parseInt(document.getElementById("rows").value) || 10;
  const cols = parseInt(document.getElementById("cols").value) || 15;
  const grid = document.getElementById("grid");
  const matrizAnterior = [...matriz];

  grid.style.gridTemplateColumns = `repeat(${cols}, 32px)`;
  grid.innerHTML = '';
  
  if (!useExisting) {
    const nuevaMatriz = Array.from({ length: rows }, (_, r) => 
      Array.from({ length: cols }, (_, c) => 
        r < matrizAnterior.length && c < matrizAnterior[0].length ? matrizAnterior[r][c] : 0
      )
    );
    matriz = nuevaMatriz;
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = r;
      cell.dataset.col = c;
      
      // Agregar manejador de clic para colocar tile seleccionado
      cell.addEventListener('click', () => {
        if (selectedTileId) {
          placeTile(cell, selectedTileId);
        }
      });

      cell.ondragover = (e) => {
        e.preventDefault();
        if (draggedId) {
          const currentRow = parseInt(cell.dataset.row);
          const currentCol = parseInt(cell.dataset.col);
          cell.innerHTML = '';
          const img = document.createElement("img");
          img.src = draggedId.startsWith('fondo') 
            ? `./tiles/${draggedId}.png` 
            : `./tiles/img${draggedId}.png`;
          img.draggable = true;
          img.ondragstart = (e) => {
            draggedId = matriz[currentRow][currentCol].toString();
            matriz[currentRow][currentCol] = 0;
            setTimeout(() => e.target.parentElement.innerHTML = '', 0);
          };
          cell.appendChild(img);
          matriz[currentRow][currentCol] = draggedId;
        }
      };
      cell.ondrop = drop;
      cell.onmousedown = handleMouseClick;
      cell.ondblclick = handleDoubleClick;
      
      if (matriz[r][c] !== 0) {
        const img = document.createElement("img");
        const imgId = matriz[r][c];
        img.src = typeof imgId === 'string' && imgId.startsWith('fondo') 
          ? `./tiles/${imgId}.png` 
          : `./tiles/img${imgId}.png`;
        img.draggable = true;
        img.ondragstart = (e) => {
          draggedId = matriz[r][c].toString();
          matriz[r][c] = 0;
          setTimeout(() => e.target.parentElement.innerHTML = '', 0);
        };
        cell.appendChild(img);
      }
      
      grid.appendChild(cell);
    }
  }
}

// Función para colocar un tile en una celda
function placeTile(cell, tileId) {
  const row = parseInt(cell.dataset.row);
  const col = parseInt(cell.dataset.col);
  
  cell.innerHTML = '';
  const img = document.createElement("img");
  img.src = tileId.startsWith('fondo') 
    ? `./tiles/${tileId}.png` 
    : `./tiles/img${tileId}.png`;
  img.draggable = true;
  img.ondragstart = (e) => {
    draggedId = matriz[row][col].toString();
    matriz[row][col] = 0;
    setTimeout(() => e.target.parentElement.innerHTML = '', 0);
  };
  cell.appendChild(img);
  matriz[row][col] = tileId;
}

function handleDoubleClick(ev) {
  const cell = ev.currentTarget;
  const row = parseInt(cell.dataset.row);
  const col = parseInt(cell.dataset.col);
  
  if (matriz[row][col] !== 0) {
    const currentId = matriz[row][col];
    const nextCol = col + 1;
    
    if (nextCol < matriz[0].length) {
      const nextCell = document.querySelector(`.cell[data-row="${row}"][data-col="${nextCol}"]`);
      if (nextCell) {
        nextCell.innerHTML = '';
        const img = document.createElement("img");
        img.src = typeof currentId === 'string' && currentId.startsWith('fondo') 
          ? `./tiles/${currentId}.png` 
          : `./tiles/img${currentId}.png`;
        img.draggable = true;
        img.ondragstart = (e) => {
          draggedId = currentId.toString();
          matriz[row][nextCol] = 0;
          setTimeout(() => e.target.parentElement.innerHTML = '', 0);
        };
        nextCell.appendChild(img);
        matriz[row][nextCol] = currentId;
      }
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
  }
}

function drag(ev) {
  draggedId = ev.target.dataset.id;
}

function drop(ev) {
  ev.preventDefault();
  const cell = ev.currentTarget;
  const row = parseInt(cell.dataset.row);
  const col = parseInt(cell.dataset.col);
  
  cell.innerHTML = '';
  const img = document.createElement("img");
  img.src = draggedId.startsWith('fondo') 
    ? `./tiles/${draggedId}.png` 
    : `./tiles/img${draggedId}.png`;
  img.draggable = true;
  img.ondragstart = (e) => {
    draggedId = matriz[row][col].toString();
    matriz[row][col] = 0;
    setTimeout(() => e.target.parentElement.innerHTML = '', 0);
  };
  cell.appendChild(img);
  matriz[row][col] = draggedId;
}

function exportarMatriz() {
  let matrizString = 'my_map = [\n';
  for (let i = 0; i < matriz.length; i++) {
    matrizString += '[';
    for (let j = 0; j < matriz[i].length; j++) {
      const valor = matriz[i][j];
      if (valor === 0) {
        matrizString += '0';
      } else {
        matrizString += `"${valor}"`;
      }
      if (j < matriz[i].length - 1) matrizString += ',';
    }
    matrizString += ']';
    if (i < matriz.length - 1) matrizString += ',\n';
  }
  matrizString += ']';

  // Guardar en localStorage
  localStorage.setItem('savedMap', matrizString);

  const blob = new Blob([matrizString], { type: 'text/plain' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'matriz.txt';
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
        const mapData = eval(content.replace('my_map = ', '')); // Convierte el string a array
        if (Array.isArray(mapData)) {
          matriz = mapData;
          document.getElementById('rows').value = matriz.length;
          document.getElementById('cols').value = matriz[0].length;
          localStorage.setItem('savedMap', content);
          generarMatriz(true);
        }
      } catch (error) {
        console.error('Error al importar el mapa:', error);
        alert('Error al importar el mapa. Asegúrate de que el formato sea correcto.');
      }
    };
    reader.readAsText(file);
  }
  event.target.value = ''; // Resetear el input file
}
