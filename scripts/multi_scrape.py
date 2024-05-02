import sys
import os

# Se configura el proyecto para que se puedan acceder a las diferentes carpetas y métodos.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from app.main import handle

# Acá es donde se deben ingresar los elementos.

DATA = {
    "date_range": {
        "since": "",
        "until": "",    
    },
    "usuario": "",
    "password": "",
    "account": "",
}

print(f'------------------ RUN START ------------------')
handle(DATA)
print(f'------------------ RUN ENDED ------------------\n')
