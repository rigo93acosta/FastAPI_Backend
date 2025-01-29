from pymongo import MongoClient

# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# Módulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost

db_client = MongoClient().local

# Descomentar el db_client local o remoto correspondiente

# Base de datos local MongoDB

# Base de datos remota MongoDB Atlas (https://mongodb.com)
# db_client = MongoClient(
#     "mongodb+srv://<user>:<password>@<url>/?retryWrites=true&w=majority").test

db_client = MongoClient(
    "mongodb+srv://rigobertoacosta:asd@cluster0.njpyu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
).test

# Despliegue API en la nube:
# Deta - https://www.deta.sh/
# Intrucciones - https://fastapi.tiangolo.com/deployment/deta/