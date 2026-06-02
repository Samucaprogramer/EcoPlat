# sistema_professores.py - Sistema de Professores e Cupons Especiais

"""
Sistema completo para gerenciamento de professores no EcoPlat
Inclui:
- Cadastro de professores com disciplinas
- Cupons especiais para professores
- Penalização de alunos (redução de pontos)
- Controle por turma
"""

# Disciplinas disponíveis
DISCIPLINAS = [
    'Matemática',
    'Português', 
    'Ciências',
    'História',
    'Geografia',
    'Inglês',
    'Ed. Física',
    'Artes',
    'Filosofia',
    'Sociologia',
    'Física',
    'Química',
    'Biologia'
]

# Turmas disponíveis
TURMAS_DISPONIVEIS = [
    '501', '502', '503', '504',
    '601', '602', '603', '604', '605', '606',
    '701', '702', '703', '704', '705', '706', '707', '708',
    '801', '802', '803', '804', '805', '806', '807',
    '901', '902', '903', '904', '905'
]

# Cupons especiais para professores
CUPONS_PROFESSORES = {
    'reducao_pontos': {
        'nome': 'Cupom de Redução de Pontos',
        'descricao': 'Permite retirar até 15 pontos de um aluno da sua turma',
        'custo_pontos': 10,
        'poder': 15,  # Quantidade de pontos que pode remover
        'tipo': 'penalizacao',
        'icone': '⚠️'
    },
    'bonus_turma': {
        'nome': 'Cupom de Bônus para Turma',
        'descricao': 'Adiciona 5 pontos para todos os alunos da turma',
        'custo_pontos': 25,
        'poder': 5,
        'tipo': 'bonus',
        'icone': '🎁'
    },
    'desafio_especial': {
        'nome': 'Cupom de Desafio Especial',
        'descricao': 'Cria um desafio ambiental para a turma (vale pontos extras)',
        'custo_pontos': 15,
        'poder': 10,
        'tipo': 'desafio',
        'icone': '🏆'
    }
}

def criar_professor(db, nome, email, senha, disciplina, turmas):
    """
    Cria novo professor no sistema
    
    Args:
        db: Firestore client
        nome: Nome do professor
        email: E-mail
        senha: Senha (já em hash)
        disciplina: Disciplina que leciona
        turmas: Lista de turmas (ex: ['701', '702'])
    
    Returns:
        dict com dados do professor
    """
    from datetime import datetime
    
    user_id = int(datetime.now().timestamp() * 1000)
    
    dados = {
        'id': user_id,
        'nome': nome,
        'email': email.lower().strip(),
        'senha': senha,
        'tipo_usuario': 'professor',  # NOVO CAMPO
        'disciplina': disciplina,
        'turmas': turmas,  # Lista de turmas
        'pontos': 0.0,
        'cuponsEspeciais': [],  # Cupons especiais do professor
        'historicoAcoes': [],  # Histórico de penalizações/bônus
        'dataCadastro': datetime.now(),
        'ativo': True
    }
    
    db.collection('usuarios').document(str(user_id)).set(dados)
    
    # Remove senha do retorno
    dados_retorno = dados.copy()
    del dados_retorno['senha']
    
    return dados_retorno

def comprar_cupom_professor(db, professor_id, cupom_tipo):
    """
    Professor compra cupom especial
    
    Args:
        db: Firestore client
        professor_id: ID do professor
        cupom_tipo: Tipo do cupom ('reducao_pontos', etc)
    
    Returns:
        (sucesso, mensagem)
    """
    from datetime import datetime
    
    if cupom_tipo not in CUPONS_PROFESSORES:
        return False, "Cupom inválido"
    
    cupom_info = CUPONS_PROFESSORES[cupom_tipo]
    
    # Buscar professor
    prof_ref = db.collection('usuarios').document(str(professor_id))
    prof_doc = prof_ref.get()
    
    if not prof_doc.exists:
        return False, "Professor não encontrado"
    
    prof_data = prof_doc.to_dict()
    
    # Verificar pontos
    if prof_data['pontos'] < cupom_info['custo_pontos']:
        return False, f"Pontos insuficientes! Você tem {prof_data['pontos']}, precisa de {cupom_info['custo_pontos']}"
    
    # Criar cupom
    cupom_id = f"CUPOM-PROF-{int(datetime.now().timestamp() * 1000)}"
    
    cupom = {
        'id': cupom_id,
        'tipo': cupom_tipo,
        'nome': cupom_info['nome'],
        'poder': cupom_info['poder'],
        'dataCompra': datetime.now(),
        'usado': False,
        'dataUso': None,
        'alvoId': None,  # ID do aluno afetado
        'alvoNome': None
    }
    
    # Atualizar professor
    cupons_atuais = prof_data.get('cuponsEspeciais', [])
    cupons_atuais.append(cupom)
    
    novos_pontos = prof_data['pontos'] - cupom_info['custo_pontos']
    
    prof_ref.update({
        'pontos': novos_pontos,
        'cuponsEspeciais': cupons_atuais
    })
    
    return True, f"✅ {cupom_info['nome']} comprado! Código: {cupom_id}"

