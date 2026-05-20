document.querySelectorAll('.product-card').forEach(card => {
  card.addEventListener('click', () => {
    document.getElementById('modalName').textContent = card.dataset.nombre;
    document.getElementById('modalDescription').textContent = card.dataset.descripcion;
    document.getElementById('modalPrice').textContent = card.dataset.precio;
    document.getElementById('modalStock').textContent = card.dataset.stock;
    document.getElementById('modalImage').src = card.dataset.imagen;
    
    document.getElementById('productModal').style.display = 'block';
  });
});

document.querySelector('.close-btn').addEventListener('click', () => {
  document.getElementById('productModal').style.display = 'none';
});

window.addEventListener('click', (e) => {
  if (e.target == document.getElementById('productModal')) {
    document.getElementById('productModal').style.display = 'none';
  }
});


document.addEventListener('DOMContentLoaded', () => {
    const reservarBtns = document.querySelectorAll('.btn-reservar');

    reservarBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const isAuthenticated = btn.dataset.authenticated === 'true';

            if (!isAuthenticated) {
                // Redirige al login
                window.location.href = "/accounts/login/?next=" + window.location.pathname;
            } else {
                // Aquí puedes llamar una función para añadir al carrito o abrir otro modal
                alert("Producto reservado (simulado). Aquí puedes añadirlo al carrito.");
            }
        });
    });
});


function reservarProducto() {
    fetch('/accounts/is_authenticated/')  // Nueva vista que crearemos
        .then(response => response.json())
        .then(data => {
            if (data.authenticated) {
                // Redirige a la vista de añadir al carrito
                const nombre = document.getElementById("modalName").innerText;
                window.location.href = `/cart/add/?product_name=${encodeURIComponent(nombre)}`;
            } else {
                // Redirige al login
                window.location.href = '/accounts/login/?next=/catalogo/';
            }
        });
}
