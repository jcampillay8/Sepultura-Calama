import os
import boto3
from botocore.client import Config
from PIL import Image

# ==========================================
# CONFIGURACIÓN DE CLOUDFLARE R2
# ==========================================
R2_ACCOUNT_ID = "8aab49bbcfe020e0a59aa2b8b6360780"
R2_ACCESS_KEY_ID = "c4418ea0e114cef18deb2566ec31ce96"
R2_SECRET_ACCESS_KEY = "2a4db56ff002e918bd4cb72d3ab878345e7477904d8aff87371b6b840269ab66"
R2_BUCKET_NAME = "oppytalent-images"
R2_PUBLIC_URL = "https://pub-693986afee154b369b5ca2b96d341053.r2.dev"

# Endpoint URL construido usando el Account ID
R2_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

# Inicializar cliente Boto3 para S3 (compatible con Cloudflare R2)
s3_client = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT_URL,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
    region_name="auto"
)

def process_and_upload_images(input_folder="Imagenes"):
    """
    Escanea la carpeta local, convierte imágenes (JPG/PNG) a WebP 
    y las sube automáticamente a Cloudflare R2.
    """
    if not os.path.exists(input_folder):
        print(f"Error: La carpeta '{input_folder}' no existe. Por favor créala y añade tus imágenes.")
        return

    uploaded_files = []

    print(f"=== INICIANDO PROCESO EN CARPETA '{input_folder}' ===")

    for filename in sorted(os.listdir(input_folder)):
        # Si la imagen ya es webp, la subiremos directamente
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            file_path = os.path.join(input_folder, filename)
            
            # Nombre base y nuevo nombre WebP
            filename_without_ext = os.path.splitext(filename)[0]
            webp_filename = f"{filename_without_ext}.webp"
            
            # Ruta temporal para guardar la conversión WebP localmente
            temp_webp_path = os.path.join(input_folder, webp_filename)
            
            try:
                # 1. Convertir a WebP si no lo es
                if not filename.lower().endswith('.webp'):
                    with Image.open(file_path) as img:
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        img.save(temp_webp_path, "webp", quality=85)
                    print(f"[*] Convertida a WebP: {filename} -> {webp_filename}")
                else:
                    print(f"[*] Imagen ya es WebP: {filename}")

                # 2. Subir a R2
                print(f"[*] Subiendo '{webp_filename}' a Cloudflare R2...")
                s3_client.upload_file(
                    Filename=temp_webp_path,
                    Bucket=R2_BUCKET_NAME,
                    Key=webp_filename,
                    ExtraArgs={"ContentType": "image/webp"}
                )
                
                # 3. Guardar URL pública para el reporte final
                public_url = f"{R2_PUBLIC_URL}/{webp_filename}"
                uploaded_files.append((webp_filename, public_url))
                print(f"[+] Éxito: {public_url}")

            except Exception as e:
                print(f"[x] Error procesando '{filename}': {str(e)}")

    # Imprimir reporte final de enlaces
    print("\n===========================================")
    print("=== RESUMEN DE ENLACES PARA EL HTML ===")
    print("===========================================")
    if uploaded_files:
        for file, url in uploaded_files:
            print(f"Nombre archivo: {file}")
            print(f"URL Pública: {url}\n")
        print("-> Copia estas URLs y asegúrate de que coincidan en la sección <img src='...'> del index.html")
    else:
        print("No se encontraron imágenes para subir o procesar.")

if __name__ == "__main__":
    process_and_upload_images()
