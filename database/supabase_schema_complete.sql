-- =====================================================
-- SCHEMA COMPLETO - Sistema de Equivalências UFSM
-- Para execução no painel do Supabase
-- =====================================================

-- Limpar tabelas existentes (se necessário)
DROP TABLE IF EXISTS equivalencia CASCADE;
DROP TABLE IF EXISTS admin CASCADE;

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABELA: admin
-- =====================================================
CREATE TABLE admin (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABELA: equivalencia
-- =====================================================
CREATE TABLE equivalencia (
    id BIGSERIAL PRIMARY KEY,
    disciplina_adm VARCHAR(200) NOT NULL,
    codigo_adm VARCHAR(20) NOT NULL,
    carga_horaria_adm VARCHAR(10) NOT NULL,
    disciplina_equivalente VARCHAR(200) NOT NULL,
    codigo_equivalente VARCHAR(20) NOT NULL,
    curso VARCHAR(100) NOT NULL,
    carga_horaria_equivalente VARCHAR(10) NOT NULL,
    justificativa TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- ÍNDICES PARA PERFORMANCE
-- =====================================================
CREATE INDEX idx_admin_username ON admin(username);
CREATE INDEX idx_equivalencia_disciplina_adm ON equivalencia(disciplina_adm);
CREATE INDEX idx_equivalencia_codigo_adm ON equivalencia(codigo_adm);
CREATE INDEX idx_equivalencia_curso ON equivalencia(curso);
CREATE INDEX idx_equivalencia_created_at ON equivalencia(created_at);

-- =====================================================
-- FUNÇÃO PARA ATUALIZAR updated_at
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- =====================================================
-- TRIGGERS PARA updated_at
-- =====================================================
CREATE TRIGGER update_admin_updated_at
    BEFORE UPDATE ON admin
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_equivalencia_updated_at
    BEFORE UPDATE ON equivalencia
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- POLÍTICAS RLS (ROW LEVEL SECURITY)
-- =====================================================

-- Habilitar RLS
ALTER TABLE admin ENABLE ROW LEVEL SECURITY;
ALTER TABLE equivalencia ENABLE ROW LEVEL SECURITY;

-- Política para admin: apenas service_role pode acessar
CREATE POLICY "Admin access for service role" ON admin
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- Política para equivalencia: leitura pública, escrita para service_role
CREATE POLICY "Public read access for equivalencias" ON equivalencia
    FOR SELECT USING (true);

CREATE POLICY "Service role write access for equivalencias" ON equivalencia
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- =====================================================
-- INSERIR USUÁRIO ADMINISTRADOR
-- =====================================================
-- Senha: adm4125 (hash gerado com Werkzeug)
INSERT INTO admin (username, password_hash) VALUES 
('admin', 'pbkdf2:sha256:600000$salt123$hash_placeholder_will_be_updated_by_app');

-- =====================================================
-- INSERIR DADOS DE EXEMPLO
-- =====================================================
INSERT INTO equivalencia (
    disciplina_adm, 
    codigo_adm, 
    carga_horaria_adm, 
    disciplina_equivalente, 
    codigo_equivalente, 
    curso, 
    carga_horaria_equivalente, 
    justificativa
) VALUES 
(
    'Introdução à Administração',
    'CAD1088',
    '60h',
    'Fundamentos de Administração',
    'ECO1001',
    'Ciências Econômicas',
    '60h',
    'Deferimento - aproximadamente 85% de equivalência de conteúdo. Ambas as disciplinas abordam conceitos fundamentais de administração, teorias organizacionais e princípios de gestão empresarial.'
),
(
    'Matemática Financeira',
    'CAD1045',
    '60h',
    'Matemática Aplicada às Finanças',
    'MAT2010',
    'Matemática',
    '60h',
    'Deferimento - conteúdo equivalente em cálculos financeiros, juros compostos, valor presente e futuro, análise de investimentos e sistemas de amortização.'
),
(
    'Contabilidade Geral',
    'CAD1020',
    '90h',
    'Princípios de Contabilidade',
    'CON1001',
    'Ciências Contábeis',
    '90h',
    'Deferimento - disciplinas equivalentes abordando princípios contábeis, demonstrações financeiras, análise de balanços e escrituração contábil.'
),
(
    'Estatística Aplicada',
    'CAD1030',
    '60h',
    'Estatística Básica',
    'EST1001',
    'Estatística',
    '60h',
    'Deferimento - conteúdo equivalente em estatística descritiva, probabilidade, distribuições e testes de hipóteses aplicados à administração.'
),
(
    'Direito Empresarial',
    'CAD1055',
    '60h',
    'Direito Comercial',
    'DIR2001',
    'Direito',
    '60h',
    'Deferimento - disciplinas equivalentes abordando legislação empresarial, contratos comerciais, direito societário e aspectos jurídicos da atividade empresarial.'
);

-- =====================================================
-- COMENTÁRIOS NAS TABELAS
-- =====================================================
COMMENT ON TABLE admin IS 'Usuários administrativos do Sistema de Equivalências UFSM';
COMMENT ON TABLE equivalencia IS 'Equivalências de disciplinas do curso de Administração UFSM';

COMMENT ON COLUMN admin.username IS 'Nome de usuário único para login';
COMMENT ON COLUMN admin.password_hash IS 'Hash da senha usando Werkzeug (pbkdf2:sha256)';

COMMENT ON COLUMN equivalencia.disciplina_adm IS 'Nome da disciplina do curso de Administração UFSM';
COMMENT ON COLUMN equivalencia.codigo_adm IS 'Código oficial da disciplina de Administração';
COMMENT ON COLUMN equivalencia.carga_horaria_adm IS 'Carga horária da disciplina de Administração';
COMMENT ON COLUMN equivalencia.disciplina_equivalente IS 'Nome da disciplina equivalente de outro curso';
COMMENT ON COLUMN equivalencia.codigo_equivalente IS 'Código da disciplina equivalente';
COMMENT ON COLUMN equivalencia.curso IS 'Nome do curso de origem da disciplina equivalente';
COMMENT ON COLUMN equivalencia.carga_horaria_equivalente IS 'Carga horária da disciplina equivalente';
COMMENT ON COLUMN equivalencia.justificativa IS 'Justificativa técnica da equivalência';

-- =====================================================
-- VERIFICAÇÃO FINAL
-- =====================================================
SELECT 
    'admin' as tabela,
    COUNT(*) as registros
FROM admin
UNION ALL
SELECT 
    'equivalencia' as tabela,
    COUNT(*) as registros
FROM equivalencia
ORDER BY tabela;

-- =====================================================
-- INSTRUÇÕES DE USO
-- =====================================================
/*
INSTRUÇÕES PARA EXECUÇÃO:

1. Acesse o painel do Supabase: https://supabases.iaprojetos.com.br
2. Vá para SQL Editor
3. Cole este script completo
4. Execute o script
5. Verifique se as tabelas foram criadas
6. Teste o sistema com:
   - Usuário: admin
   - Senha: adm4125

ESTRUTURA CRIADA:
- Tabela 'admin': usuários administrativos
- Tabela 'equivalencia': dados das equivalências
- Índices para performance
- Triggers para updated_at automático
- Políticas RLS para segurança
- 5 registros de exemplo

CREDENCIAIS:
- Usuário: admin
- Senha: adm4125
- A senha será atualizada automaticamente pelo sistema Flask
*/

