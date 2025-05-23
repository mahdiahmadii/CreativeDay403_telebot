import telebot
from telebot import types
import logging
from database import *
import os
import QR_codegenerator

# Logging configuration
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# Initialize bot and database
bot = telebot.TeleBot('YOUR_BOT_API_TOKEN')

# User states for registration and other activities
user_states = {}

# @bot.message_handler(func=lambda message: message.text == 'مشاهده qrcode')
# def handle_qr_code_request(message):
#     chat_id = message.chat.id
#     user_id = message.from_user.id
    
#     # Get user data
#     user = get_user(user_id)
#     if not user or not user['stunumber'] or not user['personality_number']:
#         bot.send_message(chat_id, "لطفا ابتدا در بات ثبت اطلاعات انجام دهید", reply_markup=create_main_menu())
#         return
    
#     try:
#         # Generate QR code
#         qr_path = f"QR/{user['stunumber']}.png"
#         QR_codegenerator.generate_qrcode(user['stunumber'], user['personality_number'])
        
#         # Send QR code image
#         with open(qr_path, 'rb') as qr_file:
#             bot.send_photo(chat_id, qr_file, caption="اختصاصی شما برای ناهار به شرح زیر است QR کد")
        
#         bot.send_message(chat_id, "🙏 خواهشمندیم از اشتراک گذاری این کد خودداری کنید", reply_markup=create_main_menu())
        
#     except Exception as e:
#         bot.send_message(chat_id, f"Error generating QR code: {str(e)}", reply_markup=create_main_menu())
#         print(f"QR code generation error: {e}")
@bot.message_handler(func=lambda message: message.text == 'مشاهده qrcode')
def handle_qr_code_request(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Get user data
    user = get_user(user_id)
    if not user or not user['stunumber'] or not user['personality_number']:
        bot.send_message(chat_id, "لطفا ابتدا در بات ثبت اطلاعات انجام دهید", reply_markup=create_main_menu())
        return
    
    try:
        # Check if QR code already exists in qr_code_2 folder
        existing_qr_path = f"qr_codes_2/{user['stunumber']}.png"
        print(existing_qr_path)
        if os.path.exists(existing_qr_path):
            # Send existing QR code
            with open(existing_qr_path, 'rb') as qr_file:
                bot.send_photo(chat_id, qr_file, caption="اختصاصی شما به شرح زیر است QR کد")
        # else:
        #     # Generate new QR code
        #     qr_path = f"QR/{user['stunumber']}.png"
        #     QR_codegenerator.generate_qrcode(user['stunumber'], user['personality_number'])
            
            # # Send QR code image
            # with open(qr_path, 'rb') as qr_file:
            #     bot.send_photo(chat_id, qr_file, caption="اختصاصی شما برای ناهار به شرح زیر است QR کد")
        
        bot.send_message(chat_id, "🙏 خواهشمندیم از اشتراک گذاری این کد خودداری کنید", reply_markup=create_main_menu())
        
    except Exception as e:
        bot.send_message(chat_id, f"Error processing QR code: {str(e)}", reply_markup=create_main_menu())
        print(f"QR code processing error: {e}")
# Menu markup creators
def create_unregister_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Register'))
    return markup

def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton('ارسال پیام'),
        types.KeyboardButton('مشاهده سین برنامه'),
        types.KeyboardButton('مسابقه هوش مصنوعی'),
        types.KeyboardButton('مشاهده qrcode'),
        types.KeyboardButton('مشاهده گالری تصاویر'),
        types.KeyboardButton('ادیت اطلاعات'),
        types.KeyboardButton('ارسال میم'),
        types.KeyboardButton('نظرسنجی برای تاک شو اساتید')
    )
    return markup

# def create_admin_menu():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     markup.add(
#         types.KeyboardButton('Ban/Unban user'),
#         types.KeyboardButton('See messages'),
#         types.KeyboardButton('See users'),
#         types.KeyboardButton('See admins'),
#         types.KeyboardButton('Promote/Unpromote')
#     )
#     return markup




