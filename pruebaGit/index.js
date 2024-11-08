//Importamos bibliotecas, cargar el modulo en este archivo
const xpress = require('express')
//Importar el modulo de path
const path= require('path')
//Creacion de la instancia
const app=xpress();

//Definir el puerto escuchar las solicitudes
const port = 3030;

//Creacion de las rutas
app.get('/',(req,res)=>{
    res.sendFile(path.join(__dirname,'index.html'));
});

//Iniciar el servidor
app.listen(port,()=>{
    console.log(`Hi bitch http://localhost:${port}`)
})