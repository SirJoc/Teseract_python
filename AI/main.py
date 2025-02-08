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

msgs = [{'role': 'system', 'content': 'Do not allucinate, only use the information provided, you are a helpful assistant.'},
        {'role': 'user', 'content': 'What is the weather in New York and London? and the sumn of 2 and 3?'}]

response = ollama.chat(
  'granite3.1-dense:8b',
  messages = msgs,
  tools = [add_two_numbers, getWeatherByCityName], # Actual function reference
)
done = False
last_message = ''
context = ''
while not done:
    for tool in response.message.tool_calls or []:
        print('Tool calls:', response.message.tool_calls)
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            context += str(function_to_call(**tool.function.arguments)) + '\n'
        else:
            print('Function not found:', tool.function.name)

    msgs.append({
        'role': 'tool',
        'name': tool.function.name,
        'content': context,
    })
    response = ollama.chat(
        'granite3.1-dense:8b',
        messages = msgs,
        tools = [add_two_numbers, getWeatherByCityName], # Actual function reference
    )
    done = response.done
    print('Function output:', msgs)
    if done:
        last_message = response.message.content

    print('Final response:', last_message)