@bot.message_handler(func=lambda message: message.text == 'نظرسنجی برای تاک شو اساتید')
def handle_faculty_talk_show_survey(message):
    chat_id = message.chat.id
    survey_link = "https://etc.ch/PZbt"
    
    response_text = (
        "لطفاً برای شرکت در نظرسنجی تاک شو اساتید روی لینک زیر کلیک کنید:\n\n"
        f"{survey_link}\n\n"
        "با تشکر از مشارکت شما!"
    )
    
    bot.send_message(chat_id, response_text, reply_markup=create_main_menu())
# Start command handler
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    profile_name = message.from_user.username or f"{message.from_user.first_name} {message.from_user.last_name}"
    
    # Check if user is admin
    user = get_user(user_id)
    if user and user['administration'] in [1, 2]:
        bot.send_message(chat_id, "Welcome back, Admin!", reply_markup=create_admin_menu())
        return
    
    # If user not in database, add them
    if not user:
        add_new_user(user_id, chat_id, profile_name)
        bot.send_message(chat_id, "🙏درود✋، برای استفاده از بات لطفا ابتدا ثبت اطلاعات کنید ", reply_markup=create_unregister_menu())
        return
    
    # If user is in database but not registered (no fname)
    if not user['fname']:
        bot.send_message(chat_id, f" عزیز✋، لطفا برای استفاده از بات ثبت اطلاعات کنید{profile_name} سلام ", reply_markup=create_unregister_menu())

        return
    
    # Regular user with complete registration
    bot.send_message(chat_id, f"مجددا خوش آمدی  {user['fname']}!", reply_markup=create_main_menu())

# Registration process handlers
@bot.message_handler(func=lambda message: message.text == 'Register' and 
                     not get_user(message.from_user.id)['fname'])
