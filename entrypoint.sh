#!/bin/sh

echo "$GOOGLE_KEY" > /app/google-key.json

exec streamlit run Streamlit.py --server.port=8501 --server.address=0.0.0.0
