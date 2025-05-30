import streamlit as st
from google.cloud import vision
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/google-key.json"

def analyze_uploaded_image(file_bytes):
    """
    Analizuje zdjęcie przesłane przez użytkownika (plik jako bytes).

    :param file_bytes: Zawartość pliku (np. file.read() z formularza)
    :return: Lista etykiet wykrytych przez Google Cloud Vision API
    """
    # Inicjalizacja klienta
    client = vision.ImageAnnotatorClient()

    # Tworzenie obrazu z bytes
    image = vision.Image(content=file_bytes)

    # Wykrywanie etykiet
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # Wyciągnięcie opisów
    descriptions = [label.description for label in labels]

    return descriptions


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

                result = analyze_uploaded_image(uploaded_file.read())
                print(result)

                typy_nadwozia = [label for label in result if label in nadwozia]

                if typy_nadwozia:
                    st.success(f"🔎 Typ nadwozia: **{typy_nadwozia[0]}**")
                else:
                    st.warning("Nie udało się jednoznacznie rozpoznać typu nadwozia.")
        except Exception as e:
            st.error(f"❌ Wystąpił błąd: {e}")