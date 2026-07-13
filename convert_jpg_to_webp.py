import os
from PIL import Image

def convert_jpg_to_webp(input_folder="Imagenes", output_folder="Imagen"):
    # Crea la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Carpeta creada: {output_folder}")

    # Verifica si la carpeta de entrada existe
    if not os.path.exists(input_folder):
        print(f"Error: La carpeta de entrada '{input_folder}' no existe.")
        return

    # Contador de imágenes convertidas
    converted_count = 0

    # Itera sobre todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            # Construye las rutas completas
            jpg_path = os.path.join(input_folder, filename)
            
            # Cambia la extensión a .webp para el archivo de salida
            filename_without_ext = os.path.splitext(filename)[0]
            webp_filename = f"{filename_without_ext}.webp"
            webp_path = os.path.join(output_folder, webp_filename)

            try:
                # Abre la imagen y la guarda como WebP
                with Image.open(jpg_path) as img:
                    # Convierte a RGB por si acaso (algunos formatos o perfiles de color pueden dar problemas)
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    # Guarda la imagen en formato webp
                    img.save(webp_path, "webp")
                print(f"Convertida: {filename} -> {webp_filename}")
                converted_count += 1
            except Exception as e:
                print(f"Error al convertir {filename}: {e}")

    print(f"\n¡Conversión completada! Se convirtieron {converted_count} imagen(es).")

if __name__ == "__main__":
    # Puedes cambiar los nombres de las carpetas aquí si lo deseas
    convert_jpg_to_webp(input_folder="Imagenes", output_folder="Imagen")
