import json
from pymongo import MongoClient
from os import environ

DB_CONNECTION_STR = environ["DB_CONNECTION_STR"]
client = MongoClient(DB_CONNECTION_STR)
db = client.typing_practice

def get_lessons():
    collection = db.conversations
    return collection.find()

def get_text(lesson, sublesson):
    collection = db.conversations
    res = collection.find_one({"lesson": lesson})["sublessons"][sublesson-1]
    text = res["text"]
    lines = text.split("\n")
    processed_text = [line.split(" ") for line in lines]
    return {"title_kor": res["title_kor"], "title_en": res["title_en"], "text": processed_text}

def get_conversation(lesson, sublesson):
    collection = db.conversations
    res = collection.find_one({"lesson": lesson})["sublessons"][sublesson-1]
    return res["text"]
