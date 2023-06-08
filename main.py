import telebot
from truecallerpy import search_phonenumber
import json
import os
api=os.environ['api']
id=os.environ['id']
admin=os.environ['admin']


def main():
  
  bot = telebot.TeleBot(api)
  
  userDict = [admin,]

  @bot.message_handler(commands=['start'])
  def start(message):
      if message.from_user.id in userDict:
          bot.reply_to(
              message, "Hello! You can find details of a number. No need to add +91")
      else:
          bot.send_message(
              chat_id=admin, text=f'{message.from_user.first_name} {message.from_user.id}')
          bot.reply_to(
              message, "You cannot access the bot. If you have access, contact 'mere mai bap ko'")


  @bot.message_handler(commands=['add'])
  def add(message):
      id = int(message.text.split()[1])
      userDict.append(id)


  @bot.message_handler(func=lambda message: True)
  def true(message):
      global id
      if message.from_user.id in userDict:
          number = message.text
          num = str(number)
          num = num.replace(' ', '')

          if num.replace('+', '').isnumeric():
              response = search_phonenumber(number, "IN", id)
              formatted_response = json.dumps(response, indent=4)
              bot.reply_to(message, formatted_response)

          else:
              bot.reply_to(message, "Enter a valid number")
      else:
          bot.reply_to(message, "Don't use me")


  bot.polling()
  
if __name__=="__main__":
  main()
