let draggedId = null;
let matriz = [];
let lastClickedId = null;
let selectedTileId = null;
let cursorImg = null;
let selectedContainer = null;

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
      document.querySelectorAll('.tiles img').forEach(i => i.classList.remove('active'));
      e.target.classList.add('active');
      selectedTileId = e.target.dataset.id;
      cursorImg.src = e.target.src;
      cursorImg.style.display = 'block';
      document.querySelectorAll('.cell').forEach(cell => cell.classList.add('cursor-tile'));
    });
  });

  document.querySelector('.grid').addEventListener('mouseleave', () => {
    if (cursorImg) cursorImg.style.display = 'none';
  });

  document.querySelector('.grid').addEventListener('mouseenter', () => {
    if (selectedTileId && cursorImg) cursorImg.style.display = 'block';
  });

  if (localStorage.getItem('savedMap')) {
    try {
      const savedMap = localStorage.getItem('savedMap');
      const mapData = eval(savedMap);
      if (Array.isArray(mapData)) {
        matriz = mapData;
        // Intentar cargar las rotaciones guardadas
        try {
          const savedRotations = localStorage.getItem('rotaciones');
          if (savedRotations) {
            rotaciones = JSON.parse(savedRotations);
          }
        } catch (e) {
          console.error('Error al cargar rotaciones:', e);
        }
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
  const rotacionesAnteriores = rotaciones.length ? [...rotaciones] : [];

  grid.style.gridTemplateColumns = `repeat(${cols}, 32px)`;
  grid.innerHTML = '';
  
  if (!useExisting) {
    matriz = Array.from({ length: rows }, (_, r) => 
      Array.from({ length: cols }, (_, c) => 
        r < matrizAnterior.length && c < matrizAnterior[0].length ? matrizAnterior[r][c] : 0
      )
    );
    
    // Inicializar matriz de rotaciones si no existe
    if (!rotaciones.length) {
      rotaciones = Array.from({ length: rows }, () => 
        Array.from({ length: cols }, () => 0)
      );
    } else {
      rotaciones = Array.from({ length: rows }, (_, r) => 
        Array.from({ length: cols }, (_, c) => 
          r < rotacionesAnteriores.length && c < rotacionesAnteriores[0].length ? rotacionesAnteriores[r][c] : 0
        )
      );
    }
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = r;
      cell.dataset.col = c;
      
      cell.addEventListener('click', () => {
        if (selectedTileId) {
          placeTile(cell, selectedTileId);
        }
      });

      cell.ondragover = (e) => {
        e.preventDefault();
        if (draggedId) {
          placeTile(cell, draggedId);
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
        
        // Aplicar rotación si existe
        if (rotaciones[r][c] > 0) {
          img.classList.add(`rotate-${rotaciones[r][c] * 90}`);
        }
        
        img.ondragstart = (e) => {
          draggedId = selectedTileId || matriz[r][c].toString();
          matriz[r][c] = 0;
          rotaciones[r][c] = 0;
          setTimeout(() => e.target.parentElement.innerHTML = '', 0);
        };
        cell.appendChild(img);
      }
      
      grid.appendChild(cell);
    }
  }
}

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
  img.src = tileId.startsWith('fondo') 
    ? `./tiles/${tileId}.png` 
    : `./tiles/img${tileId}.png`;
  img.draggable = true;
  
  // Mantener la rotación si existe
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
  localStorage.setItem('rotaciones', JSON.stringify(rotaciones));

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
        const mapData = eval(content.replace('my_map = ', ''));
        if (Array.isArray(mapData)) {
          matriz = mapData;
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

document.addEventListener('DOMContentLoaded', () => {
  // Agregar el cubo de fondo
  const cube = document.createElement('div');
  cube.className = 'background-cube';
  document.body.appendChild(cube);

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
      }
    });
  });
});
