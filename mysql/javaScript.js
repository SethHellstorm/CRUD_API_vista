function getAlumnos() {
    fetch('http://localhost:5000/alumnos')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('alumnosTableBody');
            tableBody.innerHTML = '';
            data.forEach(alumno => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${alumno.id}</td>
                        <td>${alumno.name}</td>
                        <td>${alumno.edad}</td>
                        <td>${alumno.carrera}</td>
                    </tr>
                `;
            });
        })
        .catch(error => console.error('Error:', error));
}