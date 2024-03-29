import json
from pymongo import MongoClient
from os import environ

DB_CONNECTION_STR = environ["DB_CONNECTION_STR"]
client = MongoClient(DB_CONNECTION_STR)
db = client.typing_practice

def get_lessons():
    collection = db.conversations
    return collection.find().sort("lesson")

def get_lesson(lesson):
    collection = db.conversations
    return collection.find_one({"lesson": lesson})

def get_lesson_text(lesson, sublesson):
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

def insert_lesson(dic):
    collection = db.conversations
    collection.insert_one(dic)

def delete_lesson(lesson_num):
    collection = db.conversations
    collection.delete_one({"lesson": lesson_num})

def get_admins():
    collection = db.admins
    res = collection.distinct("netid")
    return res

def insert_admin(admin):
    collection = db.admins
    collection.insert_one({"netid": admin})

def delete_admin(admin):
    collection = db.admins
    collection.delete_one({"netid": admin})

def get_existing_lesson_nums():
    collection = db.conversations
    res = collection.distinct("lesson")
    return res

def update_lesson(lesson_info):
    collection = db.conversations
    lesson = lesson_info["lesson"]
    collection.update_one({"lesson": lesson}, {"$set": lesson_info})
