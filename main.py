import pgzrun

# Constantes
TILE_SIZE = 32
WIDTH = 15 * TILE_SIZE
HEIGHT = 10 * TILE_SIZE

# Mapa base
my_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [2,2,1,1,1,1,1,1,1,1,1,2,1,1,1],
    [2,2,1,1,2,2,1,1,1,1,2,2,2,1,1],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
]

# Ítems sobre el mapa
my_items = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,4,0,5,0,0,0,0,0,0,5,4,0,0],
    [0,0,5,5,5,0,0,4,0,0,0,5,5,0,0],
    [0,0,0,0,0,0,0,5,5,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

def draw():
    screen.clear()

    for fila in range(len(my_map)):
        for columna in range(len(my_map[0])):
            x = columna * TILE_SIZE
            y = fila * TILE_SIZE

            # Dibuja el fondo del mapa (tiles)
            tile_id = my_map[fila][columna]
            tile_name = "tile" + str(tile_id)  # Ajusta el nombre de la imagen
            tile_actor = Actor(tile_name, (x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            tile_actor.draw()

            # Dibuja los ítems sobre el mapa
            item_id = my_items[fila][columna]
            if item_id != 0:  # Si hay un ítem (no es 0)
                item_name = "tile" + str(item_id)  # Usa el mismo formato de nombre
                item_actor = Actor(item_name, (x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                item_actor.draw()

pgzrun.go()
