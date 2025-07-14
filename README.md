API_FRONT_EASYGROW

## 🚀 Cómo ejecutar
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📦 Variables de entorno necesarias
Copia `.env` con tus credenciales de base de datos y correo.

## 🔐 Endpoints disponibles
- POST `/api/v1/auth/register`
- POST `/api/v1/auth/login`

## 📌 Expansión futura
- CRUD de dispositivos
- CRUD de sensores y lecturas
- Subida y gestión de imágenes
- Gestión de notificaciones por nivel de alerta

---