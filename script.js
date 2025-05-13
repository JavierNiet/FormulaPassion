// Toggle theme functionality
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('dark-theme');
}

// Scroll to top functionality
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Toggle sidebar functionality
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const body = document.body;
    if (sidebar.style.width === '250px') {
        sidebar.style.width = '0';
        body.classList.remove('sidebar-open');
    } else {
        sidebar.style.width = '250px';
        body.classList.add('sidebar-open');
        // Asegura que la barra se muestre desde la derecha
        sidebar.style.right = '0';
        sidebar.style.left = 'auto';
    }
}

// Lazy loading de imágenes
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.loading = 'lazy';
    });
});

// Mostrar un loader mientras se cargan los datos
function showLoader() {
    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.style.position = 'fixed';
    loader.style.top = '50%';
    loader.style.left = '50%';
    loader.style.transform = 'translate(-50%, -50%)';
    loader.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    loader.style.color = 'black';
    loader.style.padding = '20px';
    loader.style.borderRadius = '10px';
    loader.style.zIndex = '1000';
    loader.innerHTML = '<p>Cargando resultados...</p>';
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) loader.remove();
}

// Modificar la función de carga de resultados para incluir el loader
async function loadRaceResults() {
    const resultsBody = document.getElementById('results-body');
    if (!resultsBody) return; // Solo ejecuta si existe la tabla
    showLoader();
    try {
        const response = await fetch('http://127.0.0.1:5000/api/results');
        if (!response.ok) {
            throw new Error('Error al obtener los resultados de las carreras.');
        }
        const results = await response.json();
        resultsBody.innerHTML = '';
        results.forEach(result => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${result.race}</td>
                <td>${result.date}</td>
                <td>${result.winner}</td>
                <td>${result.equipo}</td>
                <td>${result.dorsal}</td>
            `;
            resultsBody.appendChild(row);
        });
    } catch (error) {
        if (resultsBody) {
            resultsBody.innerHTML = '<tr><td colspan="5" style="color:red;">No se pudo cargar los resultados.</td></tr>';
        }
        console.error('Error loading race results:', error);
    } finally {
        hideLoader();
    }
}

// Mostrar próxima carrera de F1 en la página principal
async function loadNextRace() {
    const nextRaceDiv = document.getElementById('next-race-info');
    try {
        const response = await fetch('http://127.0.0.1:5004/api/next_race');
        const data = await response.json();
        if (!response.ok) {
            nextRaceDiv.innerHTML = `<span style="color:red;">${data.error || 'No se pudo cargar la próxima carrera.'}</span>`;
            return;
        }
        // Renderiza la información y agrega un span para el tiempo restante
        nextRaceDiv.innerHTML = `
            <strong>${data.nombre}</strong><br>
            <span>${data.circuito} - ${data.ubicacion}</span><br>
            <span>Fecha: ${data.fecha} | Hora: ${data.hora}</span><br>
            <span id="tiempo-restante" style="font-size:1.2em;color:#1e90ff;">${data.tiempo_restante}</span>
        `;

        // Calcula el tiempo restante en milisegundos
        const targetDate = new Date(`${data.fecha}T${data.hora}:00`);
        if (window.tiempoRestanteInterval) clearInterval(window.tiempoRestanteInterval);
        window.tiempoRestanteInterval = setInterval(async () => {
            const now = new Date();
            let diff = targetDate - now;
            if (diff <= 0) {
                // Cuando se acabe el tiempo, recarga la info de la próxima carrera
                clearInterval(window.tiempoRestanteInterval);
                await loadNextRace();
                return;
            }
            const dias = Math.floor(diff / (1000 * 60 * 60 * 24));
            const horas = Math.floor((diff / (1000 * 60 * 60)) % 24);
            const minutos = Math.floor((diff / (1000 * 60)) % 60);
            const segundos = Math.floor((diff / 1000) % 60);
            document.getElementById('tiempo-restante').textContent = `${dias} días, ${horas} horas, ${minutos} minutos, ${segundos} segundos`;
        }, 1000);
    } catch (e) {
        nextRaceDiv.innerHTML = '<span style="color:red;">No se pudo cargar la próxima carrera.</span>';
    }
}

// Validar el formulario de contacto antes de enviarlo
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();

        if (!name || !email || !message) {
            alert('Por favor, completa todos los campos antes de enviar el formulario.');
            return;
        }

        alert('¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.');
        this.reset();
    });
}

// Chatbot IA Formula 1
(function() {
    const header = document.getElementById('chatbot-header');
    const body = document.getElementById('chatbot-body');
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');
    let open = false;
    header.onclick = function() {
        open = !open;
        body.style.display = open ? 'block' : 'none';
        form.style.display = open ? 'flex' : 'none';
        if(open) input.focus();
    };
    form.onsubmit = async function(e) {
        e.preventDefault();
        const question = input.value.trim();
        if (!question) return;
        body.innerHTML += `<div style='margin-bottom:8px;'><b>Tú:</b> ${question}</div>`;
        input.value = '';
        body.scrollTop = body.scrollHeight;
        body.innerHTML += `<div id='ia-typing' style='color:#e10600;'>IA escribiendo...</div>`;
        body.scrollTop = body.scrollHeight;
        try {
            const res = await fetch('http://127.0.0.1:5005/api/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });
            const data = await res.json();
            document.getElementById('ia-typing').remove();
            if(data.answer) {
                body.innerHTML += `<div style='margin-bottom:8px;'><b>IA:</b> ${data.answer}</div>`;
            } else {
                body.innerHTML += `<div style='color:red;'>Error: ${data.error || 'No se pudo obtener respuesta.'}</div>`;
            }
        } catch (err) {
            document.getElementById('ia-typing').remove();
            body.innerHTML += `<div style='color:red;'>Error de conexión con la IA.</div>`;
        }
        body.scrollTop = body.scrollHeight;
    };
})();

// Llamar a las funciones cuando se cargue la página
window.addEventListener('DOMContentLoaded', () => {
    loadRaceResults();
    loadNextRace();
});