FROM python:3.11-slim


WORKDIR /app

ARG GOOGLE_CREDENTIALS_JSON
ENV GOOGLE_CREDENTIALS_JSON=${GOOGLE_CREDENTIALS_JSON}

COPY . /app


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8501


CMD ["streamlit", "run", "Streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]