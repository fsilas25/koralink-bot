from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import json
JSON_FILE = "faqs_final.json"
bot = ChatBot("koralink-assistent")

if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            faq_data = json.load(f)

        print(f"Training on {len(faq_data)} groups...")
        bot.read_only = False
        trainer = ListTrainer(bot)

        for item in faq_data:
            answer = item.get("answer")
            questions = item.get("questions", [])  
            for question in questions:
                trainer.train([question, answer])

        bot.read_only = True
        print("Training complete. Database saved.")
else:
        print(f"Error: Could not find {JSON_FILE}")