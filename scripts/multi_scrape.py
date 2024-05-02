import sys
import os

# Agregar el directorio actual al sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from app.main import handle

# Rellena aquí tus datos para ejecutar el código

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
