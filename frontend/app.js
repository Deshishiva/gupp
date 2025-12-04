async function sendMessage() {
    let q = document.getElementById("query").value;
    let persona = document.getElementById("persona").value;

    
    document.getElementById("chat").innerHTML += 
      `<div class='text-right'><span class='bg-blue-200 px-3 py-2 rounded'>${q}</span></div>`;

    
    let body = {
        query: q,
        persona: persona,
        messages: [{ role: "user", content: q }]
    };

    
    let backendURL = "https://YOUR-BACKEND-URL-HERE";

    
    let res = await fetch(`${backendURL}/process`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    let data = await res.json();

   
    document.getElementById("chat").innerHTML += 
      `<div><span class='bg-gray-200 px-3 py-2 rounded'>${data.reply}</span></div>`;

  
    document.getElementById("memory").textContent = JSON.stringify(data.memory, null, 2);
}
