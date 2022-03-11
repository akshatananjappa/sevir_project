import json
import os

curr = os.getcwd()
ARTIFACT_INTERIM_DIRECTORY = 'event_artifacts/interim/'
CATALOG_PATH = "event_artifacts/Catalog.json"
EVENTS_CONTEXT = []
for i in os.listdir(ARTIFACT_INTERIM_DIRECTORY):
    if os.path.isdir(os.path.join(ARTIFACT_INTERIM_DIRECTORY, i)):
        EVENTS_CONTEXT.append(i)
CATALOG_DICT = json.loads(open(CATALOG_PATH, "r").read())


def get_all_events():
    all_events_list = []
    try:
        for event in CATALOG_DICT:
            if str(event["event_id"]) in EVENTS_CONTEXT:
                all_events_list.append(event)
    except Exception as e:
        print(e)

    return all_events_list


def get_event_by_event_id(event_id: dict):
    event_data = {}
    try:
        all_events = get_all_events()
        for event in all_events:
            if event["event_id"] == event_id:
                event_data = event
                break
    except Exception as e:
        print(e)

    return event_data


def get_event_by_location(location: ""):
    event_data = {}
    try:
        all_events = get_all_events()
        for event in all_events:
            if event["location"] == location:
                event_data = event
                break
    except Exception as e:
        print(e)

    return event_data

