# Proyecto de Aplicación Web con FastAPI

Este proyecto es una aplicación web construida con FastAPI que proporciona varias rutas para manejar productos y usuarios, incluyendo autenticación básica y autenticación JWT. A continuación se describe la estructura y funcionalidad de cada archivo:

## Estructura de Archivos

- **main.py**: Es el archivo principal que inicia la aplicación FastAPI y monta los routers para manejar las rutas de productos y usuarios. También monta un directorio estático para servir archivos estáticos.

### Rutas principales

- `/`: Devuelve un mensaje de bienvenida.
- `/url`: Devuelve una URL.

- **routers/products.py**: Define un router para manejar las rutas relacionadas con productos.

### Rutas de Productos

- `/products/`: Devuelve una lista de productos.
- `/products/{id}`: Devuelve un producto específico por su ID.

- **routers/users.py**: Define un router para manejar las rutas relacionadas con usuarios.

### Rutas de Usuarios

- `/usersjson`: Devuelve una lista de usuarios en formato JSON.
- `/users/`: Devuelve una lista de usuarios como objetos.
- `/username/{name}`: Devuelve un usuario por su nombre.
- `/user/{user_id}`: Devuelve un usuario por su ID.
- `/user/`: Permite crear, actualizar y eliminar usuarios.

- **routers/basic_auth_users.py**: Define un router para manejar la autenticación básica de usuarios.

### Rutas de Autenticación Básica

- `/login`: Permite a los usuarios iniciar sesión.
- `/users/me`: Devuelve la información del usuario autenticado.

- **routers/jwt_auth_users.py**: Define un router para manejar la autenticación JWT de usuarios.

### Rutas de Autenticación JWT

- `/login`: Permite a los usuarios iniciar sesión.

- **type_hints.py**: Contiene ejemplos de uso de type hints en Python.
- **static/**: Directorio para archivos estáticos, como imágenes.