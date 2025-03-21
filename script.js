function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    const chat = document.getElementById("chat");

    // Exibe a mensagem do usuário no chat
    chat.innerHTML += `<div><strong>Você:</strong> ${userInput}</div>`;

    // Resposta do chatbot
    const response = getResponse(userInput);
    chat.innerHTML += `<div><strong>Bot:</strong> ${response}</div>`;

    // Limpar o campo de input
    document.getElementById("userInput").value = "";
    chat.scrollTop = chat.scrollHeight; // Rola para o fim do chat
}

function getResponse(input) {
    // Exemplo simples de respostas
    if (input.includes("ganho")) {
        return "Quanto você ganhou?";
    } else if (input.includes("gasto")) {
        return "Qual foi o seu gasto?";
    } else if (input.includes("meta")) {
        return "Qual é a sua meta de economia?";
    } else {
        return "Desculpe, não entendi. Pode repetir?";
    }
}
