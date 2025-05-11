import os

carpeta = 'assets/fondos'  # Carpeta actual

# Obtener la lista de archivos en esa carpeta (solo archivos)
archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
archivos.sort()

# Renombrar temporalmente para evitar conflictos
for i, archivo in enumerate(archivos):
    extension = os.path.splitext(archivo)[1]
    os.rename(os.path.join(carpeta, archivo), os.path.join(carpeta, f"temp_rename_{i}{extension}"))

# Renombrar definitivamente
temporales = [f for f in os.listdir(carpeta) if f.startswith("temp_rename_")]
temporales.sort()

for i, archivo in enumerate(temporales):
    extension = os.path.splitext(archivo)[1]
    nuevo_nombre = f"tile{i}{extension}"
    os.rename(os.path.join(carpeta, archivo), os.path.join(carpeta, nuevo_nombre))
    print(f"{archivo} → {nuevo_nombre}")
