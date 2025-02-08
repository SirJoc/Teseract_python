import ollama

def add_two_numbers(a: int, b: int) -> int:
  return a + b
def getWeatherByCityName(city: str) -> str:
  if city == 'New York':
    return f'{city} Sunny 20 C°'
  elif city == 'London':
    return f'{city} Cloudy 15 C°'
  elif city == 'Paris':
    return f'{city} Rainy 10 C°'
  else:
    return f'{city} Sunny 30 C°'

available_functions = {
  'add_two_numbers': add_two_numbers,
  'getWeatherByCityName': getWeatherByCityName,
}

msgs = [{'role': 'user', 'content': 'What is the weather in New York and London?'}]

response = ollama.chat(
  'granite3.1-dense:8b',
  messages = msgs,
  tools = [add_two_numbers, getWeatherByCityName], # Actual function reference
)
done = False

while not done:
    for tool in response.message.tool_calls or []:
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            msgs.append({
            'role': 'tool',
            'name': tool.function.name,
            'content': function_to_call(**tool.function.arguments),
            })
            response = ollama.chat(
                'granite3.1-dense:8b',
                messages = msgs,
                tools = [add_two_numbers, getWeatherByCityName], # Actual function reference
            )
            done = response.done
            print('Function output:', response.message.content)
        else:
            print('Function not found:', tool.function.name)