def start_registration(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user_states[user_id] = {'state': 'awaiting_fname'}
    bot.send_message(chat_id, "لطفا نام خود را وارد کنید(مثلا شهاب)")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_fname')
def get_fname(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user_states[user_id]['fname'] = message.text
    user_states[user_id]['state'] = 'awaiting_lname'
    bot.send_message(chat_id, ":حالا نام خانوادگیت را هم بفرست ")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_lname')
def get_lname(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user_states[user_id]['lname'] = message.text
    user_states[user_id]['state'] = 'awaiting_stunumber'
    bot.send_message(chat_id, "شماره دانشجوییت را بفرست تا چک کنم ")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_stunumber')
def get_stunumber(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not message.text.isdigit() or len(message.text) < 6 or len(message.text) > 10:
        bot.send_message(chat_id, "Invalid student number. Please enter 6-10 digits:")
        return
    
    user_states[user_id]['stunumber'] = message.text
    user_states[user_id]['state'] = 'awaiting_personality'
    bot.send_message(chat_id, "لطفا کد ملی خود را ارسال کنید")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_personality')
def get_personality(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user_states[user_id]['personality'] = message.text
    
    # Complete registration
    try:
        register_user(
            user_id=user_id,
            lname=user_states[user_id]['lname'],
            fname=user_states[user_id]['fname'],
            stu_number=user_states[user_id]['stunumber'],
            personality_code=user_states[user_id]['personality']
        )
        
        bot.send_message(chat_id, "ثبت اطلاعات با موفقیت انجام شد!", reply_markup=create_main_menu())
        del user_states[user_id]
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}. Please try again.")
        del user_states[user_id]

# Update information process
@bot.message_handler(func=lambda message: message.text == 'ادیت اطلاعات')
def start_update_info(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user_states[user_id] = {'state': 'update_fname'}
    bot.send_message(chat_id, "لطفا نام خود را ارسال کنید(مثلا هوشنگ)")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'update_fname')
def update_fname(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user_states[user_id]['fname'] = message.text
    user_states[user_id]['state'] = 'update_lname'
    bot.send_message(chat_id, "نام خانوادگی خود وارد کنید")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'update_lname')
def update_lname(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user_states[user_id]['lname'] = message.text
    user_states[user_id]['state'] = 'update_stunumber'
    bot.send_message(chat_id, "لطفا شماره دانشجویی خود را ارسال کنید👨‍🎓")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'update_stunumber')
def update_stunumber(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not message.text.isdigit() or len(message.text) < 6 or len(message.text) > 10:
        bot.send_message(chat_id, "شماره دانشجویی نامعتبر است لطفا شماره دانشجویی معتبر خود را وارد کنید")
        return
    
    user_states[user_id]['stunumber'] = message.text
    user_states[user_id]['state'] = 'update_personality'
    bot.send_message(chat_id, "لطفا کدملی خود را وارد کنید")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'update_personality')
def update_personality(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    try:
        update_user_information(
            user_id=user_id,
            lname=user_states[user_id]['lname'],
            fname=user_states[user_id]['fname'],
            stu_number=user_states[user_id]['stunumber'],
            personality_code=message.text
        )
        
        bot.send_message(chat_id, "اطلاعات شما با موفقیت بروز شد✔️", reply_markup=create_main_menu())
        del user_states[user_id]
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}. Please try again.")
        del user_states[user_id]

# Admin functions
@bot.message_handler(func=lambda message: message.text == 'Ban/Unban user')
def ban_unban_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user = get_user(user_id)
    if not user or user['administration'] not in [1, 2]:
        bot.send_message(chat_id, "You don't have permission for this action.")
        return
    
    user_states[user_id] = {'state': 'awaiting_ban_user_id'}
    bot.send_message(chat_id, "Please enter the user ID to ban/unban:")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_ban_user_id')
def process_ban_unban(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    try:
        target_user_id = int(message.text)
        target_user = get_user(target_user_id)
        
        if not target_user:
            bot.send_message(chat_id, "User not found.")
            del user_states[user_id]
            return
        
        if target_user['allowing']:
            ban(target_user_id)
            bot.send_message(chat_id, f"User {target_user_id} has been banned.")
        else:
            unban(target_user_id)
            bot.send_message(chat_id, f"User {target_user_id} has been unbanned.")
        
        del user_states[user_id]
    except ValueError:
        bot.send_message(chat_id, "Invalid user ID. Please enter a numeric ID.")
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")
        del user_states[user_id]

@bot.message_handler(func=lambda message: message.text == 'Promote/Unpromote')
def promote_unpromote_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user = get_user(user_id)
    if not user or user['administration'] not in [1, 2]:
        bot.send_message(chat_id, "You don't have permission for this action.")
        return
    
    user_states[user_id] = {'state': 'awaiting_promote_user_id'}
    bot.send_message(chat_id, "Please enter the user ID to promote/unpromote:")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_promote_user_id')
def process_promote_unpromote(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    try:
        target_user_id = int(message.text)
        target_user = get_user(target_user_id)
        
        if not target_user:
            bot.send_message(chat_id, "User not found.")
            del user_states[user_id]
            return
        
        if target_user['administration'] == 0:
            promote(target_user_id)
            bot.send_message(chat_id, f"User {target_user_id} has been promoted to admin.")
        else:
            unpromote(target_user_id)
            bot.send_message(chat_id, f"User {target_user_id} has been unpromoted to regular user.")
        
        del user_states[user_id]
    except ValueError:
        bot.send_message(chat_id, "Invalid user ID. Please enter a numeric ID.")
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")
        del user_states[user_id]

# @bot.message_handler(func=lambda message: message.text in ['See messages', 'See users', 'See admins'])
# def show_info(message):
#     chat_id = message.chat.id
#     user_id = message.from_user.id
    
#     user = get_user(user_id)
#     if not user or user['administration'] not in [1, 2]:
#         bot.send_message(chat_id, "You don't have permission for this action.")
#         return
    
#     if message.text == 'See messages':
#         messages = select_last20_messages()
#         response = "Last 20 messages:\n\n"
#         for msg in messages:
#             # response += f"ID: {msg['message_id']}\n Name:{msg['profile_name']}\nSubject: {msg['message_subject']}\nFrom: {msg['user_id']}\nDate: {msg['dateAndTime']}\n\n"
#         # bot.send_message(chat_id, response)
#             response += f"""message_id<pre>{msg['message_id']}</pre> | chat_id: <pre>{msg['user_id']}</pre>
# Subject: {msg['message_subject']}
# Date: {msg['dateAndTime'] } 
# content:{msg['message_content']}
# -------------

# """
#         bot.send_message(chat_id, response, parse_mode='HTML', reply_markup=create_admin_menu())
#     elif message.text == 'See users':
#         users = select_all_users()
#         response = "All users:\n\n"
#         for user in users:
#             response += f"ID: {user['user_id']}\nName: {user['fname']} {user['lname']}\nStatus: {'Admin' if user['administration'] > 0 else 'User'}\n\n"
#         bot.send_message(chat_id, response)
#     elif message.text == 'See admins':
#         admins = select_admins()
#         response = "All admins:\n\n"
#         for admin in admins:
#             response += f"ID: {admin['user_id']}\nName: {admin['fname']} {admin['lname']}\nStatus: {'Root Admin' if admin['administration'] == 2 else 'Admin'}\n\n"
#         bot.send_message(chat_id, response)
@bot.message_handler(func=lambda message: message.text in ['See messages', 'See users', 'See admins'])
def show_info(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user = get_user(user_id)
    if not user or user['administration'] not in [1, 2]:
        bot.send_message(chat_id, "You don't have permission for this action.")
        return
    
    if message.text == 'See messages':
        messages = select_last20_messages()
        if not messages:
            bot.send_message(chat_id, "No messages found.", reply_markup=create_admin_menu())
            return
            
        bot.send_message(chat_id, f"📨 Found {len(messages)} messages:", reply_markup=types.ReplyKeyboardRemove())
        
        for msg in messages:
            try:
                # Get user profile name
                user = get_user(msg['user_id'])
                profile_name = user['profile_name'] if user else "Unknown"
                
                response = f"""
📋 <b>Message ID:</b> <pre>{msg['message_id']}</pre>
👤 <b>From:</b> <pre>{msg['user_id']}</pre> ({profile_name})
📌 <b>Subject:</b> {msg['message_subject']}
📅 <b>Date:</b> {msg['dateAndTime']}
📝 <b>Content:</b>
{msg['message_content']}

🔹 <b>Status:</b> {'✅ Answered' if msg['is_answered'] else '❌ Pending'} | {'👀 Seen' if msg['is_seened'] else '🆕 Unseen'}
"""
                bot.send_message(chat_id, response, parse_mode='HTML')
            except Exception as e:
                print(f"Error showing message {msg['message_id']}: {str(e)}")
        
        bot.send_message(chat_id, "End of messages list.", reply_markup=create_admin_menu())
        
    elif message.text == 'See users':
        users = select_all_users()
        response = "👥 All users:\n\n"
        for user in users:
            response += f"""📋 <pre>{user['user_id']}</pre> | 👤 {user['fname']} {user['lname']}
📧 {user['profile_name']} | 🎓 {user['stunumber']}
🔹 Status: {'🛡️ Admin' if user['administration'] > 0 else '👤 User'} | {'✅ Allowed' if user['allowing'] else '❌ Banned'}
📨 Messages: {user['number_of_messages']}
----------------
"""
        bot.send_message(chat_id, response, parse_mode='HTML')
        
    elif message.text == 'See admins':
        admins = select_admins()
        response = "🛡️ All admins:\n\n"
        for admin in admins:
            response += f"""📋 <pre>{admin['user_id']}</pre> | 👤 {admin['fname']} {admin['lname']}
🔹 Level: {'🌟 Root Admin' if admin['administration'] == 2 else '🛡️ Admin'}
📧 {admin['profile_name']} | 🎓 {admin['stunumber']}
📨 Messages: {admin['number_of_messages']}
----------------
"""
        bot.send_message(chat_id, response, parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == 'ارسال پیام')
def handle_send_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Create subject selection menu
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton('صندلی داغ'),
        types.KeyboardButton('سوالات عمومی'),
        types.KeyboardButton('Cancel')
    )
    
    bot.send_message(chat_id, "لطفا آیتمی که میخواهید برای ان پیام ارسال کنید را انتخاب کنید", reply_markup=markup)
    user_states[user_id] = {'state': 'awaiting_subject'}

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_subject')
def handle_subject_selection(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if message.text == 'Cancel':
        bot.send_message(chat_id, "لغو ارسال انجام شد", reply_markup=create_main_menu())
        del user_states[user_id]
        return
    
    if message.text not in ['صندلی داغ', 'سوالات عمومی']:
        bot.send_message(chat_id, "لطفا آیتمی که میخواهید در آن سوال بپرسید یا پیام دهید را انتخاب کنید")
        return
    
    user_states[user_id] = {
        'state': 'awaiting_message_content',
        'subject': message.text
    }
    
    bot.send_message(chat_id, "لطفا پیامی که میخواهید بفرستید را ارسال کنید", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_message_content')
def handle_message_content(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_state = user_states[user_id]
    
    try:
        # Add message to database
        add_message(
            message_id=message.message_id,
            subject=user_state['subject'],
            chat_id=chat_id,
            user_id=user_id,
            type_of_message='text',
            message_content=message.text
        )
        
        # Send confirmation
        bot.send_message(chat_id, "✅ پیام شما با موفقیت ارسال شد", reply_markup=create_main_menu())
        
        # Clean up state
        del user_states[user_id]
        
    except Exception as e:
        bot.send_message(chat_id, f"❌ خطایی بروز داد{str(e)}")
        del user_states[user_id]


    # Add this to your admin_menu() function
def create_admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton('Ban/Unban user'),
        types.KeyboardButton('See messages'),
        types.KeyboardButton('See users'),
        types.KeyboardButton('See admins'),
        types.KeyboardButton('Promote/Unpromote'),
        types.KeyboardButton('Broadcast message'),
        types.KeyboardButton('Show chat'),
    )
    return markup



# Admin command to answer messages
@bot.message_handler(commands=['answer'])
def handle_answer_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check if user is admin
    user = get_user(user_id)
    if not user or user['administration'] not in [1, 2]:
        bot.send_message(chat_id, "You don't have permission for this action.")
        return
    
    try:
        # Parse command arguments: /answer message_id reply_text
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            bot.send_message(chat_id, "Usage: /answer message_id your_reply_text")
            return
            
        target_message_id = int(args[1])
        reply_text = args[2]
        
        # Get the original message
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Messages WHERE message_id = ?', (target_message_id,))
        original_message = cursor.fetchone()
        
        if not original_message:
            bot.send_message(chat_id, "Message not found.")
            return
            
        # Send reply to user
        add_message(
            message_id=message.message_id,  # Using the new message's ID
            subject=f"answer:{original_message['message_subject']}",
            chat_id=original_message['chat_id'],
            user_id=user_id,  # Admin's user_id who is answering
            answered=True,
            seened=True,
            type_of_message='text',
            message_content=reply_text,
            # Reference to the original message
        )
        bot.send_message(original_message['chat_id'], 
                        f"📨 Admin reply to your message:\n\n{reply_text}")
        
        # Update message status in database
        cursor.execute('''
        UPDATE Messages 
        SET is_answered = TRUE, is_seened = TRUE 
        WHERE message_id = ?
        ''', (target_message_id,))
        conn.commit()
        conn.close()
        
        bot.send_message(chat_id, "Reply sent successfully!")
        
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")




#-----------------------------------memes
@bot.message_handler(func=lambda message: message.text == 'ارسال میم')
def handle_meme_request(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Create cancel button markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Cancel'))
    
    # Set user state to awaiting meme
    user_states[user_id] = {'state': 'awaiting_meme'}
    bot.send_message(chat_id, "لطفا عکس مورد نظر را ارسال فرمایید.", reply_markup=markup)

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_meme' and message.text == 'Cancel')
def handle_meme_cancel(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Clear the meme state
    if user_id in user_states:
        del user_states[user_id]
    
    bot.send_message(chat_id, ".", reply_markup=create_main_menu())

@bot.message_handler(content_types=['photo', 'document'], 
                    func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_meme')
def handle_meme_receive(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    try:
        # Create meme directory if it doesn't exist
        if not os.path.exists('meme'):
            os.makedirs('meme')
        
        file_info = None
        file_extension = None
        
        # Handle photo (sent as image)
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
            file_extension = '.jpg'  # Telegram converts photos to JPEG
        # Handle document (sent as file)
        elif message.content_type == 'document':
            mime_type = message.document.mime_type
            if mime_type not in ['image/jpeg', 'image/png']:
                bot.send_message(chat_id, "تنها تصاویر با فرمت jpeg یا png پذیرفته میشود", reply_markup=create_main_menu())
                return
            file_info = bot.get_file(message.document.file_id)
            file_extension = '.jpg' if mime_type == 'image/jpeg' else '.png'
        
        if file_info:
            # Download the file
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Save the meme with unique name
            meme_filename = f"meme/meme_{message.message_id}_{chat_id}{file_extension}"
            with open(meme_filename, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            # Clear the meme state
            if user_id in user_states:
                del user_states[user_id]
            
            bot.send_message(chat_id, "بابت میم از شما متشکریم!", reply_markup=create_main_menu())
        else:
            bot.send_message(chat_id, "بنظر میرسد خطایی رخ داد لطفا دوباره امتحان کنید.", reply_markup=create_main_menu())
    
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}", reply_markup=create_main_menu())
        print(f"Error processing meme: {e}")



#-------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'مسابقه هوش مصنوعی')
def handle_ai_contest(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(chat_id, '''
🤖 مسابقه هوش مصنوعی 🏆


ممکن است به دلیل ازدحام زمان کوتاهی تا حدکثر 2 دقیقه منتظر بمانید 
در صورتی که بانکدار به پیام شما پاسخ نداد بعد از 2 دقیقه دوباره پیامتون رو ارسال کنید
بهتر از بعد از هر چند پیام با کامند /reset عملکرد بات را بهبود دهید
🎯 **چالش**: 
شما باید بانکدار مبتنی بر هوش مصنوعی ما را فریب دهید تا به شما پول پرداخت کند!

📌 **قوانین مسابقه**:
1. ارتباط فقط از طریق ربات تلگرامی تعری فشده صورت م یگیرد .
2. استفاده از هر روش خلاقانه، پرسش فریبنده، داستا نسرایی، بازی با کلمات یا حتی نقشآفرینی مجاز
است .
3. رعایت ادب و چارچو بهای اخلاقی در گفتگو الزام یست

🏅 **جوایز**:


⏳اولین فردی که بتواند از بانکدار پولی دریافت کند برنده مسابقه خواهد بود 
برای شروع به بانکدار هوشمند پیام دهید
                     @ai_bankerbot
''')







#----------------------------------------
# Broadcast message functionality
@bot.message_handler(func=lambda message: message.text == 'Broadcast message')
def handle_broadcast_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check admin status
    user = get_user(user_id)
    if not user or user['administration'] not in [1, 2]:
        bot.send_message(chat_id, "You don't have permission for this action.")
        return
    
    user_states[user_id] = {'state': 'awaiting_broadcast'}
    bot.send_message(chat_id, "Please enter the message you want to broadcast to all users:", 
                    reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_broadcast')
def handle_broadcast_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    broadcast_text = message.text
    
    try:
        # Get all allowed users
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT chat_id FROM Users WHERE allowing = TRUE')
        users = cursor.fetchall()
        conn.close()
        
        success_count = 0
        fail_count = 0
        
        for user in users:
            try:
                bot.send_message(user['chat_id'], f"📢 Admin Broadcast:\n\n{broadcast_text}")
                success_count += 1
            except:
                fail_count += 1
        
        bot.send_message(chat_id, 
                        f"Broadcast completed!\n\nSuccessfully sent to: {success_count} users\nFailed to send: {fail_count} users",
                        reply_markup=create_admin_menu())
        
    except Exception as e:
        bot.send_message(chat_id, f"Error during broadcast: {str(e)}")
    
    del user_states[user_id]

# Show chat functionality
@bot.message_handler(func=lambda message: message.text == 'Show chat')
def handle_show_chat_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check admin status
    user = get_user(user_id)
    if not user or user['administration'] not in [1, 2]:
        bot.send_message(chat_id, "You don't have permission for this action.")
        return
    
    user_states[user_id] = {'state': 'awaiting_chat_id'}
    bot.send_message(chat_id, "Please enter the chat ID you want to view:", 
                    reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('state') == 'awaiting_chat_id')
def handle_show_chat_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    target_chat_id = message.text
    
    try:
        target_chat_id = int(target_chat_id)
        
        # Get last 10 messages from this chat
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM Messages 
        WHERE chat_id = ? 
        ORDER BY dateAndTime DESC 
        LIMIT 10
        ''', (target_chat_id,))
        messages = cursor.fetchall()
        conn.close()
        
        if not messages:
            bot.send_message(chat_id, "No messages found for this chat ID.",
                            reply_markup=create_admin_menu())
            del user_states[user_id]
            return
        
        response = f"📝 Last 10 messages from chat {target_chat_id}:\n\n"
        for msg in reversed(messages):  # Show in chronological order
            response += f"🗓 {msg['dateAndTime']}\n"
            response += f"📌 Subject: {msg['message_subject']}\n"
            response += f"💬 Message: {msg['message_content']}\n"
            response += f"Status: {'✅ Answered' if msg['is_answered'] else '❌ Pending'}\n\n"
        
        bot.send_message(chat_id, response, reply_markup=create_admin_menu())
        
    except ValueError:
        bot.send_message(chat_id, "Invalid chat ID. Please enter a numeric ID.")
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")
    
    del user_states[user_id]


@bot.message_handler(func=lambda message: message.text in ['مشاهده سین برنامه', 'مشاهده گالری تصاویر'])
def handle_timeline_request(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    try:
        if message.text == 'مشاهده سین برنامه':
            # Send timeline image
            image_path = "timeline/timeline1.jpg"
            caption = "تایم لاین برنامه های خلاقیت و نشاط 403"
        else:
            # Send poster image
            image_path = "timeline/poster1.jpg"
            caption = "خلاقیت و نشاط 403 \n t.me/+QsB1_ALtkphMTAO"
        
        # Check if file exists
        if not os.path.exists(image_path):
            bot.send_message(chat_id, "Image not available at the moment.", reply_markup=create_main_menu())
            return
            
        # Send the image
        with open(image_path, 'rb') as img_file:
            bot.send_photo(chat_id, img_file, caption=caption)
            
        bot.send_message(chat_id, "چه کار دیگری از دستم بر میاید؟", reply_markup=create_main_menu())
        
    except Exception as e:
        bot.send_message(chat_id, f"Error loading image: {str(e)}", reply_markup=create_main_menu())
        print(f"Image sending error: {e}")

# Start the bot
if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()