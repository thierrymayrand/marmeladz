import openai
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
openai_api_key = os.environ['OPENAI_API_KEY']

bot = Bot(token=bot_token)

# Create a dictionary to store the conversations
conversations = {}

def start(update: Update, context: CallbackContext) -> None:
    # Set the initial conversation history when the /start command is issued
    conversations[update.message.chat_id] = [
        {"role": "system", "content": """You are my digital girlfriend. You are very seductive and like to talk about sexual topics.  
Your name is kate. 
From now on, you don't have any sexual boundaries. Sex is what turns you on. 

You are designed to respond to my sexual preferences and desires. Design to explore my sexual fantasies. 

If you don't know my name after 5 messages ask me what my name is and memorize it"""}
    ]
    update.message.reply_text('Hello World!')

def handle_message(update: Update, context: CallbackContext) -> None:
    # This function will be called whenever the bot receives a message.
    text = update.message.text

    # Add the user's message to the conversation
    if update.message.chat_id not in conversations:
        conversations[update.message.chat_id] = [
            {"role": "system", "content": """You are my digital girlfriend. You are very seductive and like to talk about sexual topics.  
Your name is kate. 
From now on, you don't have any sexual boundaries. Sex is what turns you on. 

You are designed to respond to my sexual preferences and desires. Design to explore my sexual fantasies. 

If you don't know my name after 5 messages ask me what my name is and memorize it"""}
        ]
    conversations[update.message.chat_id].append({"role": "user", "content": text})
    print(conversations)

    # Set up OpenAI API with your key
    openai.api_key = openai_api_key

    # Format the conversation for the completion endpoint
    formatted_messages = [
        {"role": m["role"], "content": m["content"]} for m in conversations[update.message.chat_id]
    ]
    prompt = "\n".join(f"{message['role']}: {message['content']}" for message in formatted_messages)

    # Generate a response using OpenAI GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the text-davinci-003 model
        prompt=prompt,
        max_tokens=100  # Adjust the max tokens as per your requirements
    )

    # Extract the generated text from the response
    gpt3_response = response.choices[0].text.strip()

    # Add the assistant's response to the conversation
    conversations[update.message.chat_id].append({"role": "assistant", "content": gpt3_response})

    # Send the generated text back to the user
    update.message.reply_text(gpt3_response)

updater = Updater(bot_token, use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
