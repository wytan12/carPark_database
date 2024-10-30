FROM python:3.10
WORKDIR /carPark_db
COPY . /carPark_db
RUN apt-get update
RUN apt install -y pkg-config libhdf5-dev vim nano
RUN pip install --upgrade pip
RUN pip install --no-cache-dir django-cors-headers
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
EXPOSE 8000
EXPOSE 5432
ENV PYTHONPATH="/carPark_db"
CMD ["python", "main.py", "--uvicorn", "TRUE","--host", "0.0.0.0", "--port", "8000"]
