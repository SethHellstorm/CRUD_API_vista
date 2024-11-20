//Importamos bibliotecas, cargar el modulo en este archivo
const express = require('express')
//Importar el modulo de path
const path= require('path')
//Creacion de la instancia
const app=express();

//Definir el puerto escuchar las solicitudes
const port = 3030;

//Analizador de Json
app.use(express.json());

//Creacion de las rutas
app.get('/',(req,res)=>{
    res.sendFile(path.join(__dirname,'index.html'));
});

//Datos en memoria (temporal)
let usuarios = [{id:1,nombre:"Rafael",email:"test@gmail.com"},
    {id:2,nombre:"Rafael",email:"test@gmail.com"}
];

//Crear ruta POST
app.post('/usuarios', (req, res)=> {
    //res.send('Crear un usuario');
    //Variables los campos BD
    const{id,nombre,email}=req.body;
    //Agregar elementos al arreglo
    usuarios.push({id,nombre,email});
    res.status(201).json({mensaje:'Usuario creado', usuario:{id,nombre,email}});
})

//Creacion de una ruta GET
app.get('/usuarios',(req,res)=>{
    res.json(usuarios)
})

//Ruta para obtener un usuario email
app.get('/usuarios/:email', (req,res)=>{
    const usuario = usuarios.filter(u => u.email == req.params.email);
    //Validar objeto
    if (usuario){
        //Mostrar
        res.json(usuario)
    } else {
        res.status(404).json({mensaje: "Usuario no se encontro"})
    }
})

//Crear la ruta para actualizar
app.put('/usuarios/:id', (req,res)=>{
    const {nombre, email} = req.body
    const usuario = usuarios.find(u => u.id == req.params.id);
    if(usuario){
        usuario.nombre = nombre || usuario.nombre
        usuario.email = email || usuario.email
        res.json({mensaje: 'Usuario actualizado', usuario});
    } else {
        res.status(404).json({mensaje: 'Usuario no encontrado'});
    }
})

//Ruta para eliminar un usuario
app.delete('/usuarios/:email', (req,res)=>{
    const index = usuarios.findIndex(u => u.email== req.params.email);
    if (index !== -1){
        const usuarioEliminado = usuarios.splice(index,1);
        res.json({mensaje:'Usuario eliminado', usuario: usuarioEliminado})
    } else{
        res.status(404).json({mensaje: 'Usuario no encontrado'})
    }
})

//Iniciar el servidor
app.listen(port,()=>{
    console.log(`http://localhost:${port}`)
})