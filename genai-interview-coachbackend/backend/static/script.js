async function sendPrompt() {
  const prompt = document.getElementById('prompt').value;
  const responseDiv = document.getElementById('response');

  if (!prompt.trim()) {
    responseDiv.innerText = "Please enter a prompt.";
    return;
  }

  responseDiv.innerText = "Generating response...";

  try {
    const response = await fetch('/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: prompt }),
    });

    const data = await response.json();
    if (data.response) {
      responseDiv.innerText = data.response;
    } else {
      responseDiv.innerText = "Error: No response from server.";
    }
  } catch (error) {
    responseDiv.innerText = "An error occurred: " + error;
  }
}
