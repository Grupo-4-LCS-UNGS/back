# Backend de El Transportador

## Para el desarrollador
_En modo local_

>Se puede ejecutar todos estos comandos desde este script:

```bash
./development.sh
```


---

1. Crear entorno virtual de python
   
```bash
python -m venv virtual
```
2. Activar el entorno virtual
   
En Windows
```bash
virtual/Scripts/activate.bat
```

   En Linux
```bash
source virtual/Scripts/activate
```

3. Instalar los paquetes y dependencias necesarios
```bash
pip install psycopg2-binary
pip install -r requirements.txt
```

## Para el devops
_En Modo Stage_

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.13 python3.13-dev build-essential libpq-dev python
python3.13 -m venv virtual
source virtual/Scripts/activate
pip install psycopg2-binary
pip install -r requirements.txt
```