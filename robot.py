#Import the robot model 
from utils.robot_art import robot_art

# Import the class "Part"
from utils.parts import Part

import pyttsx3
import random


# Dictionay with available colors for the robot 
colors = {
    "Black": "\x1b[90m", 
    "Blue": "\x1b[94m",
    "Cyan": "\x1b[96m",
    "Green": "\x1b[92m",
    "Magenta": "\x1b[95m",
    "Red": "\x1b[91m",
    "White": "\x1b[97m",
    "Yellow": "\x1b[93m",
}


#Dictionary with available parts detached by the robot
inventory_options = {
  "head": ["synthovisor_cortex", 5], 
  "left Arm": ["cyber_module", 5], 
  "right Arm": ["cyber_module", 5],
  "left Leg": ["elemental_piece", True], 
  "right Leg": ["elemental_piece", True], 
  "weapon": ["electro_arrows", 10]
}

#Part options
part_options = {"head" : 0, "weapon": 1, "left Arm": 2, "right Arm": 3, "left Leg": 4, "right Leg": 5}

#Robor class 
class Robot: 
  def __init__(self, name, color_code, model): 
    self.name = name 
    self.color_code = color_code 
    self.model = model 
    self.energy = 100
    self.on = self.on_robot() 
    self.defense_total_status = False 
    self.inventory_robot = [{}, {}]
    self.available_parts = []

    self.parts = [
        Part("head", attack_level=10, defense_level= 40, energy_consumption= 20 ), 
        Part("weapon", attack_level=10, defense_level= 10, energy_consumption= 15 ), 
        Part("left Arm", attack_level=20, defense_level= 60, energy_consumption= 5 ), 
        Part("right Arm", attack_level=20, defense_level= 60, energy_consumption= 5 ), 
        Part("left Leg", attack_level=15, defense_level= 60, energy_consumption= 5 ), 
        Part("right Leg", attack_level=15, defense_level= 30, energy_consumption= 5 ), 

    ]

  #method to turn On the robot 
  def on_robot(self): 
    return True if self.energy > 0 else False 

  # Method to greet 
  def greet(self): 
    greet= f'Hello, my name is {self.name}'
    engine = pyttsx3.init()
    engine.say(greet)
    engine.runAndWait()
    print(f'Hello, my name is {self.name}')


  #Method to attack the enemy robot 
  def attack(self, enemy_robot, part_to_use, part_to_attack): 
    if self.defense_total_status == False: 
      enemy_robot.parts[part_to_attack].defense_level -= self.parts[part_to_use].attack_level 
      self.energy -= self.parts[part_to_use].energy_consumption
 

  #method to print the attack resume 
  def attack_resume(self, robot_attacker, used_part, attacked_part, robot_attacked): 
    return {
        "Robot attacker": robot_attacker,
        "Used part for attack": used_part, 
        "Attacked part": attacked_part, 
        "Robot attacked": robot_attacked
    }
  

  #Mhetod to find the available parts for attack 
  def is_available_part(self): 
    self.available_parts.clear()
    for item in self.parts: 
      if item.defense_level > 0: 
        self.available_parts.append(part_options[item.name])
      
    return self.available_parts


  #Method to update the robot inventory 
  def update_inventory(self, part_to_use, part_to_attack): 
    self.inventory_robot[1].update({self.parts[part_to_attack].name: self.parts[part_to_use].attack_level})
  

  #Method to merge parts of the enemy robot with your inventory
  def fuse_power(self, part_fusion, inventory_item): 
    self.parts[part_fusion].attack_level += self.inventory_robot[1][inventory_item]
    self.parts[part_fusion].defense_level += self.inventory_robot[1][inventory_item]

    self.delete_item_part_inventory(inventory_item)

    #Method to update bonus
    part_name = self.parts[part_fusion].name
    self.inventory_robot[0].update({ inventory_options[part_name][0]: inventory_options[part_name][1] })


  #Method to delete an intem in the inventory
  def delete_item_part_inventory(self, inventory_item): 
    self.inventory_robot[1].pop(inventory_item)
    
  #Method to use the bonus
  def use_bonus(self, part, enemy_robot, part_to_attack): 
    bonus_name = inventory_options[self.parts[part].name][0]

    if bonus_name == "synthovisor_cortex": 
      self.parts[part].attack_level += 5 
    elif bonus_name == "cyber_module": 
      self.parts[part].defense_level += 5 
    elif bonus_name == "elemental_piece": 
      self.defense_total_status = True 
    elif bonus_name == "electro_arrows":    
      enemy_robot[part_to_attack].defense_level -= 10

    self.inventory_robot[0].pop(bonus_name)


  
  #Method to print the energy robot  
  def print_energy(self): 
    return self.energy

  # Method to print the status robot 
  def print_status(self): 
    print(self.color_code)
    str_robot = robot_art.format(**self.get_part_status())
    self.greet()
    self.print_energy()
    print(str_robot)
    print(colors["White"])

  #Method to get the part dictionary and merge all parts together
  def get_part_status(self): 
    part_status= {}
    for part in self.parts: 
      status_dict = part.get_status_dict()
      part_status.update(status_dict)
    return part_status

# jarvis = Robot("Jarvis", colors["Green"], "JBK")
# print(jarvis.color_code)
# jarvis.print_status()

