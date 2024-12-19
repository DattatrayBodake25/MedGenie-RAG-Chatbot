const sendButton = document.getElementById('send-button');
const userQueryInput = document.getElementById('user-query');
const chatHistory = document.getElementById('chat-history');
const loadingSpinner = document.getElementById('loading-spinner');

sendButton.addEventListener('click', async () => {
    const userQuery = userQueryInput.value.trim();
    if (userQuery === "") return;

    // Display the user's query in the chat history
    appendMessage(userQuery, 'user-message');

    // Show the loading spinner
    loadingSpinner.style.display = 'flex';

    // Send the query to the backend
    try {
        const response = await fetch('http://127.0.0.1:8000/answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: userQuery,
                top_k: 5,
            }),
        });

        const data = await response.json();
        if (data.answer) {
            // Display the chatbot's response with emoji at the beginning
            appendMessage(`🤖 ${data.answer}`, 'chatbot-message');
        } else {
            appendMessage('Sorry, no relevant information found. Please try again. 😔', 'chatbot-message');
        }
    } catch (error) {
        appendMessage('An error occurred, please try again later. ⚠️', 'chatbot-message');
    }

    // Hide the loading spinner
    loadingSpinner.style.display = 'none';

    // Clear the input field
    userQueryInput.value = '';
});

function appendMessage(message, messageType) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    
    const bubbleElement = document.createElement('div');
    bubbleElement.classList.add(messageType);
    bubbleElement.textContent = message;

    messageElement.appendChild(bubbleElement);
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}