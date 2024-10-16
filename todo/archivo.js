fetch('http://127.0.0.1:5000/registrar_usuario', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => {
    return response.json().then(data => ({
        status: response.status,
        body: data
    }));
})
.then(result => {
    if (result.status === 201) {
        alert(result.body.message);
    } else {
        alert(`Error: ${result.body.message}`);
    }
})
.catch(error => {
    console.error('Error:', error);
    alert('Hubo un problema al conectar con el servidor.');
});


