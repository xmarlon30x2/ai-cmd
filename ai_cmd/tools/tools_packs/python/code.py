from executors import PythonProgram

code = """
from random import randint


def input_int(prompt:str):
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print('Introduce un numero valido')

def game(lives:int, start:int=0, end:int=10):
    print('Adivia el numero secreto entre 0 y 10')
    secret_number = randint(start, end)
    while True:
        target_number = input_int('Introduce un numero> ')
        if target_number == secret_number:
            print('Has ganado')
            return
        else:
            lives -= 1
            if lives <= 0:
                print('Lo siento, has perdido. Te has quedado sin vidas')
                return

if __name__ == '__main__':
    game(3)
"""

program = PythonProgram(code)
program.start()
while True:
    data = input(">").strip()
    stdout, stderr = program.comunicate(None if not data else data)
    print(f"stdout> {stdout}")
    print(f"stderr> {stderr}")
    print(f"return_code> {program.return_code}")
