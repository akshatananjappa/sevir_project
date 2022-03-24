from fastapi import FastAPI, Request
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,Response
import base64
from services.events import get_all_events, get_event_by_location

app = FastAPI()
templates = Jinja2Templates(directory="templates")
ARTIFACT_INTERIM_DIRECTORY = "event_artifacts/interim/"

@app.get("/")
async def root():
    return {"message": "Welcome! Go to /query path in the URL to show results"}


@app.get("/query", response_class=HTMLResponse)
def query(request: Request, location: str = ""):
    all_events = get_all_events()
    all_event_location = [item['location'] for item in all_events]
    try:
        if not location:
            response = templates.TemplateResponse("user_form.html", {"request": request, "events": all_event_location, "render": False, "selected_location": ""})
        else:
            event_details = get_event_by_location(location)
            file_path = os.path.join(ARTIFACT_INTERIM_DIRECTORY, str(event_details["event_id"]), 'image.png')
            with open(file_path, 'rb') as file:
                encoded_bytes = base64.b64encode(file.read())
            response = templates.TemplateResponse("user_form.html",
                                                  {"request": request, "location": location,
                                                   "events": all_event_location,
                                                   "render": True,
                                                   "selected_location": location,
                                                   "png_base64": encoded_bytes.decode('utf-8')})
    except Exception as e:
        print(e)
    return response


@app.get('/event')
def event_query(request: Request, event_id: str = ""):
    try:
        """
        Accepts an Event ID 
        """
        image_path = os.path.join(ARTIFACT_INTERIM_DIRECTORY, event_id, 'image.png')
        with open(image_path, "rb") as file:
            image_bytes: bytes = base64.b64encode(file.read())
            
        return {"data": image_bytes}
    except Exception as e:
        print(e)
        image_bytes = None
        return None
