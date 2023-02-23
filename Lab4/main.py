from controller import controller
from ui import UI

if __name__ == '__main__':
    k = int(input("Number of sensors: "))
    e = int(input("Energy value: "))
    ACOController = controller(k, e)
    ui = UI(ACOController)
    ui.run()