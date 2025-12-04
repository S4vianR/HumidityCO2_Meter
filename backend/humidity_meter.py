import random
def get_humidity():
    # Retornar datos simulados de humedad, un aleatorio entre 30% y 90%
    humidity = random.uniform(30.0, 90.0)
    return f"{round(humidity, 2)}%"
