WORKDIR /api_server
COPY . .
RUN pip install -r requirements.txt
RUN cd api/
RUN uvicorn app:app --reload
EXPOSE 8000