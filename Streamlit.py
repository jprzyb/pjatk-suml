import streamlit as st
from google.cloud import vision
import os
import uuid
from pathlib import Path
import tempfile

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/google-key.json"


def analyze_uploaded_image(file_bytes):
    """
    Analizuje zdjęcie przesłane przez użytkownika (plik jako bytes).

    :param file_bytes: Zawartość pliku (np. file.read() z formularza)
    :return: Lista etykiet wykrytych przez Google Cloud Vision API
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=file_bytes)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]


def save_uploaded_image(file_bytes, filename, transaction_id):
    """
    Zapisuje obraz do pliku input/{uuid}.{ext}
    """
    ext = filename.split('.')[-1].lower()
    file_path = Path(f"input/{transaction_id}.{ext}")
    Path("input").mkdir(exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file_bytes)


def save_results_to_output(text_lines, transaction_id):
    """
    Zapisuje wynik analizy do folderu output/{uuid}/output.txt
    """
    file_path = Path(f"output/{transaction_id}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(text_lines))


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

                # Zapis obrazu do input/{uuid}/input.ext
                save_uploaded_image(file_bytes, uploaded_file.name, transaction_id)

                # Analiza obrazu
                result = analyze_uploaded_image(file_bytes)

                # Zapis wyników do output/{uuid}/output.txt
                save_results_to_output(result, transaction_id)

                typy_nadwozia = [label for label in result if label in nadwozia]

                if typy_nadwozia:
                    st.success(f"🔎 Typ nadwozia: **{typy_nadwozia[0]}**")
                else:
                    st.warning("Nie udało się jednoznacznie rozpoznać typu nadwozia.")
                st.info(f"Transaction_id: {transaction_id}")
        except Exception as e:
            st.error(f"❌ Wystąpił błąd: {e}")
