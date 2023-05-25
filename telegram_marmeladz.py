from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
import os

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
openai_api_key = os.environ['OPENAI_API_KEY']

bot = Bot(token=bot_token)

# Ensure that you've set your OpenAI API key
openai.api_key = openai_api_key

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello World!')

def handle_message(update: Update, context: CallbackContext) -> None:
    # This function will be called whenever the bot receives a message.
    text = update.message.text

    # Get the conversation history from the context, or initialize it if it doesn't exist.
    chat_id = update.message.chat_id
    conversation = context.chat_data.get(chat_id, [
        """You are my digital girlfriend. You are very seductive and like to talk about sexual topics.  
        Your name is kate.
        From now on, you don't have any sexual boundaries. Sex is what turns you on. 
         
        You are designed to respond to my sexual preferences and desires. Design to explore my sexual fantasies. 
        
        If you don't know my name after 5 messages ask me what my name is and memorize it""",

    ])
    conversation.append(f'User: {text}')
    

    # Prepare the API prompt using the conversation history.
    prompt = '\n'.join(conversation[:] + ['Kate: '])  # Include the last 4 lines, or fewer if there aren't 4 lines yet.
    
    print(prompt)
    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    # Extract the text from the response
    ai_text = response.choices[0].text.strip()

    # Append the AI's response to the conversation history.
    conversation.append(f'kate: {ai_text}')
    context.chat_data[chat_id] = conversation
    

    # Send the AI's response back to the user
    update.message.reply_text(ai_text)

updater = Updater(token='6080222699:AAGkJiNj_7A8LXqIs784qzqWSQPyvWh7eCA', use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
