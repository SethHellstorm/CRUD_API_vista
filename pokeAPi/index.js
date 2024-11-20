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