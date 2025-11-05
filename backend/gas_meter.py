import random
def get_gas_levels():
    # Retornar datos simulados de niveles de gas, un aleatorio entre 200 y 1000 ppm
    gas_level = random.uniform(200.0, 1000.0)
    return f"{round(gas_level, 2)} ppm"