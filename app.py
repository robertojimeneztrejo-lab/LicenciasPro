import streamlit as st
import google.generativeai as genai
import json
import re
import io
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pypdf import PdfReader

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LicenceHunt",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');
:root{
    --navy:#0D2B4E;--navy-mid:#1A3F6F;--navy-light:#2E5FA3;
    --gold:#C8973A;--gold-light:#E8B84B;
    --surface:#F4F6F9;--white:#FFFFFF;
    --border:#C8D0DC;--border-light:#DDE3EC;
    --muted:#6B7A8D;--text:#3D4A5C;--bright:#0D2B4E;
    --green:#1A5232;--green-bg:#E8F5EE;--green-border:#A9D6BC;
    --red:#7B1E1E;--red-bg:#FBEAEA;--red-border:#E8AAAA;
    --gold-bg:#FDF3E3;--gold-text:#7D4E0F;--gold-border:#E8C88A;
    --accent-bg:#E8F0FA;--accent-border:#B8CEE8;
    /* alias para mantener el resto de la hoja sin tener que reescribirla */
    --ink:var(--surface);--ink2:var(--white);--card:var(--white);
    --teal:var(--navy-light);--teal-dk:var(--navy);
}
*,*::before,*::after{box-sizing:border-box;}
html,body,[data-testid="stAppViewContainer"]{background:var(--ink)!important;font-family:'DM Sans',sans-serif;color:var(--text);}
#MainMenu,footer,header{visibility:hidden;}[data-testid="stToolbar"]{display:none;}
.hero-wrap{position:relative;padding:2.8rem 3.5rem 2.2rem;margin-bottom:2rem;border-radius:20px;overflow:hidden;background:var(--card);border:1px solid var(--border);box-shadow:0 1px 6px rgba(13,43,78,.06);}
.hero-wrap::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 80% at 90% 20%,rgba(46,95,163,.07) 0%,transparent 60%),radial-gradient(ellipse 40% 60% at 10% 80%,rgba(200,151,58,.05) 0%,transparent 60%);pointer-events:none;}
.hero-tagline{font-family:'DM Sans',sans-serif;font-size:.72rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin:0 0 .9rem;}
.hero-title{font-family:'Syne',sans-serif;font-size:2.8rem;font-weight:800;line-height:1.05;color:var(--bright);margin:0 0 .7rem;letter-spacing:-.02em;}
.hero-title span{color:var(--gold);}
.hero-sub{color:var(--muted);font-size:.92rem;max-width:560px;line-height:1.65;}
.hero-stats{display:flex;gap:2rem;margin-top:1.8rem;}
.hero-stat-val{font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:var(--teal);}
.hero-stat-lbl{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;}
.section-title{font-family:'Syne',sans-serif;font-size:.65rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:.9rem;display:flex;align-items:center;gap:.6rem;}
.section-title::after{content:'';flex:1;height:1px;background:var(--border);}
.filter-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:1.5rem;margin-bottom:1.1rem;}
.stButton>button{background:linear-gradient(135deg,var(--navy),var(--navy-mid))!important;color:white!important;font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:.88rem!important;letter-spacing:.04em!important;border:none!important;border-radius:12px!important;padding:.72rem 2rem!important;transition:all .2s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(13,43,78,.22)!important;}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stSelectbox"]>div>div{background:var(--ink2)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--bright)!important;font-family:'DM Sans',sans-serif!important;}
[data-testid="stTextInput"] input:focus,[data-testid="stTextArea"] textarea:focus{border-color:var(--teal)!important;box-shadow:0 0 0 3px rgba(46,95,163,.15)!important;}
.side-stage{display:flex;flex-direction:column;gap:0;margin:.6rem 0 1.1rem;border-left:2px solid rgba(255,255,255,.18);padding-left:.9rem;}
.side-stage-item{position:relative;padding:.42rem 0;font-size:.74rem;font-weight:600;letter-spacing:.04em;color:#7E9AC0;transition:all .2s;}
.side-stage-item::before{content:'';position:absolute;left:-1.16rem;top:.62rem;width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.25);}
.side-stage-item.done{color:#9CC2E8;}
.side-stage-item.done::before{background:var(--navy-light);}
.side-stage-item.active{color:#FFFFFF;font-weight:700;}
.side-stage-item.active::before{background:var(--gold-light);box-shadow:0 0 0 3px rgba(232,184,75,.25);}
.rcard{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:1.5rem;margin-bottom:.9rem;position:relative;overflow:hidden;transition:border-color .2s,transform .15s,box-shadow .2s;box-shadow:0 1px 4px rgba(13,43,78,.05);}
.rcard:hover{border-color:var(--teal);transform:translateY(-1px);box-shadow:0 4px 16px rgba(13,43,78,.12);}
.rcard::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--gold),var(--navy-light));opacity:0;transition:opacity .2s;}
.rcard:hover::before{opacity:1;}
.rcard-num{position:absolute;top:1.3rem;right:1.3rem;font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:var(--border);line-height:1;}
.rcard-badges{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:.75rem;}
.badge{display:inline-flex;align-items:center;gap:.3rem;font-size:.66rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:.2rem .6rem;border-radius:6px;}
.badge-teal{background:var(--accent-bg);color:var(--navy-light);border:1px solid var(--accent-border);}
.badge-gold{background:var(--gold-bg);color:var(--gold-text);border:1px solid var(--gold-border);}
.badge-green{background:var(--green-bg);color:var(--green);border:1px solid var(--green-border);}
.badge-red{background:var(--red-bg);color:var(--red);border:1px solid var(--red-border);}
.badge-saved{background:var(--green-bg);color:var(--green);border:1px solid var(--green-border);}
.rcard-name{font-family:'Syne',sans-serif;font-size:1.25rem;font-weight:700;color:var(--bright);margin-bottom:.22rem;}
.rcard-url{font-size:.78rem;color:var(--navy-light);margin-bottom:1rem;word-break:break-all;}
.rcard-grid{display:grid;grid-template-columns:1fr 1fr;gap:.9rem;}
.rcard-field-lbl{font-size:.66rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.28rem;}
.rcard-field-val{font-size:.84rem;color:var(--text);line-height:1.55;}
.block-hdr{display:flex;align-items:center;gap:.8rem;margin:1.8rem 0 1rem;}
.block-num-badge{font-family:'Syne',sans-serif;font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;background:var(--accent-bg);border:1px solid var(--accent-border);color:var(--navy);padding:.28rem .75rem;border-radius:8px;}
.block-range{font-size:.8rem;color:var(--muted);}
.more-block{background:linear-gradient(135deg,rgba(46,95,163,.05),rgba(200,151,58,.05));border:1px dashed var(--accent-border);border-radius:16px;padding:1.8rem;text-align:center;margin:1.4rem 0;}
.more-title{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:var(--bright);margin-bottom:.35rem;}
.more-sub{font-size:.82rem;color:var(--muted);margin-bottom:1.1rem;}
.fb-box{background:var(--gold-bg);border:1px solid var(--gold-border);border-left:3px solid var(--gold);border-radius:0 12px 12px 0;padding:1.1rem 1.4rem;margin:1.1rem 0;}
.fb-title{font-family:'Syne',sans-serif;font-size:.66rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-text);margin-bottom:.45rem;}
.fb-body{font-size:.86rem;color:var(--text);line-height:1.6;}
.status-box{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--teal);border-radius:0 10px 10px 0;padding:.85rem 1.1rem;font-size:.86rem;color:var(--muted);margin:.7rem 0;}
.ok-box{background:var(--green-bg);border:1px solid var(--green-border);border-left:3px solid var(--green);border-radius:0 10px 10px 0;padding:.85rem 1.1rem;font-size:.86rem;color:var(--text);margin:.7rem 0;}
.save-block{background:var(--green-bg);border:1px solid var(--green-border);border-radius:14px;padding:1.2rem 1.5rem;margin:1rem 0;display:flex;align-items:center;gap:1rem;flex-wrap:wrap;}
.save-info{flex:1;font-size:.84rem;color:var(--text);line-height:1.5;}
.save-info strong{color:var(--green);}
.div{height:1px;background:var(--border);margin:1.6rem 0;}
[data-testid="stMetric"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:12px!important;padding:1rem!important;}
[data-testid="stMetricValue"]{color:var(--navy)!important;font-family:'Syne',sans-serif!important;font-weight:700!important;}
[data-testid="stMetricLabel"]{color:var(--muted)!important;font-size:.7rem!important;}
[data-testid="stExpander"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:12px!important;}
[data-testid="stMultiSelect"]>div{background:var(--white)!important;border-color:var(--border)!important;border-radius:10px!important;}
span[data-baseweb="tag"]{background:var(--accent-bg)!important;border:1px solid var(--accent-border)!important;color:var(--navy)!important;}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-track{background:var(--ink);}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}

