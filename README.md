# 🎓 Buscador Licencias v1.2

Buscador de softwares académicos con alto impacto en el desarrollo académico de la comunidad Universitaria.

Encuentra herramientas digitales que son **de pago para el público general** pero **100% gratuitas para académicos** — verificadas con proceso manual, emergentes y poco conocidas.

---

## 🚀 Deploy en Streamlit Cloud

### Paso 1 — Sube a GitHub
```bash
git init
git add .
git commit -m "Buscador Licencias v1.2"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/buscador-licencias.git
git push -u origin main
```

### Paso 2 — Despliega en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona el repositorio
4. Main file: `app.py` → **Deploy**

### Paso 3 — Configura tu API Key ⚠️ OBLIGATORIO
En Streamlit Cloud: tu app → **Settings → Secrets** → agrega:
```toml
GEMINI_API_KEY = "AIzaSy..."
```
La app lee la key automáticamente. No hay campo visible en la interfaz.

### Obtener API Key de Gemini (gratis)
[aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## 💻 Ejecutar localmente

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crea `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "AIzaSy..."
```

```bash
streamlit run app.py
```

---

## 📋 Flujo completo

| Paso | Descripción |
|------|-------------|
| **Etapa 1** | Gemini valida 5 herramientas con modelo de negocio correcto |
| **✏️ Corrección** | Escribe instrucciones para corregir resultados antes de continuar |
| **Etapa 2** | Filtra herramientas emergentes / baja popularidad |
| **Etapa 3** | Enriquece con descripción, precio, proceso de acceso y casos de uso |
| **＋ Más bloques** | Genera bloques adicionales de 10 sin perder el historial |
| **Excel** | Descarga acumulada de todos los bloques en 2 hojas |

---

## 🗂️ Estructura
```
buscador-licencias/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── README.md
└── .gitignore
```
