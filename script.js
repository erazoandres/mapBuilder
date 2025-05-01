let draggedId = null;
let matriz = [];
let lastClickedId = null;

// Generar matriz inicial al cargar la página
window.onload = () => generarMatriz();

function generarMatriz() {
  const rows = parseInt(document.getElementById("rows").value) || 10;
  const cols = parseInt(document.getElementById("cols").value) || 10;
  const grid = document.getElementById("grid");
  const matrizAnterior = [...matriz];

  grid.style.gridTemplateColumns = `repeat(${cols}, 32px)`;
  grid.innerHTML = '';
  
  const nuevaMatriz = Array.from({ length: rows }, (_, r) => 
    Array.from({ length: cols }, (_, c) => 
      r < matrizAnterior.length && c < matrizAnterior[0].length ? matrizAnterior[r][c] : 0
    )
  );
  
  matriz = nuevaMatriz;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.row = r;
      cell.dataset.col = c;
      cell.ondragover = (e) => e.preventDefault();
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

function handleDoubleClick(ev) {
  const cell = ev.currentTarget;
  const row = parseInt(cell.dataset.row);
  const col = parseInt(cell.dataset.col);
  
  // Si hay una imagen en esta celda
  if (matriz[row][col] !== 0) {
    const currentId = matriz[row][col];
    const nextCol = col + 1;
    
    // Verificar si la siguiente columna existe
    if (nextCol < matriz[0].length) {
      // Colocar la misma imagen en la siguiente celda
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
  const matrizString = JSON.stringify(matriz);
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
