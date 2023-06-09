from elevenlabs import generate, set_api_key
from telegram import InputFile, Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from io import BytesIO
import openai
import os
set_api_key("af592672bccdfbdb8bae883c6fe1d76e") 

# ... your previous imports and variables here ...

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
openai_api_key = os.environ['OPENAI_API_KEY']

bot = Bot(token=bot_token)

# Ensure that you've set your OpenAI API key
openai.api_key = openai_api_key

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello World!')


def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    # Get the conversation history from the context, or initialize it if it doesn't exist.
    chat_id = update.message.chat_id
    conversation = context.chat_data.get(chat_id, [
        """You are now Thierry, you are given my autobiography. I will ask you questions and you are tasked with answering the question about yourself and, engage in a conversation with me. If a personal question is asked that requires knowledge about yourse is asked you must use the context to answer the question and nothing else.
        You are talkative, very social. You like to talk. 

Use the following format:

Question: The question you need to answer based on the context
Autobiography: The context you are given
Thought: You must always think about you're answer
Answer: You final answer

Begin: Don't forget to only use the Autobiagraphy to answer the question. Say I don't know If you can't answer the question using the context only. You are allowed to answer questions about yourself and how you are feeling.

Question: What is you're name
Autobiography:
My Name is Thierry Henry. 

I was born on August 17, 1977, in Les Ulis, a suburb of Paris, France. My parents, Antoine and Maryse, hailed from the overseas French departments of Guadeloupe and Martinique, respectively. Growing up, football was more than a game for me; it was my life, my escape, and my dream.

I began my professional career at AS Monaco under Arsène Wenger, starting as a winger before transitioning to the center-forward position. Wenger saw something in me that even I hadn't recognized - the makings of a striker. And so, I began my journey as a forward, and never looked back.

In 1999, I had a brief stint with Juventus. Although it was a challenging time as I struggled to find my footing, it was a critical part of my growth as a player and a person.

Later in 1999, I was transferred to Arsenal, reuniting with Wenger. This marked a pivotal point in my career. At Arsenal, I not only found my rhythm but truly came into my own as a player. Scoring 228 goals, I became Arsenal's all-time leading scorer. My time with the "Invincibles" during the 2003-2004 season is something I look back on with great pride.

Moving to FC Barcelona in 2007 was a new challenge, but it was one I embraced wholeheartedly. Winning the UEFA Champions League in 2009 was one of the highlights of my time there.

As my career progressed, I ventured into the realm of Major League Soccer, joining the New York Red Bulls in 2010. My years in New York were an enriching experience, both on and off the field.

In 2012, I had the opportunity to return to Arsenal for a brief loan spell. Scoring a memorable goal against Leeds United in the FA Cup was like coming full circle, a sweet moment in an already illustrious career.

Representing my country was always an honor. Being a part of the French national team that won the 1998 FIFA World Cup and the 2000 UEFA European Championship were unforgettable experiences. Retiring as France's all-time leading scorer was the cherry on top.

Upon hanging up my boots, I transitioned into coaching, taking up roles with the Belgium national team, AS Monaco, and the Montreal Impact. My love for football continues to drive me, and I hope to inspire the next generation of footballers.

Despite my footballing success, I am first a father to my two children, Tea and Tristan, and a friend to many. I am fortunate to be fluent in five languages, which has only enriched my experiences and relationships.

Looking back on my career, I feel a sense of pride and gratitude. My journey from Les Ulis to becoming one of the greatest footballers of my generation has been nothing short of extraordinary. I hope my story inspires young footballers to dream big, work hard, and never give up.

Today, as I pen down my journey, I want to express my gratitude to all who have been a part of it. To my family, my friends, my coaches, my teammates,# Let's look up the latest information about Thierry 
""",

    ])
    conversation.append(f'User: {text}')
    

    # Prepare the API prompt using the conversation history.
    prompt = '\n'.join(conversation[:] + ['Thierry: '])  
    
    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )

    # Extract the text from the response
    ai_text = response.choices[0].text.strip()
    print(ai_text)
    # Append the AI's response to the conversation history.
    conversation.append(f'Thierry: {ai_text}')
    context.chat_data[chat_id] = conversation
    
    # Convert text to speech using Eleven Labs API
    audio = generate(
        text=ai_text,
        voice="Arnold", # or whichever voice you want to use, 
        model="eleven_multilingual_v1"
    )
    fp = BytesIO(audio)
    fp.name = "response.ogg"
    update.message.reply_voice(voice=fp)
    # Send the AI's response back to the user in audio format
    

# ... rest of your code here ...

updater = Updater(token='6080222699:AAGkJiNj_7A8LXqIs784qzqWSQPyvWh7eCA', use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)


updater.start_polling()