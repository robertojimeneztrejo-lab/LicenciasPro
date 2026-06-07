# 🎓 LicenceHunt v2.0

Buscador de licencias académicas gratuitas con integración Google Sheets.

## Secrets requeridos en Streamlit Cloud

Ve a tu app → **Settings → Secrets** y agrega:

```toml
GEMINI_API_KEY   = "AIzaSy..."
APPS_SCRIPT_URL  = "https://script.google.com/macros/s/TU_ID/exec"
SHEETS_CSV_URL   = "https://docs.google.com/spreadsheets/d/TU_ID/gviz/tq?tqx=out:csv&sheet=licencias"
```

## Configurar Google Apps Script (igual que ARIA Membresías)

1. Abre tu Google Sheet
2. Extensiones → Apps Script
3. Pega este código:

```javascript
function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet()
                .getSheetByName("licencias");
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet("licencias");
    sheet.appendRow(["Nombre","Link","Contacto","Tipo","Uso","Tema","Fecha"]);
  }
  var p = e.parameter;
  sheet.appendRow([
    p.nombre || "",
    p.link   || "",
    p.contacto || "",
    p.tipo   || "",
    p.uso    || "",
    p.tema   || "",
    p.fecha  || ""
  ]);
  return ContentService.createTextOutput("ok")
         .setMimeType(ContentService.MimeType.TEXT);
}
```

4. Implementar → Nueva implementación → Aplicación web
5. Ejecutar como: **Yo** · Acceso: **Cualquier persona**
6. Copiar la URL → pegar en `APPS_SCRIPT_URL`

## SHEETS_CSV_URL

En tu Sheet: **Archivo → Compartir → Publicar en la web**
→ Selecciona la hoja "licencias" → CSV → Publicar
→ Copia el enlace → pegar en `SHEETS_CSV_URL`

## Columnas del Sheet

| Nombre | Link | Contacto | Tipo | Uso | Tema | Fecha |
|--------|------|----------|------|-----|------|-------|
