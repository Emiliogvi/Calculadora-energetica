##Clonar el repositorio

##Crear un entorno virtual
python -m venv venv

##Activación del entorno virtual
.\venv\Scripts\Activate
deactivate

##instalar estas dependencias

pip install django

pip install python-dotenv

pip install psycopg[binary]

##Correr el proyecto
python manage.py runserver
