// Allow for HTTP methods other than "GET" and "POST"
document.addEventListener("submit", (e) => {
    e.preventDefault();

    const form = e.target;
    fetch(form.action, {
        method: form.dataset.method,
        body: new FormData(form),
    }).then(() => {
        window.location.reload();
    });
});