def usar_cupom_reducao_pontos(db, professor_id, cupom_id, aluno_id):
    """
    Professor usa cupom para reduzir pontos de um aluno
    
    Args:
        db: Firestore client
        professor_id: ID do professor
        cupom_id: ID do cupom
        aluno_id: ID do aluno alvo
    
    Returns:
        (sucesso, mensagem)
    """
    from datetime import datetime
    
    # Buscar professor
    prof_ref = db.collection('usuarios').document(str(professor_id))
    prof_doc = prof_ref.get()
    
    if not prof_doc.exists:
        return False, "Professor não encontrado"
    
    prof_data = prof_doc.to_dict()
    
    # Verificar se é professor
    if prof_data.get('tipo_usuario') != 'professor':
        return False, "Apenas professores podem usar este cupom"
    
    # Buscar aluno
    aluno_ref = db.collection('usuarios').document(str(aluno_id))
    aluno_doc = aluno_ref.get()
    
    if not aluno_doc.exists:
        return False, "Aluno não encontrado"
    
    aluno_data = aluno_doc.to_dict()
    
    # Verificar se aluno é da turma do professor
    if aluno_data.get('turma') not in prof_data.get('turmas', []):
        return False, f"Você só pode penalizar alunos das suas turmas: {', '.join(prof_data['turmas'])}"
    
    # Buscar cupom
    cupons = prof_data.get('cuponsEspeciais', [])
    cupom = None
    cupom_index = None
    
    for i, c in enumerate(cupons):
        if c['id'] == cupom_id:
            cupom = c
            cupom_index = i
            break
    
    if not cupom:
        return False, "Cupom não encontrado"
    
    if cupom['usado']:
        return False, "Cupom já foi utilizado"
    
    # Aplicar penalização
    pontos_reduzir = cupom['poder']
    pontos_atuais = aluno_data.get('pontos', 0)
    novos_pontos = max(0, pontos_atuais - pontos_reduzir)  # Não pode ficar negativo
    
    pontos_realmente_removidos = pontos_atuais - novos_pontos
    
    # Atualizar aluno
    aluno_ref.update({'pontos': novos_pontos})
    
    # Marcar cupom como usado
    cupom['usado'] = True
    cupom['dataUso'] = datetime.now()
    cupom['alvoId'] = aluno_id
    cupom['alvoNome'] = aluno_data['nome']
    
    cupons[cupom_index] = cupom
    
    # Registrar no histórico
    historico = prof_data.get('historicoAcoes', [])
    historico.append({
        'tipo': 'penalizacao',
        'cupomId': cupom_id,
        'alunoId': aluno_id,
        'alunoNome': aluno_data['nome'],
        'aluno Turma': aluno_data['turma'],
        'pontosRemovidos': pontos_realmente_removidos,
        'data': datetime.now(),
        'motivo': 'Uso de Cupom de Redução de Pontos'
    })
    
    prof_ref.update({
        'cuponsEspeciais': cupons,
        'historicoAcoes': historico
    })
    
    return True, f"✅ {pontos_realmente_removidos} pontos removidos de {aluno_data['nome']} ({aluno_data['turma']})"

def listar_alunos_da_turma(db, turma):
    """
    Lista todos os alunos de uma turma específica
    
    Args:
        db: Firestore client
        turma: Código da turma (ex: '701')
    
    Returns:
        Lista de alunos
    """
    alunos = []
    
    usuarios_ref = db.collection('usuarios')
    query = usuarios_ref.where('turma', '==', turma).where('tipo_usuario', '==', 'aluno')
    
    for doc in query.stream():
        data = doc.to_dict()
        # Remove senha
        if 'senha' in data:
            del data['senha']
        alunos.append(data)
    
    # Ordenar por pontos (maior para menor)
    alunos = sorted(alunos, key=lambda x: x.get('pontos', 0), reverse=True)
    
    return alunos

def get_ranking_turma(db, turma):
    """
    Obtém ranking de uma turma específica
    
    Args:
        db: Firestore client
        turma: Código da turma
    
    Returns:
        Lista ordenada de alunos
    """
    alunos = listar_alunos_da_turma(db, turma)
    
    # Já vem ordenado por pontos
    return alunos

def get_estatisticas_professor(db, professor_id):
    """
    Obtém estatísticas do professor
    
    Args:
        db: Firestore client
        professor_id: ID do professor
    
    Returns:
        dict com estatísticas
    """
    prof_ref = db.collection('usuarios').document(str(professor_id))
    prof_doc = prof_ref.get()
    
    if not prof_doc.exists:
        return None
    
    prof_data = prof_doc.to_dict()
    
    stats = {
        'nome': prof_data['nome'],
        'disciplina': prof_data['disciplina'],
        'turmas': prof_data['turmas'],
        'pontos': prof_data['pontos'],
        'cupons_disponiveis': len([c for c in prof_data.get('cuponsEspeciais', []) if not c['usado']]),
        'cupons_usados': len([c for c in prof_data.get('cuponsEspeciais', []) if c['usado']]),
        'total_penalizacoes': len([a for a in prof_data.get('historicoAcoes', []) if a['tipo'] == 'penalizacao']),
        'total_pontos_removidos': sum(a.get('pontosRemovidos', 0) for a in prof_data.get('historicoAcoes', []) if a['tipo'] == 'penalizacao')
    }
    
    # Estatísticas por turma
    stats['alunos_por_turma'] = {}
    for turma in prof_data['turmas']:
        alunos = listar_alunos_da_turma(db, turma)
        stats['alunos_por_turma'][turma] = {
            'total': len(alunos),
            'media_pontos': sum(a.get('pontos', 0) for a in alunos) / len(alunos) if alunos else 0,
            'primeiro_lugar': alunos[0]['nome'] if alunos else 'N/A'
        }
    
    return stats