/* ── Sidebar oscuro (navy + dorado), estilo ARIA Membresías ──────────── */
[data-testid="stSidebar"]{background:linear-gradient(180deg,var(--navy) 0%,#0A2240 100%)!important;border-right:3px solid var(--gold)!important;}
[data-testid="stSidebar"] *{color:#C8D8EC!important;}
[data-testid="stSidebar"] h3{color:var(--gold-light)!important;font-size:.78rem!important;letter-spacing:.1em!important;text-transform:uppercase!important;}
[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.12)!important;}
[data-testid="stSidebar"] [data-testid="stMetric"]{background:rgba(255,255,255,.06)!important;border:1px solid rgba(232,184,75,.25)!important;}
[data-testid="stSidebar"] [data-testid="stMetricValue"]{color:var(--gold-light)!important;}
[data-testid="stSidebar"] [data-testid="stMetricLabel"]{color:#9CB6D2!important;}
[data-testid="stSidebar"] [data-testid="stMultiSelect"] *{color:var(--navy)!important;}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────

VALIDATION_TYPES = {
    "form_manual": ("📋", "Formulario + aprobación manual",         "Llena un form; un humano aprueba"),
    "email_edu":   ("📧", "Correo .edu (USA/internacional)",        "Verificación con dominio .edu"),
    "email_uni":   ("🏫", "Correo universitario cualquier dominio", "Acepta .edu.mx, .edu.co, .ac.uk, etc."),
    "documento":   ("📄", "Verificación con documento",             "Credencial, constancia o carta institucional"),
    "grant":       ("🏆", "Grant / propuesta de investigación",     "Propuesta formal para aprobación"),
    "contacto":    ("📞", "Contacto directo con el equipo",         "Email a sales/support para solicitar acceso"),
}

DEPTH_LEVELS = {
    "startup":   ("🌱", "Startups / Beta",      "Herramientas en fase temprana, < 2 años"),
    "nicho":     ("🔬", "Nicho / Especializado", "Muy específicas, bajo volumen de búsqueda"),
    "emergente": ("📡", "Emergente general",     "Poco conocidas, no en top 5 Google"),
    "todas":     ("🌐", "Todas las capas",       "Sin restricción de popularidad"),
}

BENEFICIARY_TYPES = {
    "estudiantes":    "Estudiantes universitarios",
    "profesores":     "Profesores / Docentes",
    "investigadores": "Investigadores",
    "universidades":  "Instituciones / Universidades",
}

# ─── GOOGLE SHEETS (Apps Script bridge) ──────────────────────────────────────

def get_sheets_config():
    """Lee la URL del Apps Script y la URL pública del CSV desde st.secrets."""
    try:
        script_url = st.secrets["APPS_SCRIPT_URL"]
        csv_url    = st.secrets.get("SHEETS_CSV_URL", "")
        return script_url, csv_url
    except Exception:
        return "", ""

@st.cache_data(ttl=120)
def load_saved_names(csv_url: str) -> list:
    """Carga los nombres ya guardados en el Sheet (para deduplicación)."""
    if not csv_url:
        return []
    try:
        req = urllib.request.Request(csv_url,
              headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            content = r.read().decode("utf-8")
        names = []
        for line in content.strip().split("\n")[1:]:  # skip header
            if line.strip():
                parts = line.split(",")
                if parts:
                    name = parts[0].strip().strip('"')
                    if name:
                        names.append(name)
        return names
    except Exception:
        return []

def save_block_to_sheets(script_url: str, items: list, tema: str) -> tuple:
    """
    Guarda una lista de herramientas en Google Sheets via Apps Script doGet.
    Columnas: Nombre | Link | Contacto | Tipo | Uso | Tema | Fecha
    Returns (ok: bool, message: str)
    """
    if not script_url:
        return False, "No se encontró APPS_SCRIPT_URL en Secrets."

    saved = 0
    errors = []
    fecha = datetime.now().strftime("%Y-%m-%d")

    for item in items:
        val_key  = item.get("tipo_validacion_key", "")
        val_name = VALIDATION_TYPES.get(val_key, ("", "Sin clasificar", ""))[1]

        row_data = {
            "nombre":   item.get("nombre", ""),
            "link":     item.get("url", ""),
            "contacto": item.get("url_educativa", "") or item.get("tipo_validacion", "")[:120],
            "tipo":     val_name,
            "uso":      item.get("casos_uso", "")[:200],
            "tema":     tema,
            "fecha":    fecha,
        }

        params   = urllib.parse.urlencode(row_data)
        full_url = f"{script_url}?{params}"

        try:
            req = urllib.request.Request(full_url,
                  headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8")
                if "ok" in body.lower() or "success" in body.lower() or resp.status == 200:
                    saved += 1
                else:
                    errors.append(item.get("nombre","?"))
        except Exception as e:
            errors.append(f"{item.get('nombre','?')} ({str(e)[:40]})")

    if saved == len(items):
        return True, f"✅ {saved} herramientas guardadas en Google Sheets."
    elif saved > 0:
        return True, f"⚠️ {saved} de {len(items)} guardadas. Falló: {', '.join(errors[:3])}"
    else:
        return False, f"❌ Error al guardar. Verifica la URL del Apps Script."

# ─── URL VERIFIER ─────────────────────────────────────────────────────────────

def verify_url(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD",
              headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status < 400
    except Exception:
        try:
            req2 = urllib.request.Request(url, method="GET",
                   headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req2, timeout=5) as r:
                return r.status < 400
        except Exception:
            return False

def verify_results(results: list) -> list:
    for item in results:
        url = item.get("url", "")
        item["url_verified"] = verify_url(url) if url else False
    return results

# ─── GEMINI ───────────────────────────────────────────────────────────────────

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return ""

def get_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction="""Eres un analista de software experto en licencias académicas.
Solo incluye herramientas que EXISTEN REALMENTE. Responde ÚNICAMENTE en JSON puro sin bloques de código."""
    )

def call_gemini(model, prompt, retries=3):
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            return json.loads(text)
        except json.JSONDecodeError:
            if attempt == retries - 1:
                return {"error": "JSON inválido"}
        except Exception as e:
            if attempt == retries - 1:
                return {"error": str(e)}
            time.sleep(2 ** attempt)
    return {"error": "Sin respuesta"}

# ─── DOSSIER PDF → TEMAS CLAVE ────────────────────────────────────────────────

def extract_topics_from_pdf(pdf_file, api_key, max_chars=6000):
    """
    Extrae texto del PDF (priorizando secciones de temario/plan de estudios si existen)
    y usa una llamada a Gemini para identificar 3-6 temas/áreas clave de búsqueda.
    Funciona con dossiers institucionales, temarios de asignaturas o planes de estudio
    que listan áreas de conocimiento relevantes para encontrar software académico.
    Devuelve (lista_de_temas, None) en éxito, o (None, mensaje_error) en fallo.
    """
    try:
        reader = PdfReader(pdf_file)
        all_pages_text = []
        for page in reader.pages:
            all_pages_text.append(page.extract_text() or "")

        full_doc = " ".join(all_pages_text)
        full_doc = re.sub(r"\s+", " ", full_doc).strip()

        if len(full_doc) < 50:
            return None, "El PDF no contiene texto extraíble (puede ser un escaneo de imagen sin OCR)."

        keywords_priority = ["asignatura", "plan de estudio", "temario", "contenido",
                              "índice", "syllabus", "módulo", "unidad", "curso", "software", "herramienta"]
        priority_text = ""
        other_text = ""
        for page_text in all_pages_text:
            low = page_text.lower()
            if any(k in low for k in keywords_priority):
                priority_text += " " + page_text
            else:
                other_text += " " + page_text

        combined = re.sub(r"\s+", " ", priority_text).strip()
        if len(combined) < max_chars:
            filler = re.sub(r"\s+", " ", other_text).strip()
            combined = (combined + " " + filler)[:max_chars]
        else:
            combined = combined[:max_chars]

        if not api_key:
            return None, "No hay GEMINI_API_KEY configurada en los Secrets."

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        mini_prompt = f"""Lee el siguiente fragmento de un documento (puede ser un dossier institucional, un plan de estudios, un temario de asignaturas o un programa académico).

Identifica entre 3 y 6 TEMAS O ÁREAS DE CONOCIMIENTO clave que mejor representen el contenido técnico o académico del documento. Estos temas se usarán para buscar software con licencias académicas relacionado, así que deben ser específicos y útiles como término de búsqueda (ej: "diseño CAD", "simulación clínica", "análisis estadístico avanzado", "modelado financiero"), no genéricos como "educación" o "tecnología".

Responde ÚNICAMENTE con un array JSON de strings, sin texto adicional ni bloques de código. Ejemplo de formato: ["tema 1", "tema 2", "tema 3"]

Fragmento del documento:
{combined}

Temas clave:"""

        try:
            response = model.generate_content(
                mini_prompt,
                generation_config=genai.types.GenerationConfig(temperature=0.2, max_output_tokens=800)
            )
        except Exception as api_err:
            return None, f"Error al llamar a Gemini: {str(api_err)}"

        try:
            raw = response.text.strip()
        except Exception:
            finish_reason = None
            try:
                finish_reason = response.candidates[0].finish_reason
            except Exception:
                pass
            return None, f"Gemini no devolvió texto utilizable (finish_reason={finish_reason}). Puede ser un bloqueo de seguridad o respuesta vacía."

        raw_clean = re.sub(r"```json", "", raw)
        raw_clean = re.sub(r"```", "", raw_clean).strip()

        try:
            topics = json.loads(raw_clean)
            if isinstance(topics, list) and topics:
                return [str(t).strip() for t in topics if str(t).strip()], None
        except json.JSONDecodeError:
            match = re.search(r"\[.*\]", raw_clean, re.DOTALL)
            if match:
                try:
                    topics = json.loads(match.group())
                    if isinstance(topics, list) and topics:
                        return [str(t).strip() for t in topics if str(t).strip()], None
                except json.JSONDecodeError:
                    pass

            rescued = re.findall(r'"([^"]+)"', raw_clean)
            if rescued:
                return [s.strip() for s in rescued if s.strip()], None

        return None, f"Gemini respondió pero no en formato JSON esperado. Respuesta cruda: {raw[:300]}"

    except Exception as ex:
        return None, f"Error inesperado procesando el PDF: {str(ex)}"

# ─── PROMPTS ─────────────────────────────────────────────────────────────────

def build_prompt(tema, val_types, beneficiarios, depth, cantidad, num_inicio, historial, pdf_topics=None):
    val_desc  = "\n".join([f"  - {VALIDATION_TYPES[v][1]}: {VALIDATION_TYPES[v][2]}" for v in val_types])
    ben_desc  = ", ".join([BENEFICIARY_TYPES[b] for b in beneficiarios])
    depth_desc = DEPTH_LEVELS[depth][2]
    hist_str  = (f"\nNO repetir estas herramientas ya encontradas: {json.dumps(historial, ensure_ascii=False)}"
                 if historial else "")

    pdf_topics_block = ""
    if pdf_topics:
        ordered_list = "\n".join(f"{i+1}. {t}" for i, t in enumerate(pdf_topics))
        pdf_topics_block = f"""
TEMAS DETECTADOS EN EL DOCUMENTO CARGADO (orden de prioridad, el primero pesa más):
{ordered_list}
Usa estos temas como ejes principales de búsqueda, en el orden indicado. El tema #1 debe dominar la mayoría de los resultados; los siguientes se usan para diversificar si el primero no genera suficientes coincidencias. Trátalos con el mismo peso que el tema de búsqueda escrito por el usuario, combinándolos si es necesario.
"""

    return f"""Busca {cantidad} herramientas digitales reales para el área de "{tema}".
{pdf_topics_block}
FILTROS OBLIGATORIOS:
1. De PAGO para el público general.
2. COMPLETAMENTE GRATUITAS (no descuento) para: {ben_desc}
3. Acceso gratuito solo mediante: {val_desc}
4. Popularidad: {depth_desc}
5. NO incluir: Open Source, 100% gratuitas para todos, Adobe, Microsoft, Google, Apple, Autodesk, JetBrains, Notion, Canva.
6. EXCLUIR si solo ofrecen descuento — debe ser gratuito total.
7. EXCLUIR si requiere que la institución haya pagado primero.
{hist_str}

Devuelve JSON con este formato exacto:
{{"tema":"{tema}","lista":[{{"numero":{num_inicio},"nombre":"...","url":"...","url_educativa":"...","categoria":"...","precio_publico":"...","beneficiarios":"...","tipo_validacion":"...","tipo_validacion_key":"[form_manual|email_edu|email_uni|documento|grant|contacto]","razon_emergente":"...","casos_uso":"..."}}]}}"""

CORRECCION_PROMPT = """Resultados anteriores: {resultados}
Instrucciones: "{instrucciones}"
Tema: {tema}
Aplica las correcciones. Mismo número de herramientas. Mismo formato JSON.
{{"tema":"{tema}","lista":[{{"numero":1,"nombre":"...","url":"...","url_educativa":"...","categoria":"...","precio_publico":"...","beneficiarios":"...","tipo_validacion":"...","tipo_validacion_key":"...","razon_emergente":"...","casos_uso":"..."}}]}}"""

# ─── UI HELPERS ───────────────────────────────────────────────────────────────

def render_hero(total=0, bloques=0, guardadas=0):
    st.markdown(f"""
    <div class="hero-wrap">
        <h1 class="hero-title">ARIA <span>Licencias</span></h1>
        <p class="hero-tagline">Alliance Recognition &amp; Intelligence Architecture</p>
        <p class="hero-sub">Buscador de softwares con alto impacto en el desarrollo de la comunidad universitaria
        — filtrado por tipo de validación, beneficiario y profundidad de búsqueda.</p>
        <div class="hero-stats">
            <div><div class="hero-stat-val">{total}</div><div class="hero-stat-lbl">Encontradas</div></div>
            <div><div class="hero-stat-val">{bloques}</div><div class="hero-stat-lbl">Bloques</div></div>
            <div><div class="hero-stat-val">{guardadas}</div><div class="hero-stat-lbl">Guardadas en Sheets</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_side_stage(active):
    stages = ["1. Filtros", "2. Revisión", "3. Corrección", "4. Resultados"]
    items = ""
    for i, s in enumerate(stages):
        cls = "done" if i < active else ("active" if i == active else "")
        icon = "✓ " if i < active else ("▸ " if i == active else "")
        items += f'<div class="side-stage-item {cls}">{icon}{s}</div>'
    st.markdown(f'<div class="side-stage">{items}</div>', unsafe_allow_html=True)

def render_result_card(item):
    num     = item.get("numero", "?")
    nombre  = item.get("nombre", "")
    url     = item.get("url", "")
    url_edu = item.get("url_educativa", "")
    cat     = item.get("categoria", "")
    precio  = item.get("precio_publico", "")
    ben     = item.get("beneficiarios", "")
    val     = item.get("tipo_validacion", "")
    val_key = item.get("tipo_validacion_key", "")
    emer    = item.get("razon_emergente", "")
    casos   = item.get("casos_uso", "")
    verified = item.get("url_verified", None)
    saved    = item.get("saved_to_sheets", False)

    val_icon = VALIDATION_TYPES.get(val_key, ("🔹", "", ""))[0]
    val_name = VALIDATION_TYPES.get(val_key, ("", "Sin clasificar", ""))[1]

    ver_badge  = '<span class="badge badge-green">✅ URL ok</span>' if verified is True else \
                 '<span class="badge badge-red">⚠️ No confirmada</span>' if verified is False else ""
    save_badge = '<span class="badge badge-saved">💾 Guardada</span>' if saved else ""

    url_edu_html = (f'<div><div class="rcard-field-lbl">🔗 URL Educativa</div>'
                    f'<div class="rcard-field-val"><a href="{url_edu}" style="color:var(--teal)">{url_edu}</a></div></div>'
                    if url_edu else "<div></div>")

    num_fmt = f"{num:02d}" if isinstance(num, int) else str(num)

    st.markdown(f"""
    <div class="rcard">
        <div class="rcard-num">{num_fmt}</div>
        <div class="rcard-badges">
            <span class="badge badge-teal">{val_icon} {val_name}</span>
            <span class="badge badge-gold">💰 De pago</span>
            {ver_badge}{save_badge}
        </div>
        <div class="rcard-name">{nombre}</div>
        <div class="rcard-url">🔗 {url}</div>
        <div class="rcard-grid">
            <div><div class="rcard-field-lbl">📋 Categoría</div><div class="rcard-field-val">{cat}</div></div>
            <div><div class="rcard-field-lbl">💰 Precio Público</div><div class="rcard-field-val">{precio}</div></div>
            <div><div class="rcard-field-lbl">👥 Beneficiarios</div><div class="rcard-field-val">{ben}</div></div>
            {url_edu_html}
        </div>
        <div style="margin-top:.9rem">
            <div class="rcard-field-lbl">🎓 Proceso de Acceso Educativo</div>
            <div class="rcard-field-val">{val}</div>
        </div>
        <div style="margin-top:.7rem">
            <div class="rcard-field-lbl">🔍 Por qué es poco conocida</div>
            <div class="rcard-field-val">{emer}</div>
        </div>
        <div style="margin-top:.7rem">
            <div class="rcard-field-lbl">🏛️ Casos de uso</div>
            <div class="rcard-field-val">{casos}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_block_header(b, start, end):
    st.markdown(f"""
    <div class="block-hdr">
        <div class="block-num-badge">Bloque {b}</div>
        <span class="block-range">#{start} — #{end}</span>
    </div>""", unsafe_allow_html=True)

# ─── MAIN ────────────────────────────────────────────────────────────────────

DEFAULTS = {
    "fase":              "filtros",
    "all_results":       [],
    "bloque_num":        0,
    "tema":              "",
    "cantidad":          10,
    "val_types":         ["form_manual", "documento", "contacto"],
    "beneficiarios":     ["estudiantes", "profesores"],
    "depth":             "emergente",
    "search_result":     None,
    "corrected":         False,
    "historial_nombres": [],
    "total_guardadas":   0,
    "saved_blocks":      set(),   # set of block indices already saved
    "verify_toggle":     True,
    "pdf_topics_hidden": None,
    "trigger_pdf_search": False,
}

SIDEBAR_WIDGET_KEYS = {"val_types", "beneficiarios", "depth", "verify_toggle"}

def main():
    # ── Init ─────────────────────────────────────────────────────────────
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v if not isinstance(v, set) else set()

    # Si se solicitó un reset, aplicarlo aquí (antes de crear los widgets
    # del sidebar) para no chocar con la restricción de Streamlit de no
    # modificar session_state de un widget ya instanciado en el mismo run.
    if st.session_state.get("_reset_filters"):
        for k in SIDEBAR_WIDGET_KEYS:
            st.session_state[k] = DEFAULTS[k] if not isinstance(DEFAULTS[k], set) else set()
        st.session_state["_reset_filters"] = False

    api_key                = get_api_key()
    script_url, csv_url    = get_sheets_config()
    total   = len(st.session_state.all_results)
    bloques = st.session_state.bloque_num
    guardadas = st.session_state.total_guardadas

    # Mapeo de fase -> índice activo en el indicador de pasos
    stage_idx = {"filtros": 0, "revision": 1, "resultados": 3}.get(st.session_state.fase, 0)

    render_hero(total, bloques, guardadas)

    # Sidebar — siempre visible, con pasos + todos los filtros (estilo Pro Membresías)
    with st.sidebar:
        st.markdown("### 🎓 LicenceHunt")
        render_side_stage(stage_idx)
        st.markdown("---")

        if total:
            verified = sum(1 for r in st.session_state.all_results if r.get("url_verified") is True)
            st.metric("Encontradas", total)
            st.metric("Verificadas ✅", verified)
            st.metric("Guardadas en Sheets", guardadas)
            st.markdown("---")

        st.markdown("### 👥 Beneficiarios")
        ben_sel = st.multiselect("beneficiarios", label_visibility="collapsed",
            options=list(BENEFICIARY_TYPES.keys()),
            format_func=lambda x: BENEFICIARY_TYPES[x],
            key="beneficiarios")

        st.markdown("---")
        st.markdown("### 🎓 Tipo de validación académica")
        val_sel = st.multiselect("validacion", label_visibility="collapsed",
            options=list(VALIDATION_TYPES.keys()),
            format_func=lambda x: f"{VALIDATION_TYPES[x][0]} {VALIDATION_TYPES[x][1]}",
            key="val_types")
        for k in list(VALIDATION_TYPES.keys()):
            icon, name, desc = VALIDATION_TYPES[k]
            sel = k in (val_sel or [])
            st.markdown(
                f'<div style="font-size:.72rem;color:{"#E8B84B" if sel else "#7E9AC0"}!important;'
                f'padding:.1rem 0 .1rem .5rem;border-left:2px solid {"#E8B84B" if sel else "rgba(255,255,255,.18)"};'
                f'margin-bottom:.25rem">{icon} <strong>{name}</strong> — {desc}</div>',
                unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔬 Profundidad de búsqueda")
        depth_options = list(DEPTH_LEVELS.keys())
        depth_sel = st.radio("depth", label_visibility="collapsed",
            options=depth_options,
            format_func=lambda x: f"{DEPTH_LEVELS[x][0]} {DEPTH_LEVELS[x][1]} — {DEPTH_LEVELS[x][2]}",
            key="depth")

        st.markdown("---")
        st.markdown("### ⚙️ Opciones adicionales")
        verify_toggle = st.checkbox("✅ Verificar URLs automáticamente", key="verify_toggle")

        st.markdown("---")
        if not script_url:
            st.warning("⚠️ Falta APPS_SCRIPT_URL en Secrets")
        st.markdown("<small style='color:#7E9AC0'>LicenceHunt v2.0<br>Gemini 2.5 Flash</small>",
                    unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # FASE 1: FILTROS
    # ═══════════════════════════════════════════════════════════════════════
    if st.session_state.fase == "filtros":
        # Cargar historial del Sheet
        saved_in_sheets = []
        if csv_url:
            saved_in_sheets = load_saved_names(csv_url)
            if saved_in_sheets:
                st.markdown(
                    f'<div class="ok-box">📋 Google Sheets conectado — '
                    f'<strong>{len(saved_in_sheets)} herramientas</strong> ya guardadas serán excluidas automáticamente.</div>',
                    unsafe_allow_html=True)

        st.markdown('<div class="section-title">Tema de búsqueda</div>', unsafe_allow_html=True)
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        col_t, col_c = st.columns([3, 1])
        with col_t:
            tema_input = st.text_input("tema", label_visibility="collapsed",
                placeholder="Ej: Enfermería, Arquitectura, Diseño Gráfico, Derecho...",
                value=st.session_state.tema)
        with col_c:
            cantidad_input = st.selectbox("cant", label_visibility="collapsed",
                options=[5, 10, 15, 20],
                index=[5,10,15,20].index(st.session_state.cantidad)
                      if st.session_state.cantidad in [5,10,15,20] else 1)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔍 Buscar Licencias Académicas a partir de Tema de Búsqueda", use_container_width=True) or st.session_state.get("trigger_pdf_search"):
            st.session_state.trigger_pdf_search = False
            if not tema_input.strip():
                st.error("⚠️ Ingresa un tema de búsqueda."); return
            if not val_sel:
                st.error("⚠️ Selecciona al menos un tipo de validación."); return
            if not ben_sel:
                st.error("⚠️ Selecciona al menos un beneficiario."); return
            if not api_key:
                st.error("⚠️ No se encontró GEMINI_API_KEY en Secrets."); return

            st.session_state.tema          = tema_input.strip()
            st.session_state.cantidad      = cantidad_input
            st.session_state.all_results   = []
            st.session_state.bloque_num    = 0
            st.session_state.corrected     = False
            st.session_state.saved_blocks  = set()
            st.session_state.total_guardadas = 0
            # Seed historial from Sheet
            st.session_state.historial_nombres = list(saved_in_sheets)

            model = get_model(api_key)
            with st.spinner("⚙️ Buscando herramientas..."):
                result = call_gemini(model, build_prompt(
                    tema=st.session_state.tema,
                    val_types=val_sel, beneficiarios=ben_sel,
                    depth=depth_sel, cantidad=5,
                    num_inicio=1, historial=st.session_state.historial_nombres,
                    pdf_topics=st.session_state.get("pdf_topics_hidden"),
                ))
            if "error" in result:
                st.error(f"Error: {result['error']}"); return

            st.session_state.search_result = result
            st.session_state.fase = "revision"
            st.rerun()

        with st.expander("📄 O cargar un dossier o temario en PDF para iniciar la búsqueda automáticamente"):
            pdf_file = st.file_uploader(
                "Sube un dossier institucional, temario de asignaturas o plan de estudios (PDF)",
                type=["pdf"],
                key="pdf_dossier_uploader",
                help="Se extrae solo el texto (sin imágenes) para detectar temas de búsqueda — no se envía el PDF completo a Gemini"
            )
            if pdf_file is not None:
                if st.button("🔎 Analizar Dossier y buscar", key="detect_topic_btn", use_container_width=True):
                    with st.spinner("Analizando el documento..."):
                        detected_topics, error_msg = extract_topics_from_pdf(pdf_file, api_key)
                    if detected_topics:
                        st.session_state.pdf_topics_hidden = detected_topics
                        st.session_state.tema = detected_topics[0]
                        st.session_state.trigger_pdf_search = True
                        st.rerun()
                    else:
                        st.error(f"No se pudieron identificar temas: {error_msg}")
        return

    # ═══════════════════════════════════════════════════════════════════════
    # FASE 2: REVISIÓN + CORRECCIÓN
    # ═══════════════════════════════════════════════════════════════════════
    if st.session_state.fase == "revision":
        model = get_model(api_key)
        lista_preview = st.session_state.search_result.get("lista", [])

        st.markdown('<div class="section-title">Pre-selección — revisa antes de continuar</div>',
                    unsafe_allow_html=True)
        with st.expander(f"✅ {len(lista_preview)} herramientas pre-seleccionadas", expanded=True):
            for h in lista_preview:
                vk = h.get("tipo_validacion_key","")
                icon = VALIDATION_TYPES.get(vk, ("🔹","",""))[0]
                vname = VALIDATION_TYPES.get(vk, ("","Sin clasificar",""))[1]
                st.markdown(f"**{h.get('nombre','')}** — `{h.get('url','')}`")
                c1, c2, c3 = st.columns(3)
                c1.caption(f"💰 {h.get('precio_publico','')}")
                c2.caption(f"{icon} {vname}")
                c3.caption(f"👥 {h.get('beneficiarios','')}")
                st.markdown("---")

        st.markdown("""<div class="fb-box">
            <div class="fb-title">✏️ Corrección opcional</div>
            <div class="fb-body">¿Alguna herramienta no cumple los filtros? Escríbelo abajo.
            Si todo está correcto, déjalo vacío y haz clic en <strong>Continuar</strong>.</div>
        </div>""", unsafe_allow_html=True)

        instrucciones = st.text_area("correcciones", label_visibility="collapsed",
            placeholder='Ej: "Elimina la herramienta X porque solo da descuento. Busca una de simulación clínica."',
            height=95, key="corr_text")

        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_a:
            if st.button("✏️ Aplicar Corrección", use_container_width=True,
                         disabled=not instrucciones.strip(), key="btn_corr"):
                with st.spinner("Corrigiendo..."):
                    rc = call_gemini(model, CORRECCION_PROMPT.format(
                        resultados=json.dumps(lista_preview, ensure_ascii=False),
                        instrucciones=instrucciones.strip(),
                        tema=st.session_state.tema,
                    ))
                if "error" in rc:
                    st.error(f"Error: {rc['error']}")
                else:
                    st.session_state.search_result = rc
                    st.session_state.corrected = True
                    st.rerun()

        with col_b:
            if st.button("▶ Continuar y generar lista", use_container_width=True, key="btn_cont"):
                hist = [h.get("nombre","") for h in lista_preview] + st.session_state.historial_nombres
                with st.spinner(f"Generando {st.session_state.cantidad} herramientas..."):
                    rf = call_gemini(model, build_prompt(
                        tema=st.session_state.tema,
                        val_types=st.session_state.val_types,
                        beneficiarios=st.session_state.beneficiarios,
                        depth=st.session_state.depth,
                        cantidad=st.session_state.cantidad,
                        num_inicio=1, historial=hist,
                        pdf_topics=st.session_state.get("pdf_topics_hidden"),
                    ))
                if "error" in rf:
                    st.error(f"Error: {rf['error']}"); return

                lista = rf.get("lista", [])
                for i, item in enumerate(lista):
                    item["numero"] = i + 1
                    item["saved_to_sheets"] = False

                if st.session_state.get("verify_toggle", True):
                    with st.spinner("✅ Verificando URLs..."):
                        lista = verify_results(lista)

                st.session_state.all_results  = lista
                st.session_state.bloque_num   = 1
                st.session_state.historial_nombres = hist + [h.get("nombre","") for h in lista]
                st.session_state.fase = "resultados"
                st.rerun()

        with col_c:
            if st.button("← Volver a filtros", use_container_width=True, key="btn_back"):
                st.session_state.fase = "filtros"; st.rerun()
        return

    # ═══════════════════════════════════════════════════════════════════════
    # FASE 3: RESULTADOS
    # ═══════════════════════════════════════════════════════════════════════
    if st.session_state.fase == "resultados":
        model      = get_model(api_key)
        all_results= st.session_state.all_results
        cantidad   = st.session_state.cantidad
        tema       = st.session_state.tema

        verified_count = sum(1 for r in all_results if r.get("url_verified") is True)
        unverified     = sum(1 for r in all_results if r.get("url_verified") is False)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total encontradas",   len(all_results))
        m2.metric("Bloques generados",   st.session_state.bloque_num)
        m3.metric("URLs verificadas ✅",  verified_count)
        m4.metric("Guardadas en Sheets", st.session_state.total_guardadas)

        if st.session_state.corrected:
            st.markdown('<div class="ok-box">🔧 Lista generada con correcciones aplicadas.</div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="div"></div>', unsafe_allow_html=True)

        end_num = 0
        for b in range(st.session_state.bloque_num):
            bloque_items = all_results[b * cantidad: (b+1) * cantidad]
            if not bloque_items:
                continue
            start_n = bloque_items[0].get("numero", b * cantidad + 1)
            end_n   = bloque_items[-1].get("numero", (b+1) * cantidad)
            end_num = end_n

            render_block_header(b + 1, start_n, end_n)

            for item in bloque_items:
                render_result_card(item)

            # ── GUARDAR BLOQUE EN SHEETS ──────────────────────────────────
            already_saved = b in st.session_state.saved_blocks
            if already_saved:
                st.markdown(
                    '<div class="save-block"><span style="color:var(--green);font-size:.9rem">💾</span>'
                    '<div class="save-info"><strong>Bloque guardado en Google Sheets.</strong> '
                    'Las herramientas de este bloque no se repetirán en búsquedas futuras.</div></div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="save-block">
                    <div class="save-info">
                        <strong>Guardar Bloque {b+1} en Google Sheets</strong><br>
                        Columnas: Nombre · Link · Contacto · Tipo · Uso · Tema · Fecha
                    </div>
                </div>""", unsafe_allow_html=True)

                if st.button(f"💾 Guardar Bloque {b+1} en Google Sheets",
                             key=f"save_b{b}", use_container_width=False):
                    if not script_url:
                        st.error("⚠️ Falta APPS_SCRIPT_URL en Secrets.")
                    else:
                        with st.spinner("Guardando en Google Sheets..."):
                            ok, msg = save_block_to_sheets(script_url, bloque_items, tema)
                        if ok:
                            # Mark items as saved
                            for item in bloque_items:
                                item["saved_to_sheets"] = True
                            st.session_state.saved_blocks.add(b)
                            st.session_state.total_guardadas += len(bloque_items)
                            st.success(msg)
                            # Invalidate cache so next search reads updated sheet
                            load_saved_names.clear()
                            st.rerun()
                        else:
                            st.error(msg)

            if b < st.session_state.bloque_num - 1:
                st.markdown('<div class="div"></div>', unsafe_allow_html=True)

        # ── MÁS BLOQUES ──────────────────────────────────────────────────
        st.markdown('<div class="div"></div>', unsafe_allow_html=True)
        next_b     = st.session_state.bloque_num + 1
        next_start = end_num + 1
        next_end   = next_start + cantidad - 1

        st.markdown(f"""<div class="more-block">
            <div class="more-title">¿Más herramientas?</div>
            <div class="more-sub">Bloque {next_b} — #{next_start} al #{next_end} · sin perder el historial</div>
        </div>""", unsafe_allow_html=True)

        col_mas, col_nueva = st.columns(2)
        with col_mas:
            if st.button(f"＋ Buscar {cantidad} más (Bloque {next_b})",
                         use_container_width=True, key=f"btn_more_{st.session_state.bloque_num}"):
                with st.spinner(f"Generando Bloque {next_b}..."):
                    rm = call_gemini(model, build_prompt(
                        tema=tema,
                        val_types=st.session_state.val_types,
                        beneficiarios=st.session_state.beneficiarios,
                        depth=st.session_state.depth,
                        cantidad=cantidad, num_inicio=next_start,
                        historial=st.session_state.historial_nombres,
                        pdf_topics=st.session_state.get("pdf_topics_hidden"),
                    ))
                if "error" in rm:
                    st.error(f"Error: {rm['error']}")
                else:
                    lista_mas = rm.get("lista", [])
                    for i, item in enumerate(lista_mas):
                        item["numero"] = next_start + i
                        item["saved_to_sheets"] = False
                    if st.session_state.get("verify_toggle", True):
                        with st.spinner("✅ Verificando URLs..."):
                            lista_mas = verify_results(lista_mas)
                    nuevos = [h.get("nombre","") for h in lista_mas]
                    st.session_state.all_results.extend(lista_mas)
                    st.session_state.historial_nombres.extend(nuevos)
                    st.session_state.bloque_num += 1
                    st.rerun()

        with col_nueva:
            if st.button("🔄 Nueva búsqueda", use_container_width=True, key="btn_nueva"):
                for k, v in DEFAULTS.items():
                    if k in SIDEBAR_WIDGET_KEYS:
                        continue  # se resetean en el próximo run (ver _reset_filters)
                    st.session_state[k] = v if not isinstance(v, set) else set()
                st.session_state["_reset_filters"] = True
                st.session_state.fase = "filtros"
                st.rerun()


if __name__ == "__main__":
    main()
