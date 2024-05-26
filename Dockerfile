FROM python:3.9-slim AS streamlit-build
WORKDIR /app
Copy ./ /app/

RUN pip install --no-cache-dir streamlit
RUN pip install --no-cache-dir st_pages
Run pip install --no-cache-dir google-cloud-texttospeech
RUN pip install --no-cache-dir google-generativeai
RUN pip install --no-cache-dir vertexai
RUN pip install --no-cache-dir bcrypt
RUN pip install --no-cache-dir pytest

# Expose port 8501
EXPOSE 8501
# Healthcheck command
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit application
ENTRYPOINT ["streamlit", "run", "./app/main.py", "--server.port=8501", "--server.address=0.0.0.0","--server.enableCORS=false"]


# streamlit run ./streamlit_app/main.py --server.enableCORS=false
