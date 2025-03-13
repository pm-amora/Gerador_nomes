import openai
from dotenv import load_dotenv
import os
import numpy as np
import faiss

print("Inicializando prompt... Aguarde.")

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura a API key da OpenAI
openai.api_key = os.getenv("API_KEY")

if not openai.api_key:
    raise ValueError("Erro: API_KEY não encontrada. Verifique o arquivo .env.")

# Função para gerar embeddings
def gerar_embedding(texto):
    try:
        response = openai.Embedding.create(
            input=texto,
            model="text-embedding-ada-002"
        )
        return np.array(response['data'][0]['embedding'], dtype=np.float32)
    except Exception as e:
        print(f"Erro ao gerar embedding para {texto}: {e}")
        return None

# Classe para gerir base de dados vectorial
class VectorDatabase:
    def __init__(self):
        self.index = faiss.IndexFlatL2(1536)
        self.data = []

    def add(self, text, metadata):
        embedding = gerar_embedding(text)
        if embedding is not None:
            self.index.add(np.array([embedding]))
            self.data.append(metadata)

    def search(self, query, k=5):
        query_embedding = gerar_embedding(query)
        if query_embedding is not None:
            distances, indices = self.index.search(np.array([query_embedding]), k)
            return [self.data[i] for i in indices[0] if i < len(self.data)]
        return []

def criar_base_dados():
    db = VectorDatabase()
    exemplos = [
        {"tipo": "tecnologia", "nome": "TechInova", "valores": "inovação, confiança", "publico": "empresas"},
        {"tipo": "tecnologia", "nome": "FutureCore", "valores": "inovação, sustentabilidade", "publico": "jovens"},
        {"tipo": "moda", "nome": "ChicStyle", "valores": "elegância, modernidade", "publico": "mulheres"},
        {"tipo": "alimentação", "nome": "FreshBites", "valores": "saúde, sustentabilidade", "publico": "famílias"},
    ]
    for exemplo in exemplos:
        db.add(exemplo["nome"], exemplo)
    return db

def recuperar_informacoes(db, tipo, valores, publico):
    query = f"{tipo} {valores} {publico}"
    resultados = db.search(query, k=3)
    return resultados

def obter_informacoes():
    print("Bem-vindo ao Gerador de Nomes Criativos com IA!\n")
    tipo_negocio = input("Qual é o tipo de negócio? (ex.: tecnologia, moda, alimentação): ")
    valores = input("Quais são os valores da sua marca? (ex.: inovação, confiança, sustentabilidade): ")
    publico_alvo = input("Quem é o seu público-alvo? (ex.: jovens, empresas, famílias): ")
    estilo = input("Qual estilo de nome prefere? (ex.: moderno, clássico, divertido): ")
    return tipo_negocio, valores, publico_alvo, estilo

# Armazena nomes únicos já gerados na execução
nomes_gerados_globais = set()

def gerar_nomes_ia(tipo, valores, publico, estilo, exemplos, total_nomes_desejado=10):
    exemplos_str = "\n".join([f"- {ex['nome']} (Valores: {ex['valores']}, Público: {ex['publico']})" for ex in exemplos])
    
    # Variável local para coletar novos nomes
    novos_nomes = set()

    while len(novos_nomes) < total_nomes_desejado:
        prompt = (
            f"Aqui estão alguns exemplos de nomes de empresas relevantes:\n{exemplos_str}\n\n"
            f"Gere {total_nomes_desejado} nomes criativos em português para uma empresa de {tipo}, que valoriza {valores} e tem como público-alvo {publico}. "
            f"Os nomes devem ter um estilo {estilo}, ser criativos e não ter mais de 2 palavras. "
            f"Evite nomes já apresentados: {', '.join(nomes_gerados_globais)}.\n"
            f"Por favor, retorne apenas os nomes, um por linha, sem números ou marcadores."
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um assistente criativo especializado em criar nomes em português para empresas."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens = min(80, 4000 - len(prompt.split())), #ajuste dinâmico de max_tokens para evitar gastar tokens desnecessários e melhorar tempo de resposta
                temperature=1.2
            )
            nomes = response.choices[0].message.content.strip().split('\n')
            
            for nome in nomes:
                nome_limpo = nome.strip()
                if nome_limpo not in nomes_gerados_globais and len(nome_limpo.split()) <= 2:
                    novos_nomes.add(nome_limpo)

            # Atualiza o conjunto global com novos nomes únicos
            nomes_gerados_globais.update(novos_nomes)

        except Exception as e:
            print(f"Erro ao gerar nomes: {e}")

    return sorted(novos_nomes)[:total_nomes_desejado]

def main():
    db = criar_base_dados()
    tipo, valores, publico, estilo = obter_informacoes()
    exemplos = recuperar_informacoes(db, tipo, valores, publico)

    favoritos = []
    print("Inicializando geração de nomes... Aguarde.")
    while True:
        nomes_sugeridos = gerar_nomes_ia(tipo, valores, publico, estilo, exemplos, total_nomes_desejado=10)
        if not nomes_sugeridos:
            print("Não foi possível gerar nomes no momento. Tente novamente mais tarde.")
            break

        print("\nSugestões de nomes:")
        for i, nome in enumerate(nomes_sugeridos, 1):
            print(f"{i}. {nome}")
        
        escolha = input("\nSalvar algum nome? (Números separados por vírgula ou Enter para ignorar): ")
        if escolha:
            escolhas = escolha.split(",")
            for num in escolhas:
                if num.strip().isdigit():
                    idx = int(num.strip())
                    if 1 <= idx <= len(nomes_sugeridos):
                        favoritos.append(nomes_sugeridos[idx - 1])
                        print(f"Nome '{nomes_sugeridos[idx - 1]}' adicionado aos favoritos!")

        continuar = input("\nMais sugestões? (s/n): ")
        print("Inicializando geração de nomes... Aguarde.")
        if continuar.lower() != 's':
            break

    if favoritos:
        print("\nNomes favoritos:")
        for nome in favoritos:
            print(f"- {nome}")
    else:
        print("\nNenhum nome salvo nos favoritos.")
    
    print("\nObrigado por usar o Gerador de Nomes Criativos com IA! 🚀")

if __name__ == "__main__":
    main()