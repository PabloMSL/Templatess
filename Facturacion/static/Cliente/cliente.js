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