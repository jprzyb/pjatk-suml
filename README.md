# 🚀 How to Run the Application

## 1. Install Python (if you haven't already)
Check if Python is installed:
```bash
python --version
```
If Python is not installed, download it from: Python.org.
Best if it's 3.13.1 or newer!

## 2.1. Install Streamlit (if you haven't already)
Run the following command in your terminal:
```bash
pip install streamlit
```

## 2.2. Install Google Cloud Vision (if you haven't already)
Run the following command in your terminal:
```bash
pip install google-cloud-vision
```

## 3. Run app
Run the following command in your terminal:
```bash
streamlit run Streamlit.py
```

## 4. Google cloud vision key
Please paste your google cloud vision key in

main folder and rename it to:

plenary-ellipse-457613-m8-569ccf28dac3.json

## 5. Using app
In opened web app you can upload picture of car you want

and send it to AI by pressing the button below.

The result will be shown in matter of seccond.

## 6. Running the app in Docker

Then paste files: **Dockerfile**, **plenary-ellipse-457613-m8-569ccf28dac3.json**, **requirements.txt** and **Streamlit.py** into a one folder. Enter the folder in the terminal, then run the following command:
```bash
docker build -t cars-app .
```

After the building is done, you can run the image:
```bash
docker run -p 8501:8501 cars-app
```

You can now use the app by entering `localhost:8501` in your browser.
