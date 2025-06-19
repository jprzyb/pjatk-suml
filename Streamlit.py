import streamlit as st
from google.cloud import vision
import os
import uuid
from pathlib import Path
from azure.storage.blob import BlobServiceClient

# Ścieżka do lokalnego pliku z kluczem Google Cloud Vision
key_path = "app/google-key.json"
credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

# Azure Blob Storage
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE")
CONTAINER_NAME = "pjatksumldata"
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Zapisywanie klucza Google Vision do pliku, jeśli nie istnieje
if not os.path.exists(key_path):
    if credentials_json:
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        with open(key_path, "w") as f:
            f.write(credentials_json)
    else:
        raise RuntimeError("Missing GOOGLE_CREDENTIALS_JSON env or key file.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# Funkcja analizy obrazu
def analyze_uploaded_image(file_bytes):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=file_bytes)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]

# Zapis obrazu do Azure Blob Storage (input/)
def save_uploaded_image_to_blob(file_bytes, filename, transaction_id):
    ext = filename.split('.')[-1].lower()
    blob_name = f"input/{transaction_id}.{ext}"
    container_client.upload_blob(name=blob_name, data=file_bytes, overwrite=True)

# Zapis wyników do Azure Blob Storage (output/)
def save_results_to_output(text_lines, transaction_id):
    blob_name = f"output/{transaction_id}.txt"
    content = "\n".join(text_lines).encode("utf-8")
    container_client.upload_blob(name=blob_name, data=content, overwrite=True)

# Interfejs użytkownika
st.title("Car Body identification")
st.markdown(
    """ 
    Ta aplikacja wykorzystuje moc sztucznej inteligencji,
    aby precyzyjnie określić typ nadwozia samochodu na przesłanym zdjęciu.
    """
)

uploaded_file = st.file_uploader("Wgraj zdjęcie samochodu", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Wgrane zdjęcie", use_container_width=True)

    if st.button("Rozpoznaj nadwozie"):
        try:
            with st.spinner("Wysyłam do modelu..."):
                nadwozia = {
                    "SUV", "Crossover", "Sedan", "Saloon",
                    "Hatchback", "Coupe", "Coupé", "Convertible", "Cabriolet", "Roadster",
                    "Pickup truck", "Pickup", "Truck", "Van", "Minivan", "MPV", "Microvan",
                    "Wagon", "Estate", "Station wagon", "Fastback", "Liftback",
                    "Targa", "Hardtop", "Panel van", "Chassis cab",
                    "Sportscar", "Sports car", "Supercar", "Limousine"
                }

                transaction_id = str(uuid.uuid4())
                file_bytes = uploaded_file.read()

                # Zapis obrazu do Blob Storage
                save_uploaded_image_to_blob(file_bytes, uploaded_file.name, transaction_id)

                # Analiza obrazu
                result = analyze_uploaded_image(file_bytes)

                # Zapis wyników do Blob Storage
                save_results_to_output(result, transaction_id)

                typy_nadwozia = [label for label in result if label in nadwozia]

                if typy_nadwozia:
                    st.success(f"🔎 Typ nadwozia: **{typy_nadwozia[0]}**")
                else:
                    st.warning("Nie udało się jednoznacznie rozpoznać typu nadwozia.")
                st.info(f"Transaction ID: `{transaction_id}`")
        except Exception as e:
            st.error(f"❌ Wystąpił błąd: {e}")
