from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.getenv('TOKEN')
BOT_USERNAME: Final = '@pearldeImg_bot'

# Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! Lemme know if you wanna do fancy stuff with your image!')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Im your Image processing friend! Type something so I can respond!')
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')
     
async def shrink_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a your shrinked image!')
    
async def compress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a your compressed image!")
    
async def noise_reduction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a your noise-reduced image!")
    
async def edge_detection_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a your edge-detected image!")
    
# Response
def handle_response(text: str) -> str:
    processed: str = text.lower()
    #some cases: 
    if any(word in processed for word in ['hello', 'hi', 'hey']):
        return "Hey there! How are you?"
    if any(word in processed for word in ['good', 'great', 'well', 'fine', 'oke']):
        return "I'm glad hearing that!"
    if 'how are you' in processed:
        return "I'm good, thank you!"
    if 'thank' in processed:
        return "You're welcome!"
    if 'feel' in processed:
        return "My feelings? I'm really glad if I can help you out!"
    if 'bye' in processed:
        return "See you next time! Remember your schedule at school, mate!"
    if any(word in processed for word in ['img', 'image', 'picture', 'photo', 'pic']):
        return "I can do image processing stuffs like shrinking, compressing, noise reduction, edge detection, etc. Please choose from the menu!"
    return "I don't understand you! Click menu for more information!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type # to define it's a group or private chat
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip() #to avoid the bot from replying to random mention between users gossip
            response: str = handle_response(new_text)
        else: 
            return
    else:
        response: str = handle_response(text)
        
    print("Bot:", response)
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update "{update}" caused error "{context.error}"')
            
if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()
    
    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('compress', compress_command))
    app.add_handler(CommandHandler('shrink', shrink_command))
    app.add_handler(CommandHandler('edge_detection', edge_detection_command))
    app.add_handler(CommandHandler('noise_reduction', noise_reduction_command))
    
    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # errors
    app.add_error_handler(error)
    
    # polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
    
   
    