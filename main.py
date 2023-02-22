import constants as keys
from telegram.ext import *
import re
import long_responses as long
import help as H

print('bot started...')

order_list = [["Pizza:", "Not selected"], ["Size:", "Not selected"],
              ["Base:", "Not selected"], ["Price:", 0]]

base_len = len(order_list[2])
pizza_list = [
  'paradise', 'margherita', 'house', 'paneer', 'seasons', 'corn', 'delight',
  'dominator', 'sausage', 'pyaza', 'tikka', 'pepperoni'
]
Ppizza = [350, 350, 250, 300, 400, 400, 450, 450, 450, 500, 500, 500]
Rpizza_list = [
  "Veggie Paradise", "Margherita", "FarmHouse", "Peppy Panneer",
  "Four Seasons", "Cheese n Corn", "Chicken Golden Delight",
  "Chicken Dominator", "Chicken Sausage", "Keema Do Pyaza",
  "Indie Chicken Tikka", "Chicken Pepperoni"
]
size = ["small", "medium", "large"]
Psize = [100, 200, 300]
base = ["classic", "flat", "thin", "thick"]
Pbase = [50, 60, 50, 60]
Rbase = ["Classic Hand Tossed", "Flat Bread", "Thin Crust", "Thick Crust"]


def start_command(update, context):
  update.message.reply_text(
    # "Hey there! I am a Bot. I serve you with some amazing pizzass. to")
    """
    Hey sunshine, Welcome to PIZZABAE !\nTo order yummilicious pizza , enter "Order Pizza"\nFor any query , enter /help    """
  )


# def handle_message(update, context):

#   text = str(update.message.text)
#   response = R.sample_responses(text)
#   update.message.reply_text(response)


def help_command(update, context):
  helping = H.help()
  update.message.reply_text(helping)


def end_command(update, context):
  # update.message.reply_text("Sorry to see you go")
  update.message.reply_text("Already Leaving ? whyyyy?? ")


def message_probability(user_message,
                        recognised_words,
                        single_response=False,
                        required_words=[]):
  message_certainty = 0
  has_required_words = True

  # Counts how many words are present in each predefined message
  for word in user_message:
    if word in recognised_words:
      message_certainty += 1

  # Calculates the percent of recognised words in a user message
  percentage = float(message_certainty) / float(len(recognised_words))

  # Checks that the required words are in the string
  for word in required_words:
    if word not in user_message:
      has_required_words = False
      break

  # Must either have the required words, or be a single response
  if has_required_words or single_response:
    return int(percentage * 100)
  else:
    return 0


def check_all_messages(message):
  highest_prob_list = {}

  # Simplifies response creation / adds it to the dict
  def response(bot_response,
               list_of_words,
               single_response=False,
               required_words=[]):
    nonlocal highest_prob_list
    highest_prob_list[bot_response] = message_probability(
      message, list_of_words, single_response, required_words)

  # Responses -------------------------------------------------------------------------------------------------------

  response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'],
           single_response=True)
  response('See you!', ['bye', 'goodbye'], single_response=True)
  response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'],
           required_words=['how'])
  response('You\'re welcome!', ['thank', 'thanks'], single_response=True)

  response(
    '''
  Loved your choice! Anything else?
  if your cravings are satisfied, please type: 
  1. "checkout" to proceed with the billing,
  2. Or enter "/help" to get further assistance
  ''', [
      'black', ' olive', 'onion', 'capsicum', 'jalepeno', 'mushroom', 'classic'
      'hand', 'tossed', 'flat', 'bread', 'thin', 'cheeese', 'thick'
    ])
  response(
    'Address is noted! \nHead on to https://checkout-lac.vercel.app/ for initialising online payment\nThankyou for choosing PizzaBae🍕❤️',
    ["address"],
    required_words=["address"])
  response('Sure!', ['two'], required_words=['two'])

  response('What size?\nSmall, Medium or Large?', pizza_list)

  response('''
  What do you want to customize :)
  Base or Toppings
  ''', ['customize', 'yes', 'i', 'want', 'to'],
           required_words=['customize'])

  output = "--------------This is your order summary----------------\n\n" + str(
    order_list[0][1]
  ) + " " + str(order_list[1][1]) + " " + str(
    order_list[2][1]
  ) + "                              " + str(
    order_list[3][1]
  ) + "INR" + "\n(Extra Toppings: Olives, Mushrooms) x2" + "\n---------------------------------------------------------" + "\nDelivery                                         150 INR" + "\nTax                                                  33 INR" + "\n---------------------------------------------------------\n" + "Net Total                                         " + str(
    183 + order_list[3][1]
  ) + "INR\n\nHow do you wish to pay the bill?\n-COD\n-Online payment"

  response(output, ["checkout"], required_words=['checkout'])

  response('Order Confirmed\nThankyou for choosing PizzaBae🍕❤️',
           ['COD', 'cod'])

  response(
    'Please provide your address below and start by writing {My address is:...}',
    ['Online', 'online', 'payment'])

  # Longer responses
  response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
  response(long.R_KindPizza, ['order', 'want', 'pizza'],
           required_words=['order', 'pizza'])
  response(long.R_NonVegPizza, ['red'], required_words=['red'])
  response(long.R_VegPizza, ['green'], required_words=['green'])
  response(long.R_PizzaSelection, size, required_words=[])
  response(long.R_Toppings, ['toppings'], required_words=['toppings'])
  response(long.R_Crust, ['base'], required_words=['base'])

  best_match = max(highest_prob_list, key=highest_prob_list.get)
  # print(highest_prob_list)
  # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

  return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(update, context):
  text = str(update.message.text)
  split_message = re.split(r'\s+|[,;?!.-]\s*', text.lower())

  if split_message == ["veg"]:
    split_message[0] = "green"
  elif split_message in [["nonveg"], ['non', 'veg']]:
    split_message[0] = "red"

  if str(split_message[-1]) in pizza_list:
    i = pizza_list.index(split_message[-1])
    order_list[0][1] = Rpizza_list[i]
    order_list[3][1] += Ppizza[i]
    print("added pizza")
  elif str(split_message[0]) in size:
    i = size.index(split_message[0])
    order_list[1][1] = split_message[0]
    order_list[3][1] += Psize[i]
    print("added size")
  elif str(split_message[0]) in base:
    i = base.index(split_message[0])
    order_list[2][1] = Rbase[i]
    order_list[3][1] += Pbase[i]
    print("added base")

  if split_message == ["checkout"]:
    total = 0
    l = order_list[3]
    for i in range(len(l)):
      print(order_list[0][i], " ", order_list[1][i], " ", order_list[2][i],
            " ", order_list[3][i])

    total = order_list[3][i]

  response = check_all_messages(split_message)
  update.message.reply_text(response)


def main():

  user_input = Filters.text

  updater = Updater(keys.API_KEY, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler('start', start_command))

  dp.add_handler(CommandHandler('help', help_command))

  dp.add_handler(MessageHandler(user_input, get_response))

  updater.start_polling()
  updater.idle()


main()
