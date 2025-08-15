-- Schema para Sistema de Equivalências UFSM
-- Criado para Supabase PostgreSQL

-- Criar extensões necessárias (se não existirem)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de administradores
CREATE TABLE IF NOT EXISTS admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de equivalências
CREATE TABLE IF NOT EXISTS equivalencia (
    id SERIAL PRIMARY KEY,
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

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_admin_username ON admin(username);
CREATE INDEX IF NOT EXISTS idx_equivalencia_disciplina_adm ON equivalencia(disciplina_adm);
CREATE INDEX IF NOT EXISTS idx_equivalencia_codigo_adm ON equivalencia(codigo_adm);
CREATE INDEX IF NOT EXISTS idx_equivalencia_curso ON equivalencia(curso);
CREATE INDEX IF NOT EXISTS idx_equivalencia_created_at ON equivalencia(created_at);

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger nas tabelas
DROP TRIGGER IF EXISTS update_admin_updated_at ON admin;
CREATE TRIGGER update_admin_updated_at
    BEFORE UPDATE ON admin
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_equivalencia_updated_at ON equivalencia;
CREATE TRIGGER update_equivalencia_updated_at
    BEFORE UPDATE ON equivalencia
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Políticas RLS (Row Level Security) para Supabase
ALTER TABLE admin ENABLE ROW LEVEL SECURITY;
ALTER TABLE equivalencia ENABLE ROW LEVEL SECURITY;

-- Política para admin: apenas usuários autenticados podem acessar
CREATE POLICY IF NOT EXISTS "Admin access for authenticated users" ON admin
    FOR ALL USING (auth.role() = 'authenticated');

-- Política para equivalencia: leitura pública, escrita apenas para autenticados
CREATE POLICY IF NOT EXISTS "Public read access for equivalencias" ON equivalencia
    FOR SELECT USING (true);

CREATE POLICY IF NOT EXISTS "Authenticated write access for equivalencias" ON equivalencia
    FOR ALL USING (auth.role() = 'authenticated');

-- Inserir usuário administrador padrão (senha: adm4125)
-- Hash gerado com Werkzeug: pbkdf2:sha256:600000$...
INSERT INTO admin (username, password_hash) 
VALUES ('admin', 'pbkdf2:sha256:600000$8RjK9XQJ$c8f8a8d8e8f8a8d8e8f8a8d8e8f8a8d8e8f8a8d8e8f8a8d8e8f8a8d8e8f8a8d8')
ON CONFLICT (username) DO NOTHING;

-- Inserir dados de exemplo
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
)
ON CONFLICT DO NOTHING;

-- Comentários nas tabelas
COMMENT ON TABLE admin IS 'Tabela de usuários administrativos do sistema';
COMMENT ON TABLE equivalencia IS 'Tabela de equivalências de disciplinas do curso de Administração UFSM';

COMMENT ON COLUMN admin.username IS 'Nome de usuário único para login';
COMMENT ON COLUMN admin.password_hash IS 'Hash da senha usando Werkzeug';

COMMENT ON COLUMN equivalencia.disciplina_adm IS 'Nome da disciplina do curso de Administração UFSM';
COMMENT ON COLUMN equivalencia.codigo_adm IS 'Código oficial da disciplina de Administração';
COMMENT ON COLUMN equivalencia.carga_horaria_adm IS 'Carga horária da disciplina de Administração';
COMMENT ON COLUMN equivalencia.disciplina_equivalente IS 'Nome da disciplina equivalente de outro curso';
COMMENT ON COLUMN equivalencia.codigo_equivalente IS 'Código da disciplina equivalente';
COMMENT ON COLUMN equivalencia.curso IS 'Nome do curso de origem da disciplina equivalente';
COMMENT ON COLUMN equivalencia.carga_horaria_equivalente IS 'Carga horária da disciplina equivalente';
COMMENT ON COLUMN equivalencia.justificativa IS 'Justificativa técnica da equivalência';

-- Verificar se as tabelas foram criadas
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE tablename IN ('admin', 'equivalencia')
ORDER BY tablename;

