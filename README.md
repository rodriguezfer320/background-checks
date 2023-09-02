# background-checks
Es un microservicio de la aplicación de Finishing Schools Univalle que permite la verificación de los antecedentes de un candidato específico.

Para ejecutar este microservicio, se deben ejecutar los siguientes pasos:

1. Crear la imagen docker del backend:
    
    * Esteblecer el entorno (desarrollo, producción o prueba) modificando el archivo .env:
        ENVIRONMENT=development
    * Para crear la imagen ejecutar el siguiente comando:
        docker build -t background-checks-backend:v1.0 ./backend

2. Crear la imagen docker del frontend ejecutando el comando:
    
    * Esteblecer el entorno (desarrollo o producción):
        copiar el contenido del archivo .dev o .prod al Dockerfile
    * Para crear la imagen ejecutar el siguiente comando:
        docker build -t background-checks-frontend:v1.0 ./frontend

3. Ejecutar el docker compose para crear los contenedores:

    * Esteblecer el entorno (desarrollo o producción):
        copiar el contenido del archivo .yml.dev o .yml.prod al docker-compose.yml
    * Para crear los contendores ejecutar el siguiente comando:
        docker compose up