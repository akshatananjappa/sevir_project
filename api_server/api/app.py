from fastapi import FastAPI
from models.Users import Users
#import SQLAlchemy

#db = SQLAlchemy(host="", user="", password="", port="")

app = FastAPI()

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