import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class SupabaseConfig:
    """Configuração do cliente Supabase"""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL', 'https://supabases.iaprojetos.com.br')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzE1MDUwODAwLAogICJleHAiOiAxODcyODE3MjAwCn0.TKsuZpcWuZTmGvi2ZihI_xNTTWKdGUJ_9jpf49rIHLE')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogInNlcnZpY2Vfcm9sZSIsCiAgImlzcyI6ICJzdXBhYmFzZSIsCiAgImlhdCI6IDE3MTUwNTA4MDAsCiAgImV4cCI6IDE4NzI4MTcyMDAKfQ.3HrXvFpCTuI8a9NPJjNY-frjGSx0iwMbhO9Gah9RkVs')
        
        # Cliente público (para operações de leitura)
        self.client = create_client(self.url, self.anon_key)
        
        # Cliente admin (para operações administrativas)
        self.admin_client = create_client(self.url, self.service_role_key)
    
    def get_client(self, admin=False) -> Client:
        """
        Retorna o cliente Supabase apropriado
        
        Args:
            admin (bool): Se True, retorna cliente admin. Se False, retorna cliente público.
        
        Returns:
            Client: Cliente Supabase configurado
        """
        return self.admin_client if admin else self.client
    
    def test_connection(self):
        """Testa a conexão com o Supabase"""
        try:
            # Tenta fazer uma consulta simples
            response = self.client.table('equivalencias').select('*').limit(1).execute()
            return True, "Conexão com Supabase estabelecida com sucesso!"
        except Exception as e:
            return False, f"Erro na conexão com Supabase: {str(e)}"

# Instância global do Supabase
supabase_config = SupabaseConfig()

