from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, File
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, ConversationHandler, CallbackQueryHandler
from PIL import Image, ImageFilter
from rembg import remove
import cv2
from tkinter.filedialog import *
import os
from io import BytesIO
from dotenv import load_dotenv
# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#     format='%(asctime)s - %(levelname)s - %(message)s'  # Set the format of log messages
# )

load_dotenv()

TOKEN: Final = os.getenv('TOKEN')
BOT_USERNAME: Final = '@pearldeImg_bot'

#Define states for the convo
MENU, SHRINK, COMPRESS, NOISEREDUCTION, EDGEDETECTION, CROP, BGREMOVAL = range(7)

# Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton('Shrink', callback_data='shrink')],
        [InlineKeyboardButton('Compress', callback_data='compress')],
        [InlineKeyboardButton('Noise Reduction', callback_data='noiseReduction')],
        [InlineKeyboardButton('Edge Detection', callback_data='edgeDetection')],
        [InlineKeyboardButton('Background Removal', callback_data='bgRemoval')],
        [InlineKeyboardButton('Crop', callback_data='crop')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Hello! Please choose an image processing option:', reply_markup=reply_markup)
    return MENU
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Im your Image processing friend! Type something so I can respond!')
    
# async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('This is a custom command!')

# Buttons on start command
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "shrink":
        await query.edit_message_text("Please upload the image you want to shrink")
        return SHRINK
    elif query.data == "compress":
        await query.edit_message_text("Please upload the image you want to compress")
        return COMPRESS
    elif query.data == "noiseReduction":
        await query.edit_message_text("Please upload the image for noise reduction")
        return NOISEREDUCTION
    elif query.data == "edgeDetection":
        await query.edit_message_text("Please upload the image for edge detection")
        return EDGEDETECTION
    elif query.data == "crop":
        await query.edit_message_text("Please upload the image to crop")
        return CROP
    elif query.data == "bgRemoval":
        await query.edit_message_text("Please upload the image for background removal")
        return BGREMOVAL
    
# Process image with each features
async def process_image(update: Update, context: ContextTypes.DEFAULT_TYPE, process_type: str):
    if update.message.photo:
        # extract file id of the highest resolution image cause tele sends multiple resolution version of image
        photo = update.message.photo[-1] #the last image is usually the highest resolution
        file_id = photo.file_id
        #get the file from the file_id
        file = await context.bot.get_file(file_id)
        #download the file for bot processing
        file_path = f"{file_id}.jpg"
        await file.download_to_drive(file_path)
        await update.message.reply_text(f"Processing the image for {process_type}...")
    
        #image processing code
        image = Image.open(file_path)
        img_size = image.size #get size of dimensions
        original_size_kb = os.path.getsize(file_path) / 1024 # get size in kb
        img_wh1 = "width: " + str(img_size[0]) + " height: " +  str(img_size[1]) #get dimensions
        output_image = None
        response_text = ""
        
        if process_type == "noiseReduction":
            output_image = image.filter(ImageFilter.DETAIL())
            output_image = output_image.filter(ImageFilter.SHARPEN())
            response_text = f"Noise reduction finished!"
            
        elif process_type == "edgeDetection":
            image = image.convert("L") 
            output_image = image.filter(ImageFilter.FIND_EDGES)
            response_text = f"Edge detection finished!"
            
        elif process_type == "shrink":  
            output_image = image.resize((image.size[0] // 2, image.size[1] // 2))
            img_wh2 = "width: " + str(output_image.size[0]) + " height: " + str(output_image.size[1])
            response_text = f"Original dimensions: {img_wh1} \n New dimensions: {img_wh2}"
            
        elif process_type == "compress":
            output_image = image.resize((image.size[0] // 1, image.size[1] // 1))
            img_file = BytesIO()
            output_image.save(img_file, format='JPEG')
            new_size_kb = img_file.tell() / 1024  # size in KB
            response_text = f"Original size: {original_size_kb:.2f} KB\nNew size: {new_size_kb:.2f} KB"
            
        elif process_type == "bgRemoval":
            img_convert = image.convert("RGB")
            output_rgba = remove(img_convert)
            output_image = output_rgba.convert("RGB")
            print("remove bg")
            response_text = f"Background removal finished!"    
                    
        # elif process_type == "crop":
        #     output_image = remove(image)

        # Save the processed image to a new file
        if output_image is not None:
            processed_file_path = f"{process_type}_{file_id}.jpg"
            output_image.save(processed_file_path)
        
            # Send the processed image back to the user
            with open(processed_file_path, 'rb') as processed_image:
                await update.message.reply_photo(photo=processed_image, caption=f"\n {response_text}")

            # clean up the files if needed
            os.remove(file_path)
            os.remove(processed_file_path)
        else:
            await update.message.reply_text("Error processing the image. Please try again.")
            
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please upload a valid image!")
        return MENU

async def shrink_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await process_image(update, context, "shrink")

async def compress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await process_image(update, context, "compress")

async def noise_reduction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await process_image(update, context, "noiseReduction")

async def edge_detection_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await process_image(update, context, "edgeDetection")

async def crop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await process_image(update, context, "crop")

async def bg_removal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await process_image(update, context, "bgRemoval")

# Cancel selection
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation calcelled!")
    return ConversationHandler.END

# Response
def handle_response(text: str) -> str:
    processed: str = text.lower()
    #some cases: 
    if any(word in processed for word in ['hello', 'hi', 'hey']):
        return "Hey there! How are you?"
    if any(word in processed for word in ['good', 'great', 'well', 'fine', 'oke', 'nice', 'awesome']):
        return "I'm glad hearing that!"
    if 'how are you' in processed:
        return "I'm good, thank you!"
    if any(word in processed for word in ['thank', 'thanks', 'thank you', 'thank you so much']):
        return "You're welcome!"
    if 'feel' in processed:
        return "My feelings? I'm really glad if I can help you out!"
    if any(word in processed for word in ['bye', 'see you', 'see you later', 'goodbye']):
        return "See you next time!"
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
 
def main():
    print("Starting bot...")
    app = Application.builder().token(TOKEN).read_timeout(10).write_timeout(10).concurrent_updates(True).build()
    
    # ConversationHandler to handle the state machine
    conversation_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start_command)],
        states = {
            MENU: [CallbackQueryHandler(button)],
            SHRINK: [MessageHandler(filters.PHOTO, shrink_command)],
            COMPRESS: [MessageHandler(filters.PHOTO, compress_command)],
            NOISEREDUCTION: [MessageHandler(filters.PHOTO, noise_reduction_command)],
            EDGEDETECTION: [MessageHandler(filters.PHOTO, edge_detection_command)],
            BGREMOVAL: [MessageHandler(filters.PHOTO, bg_removal_command)],
            CROP: [MessageHandler(filters.PHOTO, crop_command)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # commands
    # app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('custom', custom_command))
    
    app.add_handler(conversation_handler)
    
    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # errors
    app.add_error_handler(error)
    
    # polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
            
if __name__ == '__main__':
    main()
    
#    '7858370163:AAHSRhPPxoxHzBbL_-ph-V5LWstDuKNiuGY'
    