import random

R_Toppings = '''
Okay. Which toppings ?
1. Black Olives
2. Capsicum
3. Onion
4. Jalepeno
5. Mushroom
'''

R_KindPizza = '''
What kind of pizza do you want?
1.VEG
2.NON-VEG
'''

R_PizzaSelection = '''
Lets customise your pizza!
1.Base 
2.Toppings 
'''

R_VegPizza = '''
Cool, Veg Pizza it is! Please choose amongst the following: 
1. Veggie Paradise
2. Margherita
3. Farm House
4. Peppy Paneer
5. Four Seasons 
6. Cheese N Corn
'''

R_NonVegPizza = '''
Cool , Non-Veg Pizza it is! Please choose amongst the following: 
1. Chicken Golden Delight
2. Chicken Dominator
3. Chicken Sausage
4. Chicken Pepperoni
5. Keema Do Pyaza
6. Indie Chicken Tikka
'''

R_Crust = '''
Select Pizza Base: 
1. Classic Hand Tossed
2. Flatbread Crust
3. Thin Crust
4. Thick Crust
'''

R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"


def unknown():
  response = [
    "Could you please re-phrase that? ",
    "Didn't get you:(\nEnter /help to move forward",
    # "Sounds all right.",
    "What does that mean?"
  ][random.randrange(3)]
  return response
