from fastapi import FastAPI, Request
from models.Users import Users
import os
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import base64
#import SQLAlchemy

#db = SQLAlchemy(host="", user="", password="", port="")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/validate")
def validate():

    return {"message": "Validation successful"}

@app.get("/login")
def login():
    data = request.body
    username = data.get('username')
    password = data.get('password')
    query = db.query(Users).filter(Users.username == username)
    if query.password == password:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid credentials"}


@app.get("/get-images/{event_id}", response_class=HTMLResponse)
def get_images(request:Request, event_id):
    try:
        print(os.getcwd())
        if event_id:
            base_dir = 'event_artifacts/interim/'
            file_path = os.path.join(base_dir, event_id, 'image.png')
            with open(file_path, 'rb') as file:
                encoded_bytes = base64.b64encode(file.read()) 
            print(encoded_bytes)
            #image_bytes = open(file_path, 'rb').read()
            #print(image_bytes)
            return templates.TemplateResponse("index.html", {"request": request, "event_id": event_id, "png_base64": encoded_bytes.decode('utf-8')})

    except Exception as e:
        print(e)





