#--------------------------------

# Imports
from transformers import pipeline
#--------------------------------

def text_sum(text):
    """
    want sum text dawg
    """
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    summary = summarizer(
        text, 
        max_length=60,
        min_length=30,
        do_sample=False
    )
    #print(summary[0]['summary_text'])
    return summary[0]['summary_text']
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
    sum = text_sum(text)
    print(sum)
#--------------------------------
