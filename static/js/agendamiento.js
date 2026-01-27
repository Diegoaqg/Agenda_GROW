// Configuración base de la agencia
const duracionEmpresa = 8; 

const menuStates = {
    servicio: { isOpen: false, selected: "Sesiones", placeholder: "Servicio..." },
    tipo: { isOpen: false, selected: "Tipo de sesión", placeholder: "Selecciona..." },
    estado: { isOpen: false, selected: "---", placeholder: "Opciones..." }
};

const opcionesServicios = {
    "Sesiones": { label: "Tipo de sesión", items: ["Sesión de Estrategia", "Sesión Extra"] },
    "Reunión de Área": { label: "Área", items: ["Marketing", "Ventas", "Operaciones"] },
    "Diseño": { label: "Diseño...", items: ["UI/UX", "Branding", "Social Media"] }
};

function validarSeleccion() {
    const btn = document.getElementById('btn-programar');
    const { servicio, tipo, estado } = menuStates;

    const esValido = servicio.selected !== "Selecciona..." && 
                     tipo.selected !== "Tipo de sesión" && 
                     !["---", "Elegir opción"].includes(estado.selected);

    if (esValido) {
        btn.classList.remove('bg-white/20', 'text-white/40', 'pointer-events-none', 'cursor-not-allowed');
        btn.classList.add('bg-white', 'text-black', 'hover:bg-[var(--primary)]', 'hover:text-white');
    } else {
        btn.classList.add('bg-white/20', 'text-white/40', 'pointer-events-none', 'cursor-not-allowed');
        btn.classList.remove('bg-white', 'text-black', 'hover:bg-[var(--primary)]', 'hover:text-white');
    }
}

function toggleMenu(menuId) {
    const state = menuStates[menuId];
    const list = document.getElementById(`list-${menuId}`);
    const chevron = document.getElementById(`chevron-${menuId}`);
    const container = document.getElementById(`container-${menuId}`);
    const textElement = document.getElementById(`text-${menuId}`);

    state.isOpen = !state.isOpen;

    if (state.isOpen) {
        if (menuId === 'tipo') renderOpcionesTipo();
        if (menuId === 'estado') renderOpcionesDetalle();
        
        Object.keys(menuStates).forEach(id => {
            if(id !== menuId && menuStates[id].isOpen) toggleMenu(id);
        });

        textElement.innerText = "Selecciona...";
        textElement.classList.add('opacity-40');
        list.classList.remove('hidden');
        if(chevron) chevron.classList.add('rotate-180');
        container.style.borderColor = 'var(--primary)';
    } else {
        textElement.innerText = state.selected;
        textElement.classList.remove('opacity-40');
        list.classList.add('hidden');
        if(chevron) chevron.classList.remove('rotate-180');
        container.style.borderColor = 'rgba(255, 255, 255, 0.1)';
    }
}

function renderOpcionesTipo() {
    const items = opcionesServicios[menuStates.servicio.selected].items;
    document.getElementById('list-tipo').innerHTML = items.map(item => `
        <button onclick="selectOption('tipo', '${item}')" class="btn-option">${item}</button>
    `).join('');
}

function renderOpcionesDetalle() {
    const listEstado = document.getElementById('list-estado');
    // Leemos la configuración que inyectó Django
    const config = window.BusinessConfig || { duracion: 8, drone: false, dividir: true };
    
    let options = [];

    if (menuStates.tipo.selected === "Sesión de Estrategia") {
        // Regla: Solo permitir dividir si la empresa lo tiene activado y es de 8h
        if (config.duracion === 8 && config.dividir) {
            options = ["Sesión completa (8h)", "Dividir (4h + 4h)"];
        } else {
            options = [`Sesión única (${config.duracion}h)`];
        }
    } 
    else if (menuStates.tipo.selected === "Sesión Extra") {
        options = ["Sesión por horas"];
        // Regla: Solo añadir Drone si la empresa lo ofrece
        if (config.drone) {
            options.push("Sesión con Drone");
        }
        options.push("Sesión Urgente");
    }

    listEstado.innerHTML = options.map(opt => `
        <button onclick="selectOption('estado', '${opt}')" class="btn-option">${opt}</button>
    `).join('');
}

function selectOption(menuId, value) {
    menuStates[menuId].selected = value;
    
    if (menuId === 'servicio') {
        const labelDefault = opcionesServicios[value].label;
        menuStates.tipo.selected = labelDefault;
        document.getElementById('text-tipo').innerText = labelDefault;
        activarDetalle(false);
    }

    if (menuId === 'tipo') {
        activarDetalle(true);
        menuStates.estado.selected = "Elegir opción";
        document.getElementById('text-estado').innerText = "Elegir opción";
    }
    
    toggleMenu(menuId);
    validarSeleccion();
}

function activarDetalle(activar) {
    const cont = document.getElementById('container-estado');
    if (activar) {
        cont.classList.remove('opacity-40', 'pointer-events-none');
    } else {
        cont.classList.add('opacity-40', 'pointer-events-none');
        menuStates.estado.selected = "---";
        document.getElementById('text-estado').innerText = "---";
    }
}

function enviarAlCalendario(event) {
    event.preventDefault();
    const { servicio, tipo, estado } = menuStates;
    
    // 1. Obtenemos el slug del cliente desde la URL actual
    // Si estás en /c/mi-empresa/, esto sacará "mi-empresa"
    const pathArray = window.location.pathname.split('/');
    const slug = pathArray[pathArray.indexOf('c') + 1];

    // 2. Construimos la URL profesional que definimos en urls.py
    const urlFinal = `/c/${slug}/calendario/?servicio=${encodeURIComponent(servicio.selected)}&tipo=${encodeURIComponent(tipo.selected)}&detalle=${encodeURIComponent(estado.selected)}`;
    
    window.location.href = urlFinal;
}

document.addEventListener('click', (e) => {
    Object.keys(menuStates).forEach(id => {
        const el = document.getElementById(`container-${id}`);
        if (el && !el.contains(e.target) && menuStates[id].isOpen) toggleMenu(id);
    });
});