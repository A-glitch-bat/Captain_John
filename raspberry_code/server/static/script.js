document.getElementById("routerbot-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const msg = document.getElementById("routerbot-input").value;
    const response = await fetch("/routerbot", {
        method: "POST",
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ message: msg })
    });
    const text = await response.text();
    document.getElementById("routerbot-input").value = "";
    document.getElementById("routerbot-response").innerText = "Q: "+msg+"\n\nA: "+text;
});

document.getElementById("mainbot-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const msg = document.getElementById("mainbot-input").value;
    const response = await fetch("/mainbot", {
        method: "POST",
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ message: msg })
    });
    const data = await response.json();
    const { taskID, answer } = data;
    document.getElementById("mainbot-input").value = "";
    document.getElementById("mainbot-response").innerText = "Q: "+msg+"\n\ntID: "+taskID+"\n"+answer;
});

document.getElementById("schizobot-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const msg = document.getElementById("schizobot-input").value;
    const response = await fetch("/schizobot", {
        method: "POST",
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ message: msg })
    });
    const text = await response.text();
    document.getElementById("schizobot-input").value = "";
    document.getElementById("schizobot-response").innerText = "Q: "+msg+"\n\nA: "+text;
});

document.getElementById("sumbot-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const msg = document.getElementById("sumbot-input").value;
    const response = await fetch("/sumbot", {
        method: "POST",
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ message: msg })
    });
    const text = await response.text();
    document.getElementById("sumbot-input").value = "";
    document.getElementById("sumbot-response").innerText = "Q: "+msg+"\n\nA: "+text;
});
