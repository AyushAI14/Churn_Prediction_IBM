FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 8501

# CMD ["Python3","mlops/serving/api/app.py.py"]
CMD ["streamlit","run","mlops/serving/api/app.py"]