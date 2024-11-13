async function llenarTabla() {
    const response = await fetch('http://127.0.0.1:5000/alumnos');
    const items = await response.json();
    const tableBody = document.getElementById('item-table-body');
    tableBody.innerHTML = '';  // Limpiar la tabla antes de añadir nuevos datos

    items.forEach(item => {
        const row = document.createElement('tr');
        
        const idCell = document.createElement('td');
        idCell.textContent = item.id;
        
        const nameCell = document.createElement('td');
        nameCell.textContent = item.name;

        const ageCell = document.createElement('td');
        ageCell.textContent = item.edad;

        const carreraCell = document.createElement('td');
        carreraCell.textContent = item.carrera;

        row.appendChild(idCell);
        row.appendChild(nameCell);
        row.appendChild(ageCell);
        row.appendChild(carreraCell);
        
        tableBody.appendChild(row);
    });
}
llenarTabla();

async function guardarAlumno() {
    const name = document.getElementById('nombre_alumno').value;
    const edad = document.getElementById('edad_alumno').value;
    const carrera = document.getElementById('carrera_alumno').value;

    const itemData = { name, edad: parseInt(edad), carrera };
    await fetch('http://127.0.0.1:5000/alumnos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itemData)
    });

    document.getElementById('nombre_alumno').value = '';
    document.getElementById('edad_alumno').value = '';
    document.getElementById('carrera_alumno').value = '';
    llenarTabla();
}

async function modificarAlumno() {
    const id = document.getElementById('id_alumno').value;
    const name = document.getElementById('nombre_alumno').value;
    const edad = document.getElementById('edad_alumno').value;
    const carrera = document.getElementById('carrera_alumno').value;

    const itemData = { name, edad: parseInt(edad), carrera };

    
    await fetch(`http://127.0.0.1:5000/alumnos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itemData)
    });

    document.getElementById('id_alumno').value = '';
    document.getElementById('nombre_alumno').value = '';
    document.getElementById('edad_alumno').value = '';
    document.getElementById('carrera_alumno').value = '';
    llenarTabla();
}

async function eliminarAlumno() {
    const id = document.getElementById('id_alumno').value;
    await fetch(`http://127.0.0.1:5000/alumnos/${id}`, { method: 'DELETE' });
    llenarTabla();
}