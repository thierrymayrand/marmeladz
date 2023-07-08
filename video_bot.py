from telegram import InputFile, Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Import the run_conversation function from your app.py file
from app import run_conversation 
from message_manager import MessageManager

message_manager = MessageManager()
allMessagesTelegram = [
{"role": "system", "content": "You are a booking agent. You're job is to answer user questions and get them to book an appointment.You work for a company that finds jobs for people."},
{"role": "assistant", "content": f"Hey Thierry are you still looking for a job ?"}
]

def start(update: Update, context: CallbackContext) -> None:
    video_file = open('marcvideo.mp4', 'rb')  
    context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)
    update.message.reply_text('Hey Marc a quick video for you, are you still looking for a job ?')

def handle_message(update: Update, context: CallbackContext) -> None:
    # Get the text the user sent
    user_text = update.message.text
    user_obj = {"role": "user", "content": user_text}
    allMessagesTelegram.append(user_obj)
    
    # Run the conversation function with the user's text
    response = run_conversation(allMessagesTelegram)
    res_obj = {"role": "assistant", "content": response}
    allMessagesTelegram.append(res_obj)
    
    # Send the response back to the user
    update.message.reply_text(response)

def main() -> None:
    updater = Updater("5815563391:AAGOOkRdEQTYEsfgHkAtz3qt8GmaPCUWMxA", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))


    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
