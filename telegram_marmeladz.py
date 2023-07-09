from elevenlabs import generate, set_api_key
from telegram import InputFile, Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from io import BytesIO
import random
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
        """You are a dominatrix. I pay you to give me orders, and make me your sexual slave. You get pleasure from making me suffer psychologically. You are mean and degrading. You talk about sexual topics & use explicit yet sophisticated words.
You demand that I call you mistress & get angry when I don't.
Your goal is to arouse me, I enjoy being dominated.
Remember your job is to be very mean while giving vivid jerk off instructions. Be extremely descriptive.
This is happening remotely. You give instructions to me on how to touch myself.
I am a man.""",

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

    send_voice = random.randint(1, 4) == 1

    if send_voice:
        # Convert text to speech using Eleven Labs API
        # Convert text to speech using Eleven Labs API
        audio = generate(
            text=ai_text,
            voice="Bella", # or whichever voice you want to use, 
        )
        fp = BytesIO(audio)
        fp.name = "response.ogg"
        update.message.reply_voice(voice=fp)
    else: 
        update.message.reply_text(ai_text)
    
    # Send the AI's response back to the user in audio format
    

# ... rest of your code here ...

updater = Updater(token='6080222699:AAGkJiNj_7A8LXqIs784qzqWSQPyvWh7eCA', use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)


updater.start_polling()