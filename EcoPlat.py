# ============================================================
# EcoPlat — Plataforma de Sustentabilidade Digital
# Versão 3.0 — Completo e funcional
#
# Requisitos:
#   pip install streamlit firebase-admin bcrypt requests
#
# Rode:
#   streamlit run EcoPlat.py
# ============================================================

import streamlit as st
import json, re, bcrypt, random, time
import requests as _req
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

# ============================================================
# PÁGINA
# ============================================================
st.set_page_config(page_title="EcoPlat", page_icon="🌱", layout="wide",
                   initial_sidebar_state="collapsed")

# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #f4f7f4; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 16px !important; }

/* NAV */
.nav-bar {
    background: #1a472a;
    border-radius: 14px;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}
.nav-logo { color: white; font-size: 1.35em; font-weight: 800; }
.nav-logo span { color: #74c69d; }
.nav-pts {
    background: #2d6a4f;
    color: #b7e4c7;
    padding: 5px 16px;
    border-radius: 20px;
    font-size: 0.88em;
    font-weight: 600;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #1a472a 0%, #2d6a4f 60%, #52b788 100%);
    border-radius: 20px;
    padding: 52px 44px;
    color: white;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '🌱';
    position: absolute;
    right: 40px; top: 50%;
    transform: translateY(-50%);
    font-size: 8em;
    opacity: 0.12;
}
.hero h1 { font-size: 2.5em; font-weight: 800; margin-bottom: 12px; color: white; line-height: 1.2; }
.hero p  { font-size: 1.05em; opacity: 0.9; color: white; max-width: 500px; line-height: 1.7; }

/* CARDS */
.card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    border: 1.5px solid #e2e8e2;
    height: 100%;
}
.card h3 { color: #1a472a; font-size: 1em; font-weight: 700; margin-bottom: 8px; }
.card p  { color: #555; font-size: 0.88em; line-height: 1.6; }
.card .ico { font-size: 2em; margin-bottom: 12px; }

/* STAT CARDS */
.stat {
    background: #1a472a;
    border-radius: 14px;
    padding: 22px 18px;
    text-align: center;
    color: white;
}
.stat .num { font-size: 2em; font-weight: 800; color: #74c69d; }
.stat .lbl { font-size: 0.8em; opacity: 0.85; margin-top: 4px; line-height: 1.4; }

/* NOTÍCIAS */
.noticia {
    background: white;
    border-radius: 12px;
    padding: 16px 18px;
    border: 1.5px solid #e2e8e2;
    margin-bottom: 10px;
}
.noticia h4 { font-size: 0.92em; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }
.noticia p  { font-size: 0.82em; color: #555; line-height: 1.5; margin-bottom: 6px; }
.noticia .fonte { font-size: 0.75em; color: #999; font-weight: 600; }

/* STATUS BADGES */
.badge-ok   { background: #d4edda; color: #155724; border: 1px solid #28a745;
              padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 600; }
.badge-wait { background: #fff3cd; color: #856404; border: 1px solid #ffc107;
              padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 600; }
.badge-no   { background: #f8d7da; color: #721c24; border: 1px solid #dc3545;
              padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 600; }

/* ITEM ROWS */
.item-row {
    background: white;
    border-radius: 10px;
    padding: 14px 18px;
    border: 1.5px solid #e2e8e2;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.item-row h4 { font-size: 0.92em; font-weight: 600; color: #1a1a1a; margin-bottom: 2px; }
.item-row p  { font-size: 0.8em; color: #777; }

/* IMPACTO PREVIEW */
.impacto {
    background: #f0faf4;
    border: 1.5px solid #74c69d;
    border-radius: 12px;
    padding: 16px 18px;
    margin-top: 14px;
}
.impacto h4 { color: #1a472a; font-size: 0.9em; font-weight: 700; margin-bottom: 10px; }
.impacto-row { display: flex; justify-content: space-between; font-size: 0.84em;
               padding: 3px 0; color: #333; border-bottom: 1px solid #e0f0e8; }
.impacto-row:last-child { border-bottom: none; }
.impacto-row b { color: #1a472a; }

/* CLÃ CARDS */
.cla-card {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1.5px solid #e2e8e2;
    margin-bottom: 8px;
}
.cla-card.meu { border-color: #52b788; background: #f0faf4; }
.cla-rank-1 { border-left: 4px solid #ffd700; }
.cla-rank-2 { border-left: 4px solid #c0c0c0; }
.cla-rank-3 { border-left: 4px solid #cd7f32; }
.codigo-box {
    background: #1a472a;
    color: #74c69d;
    font-family: monospace;
    font-size: 1.4em;
    font-weight: 700;
    letter-spacing: 4px;
    padding: 10px 24px;
    border-radius: 10px;
    display: inline-block;
    margin: 8px 0;
}

/* CONQUISTA */
.conquista {
    background: white;
    border-radius: 12px;
    padding: 14px 18px;
    border: 1.5px solid #e2e8e2;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.conquista.done { border-color: #ffc107; background: #fffdf0; }
.conquista .ico2 { font-size: 1.8em; min-width: 40px; text-align: center; }
.conquista h4 { font-size: 0.9em; font-weight: 700; color: #1a1a1a; margin-bottom: 2px; }
.conquista p  { font-size: 0.78em; color: #666; }
.conquista .pts { font-weight: 700; color: #e6a817; font-size: 0.9em; margin-left: auto; white-space: nowrap; }

/* PREMIUM */
.premium-box {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border-radius: 16px;
    padding: 28px;
    color: white;
    text-align: center;
}
.premium-box h3 { color: #f4d03f; font-size: 1.3em; margin-bottom: 8px; }
.premium-box .preco { font-size: 1.8em; font-weight: 800; color: white; margin: 12px 0; }
.premium-box p { opacity: 0.75; font-size: 0.88em; }
.premium-box ul { text-align: left; margin: 14px 0; padding: 0; list-style: none; }
.premium-box ul li { font-size: 0.86em; opacity: 0.85; margin-bottom: 6px; }
.premium-box ul li::before { content: '✓ '; color: #f4d03f; font-weight: 700; }

/* CUPOM */
.cupom-card {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1.5px solid #e2e8e2;
    margin-bottom: 10px;
}
.cupom-card h4 { font-size: 0.95em; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; }
.cupom-card p  { font-size: 0.82em; color: #666; }

/* DESAFIO */
.desafio-box {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-radius: 14px;
    padding: 22px;
    color: white;
    margin-bottom: 14px;
}
.desafio-box h4 { font-size: 0.95em; margin-bottom: 14px; line-height: 1.5; }
.opcao-btn {
    background: rgba(255,255,255,0.08);
    border: 1.5px solid rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 10px 14px;
    color: white;
    font-size: 0.85em;
    cursor: pointer;
    width: 100%;
    text-align: left;
    margin-bottom: 6px;
}

/* AUTH */
.auth-box {
    background: white;
    border-radius: 16px;
    padding: 32px;
    border: 1.5px solid #e2e8e2;
    max-width: 420px;
    margin: 0 auto;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #1a472a;
    border-radius: 12px;
    padding: 5px;
    gap: 3px;
}
.stTabs [data-baseweb="tab"] {
    color: #b7e4c7 !important;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #1a472a !important;
}

/* BOTÕES */
.stButton > button {
    background: #1a472a;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 22px;
    width: 100%;
}
.stButton > button:hover { background: #2d6a4f; }

/* INPUTS */
.stTextInput input, .stNumberInput input, .stSelectbox > div > div {
    border-radius: 8px !important;
    border: 1.5px solid #c8e6c9 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# FIREBASE
# ============================================================
@st.cache_resource
def init_db():
    if not firebase_admin._apps:
        try:
            if "firebase" in st.secrets:
                key = st.secrets["firebase"]["key"]
                kd  = json.loads(key) if isinstance(key, str) else dict(key)
                cred = credentials.Certificate(kd)
            else:
                cred = credentials.Certificate("firebase-credentials.json")
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"❌ Firebase: {e}")
            return None
    return firestore.client()

db = init_db()

# ============================================================
# UTILITÁRIOS
# ============================================================
def email_ok(e):
    return bool(re.match(r'^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$', e))

def hash_pw(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def check_pw(pw, h):
    return bcrypt.checkpw(pw.encode(), h.encode())

def ts_str(ts):
    if hasattr(ts, 'strftime'):
        return ts.strftime('%d/%m/%Y %H:%M')
    return str(ts)

# ============================================================
# DB — USUÁRIOS
# ============================================================
def criar_usuario(nome, email, senha):
    if not db: return None, "Firebase não conectado"
    if not nome.strip(): return None, "Nome obrigatório"
    if not email_ok(email): return None, "E-mail inválido"
    if len(senha) < 6: return None, "Senha mínimo 6 caracteres"
    if list(db.collection("usuarios").where("email","==",email.lower()).limit(1).stream()):
        return None, "E-mail já cadastrado"

    uid = int(datetime.now().timestamp()*1000)
    d = {
        "id": uid, "nome": nome.strip(), "email": email.lower(),
        "senha": hash_pw(senha), "pontos": 0.0, "plano": "gratuito",
        "consentimento_lgpd": None, "cla_id": None,
        "conquistas": [], "criado_em": datetime.now()
    }
    db.collection("usuarios").document(str(uid)).set(d)
    d.pop("senha"); d["criado_em"] = ts_str(d["criado_em"])
    return d, "Conta criada!"

def login_usuario(email, senha):
    if not db: return None
    docs = list(db.collection("usuarios").where("email","==",email.lower()).limit(1).stream())
    if not docs: return None
    d = docs[0].to_dict()
    if not check_pw(senha, d["senha"]): return None
    d.pop("senha")
    d["criado_em"] = ts_str(d.get("criado_em",""))
    return d

def get_usuario(uid):
    if not db: return None
    doc = db.collection("usuarios").document(str(uid)).get()
    if not doc.exists: return None
    d = doc.to_dict(); d.pop("senha", None)
    d["criado_em"] = ts_str(d.get("criado_em",""))
    return d

def update_pontos(uid, delta):
    if not db: return
    ref = db.collection("usuarios").document(str(uid))
    doc = ref.get()
    if doc.exists:
        atual = doc.to_dict().get("pontos", 0)
        ref.update({"pontos": max(0, atual + delta)})

def update_plano(uid, plano):
    if not db: return
    db.collection("usuarios").document(str(uid)).update({"plano": plano})

def salvar_consentimento(uid, aceito):
    if not db: return
    db.collection("usuarios").document(str(uid)).update({
        "consentimento_lgpd": aceito, "data_consentimento": datetime.now()
    })

def add_conquista(uid, cid):
    if not db: return
    ref = db.collection("usuarios").document(str(uid))
    doc = ref.get()
    if doc.exists:
        lista = doc.to_dict().get("conquistas", [])
        if cid not in lista:
            lista.append(cid)
            ref.update({"conquistas": lista})

# ============================================================
# DB — DESCARTES
# ============================================================
MATERIAIS = {
    "Linha Marrom": {"Televisor":5.0,"Computador":4.0,"Notebook":3.5,"Monitor":3.0},
    "Linha Azul":   {"Liquidificador":1.5,"Ferro de Passar":1.0,"Ventilador":2.0},
    "Linha Verde":  {"Celular":2.5,"Bateria":1.5,"Carregador":1.0,"Fone de Ouvido":0.5},
}

IMPACTO_BASE = {
    "Televisor":    {"co2":4.0,"energia":12.0,"agua":800,"chumbo":0.05,"mercurio":0.002},
    "Computador":   {"co2":3.5,"energia":10.0,"agua":600,"chumbo":0.04,"mercurio":0.001},
    "Notebook":     {"co2":2.5,"energia":8.0, "agua":400,"chumbo":0.02,"mercurio":0.001},
    "Monitor":      {"co2":2.0,"energia":6.0, "agua":300,"chumbo":0.03,"mercurio":0.001},
    "Liquidificador":{"co2":1.0,"energia":3.0,"agua":200,"chumbo":0.01,"mercurio":0.0},
    "Ferro de Passar":{"co2":0.8,"energia":2.0,"agua":150,"chumbo":0.01,"mercurio":0.0},
    "Ventilador":   {"co2":1.2,"energia":4.0, "agua":200,"chumbo":0.01,"mercurio":0.0},
    "Celular":      {"co2":0.7,"energia":2.0, "agua":600,"chumbo":0.005,"mercurio":0.0005},
    "Bateria":      {"co2":0.5,"energia":1.5, "agua":300,"chumbo":0.02,"mercurio":0.002},
    "Carregador":   {"co2":0.3,"energia":1.0, "agua":100,"chumbo":0.003,"mercurio":0.0},
    "Fone de Ouvido":{"co2":0.2,"energia":0.5,"agua":50, "chumbo":0.001,"mercurio":0.0},
}

def calc_impacto(material, qtd):
    b = IMPACTO_BASE.get(material)
    if not b: return None
    return {k: round(v*qtd, 4) for k,v in b.items()}

def criar_descarte(uid, linha, material, qtd, pontos, custom=False):
    if not db: return
    did = int(datetime.now().timestamp()*1000)
    db.collection("descartes").document(str(did)).set({
        "id":did,"usuario_id":uid,"numero":f"DSC-{did}",
        "linha":linha,"material":material,"quantidade":qtd,
        "pontos":pontos,"status":"Pendente","customizado":custom,
        "data":datetime.now()
    })

def get_descartes(uid=None):
    if not db: return []
    docs = db.collection("descartes").stream()
    r = []
    for doc in docs:
        d = doc.to_dict(); d["data"] = ts_str(d.get("data",""))
        if uid is None or d.get("usuario_id")==uid: r.append(d)
    return r

def update_descarte(did, status):
    if not db: return
    db.collection("descartes").document(str(did)).update({"status":status})

# ============================================================
# DB — CUPONS
# ============================================================
CUPONS = {
    "Desconto 10% — Loja Verde":   {"pontos":30,"desc":"Produtos sustentáveis","emoji":"🛒"},
    "Desconto 15% — Livraria":     {"pontos":40,"desc":"Qualquer livro","emoji":"📚"},
    "R$15 de crédito — Restaurante":{"pontos":50,"desc":"Pedidos acima de R$40","emoji":"🍽️"},
    "Desconto 20% — Mercado Bio":  {"pontos":35,"desc":"Produtos orgânicos","emoji":"🌿"},
    "Ingresso Cinema":             {"pontos":60,"desc":"1 ingresso meia entrada","emoji":"🎬"},
    "Desconto 10% — Farmácia":     {"pontos":25,"desc":"Medicamentos e higiene","emoji":"💊"},
}
PRECO_PREMIUM = 120

def criar_resgate(uid, nome_cupom, codigo, pontos):
    if not db: return
    rid = int(datetime.now().timestamp()*1000)
    db.collection("resgates").document(str(rid)).set({
        "id":rid,"usuario_id":uid,"cupom":nome_cupom,
        "codigo":codigo,"pontos":pontos,"status":"Pendente","data":datetime.now()
    })

def get_resgates(uid=None):
    if not db: return []
    docs = db.collection("resgates").stream()
    r = []
    for doc in docs:
        d = doc.to_dict(); d["data"] = ts_str(d.get("data",""))
        if uid is None or d.get("usuario_id")==uid: r.append(d)
    return r

# ============================================================
# DB — MONITORAMENTO
# ============================================================
def salvar_meta(uid, horas, dias_meta):
    if not db: return
    db.collection("monitoramento").document(str(uid)).set({
        "usuario_id":uid,"horas_limite":horas,"meta_dias":dias_meta,
        "dias_consecutivos":0,"historico":[],"atualizado_em":datetime.now()
    }, merge=True)

def get_meta(uid):
    if not db: return None
    doc = db.collection("monitoramento").document(str(uid)).get()
    if doc.exists:
        d = doc.to_dict()
        d["atualizado_em"] = ts_str(d.get("atualizado_em",""))
        return d
    return None

def registrar_dia(uid, bateu):
    if not db: return 0
    ref = db.collection("monitoramento").document(str(uid))
    doc = ref.get()
    if not doc.exists: return 0
    d   = doc.to_dict()
    dias = d.get("dias_consecutivos",0)
    hist = d.get("historico",[])
    hist.append({"data":datetime.now().strftime("%d/%m"),"bateu":bateu})
    if len(hist)>30: hist = hist[-30:]
    if bateu:
        dias+=1
        ref.update({"dias_consecutivos":dias,"historico":hist,"atualizado_em":datetime.now()})
        if dias % d.get("meta_dias",7) == 0:
            update_pontos(uid, 10)
            return 10
    else:
        ref.update({"dias_consecutivos":0,"historico":hist,"atualizado_em":datetime.now()})
    return 0

# ============================================================
# DB — CLÃS
# ============================================================
LIMITE_CLA = 20

DESAFIOS = [
    {"materia":"📐 Matemática","nivel":1,"pergunta":"Quanto é 15% de 200?",
     "opcoes":["A) 25","B) 30","C) 35","D) 40"],"correta":1,"pts":5},
    {"materia":"📐 Matemática","nivel":1,"pergunta":"Qual é a raiz quadrada de 144?",
     "opcoes":["A) 10","B) 11","C) 12","D) 13"],"correta":2,"pts":5},
    {"materia":"📐 Matemática","nivel":2,"pergunta":"Se x² - 5x + 6 = 0, quais são os valores de x?",
     "opcoes":["A) 1 e 6","B) 2 e 3","C) -2 e -3","D) -1 e 6"],"correta":1,"pts":10},
    {"materia":"🌍 Ciências","nivel":1,"pergunta":"Qual metal pesado em baterias afeta o hipocampo?",
     "opcoes":["A) Ferro","B) Cobre","C) Chumbo","D) Zinco"],"correta":2,"pts":5},
    {"materia":"🌍 Ciências","nivel":1,"pergunta":"O que é e-waste?",
     "opcoes":["A) Lixo orgânico","B) Lixo eletrônico","C) Energia renovável","D) Água residual"],"correta":1,"pts":5},
    {"materia":"🌍 Ciências","nivel":2,"pergunta":"Quantos litros de água 1 celular mal descartado pode contaminar?",
     "opcoes":["A) 60 litros","B) 200 litros","C) 600 litros","D) 6000 litros"],"correta":2,"pts":10},
    {"materia":"📖 História","nivel":1,"pergunta":"Em que ano foi criada a PNRS (Política Nacional de Resíduos Sólidos) no Brasil?",
     "opcoes":["A) 2000","B) 2005","C) 2010","D) 2015"],"correta":2,"pts":5},
    {"materia":"🌎 Geografia","nivel":1,"pergunta":"Qual país é o maior gerador de lixo eletrônico do mundo?",
     "opcoes":["A) Brasil","B) China","C) EUA","D) Índia"],"correta":1,"pts":5},
    {"materia":"📐 Matemática","nivel":3,"pergunta":"Uma PA tem primeiro termo 3 e razão 4. Qual é o 10º termo?",
     "opcoes":["A) 35","B) 39","C) 43","D) 47"],"correta":1,"pts":15},
    {"materia":"🌍 Ciências","nivel":3,"pergunta":"Qual é o nome do processo de separar metais valiosos do lixo eletrônico?",
     "opcoes":["A) Compostagem","B) Hidrometalurgia","C) Fotossíntese","D) Destilação"],"correta":1,"pts":15},
]

NIVEL_CLA = {1:"Iniciante",2:"Aprendiz",3:"Experiente",4:"Avançado",5:"Mestre"}
PONTOS_NIVEL = {1:0, 2:500, 3:1500, 4:3000, 5:6000}

def nivel_cla(pts):
    n = 1
    for nv, minpts in sorted(PONTOS_NIVEL.items()):
        if pts >= minpts: n = nv
    return n

def gerar_codigo():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(random.choices(chars, k=6))

def criar_cla(nome, lider_id, lider_nome):
    if not db: return None,"Firebase não conectado"
    if not nome.strip(): return None,"Nome obrigatório"
    if get_cla_do_user(lider_id): return None,"Você já está em um clã"
    if list(db.collection("claes").where("nome","==",nome.strip()).limit(1).stream()):
        return None,"Nome já existe"
    codigo = gerar_codigo()
    while list(db.collection("claes").where("codigo","==",codigo).limit(1).stream()):
        codigo = gerar_codigo()
    cid = int(datetime.now().timestamp()*1000)
    dados = {
        "id":cid,"nome":nome.strip(),"codigo":codigo,
        "lider_id":lider_id,"lider_nome":lider_nome,
        "membros":[{"id":lider_id,"nome":lider_nome}],
        "pontos_total":0.0,"criado_em":datetime.now()
    }
    db.collection("claes").document(str(cid)).set(dados)
    db.collection("usuarios").document(str(lider_id)).update({"cla_id":cid})
    return dados,"Clã criado!"

def entrar_cla(codigo, uid, nome):
    if not db: return False,"Firebase não conectado"
    if get_cla_do_user(uid): return False,"Você já está em um clã"
    docs = list(db.collection("claes").where("codigo","==",codigo.upper()).limit(1).stream())
    if not docs: return False,"Código inválido"
    cla = docs[0].to_dict(); ref = docs[0].reference
    if len(cla["membros"]) >= LIMITE_CLA: return False,f"Clã cheio ({LIMITE_CLA} membros)"
    if any(m["id"]==uid for m in cla["membros"]): return False,"Você já é membro"
    ref.update({"membros": cla["membros"]+[{"id":uid,"nome":nome}]})
    db.collection("usuarios").document(str(uid)).update({"cla_id":cla["id"]})
    return True,f"Entrou em **{cla['nome']}**!"

def sair_cla(uid):
    if not db: return False,"Firebase não conectado"
    cla = get_cla_do_user(uid)
    if not cla: return False,"Você não está em nenhum clã"
    if cla["lider_id"]==uid: return False,"Líder não pode sair. Dissolva o clã."
    membros = [m for m in cla["membros"] if m["id"]!=uid]
    db.collection("claes").document(str(cla["id"])).update({"membros":membros})
    db.collection("usuarios").document(str(uid)).update({"cla_id":None})
    return True,"Você saiu do clã."

def dissolver_cla(cid, lider_id):
    if not db: return False,"Firebase não conectado"
    ref = db.collection("claes").document(str(cid))
    doc = ref.get()
    if not doc.exists: return False,"Clã não encontrado"
    cla = doc.to_dict()
    if cla["lider_id"]!=lider_id: return False,"Apenas o líder pode dissolver"
    for m in cla["membros"]:
        db.collection("usuarios").document(str(m["id"])).update({"cla_id":None})
    ref.delete()
    return True,"Clã dissolvido."

def remover_membro(cid, lider_id, mid):
    if not db: return False,"Firebase não conectado"
    ref = db.collection("claes").document(str(cid))
    doc = ref.get()
    if not doc.exists: return False,"Clã não encontrado"
    cla = doc.to_dict()
    if cla["lider_id"]!=lider_id: return False,"Apenas o líder pode remover"
    ref.update({"membros":[m for m in cla["membros"] if m["id"]!=mid]})
    db.collection("usuarios").document(str(mid)).update({"cla_id":None})
    return True,"Membro removido."

def get_cla_do_user(uid):
    if not db: return None
    doc = db.collection("usuarios").document(str(uid)).get()
    if not doc.exists: return None
    cid = doc.to_dict().get("cla_id")
    if not cid: return None
    cdoc = db.collection("claes").document(str(cid)).get()
    return cdoc.to_dict() if cdoc.exists else None

def get_ranking_claes():
    if not db: return []
    claes = []
    for doc in db.collection("claes").stream():
        cla = doc.to_dict()
        total = 0.0
        for m in cla.get("membros",[]):
            u = db.collection("usuarios").document(str(m["id"])).get()
            if u.exists: total += u.to_dict().get("pontos",0)
        cla["pontos_total"] = total
        claes.append(cla)
    return sorted(claes, key=lambda x: x["pontos_total"], reverse=True)

# ============================================================
# CONQUISTAS
# ============================================================
CONQUISTAS = [
    {"id":"c01","ico":"♻️","nome":"Primeiro Descarte","desc":"Registre seu primeiro eletrônico","pts":5},
    {"id":"c02","ico":"📺","nome":"Linha Marrom x5","desc":"Descarte 5 itens da linha marrom","pts":10},
    {"id":"c03","ico":"📺","nome":"Linha Marrom x10","desc":"Descarte 10 itens da linha marrom","pts":15},
    {"id":"c04","ico":"📱","nome":"Linha Verde x5","desc":"Descarte 5 itens da linha verde","pts":10},
    {"id":"c05","ico":"🧘","nome":"Primeiro Dia Consciente","desc":"Bata sua meta de tela pela 1ª vez","pts":5},
    {"id":"c06","ico":"📵","nome":"Desintoxicação","desc":"Fique 12h sem celular (meta ≤ 0h)","pts":20},
    {"id":"c07","ico":"🔥","nome":"Sequência de Fogo","desc":"7 dias consecutivos na meta","pts":25},
    {"id":"c08","ico":"🤝","nome":"Fundador","desc":"Crie seu primeiro clã","pts":10},
    {"id":"c09","ico":"📚","nome":"Estudioso","desc":"Acerte 5 desafios no clã","pts":20},
    {"id":"c10","ico":"⭐","nome":"Cem Pontos","desc":"Acumule 100 pontos na plataforma","pts":15},
]

def checar_conquistas(uid):
    """Verifica e concede conquistas automaticamente."""
    if not db: return []
    u = get_usuario(uid)
    if not u: return []
    ja_tem = u.get("conquistas",[])
    novas  = []

    descartes = get_descartes(uid)
    aprovados = [d for d in descartes if d["status"]=="Aprovado"]
    marrom    = [d for d in aprovados if d["linha"]=="Linha Marrom"]
    verde     = [d for d in aprovados if d["linha"]=="Linha Verde"]

    checks = {
        "c01": len(aprovados) >= 1,
        "c02": sum(d["quantidade"] for d in marrom) >= 5,
        "c03": sum(d["quantidade"] for d in marrom) >= 10,
        "c04": sum(d["quantidade"] for d in verde)  >= 5,
        "c10": u.get("pontos",0) >= 100,
    }
    meta = get_meta(uid)
    if meta:
        checks["c07"] = meta.get("dias_consecutivos",0) >= 7

    cla = get_cla_do_user(uid)
    if cla: checks["c08"] = True

    for cid, cond in checks.items():
        if cond and cid not in ja_tem:
            c = next((x for x in CONQUISTAS if x["id"]==cid), None)
            if c:
                add_conquista(uid, cid)
                update_pontos(uid, c["pts"])
                novas.append(c)
    return novas

# ============================================================
# NOTÍCIAS (Claude API + web search)
# ============================================================
def buscar_noticias():
    TTL = 1800
    if ("_news" in st.session_state and
            st.session_state.get("_news_ts",0)+TTL > time.time()):
        return st.session_state["_news"]

    prompt = """Busque notícias recentes (últimas 2 semanas) sobre:
1. Lixo eletrônico, e-waste, reciclagem no Brasil e mundo (3 notícias)
2. Saúde digital, vício em celular, tempo de tela (3 notícias)

Responda SOMENTE com JSON válido, sem markdown nem texto extra:
[{"tema":"eco" ou "digital","emoji":"...","titulo":"máx 75 chars","resumo":"máx 130 chars","fonte":"nome do veículo"}]"""

    try:
        r = _req.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json"},
            json={
                "model":"claude-sonnet-4-20250514",
                "max_tokens":1000,
                "tools":[{"type":"web_search_20250305","name":"web_search"}],
                "messages":[{"role":"user","content":prompt}]
            },
            timeout=30
        )
        data  = r.json()
        texto = " ".join(b.get("text","") for b in data.get("content",[]) if b.get("type")=="text")
        i, j  = texto.find("["), texto.rfind("]")+1
        if i==-1 or j==0: return []
        news = json.loads(texto[i:j])
        st.session_state["_news"]    = news
        st.session_state["_news_ts"] = time.time()
        return news
    except Exception:
        return []

# ============================================================
# SESSION STATE
# ============================================================
for k,v in {"user":None,"auth_modo":"login","lgpd_ok":False}.items():
    if k not in st.session_state: st.session_state[k] = v

# ============================================================
# NAVBAR
# ============================================================
def navbar():
    u = st.session_state.user
    col1, col2 = st.columns([6,1])
    with col1:
        pts = f"⭐ {u['pontos']:.0f} pts" if u else ""
        st.markdown(f"""
        <div class='nav-bar'>
            <span class='nav-logo'>🌱 Eco<span>Plat</span></span>
            <span class='nav-pts'>{pts}</span>
        </div>""", unsafe_allow_html=True)
    if u:
        with col2:
            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.user = None
                st.rerun()

# ============================================================
# LGPD
# ============================================================
def lgpd_check():
    u = st.session_state.user
    if not u or st.session_state.lgpd_ok: return
    if u.get("consentimento_lgpd") is not None:
        st.session_state.lgpd_ok = True; return
    with st.container():
        st.info("📋 **Consentimento LGPD** — Gostaríamos de coletar dados anônimos para melhorar a plataforma e contribuir com pesquisas ambientais. Nenhum dado pessoal é compartilhado.")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("✅ Autorizar"):
                salvar_consentimento(u["id"],True)
                st.session_state.user["consentimento_lgpd"]=True
                st.session_state.lgpd_ok=True; st.rerun()
        with c2:
            if st.button("❌ Não autorizar"):
                salvar_consentimento(u["id"],False)
                st.session_state.user["consentimento_lgpd"]=False
                st.session_state.lgpd_ok=True; st.rerun()
        st.stop()

# ============================================================
# AUTH
# ============================================================
def tela_auth():
    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
    modo = st.session_state.auth_modo
    st.markdown(f"### {'🔑 Entrar' if modo=='login' else '📝 Criar conta'}")

    if modo=="login":
        with st.form("f_login"):
            email = st.text_input("📧 E-mail")
            senha = st.text_input("🔒 Senha", type="password")
            ok    = st.form_submit_button("Entrar", use_container_width=True)
        if ok:
            if not email or not senha: st.error("Preencha tudo.")
            else:
                u = login_usuario(email, senha)
                if u:
                    st.session_state.user = u
                    st.session_state.lgpd_ok = False
                    st.rerun()
                else: st.error("E-mail ou senha incorretos.")
        if st.button("Não tem conta? Cadastre-se"):
            st.session_state.auth_modo="cadastro"; st.rerun()
    else:
        with st.form("f_cad"):
            nome  = st.text_input("📛 Nome")
            email = st.text_input("📧 E-mail")
            senha = st.text_input("🔒 Senha (mín. 6 caracteres)", type="password")
            senha2= st.text_input("🔒 Confirme a senha", type="password")
            ok    = st.form_submit_button("Criar conta", use_container_width=True)
        if ok:
            if senha!=senha2: st.error("Senhas não coincidem.")
            else:
                u,msg = criar_usuario(nome,email,senha)
                if u:
                    st.session_state.user=u
                    st.session_state.lgpd_ok=False
                    st.balloons(); st.rerun()
                else: st.error(msg)
        if st.button("Já tem conta? Entrar"):
            st.session_state.auth_modo="login"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def gate():
    """Exibe auth se não logado."""
    st.markdown("<br>", unsafe_allow_html=True)
    _,c,_ = st.columns([1,2,1])
    with c: tela_auth()

# ============================================================
# ABA INÍCIO
# ============================================================
def aba_inicio():
    # Hero
    st.markdown("""
    <div class='hero'>
        <h1>Use melhor.<br>Viva melhor.</h1>
        <p>Descarte eletrônicos corretamente, monitore seu uso de tela e
        ganhe recompensas por cada boa ação. Juntos, fazemos a diferença.</p>
    </div>""", unsafe_allow_html=True)

    # Você sabia
    st.markdown("### 💡 Você sabia?")
    c1,c2,c3 = st.columns(3)
    cards = [
        ("📱","1 celular descartado errado","contamina até <b>600 litros de água</b> com metais pesados como chumbo e mercúrio."),
        ("⏱️","Uso excessivo do celular","aumenta ansiedade e reduz a concentração. Pequenas pausas fazem <b>grande diferença</b>."),
        ("♻️","Reciclar 1 computador","evita até <b>4 kg de CO₂</b> e recupera metais valiosos como ouro e cobre."),
    ]
    for col,(ico,titulo,txt) in zip([c1,c2,c3],cards):
        with col:
            st.markdown(f"""<div class='card' style='text-align:center'>
                <div class='ico'>{ico}</div><h3>{titulo}</h3><p>{txt}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Impacto
    st.markdown("### 🌍 Impacto coletivo da plataforma")
    c1,c2,c3,c4 = st.columns(4)
    stats = [("2.4t","lixo eletrônico descartado"),("380kg","de CO₂ evitados"),
             ("12k","horas de tela economizadas"),("847","alunos ativos")]
    for col,(num,lbl) in zip([c1,c2,c3,c4],stats):
        with col:
            st.markdown(f"<div class='stat'><div class='num'>{num}</div><div class='lbl'>{lbl}</div></div>",
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Notícias
    st.markdown("### 📰 Notícias recentes")
    st.caption("Buscadas automaticamente na web · atualiza a cada 30 min")

    col_btn, _ = st.columns([1,5])
    with col_btn:
        if st.button("🔄 Atualizar"):
            st.session_state.pop("_news",None)
            st.session_state.pop("_news_ts",None)
            st.rerun()

    with st.spinner("Buscando notícias..."):
        news = buscar_noticias()

    if not news:
        st.info("Não foi possível carregar notícias agora. Tente atualizar.")
    else:
        eco  = [n for n in news if n.get("tema")=="eco"]
        dig  = [n for n in news if n.get("tema")=="digital"]
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("<div style='background:#e8f5e9;border-radius:10px;padding:8px 14px;"
                        "font-weight:600;color:#1a472a;margin-bottom:10px;font-size:0.9em;'>"
                        "♻️ Lixo Eletrônico & Reciclagem</div>", unsafe_allow_html=True)
            for n in eco:
                st.markdown(f"""<div class='noticia'>
                    <h4>{n.get('emoji','')} {n.get('titulo','')}</h4>
                    <p>{n.get('resumo','')}</p>
                    <span class='fonte'>📌 {n.get('fonte','')}</span>
                </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("<div style='background:#e3f2fd;border-radius:10px;padding:8px 14px;"
                        "font-weight:600;color:#1565c0;margin-bottom:10px;font-size:0.9em;'>"
                        "📱 Saúde Digital & Bem-estar</div>", unsafe_allow_html=True)
            for n in dig:
                st.markdown(f"""<div class='noticia'>
                    <h4>{n.get('emoji','')} {n.get('titulo','')}</h4>
                    <p>{n.get('resumo','')}</p>
                    <span class='fonte'>📌 {n.get('fonte','')}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.user:
        st.markdown("""<div style='text-align:center;padding:32px;background:white;
            border-radius:16px;border:1.5px solid #e2e8e2;'>
            <h3 style='color:#1a472a;'>Pronto para fazer a diferença?</h3>
            <p style='color:#555;'>Crie sua conta gratuitamente e comece a acumular pontos hoje mesmo.</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        _,c,_ = st.columns([1,2,1])
        with c: tela_auth()

# ============================================================
# ABA ECO-ELETRÔNICO
# ============================================================
def aba_eco():
    if not st.session_state.user: gate(); return
    u   = st.session_state.user
    uid = u["id"]

    st.markdown(f"### ♻️ Eco-Eletrônico")
    st.markdown(f"<div style='background:#e8f5e9;border:1.5px solid #a5d6a7;border-radius:20px;"
                f"padding:6px 16px;display:inline-block;font-weight:600;color:#1a472a;"
                f"margin-bottom:16px;'>⭐ {u['pontos']:.0f} pontos</div>", unsafe_allow_html=True)

    t1,t2 = st.tabs(["📥 Cadastrar descarte","📋 Meus descartes"])

    with t1:
        linha = st.selectbox("Linha", ["Selecione..."]+list(MATERIAIS.keys()))
        if linha != "Selecione...":
            mats  = MATERIAIS[linha]
            opcoes= list(mats.keys())+["📝 Outro"]
            mat_sel = st.selectbox("Material", opcoes,
                format_func=lambda x: f"{x}  (+{mats.get(x,'?')} pts/un)" if x!="📝 Outro" else x)

            mat_final=""; pts_unit=0.0
            if mat_sel=="📝 Outro":
                mat_final = st.text_input("Descreva o material:")
                pts_unit  = st.number_input("Pontos por unidade:", 0.5, 5.0, 2.0, 0.5)
            else:
                mat_final = mat_sel
                pts_unit  = mats[mat_sel]
                st.info(f"✅ **{mat_final}** — {pts_unit} pts/unidade")

            qtd = st.number_input("Quantidade", min_value=1, value=1)

            if mat_final:
                imp = calc_impacto(mat_final, qtd)
                if imp:
                    st.markdown(f"""<div class='impacto'>
                        <h4>🌿 Impacto ambiental estimado</h4>
                        <div class='impacto-row'><span>CO₂ evitado</span><b>{imp['co2']} kg</b></div>
                        <div class='impacto-row'><span>Energia economizada</span><b>{imp['energia']} kWh</b></div>
                        <div class='impacto-row'><span>Água preservada</span><b>{imp['agua']} L</b></div>
                        <div class='impacto-row'><span>Chumbo evitado</span><b>{imp['chumbo']} kg</b></div>
                        <div class='impacto-row'><span>Mercúrio evitado</span><b>{imp['mercurio']} kg</b></div>
                    </div>""", unsafe_allow_html=True)

                total_pts = pts_unit * qtd
                st.markdown(f"**Total: {total_pts:.1f} pontos** (após aprovação pelo admin)")

                if st.button("📥 Registrar descarte", use_container_width=True):
                    criar_descarte(uid, linha, mat_final, qtd, total_pts, mat_sel=="📝 Outro")
                    # Checar conquistas
                    novas = checar_conquistas(uid)
                    st.session_state.user = get_usuario(uid)
                    st.success(f"✅ Descarte registrado! **{total_pts:.1f} pts** após aprovação.")
                    for n in novas:
                        st.balloons()
                        st.success(f"🏆 Conquista desbloqueada: **{n['nome']}** +{n['pts']} pts!")
                    st.rerun()

    with t2:
        descartes = get_descartes(uid)
        if not descartes:
            st.info("Nenhum descarte ainda. Cadastre seu primeiro eletrônico!")
        else:
            for d in sorted(descartes, key=lambda x: x.get("data",""), reverse=True):
                s = d["status"]
                badge = (f"<span class='badge-ok'>✅ Aprovado</span>" if s=="Aprovado" else
                         f"<span class='badge-no'>❌ Recusado</span>" if s=="Recusado" else
                         f"<span class='badge-wait'>⏳ Pendente</span>")
                st.markdown(f"""<div class='item-row'>
                    <div>
                        <h4>{d['numero']} · {d['material']} ({d['quantidade']} un)</h4>
                        <p>{d['linha']} · {d['pontos']:.1f} pts · {d['data']}</p>
                    </div>
                    {badge}
                </div>""", unsafe_allow_html=True)

# ============================================================
# ABA MONITORAMENTO
# ============================================================
def aba_monitor():
    if not st.session_state.user: gate(); return
    u   = st.session_state.user
    uid = u["id"]
    plano = u.get("plano","gratuito")

    st.markdown("### 📱 Monitoramento Digital")
    st.markdown(f"<div style='background:#e3f2fd;border:1.5px solid #90caf9;border-radius:20px;"
                f"padding:6px 16px;display:inline-block;font-weight:600;color:#1565c0;"
                f"margin-bottom:16px;'>⭐ {u['pontos']:.0f} pts · "
                f"{'🌟 Premium' if plano=='premium' else '🆓 Gratuito'}</div>",
                unsafe_allow_html=True)

    t1,t2,t3 = st.tabs(["🎯 Meta","📊 Registrar dia","🌟 Premium"])

    with t1:
        meta = get_meta(uid)
        h_atual = meta["horas_limite"] if meta else 4.0
        d_atual = meta["meta_dias"]    if meta else 7

        st.markdown("**Configure seu limite diário de uso do celular:**")
        horas = st.slider("Limite diário (horas)", 0.5, 12.0, float(h_atual), 0.5)
        dias  = st.number_input("Dias consecutivos para ganhar pontos", 1, 30, int(d_atual))
        st.info(f"💡 A cada **{dias} dias consecutivos** dentro da meta → **+10 pontos**")

        if st.button("💾 Salvar meta", use_container_width=True):
            salvar_meta(uid, horas, dias)
            st.success("✅ Meta salva!")

        if meta:
            seq = meta.get("dias_consecutivos",0)
            prox = dias - (seq % dias) if seq>0 else dias
            st.markdown(f"""
            <div style='background:#fff3cd;border:1.5px solid #ffc107;border-radius:12px;
                        padding:18px 22px;margin-top:16px;text-align:center;'>
                <div style='font-size:2em;font-weight:800;color:#e65100;'>{seq}</div>
                <div style='font-size:0.85em;color:#555;'>dias consecutivos 🔥</div>
                <div style='font-size:0.8em;color:#777;margin-top:4px;'>Faltam {prox} dias para +10 pts</div>
            </div>""", unsafe_allow_html=True)

    with t2:
        meta = get_meta(uid)
        if not meta:
            st.warning("⚠️ Configure sua meta primeiro na aba 'Meta'.")
        else:
            st.markdown(f"**Sua meta: até {meta['horas_limite']}h de tela por dia**")
            usadas = st.number_input("Horas de tela hoje:", 0.0, 24.0, 0.0, 0.5)
            bateu  = usadas <= meta["horas_limite"]

            if bateu:
                st.success(f"✅ Dentro da meta! Você usou {usadas}h de {meta['horas_limite']}h")
            else:
                st.error(f"❌ Acima da meta. {usadas}h usadas de {meta['horas_limite']}h")

            if st.button("📊 Registrar este dia", use_container_width=True):
                pts = registrar_dia(uid, bateu)
                novas = checar_conquistas(uid)
                st.session_state.user = get_usuario(uid)
                if bateu:
                    if pts>0:
                        st.balloons()
                        st.success(f"🎉 Sequência! Você ganhou **{pts} pontos**!")
                    else:
                        st.success("✅ Dia registrado! Continue assim.")
                else:
                    st.warning("😔 Sequência zerada. Tente amanhã!")
                for n in novas:
                    st.success(f"🏆 Conquista: **{n['nome']}** +{n['pts']} pts!")
                st.rerun()

    with t3:
        if plano=="premium":
            st.success("🌟 Você já tem o Plano Premium!")
            st.markdown("""
            **Benefícios ativos:**
            - 📊 Relatórios detalhados por app
            - 🎯 Metas personalizadas por categoria
            - 🔔 Alertas inteligentes em tempo real
            - 📈 Histórico completo de 90 dias
            - 🏆 Badge exclusivo no perfil
            """)
        else:
            st.markdown(f"""<div class='premium-box'>
                <h3>🌟 Plano Premium</h3>
                <p>Desbloqueie recursos avançados de monitoramento</p>
                <ul>
                    <li>Relatórios detalhados por app</li>
                    <li>Metas por categoria (redes sociais, jogos...)</li>
                    <li>Alertas inteligentes em tempo real</li>
                    <li>Histórico completo de 90 dias</li>
                    <li>Badge exclusivo no perfil</li>
                </ul>
                <div class='preco'>{PRECO_PREMIUM} pontos</div>
                <p>ou R$9,90/mês</p>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            saldo = u["pontos"]
            if saldo >= PRECO_PREMIUM:
                if st.button(f"⭐ Ativar Premium por {PRECO_PREMIUM} pts", use_container_width=True):
                    update_pontos(uid, -PRECO_PREMIUM)
                    update_plano(uid, "premium")
                    st.session_state.user = get_usuario(uid)
                    st.balloons(); st.success("🎉 Premium ativado!"); st.rerun()
            else:
                faltam = PRECO_PREMIUM - saldo
                st.warning(f"⚠️ Faltam **{faltam:.0f} pontos**. Continue descartando e batendo metas!")

# ============================================================
# ABA CUPONS
# ============================================================
def aba_cupons():
    if not st.session_state.user: gate(); return
    u   = st.session_state.user
    uid = u["id"]

    st.markdown("### 🎁 Cupons & Ofertas")
    st.markdown(f"<div style='background:#fef9e7;border:1.5px solid #f4d03f;border-radius:20px;"
                f"padding:6px 16px;display:inline-block;font-weight:600;color:#7d6608;"
                f"margin-bottom:16px;'>⭐ Seu saldo: {u['pontos']:.0f} pontos</div>",
                unsafe_allow_html=True)

    t1,t2 = st.tabs(["🛒 Catálogo","🎫 Meus cupons"])

    with t1:
        st.markdown("**Troque seus pontos por descontos em empresas parceiras:**")
        meus = {r["cupom"] for r in get_resgates(uid)}

        for nome,(info) in CUPONS.items():
            ja = nome in meus
            c1,c2 = st.columns([4,1])
            with c1:
                cor   = "#f0faf4" if ja else "white"
                borda = "#52b788" if ja else "#e2e8e2"
                st.markdown(f"""<div class='cupom-card' style='background:{cor};border-color:{borda};'>
                    <h4>{info['emoji']} {nome}</h4>
                    <p>{info['desc']} · <b>{info['pontos']} pontos</b>
                    {'· ✅ Já resgatado' if ja else ''}</p>
                </div>""", unsafe_allow_html=True)
            with c2:
                pode = not ja and u["pontos"] >= info["pontos"]
                if st.button("Resgatar", key=f"cup_{nome}", disabled=not pode,
                             use_container_width=True):
                    cod = f"ECO-{nome[:3].upper()}-{random.randint(1000,9999)}"
                    update_pontos(uid, -info["pontos"])
                    criar_resgate(uid, nome, cod, info["pontos"])
                    st.session_state.user = get_usuario(uid)
                    st.success(f"✅ Cupom **{cod}** resgatado!")
                    st.rerun()

        # Oferta premium
        st.markdown("---")
        st.markdown("**⭐ Oferta especial:**")
        c1,c2 = st.columns([4,1])
        with c1:
            st.markdown(f"""<div class='cupom-card' style='border-color:#f4d03f;background:#fffdf0;'>
                <h4>🌟 Plano Premium — Monitoramento Digital</h4>
                <p>Relatórios avançados, alertas inteligentes e histórico de 90 dias
                · <b>{PRECO_PREMIUM} pontos</b></p>
            </div>""", unsafe_allow_html=True)
        with c2:
            if u.get("plano")=="premium":
                st.markdown("✅ Ativo")
            elif u["pontos"] >= PRECO_PREMIUM:
                if st.button("Ativar", key="cup_premium", use_container_width=True):
                    update_pontos(uid, -PRECO_PREMIUM)
                    update_plano(uid, "premium")
                    st.session_state.user = get_usuario(uid)
                    st.balloons(); st.success("🎉 Premium ativado!"); st.rerun()
            else:
                st.markdown(f"<small>Faltam {PRECO_PREMIUM-u['pontos']:.0f} pts</small>",
                            unsafe_allow_html=True)

    with t2:
        resgates = get_resgates(uid)
        if not resgates:
            st.info("Nenhum cupom resgatado ainda.")
        else:
            for r in sorted(resgates, key=lambda x: x.get("data",""), reverse=True):
                s = r["status"]
                badge = (f"<span class='badge-ok'>✅ Aprovado</span>" if s=="Aprovado" else
                         f"<span class='badge-no'>❌ Recusado</span>" if s=="Recusado" else
                         f"<span class='badge-wait'>⏳ Pendente</span>")
                st.markdown(f"""<div class='item-row'>
                    <div>
                        <h4>🎫 {r['cupom']}</h4>
                        <p>Código: <b style='letter-spacing:1px'>{r['codigo']}</b> · {r['data']}</p>
                    </div>
                    {badge}
                </div>""", unsafe_allow_html=True)

# ============================================================
# ABA CLÃS
# ============================================================
def aba_claes():
    if not st.session_state.user: gate(); return
    u   = st.session_state.user
    uid = u["id"]

    st.markdown("### ⚔️ Clãs")
    meu_cla = get_cla_do_user(uid)

    if not meu_cla:
        st.info("Você não pertence a nenhum clã. Crie um ou entre com código de convite.")
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("#### ➕ Criar clã")
            with st.form("f_criar_cla"):
                nome_c = st.text_input("Nome do clã")
                ok     = st.form_submit_button("Criar", use_container_width=True)
            if ok:
                cla,msg = criar_cla(nome_c, uid, u["nome"])
                if cla:
                    st.balloons(); st.success(msg)
                    novas = checar_conquistas(uid)
                    st.session_state.user = get_usuario(uid)
                    st.rerun()
                else: st.error(msg)
        with c2:
            st.markdown("#### 🔑 Entrar com código")
            with st.form("f_entrar_cla"):
                cod = st.text_input("Código de convite")
                ok  = st.form_submit_button("Entrar", use_container_width=True)
            if ok:
                ok2,msg = entrar_cla(cod, uid, u["nome"])
                if ok2: st.success(msg); st.rerun()
                else:   st.error(msg)

        st.markdown("---")
        _comp_ranking()
        return

    # Com clã
    eh_lider = meu_cla["lider_id"]==uid
    nivel    = nivel_cla(meu_cla.get("pontos_total",0))
    nome_nv  = NIVEL_CLA.get(nivel,"?")
    prox_nv  = PONTOS_NIVEL.get(nivel+1)

    # Header do clã
    pts_cla = meu_cla.get("pontos_total",0)
    progresso = ""
    if prox_nv:
        pct = min(int((pts_cla/prox_nv)*100),100)
        progresso = f"<div style='background:rgba(255,255,255,0.2);border-radius:10px;height:8px;margin-top:10px;'><div style='background:#74c69d;width:{pct}%;height:100%;border-radius:10px;'></div></div><div style='font-size:0.78em;opacity:0.8;margin-top:4px;'>{pts_cla:.0f} / {prox_nv} pts para Nível {nivel+1}</div>"

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1a1a2e,#2d1b69);border-radius:18px;
                padding:28px 32px;color:white;margin-bottom:20px;'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
            <div>
                <div style='font-size:1.5em;font-weight:800;'>⚔️ {meu_cla['nome']}</div>
                <div style='opacity:0.8;font-size:0.9em;margin-top:4px;'>
                    👑 {meu_cla['lider_nome']} · 👥 {len(meu_cla['membros'])}/{LIMITE_CLA} membros
                    · 🔑 <b>{meu_cla['codigo']}</b>
                </div>
                {progresso}
            </div>
            <div style='background:linear-gradient(135deg,#c9a84c,#f4d03f);color:#1a1a1a;
                        padding:8px 20px;border-radius:20px;font-weight:800;font-size:0.9em;
                        white-space:nowrap;'>
                ⚔️ Nível {nivel} — {nome_nv}
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    t1,t2,t3,t4 = st.tabs(["👥 Membros","🏆 Ranking","📚 Desafios","⚙️ Gerenciar"])

    with t1:
        st.markdown("**Membros do clã (ordenados por pontos):**")
        total = 0.0
        membros_pts = []
        for m in meu_cla["membros"]:
            mu = get_usuario(m["id"])
            pts = mu["pontos"] if mu else 0
            total += pts
            membros_pts.append((m["nome"], pts, m["id"]))

        st.markdown(f"**⭐ Pontuação total do clã: {total:.0f} pontos**")
        st.markdown("<br>", unsafe_allow_html=True)

        for nome_m, pts_m, mid in sorted(membros_pts, key=lambda x: x[1], reverse=True):
            lider_tag = "👑 " if mid==meu_cla["lider_id"] else ""
            st.markdown(f"""<div class='item-row'>
                <span>{lider_tag}<b>{nome_m}</b></span>
                <span style='font-weight:700;color:#1a472a;'>⭐ {pts_m:.0f} pts</span>
            </div>""", unsafe_allow_html=True)

        if not eh_lider:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🚪 Sair do clã"):
                st.warning("Você perderá sua contribuição para o clã.")
                if st.button("Confirmar saída", use_container_width=True):
                    ok,msg = sair_cla(uid)
                    if ok: st.success(msg); st.session_state.user=get_usuario(uid); st.rerun()
                    else:  st.error(msg)

    with t2:
        _comp_ranking(destacar=meu_cla["id"])

    with t3:
        st.markdown("**Responda e ganhe pontos para o clã!**")
        # Filtrar por nível do clã
        disp = [d for d in DESAFIOS if d["nivel"] <= nivel]
        if not disp:
            disp = DESAFIOS[:3]

        # Mostrar 3 desafios aleatórios
        selec = random.sample(disp, min(3, len(disp)))

        for i, des in enumerate(selec):
            st.markdown(f"""<div class='desafio-box'>
                <div style='display:flex;justify-content:space-between;margin-bottom:12px;'>
                    <span style='background:rgba(255,255,255,0.1);padding:3px 12px;
                                 border-radius:12px;font-size:0.82em;'>{des['materia']}</span>
                    <span style='color:#fbbf24;font-size:0.82em;font-weight:600;'>
                        ⚡ Nível {des['nivel']} · +{des['pts']} pts</span>
                </div>
                <h4>{des['pergunta']}</h4>
            </div>""", unsafe_allow_html=True)

            resp = st.radio("Sua resposta:", des["opcoes"],
                            key=f"des_{i}_{des['pergunta'][:20]}", index=None,
                            label_visibility="collapsed")

            if resp:
                idx = des["opcoes"].index(resp)
                if idx == des["correta"]:
                    st.success(f"✅ Correto! +{des['pts']} pontos para o clã!")
                    update_pontos(uid, des["pts"])
                    st.session_state.user = get_usuario(uid)
                else:
                    correto = des["opcoes"][des["correta"]]
                    st.error(f"❌ Errado. A resposta correta era: **{correto}**")
            st.markdown("<br>", unsafe_allow_html=True)

    with t4:
        if not eh_lider:
            st.info("Apenas o líder pode gerenciar o clã.")
        else:
            st.markdown("#### 🗑️ Remover membro")
            outros = [(m["nome"],m["id"]) for m in meu_cla["membros"] if m["id"]!=uid]
            if not outros:
                st.info("Nenhum outro membro ainda.")
            else:
                opcoes = {n:mid for n,mid in outros}
                esc    = st.selectbox("Membro", list(opcoes.keys()))
                if st.button("❌ Remover", use_container_width=True):
                    ok,msg = remover_membro(meu_cla["id"],uid,opcoes[esc])
                    if ok: st.success(msg); st.rerun()
                    else:  st.error(msg)

            st.markdown("---")
            st.markdown("#### 💣 Dissolver clã")
            st.error("⚠️ Esta ação é permanente e remove todos os membros.")
            with st.expander("Dissolver clã"):
                conf = st.text_input("Digite o nome do clã para confirmar:")
                if st.button("Dissolver permanentemente", use_container_width=True):
                    if conf==meu_cla["nome"]:
                        ok,msg = dissolver_cla(meu_cla["id"],uid)
                        if ok:
                            st.session_state.user=get_usuario(uid)
                            st.success(msg); st.rerun()
                        else: st.error(msg)
                    else: st.error("Nome incorreto.")

def _comp_ranking(destacar=None):
    st.markdown("#### 🏆 Ranking de Clãs")
    with st.spinner("Calculando..."):
        claes = get_ranking_claes()
    if not claes:
        st.info("Nenhum clã criado ainda. Seja o primeiro!")
        return
    medalhas = {1:"🥇",2:"🥈",3:"🥉"}
    bordas   = {1:"#ffd700",2:"#c0c0c0",3:"#cd7f32"}
    for i,cla in enumerate(claes,1):
        med   = medalhas.get(i,f"**{i}º**")
        borda = bordas.get(i,"#e2e8e2")
        dest  = "background:#f0faf4;" if cla["id"]==destacar else ""
        nv    = nivel_cla(cla["pontos_total"])
        st.markdown(f"""<div class='cla-card' style='border-left:4px solid {borda};{dest}'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                    <span style='font-size:1.2em;margin-right:8px;'>{med}</span>
                    <b>{cla['nome']}</b>
                    {'<span style="color:#2d6a4f;font-size:0.8em;"> ← seu clã</span>' if cla['id']==destacar else ''}
                    <span style='font-size:0.78em;color:#888;margin-left:8px;'>Nível {nv}</span>
                </div>
                <b style='color:#1a472a;'>⭐ {cla['pontos_total']:.0f}</b>
            </div>
            <div style='font-size:0.82em;color:#777;margin-top:4px;'>
                👑 {cla['lider_nome']} · 👥 {len(cla['membros'])} membros
            </div>
        </div>""", unsafe_allow_html=True)

# ============================================================
# MAIN
# ============================================================
def main():
    navbar()
    if st.session_state.user:
        lgpd_check()
        # Sincroniza pontos
        st.session_state.user = get_usuario(st.session_state.user["id"]) or st.session_state.user

    abas = ["🌱 Início","♻️ Eco-Eletrônico","📱 Monitoramento","🎁 Cupons","⚔️ Clãs"]
    tabs = st.tabs(abas)

    with tabs[0]: aba_inicio()
    with tabs[1]: aba_eco()
    with tabs[2]: aba_monitor()
    with tabs[3]: aba_cupons()
    with tabs[4]: aba_claes()

if __name__ == "__main__":
    main()