def play(): 
  playing= True 
  count = 0

  print("Welcome to the game............ Good look")

  # Inputs to digit the properties of the one robot
  #robot_one_name = str(input("Enter a name for player 1: "))
  #print("Permited colors: Red, Yellow, White, Magenta, Green, Cyan, Blue, Black")
  #robot_one_color = str(input("Enter a color for your first robot"))
  #robot_one_model = str(input("Enter a model of your one robot "))
#
  # Inputs to digit the properties of the two robot 
  #robot_two_name = str(input("Enter a name for player 2: "))
  #print("Permited colors: Red, Yellow, White, Magenta, Green, Cyan, Blue, Black")
  #robot_two_color = str(input("Enter a color for your second robot"))
  #robot_two_model = str(input("Enter a model of your second robot  "))
#
  ##Instance the robot
  robot_one = Robot("Jarvis", colors["Red"], "JFG")
  robot_two = Robot("Alex", colors["Green"], "FFL")
  
  while playing:

    if count % 2 == 0: 
      current_robot = robot_one
      enemy_robot = robot_two

      #Recalculate the available parts of the robot 
      current_robot.is_available_part()
      enemy_robot.is_available_part()

      print(current_robot.available_parts)
      print(enemy_robot.available_parts)


      current_robot.print_status()

      # Select the part to use and the part to attack 
      part_to_use = int(input("Choose a part to use for attack"))
      part_to_attack = int(input("Choose a part to attack"))


      #Validate existence of the part to use and part to attack
      if part_to_use in current_robot.available_parts and part_to_attack in enemy_robot.available_parts:  
        permission = True
      else: 
        permission = False

        while not permission: 
          print("The choose option is not available, try again")
           # Select the part to use and the part to attack 
          part_to_use = int(input("Choose a part to use for attack"))
          part_to_attack = int(input("Choose a part to attack"))

          if part_to_use in current_robot.available_parts and part_to_attack in enemy_robot.available_parts:   
            permission = True

      # Si el invemtario del robot en las partes a fusionar no está vacio, preguntamos si desea fusionar ya 
      if len(current_robot.inventory_robot[1]) > 0: 
        use_fuse_power = str(input("Should you use the fouse power (Y/N): ")).lower()
        corretc_response_options = ["y", "n"]

        while use_fuse_power not in corretc_response_options: 
          print("choose a correct option, try again")
          use_fuse_power = str(input("Should you use the fouse power (Y/N): ")).lower()
      

        if use_fuse_power == "y":
            print("Choose an option for fusion: ")
            print(current_robot.inventory_robot[1])
            part_option = input("Choose: ")
            current_robot.fuse_power(part_to_use, part_option)

            current_robot.use_bonus(part_to_use, enemy_robot, part_to_attack)
            current_robot.print_status()   

      current_robot.attack(enemy_robot, part_to_use, part_to_attack)

      #Cambiamos el estado de la defensa total a Falso nuevamente en caso de que este activo (Para el robot enemigo)
      if enemy_robot.defense_total_status == True: 
        enemy_robot.defense_total_status = False 

      print(current_robot.update_inventory(part_to_use, part_to_attack))

      print(enemy_robot.color_code)
      print(current_robot.attack_resume(current_robot.name, part_to_use, part_to_attack, enemy_robot.name))
      enemy_robot.print_status()
      print(current_robot.inventory_robot)


    else:
      current_robot = robot_two
      enemy_robot = robot_one
      #Mandamos a recalcular las partes disponibles de cada robot 
      current_robot.is_available_part()
      enemy_robot.is_available_part()

      current_robot.print_status()
      #Selecciona una parte aleatoria el robot enemigo 
      part_to_use = int(random.choice(current_robot.available_parts))
      part_to_attack = int(random.choice(current_robot.available_parts))

      # if inventory robot is not empty, ask if you want to fuse_power() any part
      if len(current_robot.inventory_robot[1]) > 0: 
        corretc_response_options = ["y", "n"]
        use_fuse_power = random.choice(corretc_response_options)


        if use_fuse_power == "y":
            print("Choose an option for fusion: ")
            print(current_robot.inventory_robot[1])
            part_option = random.choice( list(current_robot.inventory_robot[1].keys() ) )
            current_robot.fuse_power(part_to_use, part_option)

            current_robot.use_bonus(part_to_use, enemy_robot, part_to_attack)
            current_robot.print_status() 

      current_robot.attack(enemy_robot, part_to_use, part_to_attack)

      #If enemy robot is defense_total_status = True, we change this value to False
      if enemy_robot.defense_total_status == True: 
        enemy_robot.defense_total_status = False 

      #Update the inventory robot 
      current_robot.update_inventory(part_to_use, part_to_attack)

      print(enemy_robot.color_code)
      print(current_robot.attack_resume(current_robot.name, part_to_use, part_to_attack, enemy_robot.name))
      enemy_robot.print_status()

      print(current_robot.inventory_robot)


    if not enemy_robot.on_robot() or len(enemy_robot.available_parts) < 2:
        greet= f'Hello, my name is {current_robot.name}'
        engine = pyttsx3.init()
        engine.say(f'Congratulations, you won, Robot {current_robot.name}')
        engine.runAndWait()
        Playing = False       
    count += 1


play()
   