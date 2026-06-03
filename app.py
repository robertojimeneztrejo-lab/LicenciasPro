import streamlit as st
import google.generativeai as genai
import json
import re
import io
import time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Buscador Licencias",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');
:root{--teal:#0d9488;--teal-lt:#14b8a6;--navy:#0f172a;--slate:#1e293b;--muted:#475569;--border:#1e3a5f;--card:#0f2137;--amber:#f59e0b;}
html,body,[data-testid="stAppViewContainer"]{background:var(--navy)!important;font-family:'DM Sans',sans-serif;color:#e2e8f0;}
#MainMenu,footer,header{visibility:hidden;}[data-testid="stToolbar"]{display:none;}
.hero{background:#0c3b4a;border:1px solid var(--border);border-radius:16px;padding:2.2rem 2.8rem;margin-bottom:2rem;}
.hero-badge{display:inline-block;background:rgba(13,148,136,.2);border:1px solid var(--teal);color:var(--teal-lt);font-size:.72rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;padding:.3rem .8rem;border-radius:99px;margin-bottom:1rem;}
.hero h1{font-family:'DM Serif Display',serif;font-size:2.4rem;line-height:1.15;color:#f1f5f9;margin:0 0 .7rem;font-weight:400;}
.hero h1 span{color:var(--teal-lt);}
.hero p{color:#94a3b8;font-size:.95rem;max-width:620px;line-height:1.65;margin:0;}
.stage-row{display:flex;gap:.75rem;margin-bottom:1.5rem;flex-wrap:wrap;}
.stage-pill{display:flex;align-items:center;gap:.5rem;background:var(--card);border:1px solid var(--border);border-radius:99px;padding:.4rem .9rem;font-size:.8rem;font-weight:500;color:#94a3b8;}
.stage-pill.active{background:rgba(13,148,136,.15);border-color:var(--teal);color:var(--teal-lt);}
.stage-dot{width:7px;height:7px;border-radius:50%;background:currentColor;opacity:.6;}
.config-label{font-size:.75rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.45rem;}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stSelectbox"] select{background:#0a1929!important;border:1px solid var(--border)!important;border-radius:8px!important;color:#e2e8f0!important;font-family:'DM Sans',sans-serif!important;}
.stButton>button{background:linear-gradient(135deg,var(--teal) 0%,#0d7a70 100%)!important;color:white!important;font-family:'DM Sans',sans-serif!important;font-weight:600!important;font-size:.88rem!important;border:none!important;border-radius:10px!important;padding:.6rem 1.6rem!important;transition:all .2s!important;}
.stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 6px 20px rgba(13,148,136,.35)!important;}
.stDownloadButton>button{background:linear-gradient(135deg,#065f46 0%,#047857 100%)!important;color:white!important;font-family:'DM Sans',sans-serif!important;font-weight:600!important;border:1px solid #059669!important;border-radius:10px!important;padding:.6rem 1.6rem!important;}
.status-box{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--teal);border-radius:0 8px 8px 0;padding:.9rem 1.1rem;font-size:.88rem;color:#94a3b8;margin:.8rem 0;}
.feedback-box{background:rgba(245,158,11,.05);border:1px solid rgba(245,158,11,.3);border-left:3px solid var(--amber);border-radius:0 10px 10px 0;padding:1.2rem 1.4rem;margin:1.2rem 0;}
.feedback-title{font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);margin-bottom:.5rem;}
.feedback-body{font-size:.88rem;color:#cbd5e1;line-height:1.55;margin:0;}
.correction-box{background:rgba(13,148,136,.06);border:1px solid rgba(13,148,136,.3);border-left:3px solid var(--teal-lt);border-radius:0 8px 8px 0;padding:.9rem 1.1rem;margin:.8rem 0;font-size:.88rem;color:#94a3b8;}
.result-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:1.4rem;margin-bottom:.9rem;transition:border-color .2s;}
.result-card:hover{border-color:var(--teal);}
.result-num{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;background:rgba(13,148,136,.2);border:1px solid var(--teal);border-radius:50%;font-size:.78rem;font-weight:700;color:var(--teal-lt);margin-bottom:.65rem;}
.result-name{font-family:'DM Serif Display',serif;font-size:1.15rem;color:#f1f5f9;margin-bottom:.25rem;}
.result-url{font-size:.8rem;color:var(--teal-lt);margin-bottom:.9rem;word-break:break-all;}
.result-field{margin-bottom:.7rem;}
.result-field-label{font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.22rem;}
.result-field-value{font-size:.86rem;color:#cbd5e1;line-height:1.55;}
.block-header{display:flex;align-items:center;gap:.6rem;margin-bottom:.8rem;}
.block-badge{background:rgba(13,148,136,.15);border:1px solid rgba(13,148,136,.3);color:var(--teal-lt);font-size:.7rem;font-weight:600;padding:.22rem .7rem;border-radius:99px;}
.block-range{font-size:.8rem;color:var(--muted);}
.more-block{background:rgba(13,148,136,.04);border:1px dashed rgba(13,148,136,.35);border-radius:12px;padding:1.5rem 1.8rem;margin:1.2rem 0;text-align:center;}
.more-badge{display:inline-block;background:rgba(13,148,136,.15);border:1px solid rgba(13,148,136,.3);color:var(--teal-lt);font-size:.68rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;padding:.22rem .7rem;border-radius:99px;margin-bottom:.6rem;}
.more-title{font-size:.95rem;color:#e2e8f0;font-weight:500;margin-bottom:.3rem;}
.more-sub{font-size:.82rem;color:#64748b;margin-bottom:.9rem;}
.divider{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:1.5rem 0;}
[data-testid="stMetric"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:10px!important;padding:1rem!important;}
[data-testid="stMetricValue"]{color:var(--teal-lt)!important;font-family:'DM Serif Display',serif!important;}
[data-testid="stMetricLabel"]{color:var(--muted)!important;font-size:.75rem!important;}
[data-testid="stExpander"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:10px!important;}
[data-testid="stSidebar"]{background:var(--slate)!important;border-right:1px solid var(--border)!important;}
::-webkit-scrollbar{width:6px;}::-webkit-scrollbar-track{background:var(--navy);}::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ─── PROMPTS ─────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Eres un analista de software experto especializado en herramientas para el sector académico y universitario.
Tu tarea es encontrar herramientas digitales (softwares, web apps o apps) siguiendo un proceso de etapas estrictas.
REGLAS: Responde SIEMPRE en JSON válido sin texto extra ni bloques de código. Solo el JSON puro."""

ETAPA1_PROMPT = """ETAPA 1 — FILTRO DE MODELO DE NEGOCIO

Tema: {tema}

Encuentra herramientas que cumplan TODAS estas condiciones:
1. De PAGO para el público general.
2. 100% GRATUITO para académicos/estudiantes/instituciones — sin costo para ellos NI su institución.
3. Acceso gratuito NO automático: requiere formulario, cuestionario o correo .edu con aprobación manual.
4. EXCLUIR si solo ofrecen descuento.
5. EXCLUIR si requiere que la universidad haya comprado licencia.

Busca frases como: "Apply for Academic Grant", "Request Educational License", "Academic Application Form".
Si el plan PRO se regala a académicos tras verificación manual → SÍ es válido.

Devuelve exactamente 5 herramientas en este JSON:
{{"etapa":1,"tema":"{tema}","herramientas_validacion":[{{"nombre":"...","url":"...","descripcion_breve":"...","evidencia_pago":"...","evidencia_acceso_educativo":"..."}}]}}"""

ETAPA1_CORRECCION_PROMPT = """CORRECCIÓN ETAPA 1

Resultados anteriores: {resultados_anteriores}
Instrucciones del usuario: "{instrucciones_usuario}"
Tema: {tema}

Aplica las correcciones. Mantén exactamente 5 herramientas.

{{"etapa":1,"tema":"{tema}","herramientas_validacion":[{{"nombre":"...","url":"...","descripcion_breve":"...","evidencia_pago":"...","evidencia_acceso_educativo":"..."}}]}}"""

ETAPA2_PROMPT = """ETAPA 2 — FILTRO EMERGENTES + ENRIQUECIMIENTO

Herramientas de referencia (Etapa 1): {herramientas_etapa1}
Tema: {tema}
Cantidad: {cantidad}
Numeración desde: {num_inicio}

Busca {cantidad} herramientas DIFERENTES a las anteriores, emergentes y poco conocidas para "{tema}" que cumplan:
1. Pago para el público general.
2. 100% gratis para académicos con validación manual.
3. NO aparecen en los primeros 5 resultados de Google.
4. Son startups, betas, o herramientas de muy baja visibilidad.
5. NO son Open Source ni software masivo (Adobe, Microsoft, etc).

Para cada herramienta incluye descripción detallada, precio exacto, proceso de validación educativa y casos de uso.

{{"etapa":2,"tema":"{tema}","lista_definitiva":[{{"numero":{num_inicio},"nombre":"...","url":"...","que_hace_categoria":"...","precio_publico_general":"...","metodo_acceso_educativo_gratuito":"...","razon_baja_popularidad":"...","casos_uso":"..."}}]}}"""


# ─── GEMINI ───────────────────────────────────────────────────────────────────
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return ""

def get_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)

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
                return {"error": "JSON inválido", "raw": text}
        except Exception as e:
            if attempt == retries - 1:
                return {"error": str(e)}
            time.sleep(2 ** attempt)
    return {"error": "Sin respuesta"}


# ─── EXCEL ────────────────────────────────────────────────────────────────────
def build_excel(results, tema):
    wb = Workbook()
    ws = wb.active
    ws.title = "Resultados"
    ws.sheet_view.showGridLines = False
    HEADERS = ["N°","Nombre","URL","Categoría / Función","Precio Público","Acceso Educativo Gratuito","Razón Baja Popularidad","Casos de Uso"]
    WIDTHS  = [5, 28, 35, 30, 30, 45, 40, 45]
    NAVY="0F172A"; SLATE="1E293B"; TEAL="0D9488"; WHITE="F1F5F9"; LIGHT="E2E8F0"
    def bd():
        s=Side(style="thin",color="1E3A5F"); return Border(left=s,right=s,top=s,bottom=s)

    ws.merge_cells("A1:H1")
    c=ws["A1"]; c.value=f"Buscador Licencias — {tema}"
    c.font=Font(name="Arial",bold=True,size=16,color=WHITE)
    c.fill=PatternFill("solid",start_color=NAVY)
    c.alignment=Alignment(horizontal="center",vertical="center")
    ws.row_dimensions[1].height=36

    ws.merge_cells("A2:H2")
    s=ws["A2"]; s.value="Softwares académicos con alto impacto · Pago público | Gratuito académico verificado | Emergentes"
    s.font=Font(name="Arial",size=9,color="94A3B8")
    s.fill=PatternFill("solid",start_color=NAVY)
    s.alignment=Alignment(horizontal="center",vertical="center")
    ws.row_dimensions[2].height=18

    for col in range(1,9):
        ws.cell(row=3,column=col).fill=PatternFill("solid",start_color=NAVY)
    ws.row_dimensions[3].height=6

    for ci,(h,w) in enumerate(zip(HEADERS,WIDTHS),1):
        cell=ws.cell(row=4,column=ci,value=h)
        cell.font=Font(name="Arial",bold=True,size=9,color=WHITE)
        cell.fill=PatternFill("solid",start_color=TEAL)
        cell.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True)
        cell.border=bd()
        ws.column_dimensions[get_column_letter(ci)].width=w
    ws.row_dimensions[4].height=28

    for i,item in enumerate(results):
        row=5+i; bg=NAVY if i%2==0 else SLATE
        vals=[item.get("numero",i+1),item.get("nombre",""),item.get("url",""),
              item.get("que_hace_categoria",""),item.get("precio_publico_general",""),
              item.get("metodo_acceso_educativo_gratuito",""),item.get("razon_baja_popularidad",""),
              item.get("casos_uso","")]
        for ci,v in enumerate(vals,1):
            cell=ws.cell(row=row,column=ci,value=str(v))
            cell.fill=PatternFill("solid",start_color=bg); cell.border=bd()
            cell.alignment=Alignment(vertical="top",wrap_text=True,horizontal="center" if ci==1 else "left")
            if ci==1: cell.font=Font(name="Arial",bold=True,size=10,color="0D9488")
            elif ci==2: cell.font=Font(name="Arial",bold=True,size=9,color=WHITE)
            elif ci==3: cell.font=Font(name="Arial",size=8,color="14B8A6",underline="single")
            else: cell.font=Font(name="Arial",size=9,color=LIGHT)
        ws.row_dimensions[row].height=80
    ws.freeze_panes="A5"

    ws2=wb.create_sheet("Resumen")
    ws2.sheet_view.showGridLines=False
    ws2.column_dimensions["A"].width=32; ws2.column_dimensions["B"].width=55
    ws2.merge_cells("A1:B1"); t=ws2["A1"]; t.value="Resumen de Búsqueda"
    t.font=Font(name="Arial",bold=True,size=14,color=WHITE)
    t.fill=PatternFill("solid",start_color=NAVY)
    t.alignment=Alignment(horizontal="center",vertical="center"); ws2.row_dimensions[1].height=32
    for ri,(label,value) in enumerate([("Tema",tema),("Total",len(results)),
        ("Bloques",max(1,(len(results)+9)//10)),("Motor IA","Gemini 2.5 Flash"),
        ("Generado con","Buscador Licencias v1.3")],2):
        bg=NAVY if ri%2==0 else SLATE
        lc=ws2.cell(row=ri,column=1,value=label); lc.font=Font(name="Arial",bold=True,size=9,color="94A3B8")
        lc.fill=PatternFill("solid",start_color=bg); lc.border=bd(); lc.alignment=Alignment(vertical="center")
        vc=ws2.cell(row=ri,column=2,value=str(value)); vc.font=Font(name="Arial",size=9,color=WHITE)
        vc.fill=PatternFill("solid",start_color=bg); vc.border=bd()
        vc.alignment=Alignment(vertical="center",wrap_text=True); ws2.row_dimensions[ri].height=22

    buf=io.BytesIO(); wb.save(buf); buf.seek(0); return buf.getvalue()


# ─── UI HELPERS ──────────────────────────────────────────────────────────────
def render_hero():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">🎓 Licencias Académicas Gratuitas</div>
        <h1>Buscador de <span>Licencias</span></h1>
        <p>Buscador de softwares académicos con alto impacto en el desarrollo académico de la comunidad Universitaria.</p>
    </div>""", unsafe_allow_html=True)

def render_stage_indicator(active):
    stages=[("1","Modelo de Negocio"),("2","Filtro Emergentes"),("3","Lista Definitiva")]
    pills="".join(f'<div class="stage-pill{"active" if int(n)<=active else ""}"><div class="stage-dot"></div> Etapa {n}: {l}</div>'
                  for n,l in stages)
    # fix: add space before class active
    pills=pills.replace('"stage-pillactive"','"stage-pill active"')
    st.markdown(f'<div class="stage-row">{pills}</div>', unsafe_allow_html=True)

def render_result_card(item):
    num=item.get("numero","?"); nombre=item.get("nombre",""); url=item.get("url","")
    cat=item.get("que_hace_categoria",""); precio=item.get("precio_publico_general","")
    acceso=item.get("metodo_acceso_educativo_gratuito",""); popular=item.get("razon_baja_popularidad","")
    casos=item.get("casos_uso","")
    casos_html=(f'<div class="result-field"><div class="result-field-label">🏥 Casos de Uso</div>'
                f'<div class="result-field-value">{casos}</div></div>') if casos else ""
    st.markdown(f"""<div class="result-card">
        <div class="result-num">{num}</div>
        <div class="result-name">{nombre}</div>
        <div class="result-url">🔗 {url}</div>
        <div class="result-field"><div class="result-field-label">📋 Categoría</div><div class="result-field-value">{cat}</div></div>
        <div class="result-field"><div class="result-field-label">💰 Precio Público</div><div class="result-field-value">{precio}</div></div>
        <div class="result-field"><div class="result-field-label">🎓 Acceso Educativo Gratuito</div><div class="result-field-value">{acceso}</div></div>
        <div class="result-field"><div class="result-field-label">🔍 Por qué es Emergente</div><div class="result-field-value">{popular}</div></div>
        {casos_html}</div>""", unsafe_allow_html=True)

def render_block_header(bloque_num, start, end):
    st.markdown(f'<div class="block-header"><div class="block-badge">Bloque {bloque_num}</div>'
                f'<span class="block-range">#{start} — #{end}</span></div>', unsafe_allow_html=True)


# ─── MAIN ────────────────────────────────────────────────────────────────────
# FASE values: "inicio" | "e1_done" | "resultados"
def main():

    # ── Init session state FIRST — before any widget ──────────────────────
    defaults = {
        "fase": "inicio",        # controls which screen to show
        "e1_result": None,
        "model_key": None,
        "corrected": False,
        "all_results": [],
        "bloque_num": 0,
        "tema": "",
        "cantidad": 10,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    api_key = get_api_key()

    render_hero()

    # Sidebar
    with st.sidebar:
        st.markdown("### 🎓 Buscador Licencias")
        st.markdown("""**Flujo:**
1. Valida modelo de negocio
2. ✏️ Corrección opcional
3. Filtra emergentes
4. ＋ Más bloques
5. Descarga Excel""")
        st.markdown("---")
        st.markdown("<small style='color:#475569'>Buscador Licencias v1.3<br>Gemini 2.5 Flash</small>",
                    unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # PANTALLA 1: INICIO — formulario de búsqueda
    # ═══════════════════════════════════════════════════════════════════════
    if st.session_state.fase == "inicio":
        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.markdown('<div class="config-label">Tema de búsqueda</div>', unsafe_allow_html=True)
            tema_input = st.text_input("tema", label_visibility="collapsed",
                placeholder="Ej: Enfermería, Arquitectura, Marketing Digital, Derecho...",
                value=st.session_state.tema)
        with col_r:
            st.markdown('<div class="config-label">Resultados por bloque</div>', unsafe_allow_html=True)
            cantidad_input = st.selectbox("cantidad", label_visibility="collapsed",
                options=[5, 10, 15, 20], index=[5,10,15,20].index(st.session_state.cantidad)
                if st.session_state.cantidad in [5,10,15,20] else 1)

        if st.button("🔍 Buscar Herramientas", use_container_width=True):
            if not tema_input.strip():
                st.error("⚠️ Ingresa un tema de búsqueda.")
                return
            if not api_key:
                st.error("⚠️ No se encontró GEMINI_API_KEY en Secrets.")
                return

            # Save inputs
            st.session_state.tema = tema_input.strip()
            st.session_state.cantidad = cantidad_input
            st.session_state.all_results = []
            st.session_state.bloque_num = 0
            st.session_state.corrected = False
            st.session_state.e1_result = None

            # Run Etapa 1
            model = get_model(api_key)
            st.session_state.model_key = api_key  # store to rebuild later

            render_stage_indicator(1)
            with st.spinner("⚙️ Etapa 1 — Analizando modelos de negocio..."):
                result1 = call_gemini(model, ETAPA1_PROMPT.format(tema=st.session_state.tema))

            if "error" in result1:
                st.error(f"Error en Etapa 1: {result1['error']}")
                return

            st.session_state.e1_result = result1
            st.session_state.fase = "e1_done"
            st.rerun()

        # Placeholder
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_stage_indicator(0)
        st.markdown('<div class="status-box">👆 Ingresa un tema y presiona <strong>Buscar Herramientas</strong>.</div>',
                    unsafe_allow_html=True)
        return

    # ═══════════════════════════════════════════════════════════════════════
    # PANTALLA 2: E1_DONE — mostrar resultados E1 + formulario corrección
    # ═══════════════════════════════════════════════════════════════════════
    if st.session_state.fase == "e1_done":
        model = get_model(api_key)
        herramientas_e1 = st.session_state.e1_result.get("herramientas_validacion", [])

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_stage_indicator(1)

        with st.expander(f"✅ Etapa 1 — {len(herramientas_e1)} herramientas pre-seleccionadas (revisa antes de continuar)", expanded=True):
            for h in herramientas_e1:
                st.markdown(f"**{h.get('nombre')}** — `{h.get('url')}`")
                c1, c2 = st.columns(2)
                c1.caption(f"💰 {h.get('evidencia_pago','')}")
                c2.caption(f"🎓 {h.get('evidencia_acceso_educativo','')}")
                st.markdown("---")

        # Feedback box
        st.markdown("""<div class="feedback-box">
            <div class="feedback-title">✏️ Revisión opcional antes de continuar</div>
            <div class="feedback-body">Revisa los resultados de Etapa 1. Si alguna herramienta no cumple el filtro,
            escribe tus instrucciones abajo. Si todo está correcto, déjalo vacío y haz clic en
            <strong>Continuar a Etapa 2</strong>.</div></div>""", unsafe_allow_html=True)

        instrucciones = st.text_area("Instrucciones de corrección", label_visibility="collapsed",
            placeholder='Ej: "Elimina NVivo porque solo ofrece descuento. Reemplázalo por una herramienta de simulación."',
            height=110, key="feedback_text")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✏️ Aplicar Corrección", use_container_width=True,
                         disabled=not instrucciones.strip(), key="btn_corr"):
                with st.spinner("Aplicando correcciones..."):
                    result_corr = call_gemini(model, ETAPA1_CORRECCION_PROMPT.format(
                        resultados_anteriores=json.dumps(herramientas_e1, ensure_ascii=False),
                        instrucciones_usuario=instrucciones.strip(),
                        tema=st.session_state.tema,
                    ))
                if "error" in result_corr:
                    st.error(f"Error: {result_corr['error']}")
                else:
                    st.session_state.e1_result = result_corr
                    st.session_state.corrected = True
                    st.rerun()

        with col_b:
            if st.button("▶ Continuar a Etapa 2", use_container_width=True, key="btn_cont"):
                # Run Etapas 2+3 immediately
                herramientas_e1 = st.session_state.e1_result.get("herramientas_validacion", [])
                nombres_e1 = [h.get("nombre","") for h in herramientas_e1]
                num_inicio = 1

                render_stage_indicator(2)
                with st.spinner("🔍 Etapa 2 — Filtrando y enriqueciendo..."):
                    result2 = call_gemini(model, ETAPA2_PROMPT.format(
                        herramientas_etapa1=json.dumps(nombres_e1, ensure_ascii=False),
                        cantidad=st.session_state.cantidad,
                        tema=st.session_state.tema,
                        num_inicio=num_inicio,
                    ))

                if "error" in result2:
                    st.error(f"Error en Etapa 2: {result2['error']}")
                    return

                lista = result2.get("lista_definitiva", [])
                for i, item in enumerate(lista):
                    item["numero"] = num_inicio + i

                st.session_state.all_results = lista
                st.session_state.bloque_num = 1
                st.session_state.fase = "resultados"
                st.rerun()
        return

    # ═══════════════════════════════════════════════════════════════════════
    # PANTALLA 3: RESULTADOS — bloques acumulados + buscar más
    # ═══════════════════════════════════════════════════════════════════════
    if st.session_state.fase == "resultados":
        model = get_model(api_key)
        all_results = st.session_state.all_results
        cantidad = st.session_state.cantidad
        tema = st.session_state.tema

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Metrics
        end_num = all_results[-1].get("numero", len(all_results)) if all_results else 0
        m1, m2, m3 = st.columns(3)
        m1.metric("Total encontradas", len(all_results))
        m2.metric("Bloques generados", st.session_state.bloque_num)
        m3.metric("Rango actual", f"#1 → #{end_num}")

        if st.session_state.corrected:
            st.markdown('<div class="correction-box">🔧 Lista generada con correcciones de Etapa 1.</div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Render all blocks
        for b in range(st.session_state.bloque_num):
            bloque_items = all_results[b * cantidad: (b + 1) * cantidad]
            if not bloque_items:
                continue
            start_n = bloque_items[0].get("numero", b * cantidad + 1)
            end_n   = bloque_items[-1].get("numero", (b+1) * cantidad)
            render_block_header(b + 1, start_n, end_n)
            for item in bloque_items:
                render_result_card(item)
            if b < st.session_state.bloque_num - 1:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Buscar más
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        next_bloque = st.session_state.bloque_num + 1
        next_start  = end_num + 1
        next_end    = next_start + cantidad - 1

        st.markdown(f"""<div class="more-block">
            <div class="more-badge">Continuar búsqueda</div>
            <div class="more-title">¿Quieres más herramientas?</div>
            <div class="more-sub">Bloque {next_bloque}: #{next_start}–#{next_end} sin perder el historial</div>
        </div>""", unsafe_allow_html=True)

        col_mas, col_nueva = st.columns([1, 1])
        with col_mas:
            if st.button(f"＋ Buscar {cantidad} más (Bloque {next_bloque})",
                         use_container_width=True, key=f"btn_more_{st.session_state.bloque_num}"):
                nombres_e1 = [h.get("nombre","") for h in
                              st.session_state.e1_result.get("herramientas_validacion",[])]
                with st.spinner(f"Generando Bloque {next_bloque}..."):
                    result2 = call_gemini(model, ETAPA2_PROMPT.format(
                        herramientas_etapa1=json.dumps(nombres_e1, ensure_ascii=False),
                        cantidad=cantidad,
                        tema=tema,
                        num_inicio=next_start,
                    ))
                if "error" in result2:
                    st.error(f"Error: {result2['error']}")
                else:
                    lista = result2.get("lista_definitiva", [])
                    for i, item in enumerate(lista):
                        item["numero"] = next_start + i
                    st.session_state.all_results.extend(lista)
                    st.session_state.bloque_num += 1
                    st.rerun()

        with col_nueva:
            if st.button("🔄 Nueva búsqueda", use_container_width=True, key="btn_nueva"):
                st.session_state.fase = "inicio"
                st.session_state.all_results = []
                st.session_state.bloque_num = 0
                st.session_state.e1_result = None
                st.session_state.corrected = False
                st.rerun()

        # Excel
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📥 Exportar Resultados")
        col_dl1, col_dl2 = st.columns([1, 3])
        with col_dl1:
            st.download_button(
                label="⬇️ Descargar Excel completo",
                data=build_excel(all_results, tema),
                file_name=f"buscador_licencias_{tema.lower().replace(' ','_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        with col_dl2:
            st.markdown(f'<div class="status-box">Excel con <strong>{len(all_results)} herramientas</strong> '
                        f'en 2 hojas: Resultados y Resumen.</div>', unsafe_allow_html=True)

        with st.expander("🔧 Ver JSON completo"):
            st.json(all_results)


if __name__ == "__main__":
    main()
