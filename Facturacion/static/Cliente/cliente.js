function openModal(id) {      
    document.getElementById(id).style.display = "block";     
}

function closeModal(id) {       
    document.getElementById(id).style.display = "none";     
}

        
function pagarFactura(id) {         
    // Simulación de pago        
    showToast("Factura " + id + " pagada con éxito!");    
    //Aquí podrías hacer una llamada AJAX para actualizar el estado      
}

        
function showToast(message) {          
    const toast = document.getElementById("toast");         
    toast.innerText = message;           
    toast.className = "toast show";           
    setTimeout(() => {              
        toast.className = "toast";        
    }, 3000);        
}

// Cerrar modales si clic fuera
        
window.onclick = function(event) {
    const modales = document.getElementsByClassName("modal");        
    for (let modal of modales) {      
        if (event.target == modal) {           
            modal.style.display = "none";            
        }       
    }    
}

// cliente.js

// ... (funciones openModal, closeModal, showToast, window.onclick) ...

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function pagarFactura(id) {
    const csrftoken = getCookie('csrftoken'); // Obtener el token CSRF

    fetch(`/api/facturas/${id}/pagar/`, { // <-- La URL que crearemos en Django
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Adjuntar el token de seguridad
        },
        // Opcional: Si quieres enviar datos en el cuerpo
        body: JSON.stringify({ 'metodo_pago': 'Tarjeta' }) 
    })
    .then(response => {
        if (!response.ok) {
            // Manejar errores de servidor (4xx, 5xx)
            throw new Error(`Error en el pago: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showToast(`Factura ${id} pagada con éxito!`);
            
            // ⭐️ LO MÁS IMPORTANTE: Actualizar el DOM
            actualizarFacturaEnDOM(id, data.total, data.metodo_pago);
            
        } else {
            showToast(`Error: ${data.message || 'No se pudo procesar el pago.'}`);
        }
    })
    .catch(error => {
        console.error('Error al realizar el pago:', error);
        showToast(`Error de conexión: ${error.message}`);
    });
}

function actualizarFacturaEnDOM(facturaId, total, metodoPago) {
    // 1. Encontrar el elemento card que contiene la factura
    // Necesitas una forma de identificar la CARD en el HTML (ver paso 3)
    const card = document.getElementById(`factura-card-${facturaId}`);
    
    if (card) {
        // 2. Encontrar y actualizar el estado
        const estadoElement = card.querySelector('p:nth-last-child(3)'); // Busca el párrafo de estado
        if (estadoElement && estadoElement.innerText.includes('Pendiente')) {
            estadoElement.innerText = `Estado: Pagada`;
        }
        
        // 3. Opcional: Actualizar el método de pago
        const metodoElement = card.querySelector('p:nth-last-child(2)'); 
        if (metodoElement) {
            metodoElement.innerText = `Método de pago: ${metodoPago}`;
        }

        // 4. Eliminar el botón "Pagar Ahora"
        const botonPagar = card.querySelector('.btn-action');
        if (botonPagar) {
            botonPagar.remove();
        }
    }
}