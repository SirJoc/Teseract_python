const weatherFunctionSpecs = {
    name: "get_weather",
    description: "Get the current weather for a city",
    parameters: {
        type: "object",
        properties: {
            city: {
                type: "string",
                description: "The city and state, e.g. San Francisco, CA",
            },
        },
        required: ["city"],
    },
};

async function callOllama(model, systemPrompt, userPrompt) {
    let messages = [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
    ];

    while (true) {
        console.log("Calling Ollama...");
        console.log(messages);

        const response = await fetch("http://localhost:11434/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: model,
                messages: messages,
                functions: [weatherFunctionSpecs],
            }),
            stream: false,
            format: "json",
        }).then(res => res.json());

        let responseMessage = response.message;
        console.log("Got response", response);
        messages.push(responseMessage);

        if (responseMessage.function_call?.name === "get_weather") {
            const args = JSON.parse(responseMessage.function_call.arguments);
            const city = args.city;
            console.log(`Getting weather for ${city}`);
            const weather = await getWeather(city);
            messages.push({
                role: "function",
                name: "get_weather",
                content: JSON.stringify(weather),
            });
        } else if (response.stop === "stop") {
            return responseMessage;
        }
    }
}

function getWeather(city) {
    // Aquí puedes implementar la lógica para obtener el clima de la ciudad
    // y devolver un objeto con la información del clima
    // Por ejemplo:
    return {
        city: city,
        temperature: 25,
        description: "Sunny",
    };
}

const finalMessage = await callOllama(
    "granite3.1-dense:8b", // Ajusta el modelo según lo que tengas en Ollama
    "You are a helpful assistant. You give very short answers",
    "What is the weather like in San Francisco?"
);
