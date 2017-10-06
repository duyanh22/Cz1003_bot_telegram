import sys
import time
import datetime
import random
import traceback
import telepot
import telepot.helper
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

n01 = "" #Fabre, Arcine, Regal, Llyod, Trek
namelist = [n01]
if n01 == "":
    namelist.remove (n01)
print (namelist)

planner_records = telepot.helper.SafeDict()  # thread-safe dict

class TimePlanner(telepot.helper.ChatHandler):
    
    keyboard1_0 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Yes', callback_data='yes1_0'),
                    InlineKeyboardButton(text='No', callback_data='no1_0'),
                ]])
    keyboard1_1 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Next', callback_data='next1_1'),
                ]])
    keyboard1_2 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Next', callback_data='next1_2'),
                ]])
    keyboard1_3 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Next', callback_data='next1_3'),
                ]])
    keyboard1_4 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Upload', callback_data='upload1_4'),
                    InlineKeyboardButton(text='Exit', callback_data='exit1_4'),
                ]])
    keyboard1_5 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Next', callback_data='next1_5'),
                ]])
    keyboard1_6 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Exit', callback_data='exit1_6'),
                ]])
    keyboard2_0 = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Add User', callback_data='add2_0'),
                    InlineKeyboardButton(text='Delete User', callback_data='delete2_0')],
                    [InlineKeyboardButton(text='Namelist', callback_data='namelist2_0'),
                    InlineKeyboardButton(text='Exit', callback_data='exit2_0')]
                ])
    keyboard2_3 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Back', callback_data='back2_3'),
                ]])
    keyboard3_0 = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Yes', callback_data='yes3_0'),
                    InlineKeyboardButton(text='No', callback_data='no3_0'),
                ]])
    

    def __init__(self, *args, **kwargs):
        super(TimePlanner, self).__init__(*args, **kwargs)

        # Retrieve from database
        global planner_records
        if self.id in planner_records:
            self._edit_msg_ident = planner_records[self.id]
            self._editor = telepot.helper.Editor(self.bot, self._edit_msg_ident) if self._edit_msg_ident else None
        else:
            self._edit_msg_ident = None
            self._editor = None
                                
    def _plan1_0(self):
        sent = self.sender.sendMessage("Do you have a Html file for upload?", reply_markup=self.keyboard1_0)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan1_1(self):
        sent = self.sender.sendMessage('Once you are done logging in, press the "Next" button to proceed.', reply_markup=self.keyboard1_1)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan1_2(self):
        sent = self.sender.sendMessage('Once you are on the printable page, press the "Next" button to proceed.', reply_markup=self.keyboard1_2)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan1_3(self):
        sent = self.sender.sendMessage('Once you have saved the file, press the "Next" button to proceed.', reply_markup=self.keyboard1_3)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan1_4(self):
        sent = self.sender.sendMessage("Great! We're done with getting the file. We can either proceed with uploading the file, or do it another time.", reply_markup=self.keyboard1_4)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan1_5(self):
        sent = self.sender.sendMessage('Once you have uploaded the Html file, press the "Next" button to proceed.', reply_markup=self.keyboard1_5)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan1_6(self):
        sent = self.sender.sendMessage("Awesome! Group admin Tsukimiya will save a copy of your file once he's ready. If you haven't done so, you can add yourself as a user in the group via /user to facilitate timetable comparison." ,reply_markup=self.keyboard1_6)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan2_0(self):
        sent = self.sender.sendMessage("How may I help you?", reply_markup=self.keyboard2_0)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan2_1(self):
        sent = self.sender.sendMessage('Type out the name you would like to add, following this format-> Example: Add Arcine')
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan2_2(self):
        sent = self.sender.sendMessage('Type out the name you would like to remove, following this format-> Example: Remove Fabre')
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
    def _plan2_3(self):
        displaynames = namelist
        sent = self.sender.sendMessage("These are names added currently: "+str(', '.join(displaynames)), reply_markup=self.keyboard2_3)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
        print(', '.join(displaynames))
    def _plan3_0(self):
        sent = self.sender.sendMessage('Would you like to compare your free time?', reply_markup=self.keyboard3_0)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent) 

    def _cancel_last(self):
        if self._editor:
            self._editor.editMessageReplyMarkup(reply_markup=None)
            self._editor = None
            self._edit_msg_ident = None
    
    def on_chat_message(self, msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        namevalue = str (command)
        grpname = msg['chat']['first_name']
        print (chat_id)
                          
        if command == '/start':
            bot.sendMessage(chat_id, "Hello! "+str(grpname)+" Nice to meet you! How may I help you?")
            bot.sendMessage(chat_id, "Use /upload to upload your html file, /user to register yourself as a user, /compare to start comparing timetables, and /help should you require any assistance. Let's get started!")
        elif command == '/upload':
            self._plan1_0()
        elif command == '/user':
            self._plan2_0()
        elif command == '/compare':
            self._plan3_0()    
        elif command == '/help':
            bot.sendMessage(chat_id, "https://68.media.tumblr.com/e1f5efa7b149ec74841299f1f77a7d7d/tumblr_n0ag27Uxxz1qbvovho2_500.gif")
        elif "Add" in namevalue:
            namevalue = namevalue.replace ("Add ", "")
            bot.sendMessage(chat_id, "Awesome! "+namevalue+ " has been added.")
            n01 = namevalue
            namelist.append (n01)
            print (namevalue)
            print (namelist)
            print (', '.join(namelist))
            print (namelist[0])
        elif "Remove" in namevalue:
            namevalue = namevalue.replace ("Remove ", "")
            try:
                namelist.remove (namevalue)
            except ValueError:
                bot.sendMessage(chat_id, "Sorry! "+namevalue+" does not exist.")
            else:
                bot.sendMessage(chat_id, "Awesome! "+namevalue+ " has been removed.")
            print (namevalue)
            print (namelist)
        elif command == '/test':
            myname = namelist [0]
            try:
                with open (myname+".html") as fp:
                    soup = BeautifulSoup(fp,'html.parser')
                    bot.sendMessage(chat_id, soup.table.table.get_text())
                    print(soup.table.table.get_text())
            except:
                bot.sendMessage(chat_id, "File not found!")
                print ("File not recognised!")
            else:
                bot.sendMessage(chat_id, "Success!")
        else:
            bot.sendMessage(chat_id, "...")           
                
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            
        if query_data == 'yes1_0':
            self._cancel_last()
            self.sender.sendMessage("Great! Please upload your file as an attachment. Please tag group admin Tsukimiya so that he easily can find your attachment.")
            self._plan1_5()
            self.close()
        elif query_data == 'no1_0':
            self._cancel_last()
            self.sender.sendMessage("Please use the following link to login and access Stars Planner: https://sso.wis.ntu.edu.sg/webexe88/ntlm/sso_express.asp?app=https://wish.wis.ntu.edu.sg/pls/webexe/aus_stars_planner.main.")
            self._plan1_1()
            self.close()
        elif query_data == 'next1_1':
            self._cancel_last()
            self.sender.sendMessage('You should see "Printable Page" on your Stars Planner located on the right. Click on it go access the page.')
            self._plan1_2()
            self.close()
        elif query_data == 'next1_2':
            self._cancel_last()
            self.sender.sendMessage('Right click "Save As" and save the webpage as a Html file.')
            self.sender.sendMessage("Please save the name of the file as the SAME name that you will use/have used in the add user option. Note: The name is case-sensitive.")
            self._plan1_3()
            self.close()
        elif query_data == 'next1_3':
            self._cancel_last()
            self._plan1_4()
            self.close()
        elif query_data == 'upload1_4':
            self._cancel_last()
            self.sender.sendMessage("Great! Please upload your file as an attachment. Please tag group admin Tsukimiya so that he easily can find your attachment.")
            self._plan1_5()
            self.close()
        elif query_data == 'exit1_4':
            self.bot.answerCallbackQuery(query_id, text="Nice working with you.")
            self.sender.sendMessage("Use the /upload function whenever you're ready to proceed with uploading the file.")
            self._cancel_last()
            self.close()
        elif query_data == 'next1_5':
            self._cancel_last()
            self._plan1_6()
            self.close()
        elif query_data == 'exit1_6':
            self.bot.answerCallbackQuery(query_id, text="Nice working with you.")
            self._cancel_last()
            self.close()
        elif query_data == 'add2_0':
            self._cancel_last()
            self._plan2_1()
            self.close()
        elif query_data == 'delete2_0':
            self._cancel_last()
            self._plan2_2()
            self.close()
        elif query_data == 'namelist2_0':
            self._cancel_last()
            self._plan2_3()
            self.close()
        elif query_data == 'exit2_0':
            self.bot.answerCallbackQuery(query_id, text="Nice working with you.")
            self.sender.sendMessage("See you again.")
            self._cancel_last()
            self.close()      
        elif query_data == 'next2_2':
            self._cancel_last()
            self._plan2_0()
            self.close()
        elif query_data == 'back2_3':
            self._cancel_last()
            self._plan2_0()
            self.close()
        elif query_data == 'yes3_0':
            self._cancel_last()
            self.sender.sendMessage("Let's get started then!")
            self.close()
        elif query_data == 'no3_0':
            self._cancel_last()
            self.sender.sendMessage("I'm always ready.")
            self.close()
        else:
            self.bot.answerCallbackQuery(query_id, text="Request timeout.")
            self._cancel_last()
            self.close()

    def on__idle(self, event):
        self.sender.sendMessage('Need a break? No worries, I will always be here to assist you.')
        self.close()

    def on_close(self, ex):
        # Save to database
        global planner_records
        planner_records[self.id] = (self._edit_msg_ident)
    
bot = telepot.DelegatorBot("419378467:AAErbpva9dd_jhdDOgP3RWgQ1zdNQMaCeCU", [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']), create_open, TimePlanner, timeout=30),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(30)
