import json
from pymongo import MongoClient


client = MongoClient("mongodb+srv://karenli:VLVvTdRnx4BBxHb0@cluster0.8thfppb.mongodb.net/?retryWrites=true&w=majority")
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
