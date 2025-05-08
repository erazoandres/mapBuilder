import os

# Directorio donde están las imágenes
directorio = "images"

# Obtener lista de archivos y ordenarlos
archivos = os.listdir(directorio)
archivos_png = [f for f in archivos if f.endswith(".png")]
archivos_png.sort()  # Ordenar los archivos alfabéticamente
print("Archivos a procesar:", archivos_png)

# Primero, eliminar los archivos tile existentes
for archivo in archivos_png:
    if archivo.startswith("tile"):
        try:
            os.remove(os.path.join(directorio, archivo))
            print(f"Eliminado: {archivo}")
        except Exception as e:
            print(f"Error al eliminar {archivo}: {str(e)}")

# Ahora renombrar los archivos
contador = 1
for archivo in archivos_png:
    if not archivo.startswith("tile"):  # Solo renombrar archivos que no sean tiles
        ruta_vieja = os.path.join(directorio, archivo)
        nuevo_nombre = f"tile{contador}.png"
        ruta_nueva = os.path.join(directorio, nuevo_nombre)
        
        try:
            os.rename(ruta_vieja, ruta_nueva)
            print(f"Renombrado: {archivo} -> {nuevo_nombre}")
            contador += 1
        except Exception as e:
            print(f"Error al renombrar {archivo}: {str(e)}")

print("\nProceso completado!")
