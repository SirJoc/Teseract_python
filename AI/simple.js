async function callOllama(model, systemPrompt, userPrompt) {
    let messages = [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
    ];

    while (true) {
        console.log("Calling Ollama...");
        console.log(messages);

        const response = await fetch("http://localhost:11434/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: model,
                messages: messages,
            }),
        }).then(res => res.json());

        //let responseMessage = response.response;
        const holiwis = await response;
        console.log("Got response", holiwis);
        if (response.done_reason  === "stop") {
            break;
        }
    }
}

const finalMessage = await callOllama(
    "granite3.1-dense:8b", // Ajusta el modelo según lo que tengas en Ollama
    "You are a helpful assistant. You give very short answers",
    "What is the weather like in San Francisco?"
);