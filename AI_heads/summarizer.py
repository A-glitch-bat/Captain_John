#--------------------------------

# Imports
import json
import os
os.environ["USE_TF"] = "0"

from transformers import pipeline
from tasks.scrape import ask_the_web
#--------------------------------

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", 
                          model="./models/distilbart-cnn-12-6",
                          framework="pt")
    #--------------------------------

    def text_sum(self, text, max_length=60, min_length=30):
        """
        want sum text dawg
        """
        summary = self.summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return summary[0]["summary_text"]
    
    def process_reply(self, reply):
        analyse = json.loads(reply['data'])
        #--------------------------------
        # 0 -> task not defined yet
        # 1 -> task finished
        # 2 -> short reply, process accordingly
        # 3 -> timer
        # 4 -> music
        # 5 -> idk google it
        #--------------------------------
        if analyse["taskID"] == 1:
            print("task finished") 
        elif analyse["taskID"] == 2:
            print("yesno")
            t, q = analyse["answer"].split(str(analyse["taskID"]), 1)
            print(t);print(q)
        elif analyse["taskID"] == 3:
            print("timer")
        elif analyse["taskID"] == 4:
            print("spotify")
            t, q = analyse["answer"].split(str(analyse["taskID"]), 1)
            print(t);print(q)
        else:
            # Don't know the specific task? Google it!
            print("Googlin' it")
            web_finds = ask_the_web(analyse["answer"])
            combined_snippets = " ".join(web_finds[1].split(". ")[:5])
            return self.text_sum(combined_snippets)
#--------------------------------

# Temporary main
if __name__ == "__main__":
    text = """
    Learn about Paris, the largest and most populous city in France, and its history, 
    geography, economy, tourism, and administration. Learn why Paris is the capital of 
    France and how it became a global city with a rich cultural heritage. 
    Artificial intelligence (AI) is a rapidly evolving field of computer science 
    that focuses on building systems capable of performing tasks that would normally 
    require human intelligence. These tasks include understanding natural language, 
    recognizing patterns in data, solving complex problems, and making predictions. 
    This is a multi-line string. Python keeps the line breaks as part of the string. 
    Paris (French pronunciation: [paʁi]) is the capital and largest city of France. 
    With an estimated population of 2,048,472 in January 2025 in an area of more than 
    105 km 2 (41 sq mi), Paris is the fourth-most populous city in the European Union 
    and the 30th most densely populated city in the world in 2022. Since the 17th century, 
    Paris has been one of the world's major centres for centuries. 
    Recent advances in machine learning and deep learning have dramatically 
    accelerated progress in AI. Applications of AI are now common in industries 
    ranging from healthcare and finance to transportation and entertainment. 
    However, AI also raises important ethical questions, including concerns about 
    privacy, bias, and job displacement. 
    """
    summy = Summarizer()
    sum = summy.text_sum(text)
    print(sum)
#--------------------------------
