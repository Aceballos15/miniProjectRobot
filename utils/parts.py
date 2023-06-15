class Part: 
  def __init__(self, name: str, attack_level = 0, defense_level= 0, energy_consumption=0 ): 
    self.name = name 
    self.attack_level = attack_level
    self.defense_level = defense_level 
    self.energy_consumption = energy_consumption 

  
  def get_status_dict(self): 
    formatted_name = self.name.replace(" ", "_").lower()
    return {
        "{}_name".format(formatted_name): self.name.upper(), 
        "{}_status".format(formatted_name): self.is_available(), 
        "{}_attack".format(formatted_name): self.attack_level,
        "{}_defense".format(formatted_name): self.defense_level, 
        "{}_energy_consump".format(formatted_name): self.energy_consumption 
    }

  # Método para determinar si una parte está disponible 
  def is_available(self): 
    return False if self.defense_level <= 0 else True

  #Método para cambiar el estado de una parte 
  def change_status(self): 
    pass


