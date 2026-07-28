const API_URL = 'http://localhost:8000';

// 1. BOTON CRM - Este ya te funciona
document.getElementById('btn-crm-demo').onclick = async () => {
    const res = await fetch(`${API_URL}/api/crm/demo`);
    const data = await res.json();
    alert(data.mensaje + " | Fecha: " + data.fecha);
};

// 2. ABRIR MODAL NUEVO
document.getElementById('btn-probar').onclick = () => {
    document.getElementById('modal-joyart').style.display = 'flex';
};

// 3. CERRAR MODAL NUEVO
document.getElementById('cerrar-modal').onclick = () => {
    document.getElementById('modal-joyart').style.display = 'none';
};
document.getElementById('modal-joyart').onclick = (e) => { 
    if(e.target.id === 'modal-joyart') document.getElementById('modal-joyart').style.display = 'none'; 
}

// 4. ENVIAR FORM NUEVO
document.getElementById('form-demo').onsubmit = async (e) => {
    e.preventDefault();
    const email = document.getElementById('input-email').value;
    
    await fetch(`${API_URL}/api/lead`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email})
    });
    
    alert('Demo solicitada! Te contactamos a: ' + email);
    document.getElementById('modal-joyart').style.display = 'none';
    e.target.reset();
};