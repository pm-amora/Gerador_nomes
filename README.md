# Gerador de Nomes Criativos com IA

## Descrição
Este projeto é um chatbot gerador de nomes criativos para empresas, utilizando a API da OpenAI para criação de embeddings e um banco de dados vetorial com FAISS para buscas otimizadas.

## Funcionalidades
- Gera nomes criativos para empresas baseado no tipo de negócio, valores e público-alvo.
- Utiliza modelos de IA da OpenAI para criação de embeddings e geração de nomes.
- Armazena nomes gerados em uma base vetorial para evitar repetição.
- Permite que usuários selecionem e salvem seus nomes favoritos.

## Tecnologias Utilizadas
- Python
- OpenAI API
- FAISS (Facebook AI Similarity Search)
- NumPy
- Dotenv

## Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd seu-repositorio
   ```
3. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate  # Para Windows
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Crie um arquivo `.env` e adicione sua chave de API da OpenAI:
   ```
   API_KEY=your_openai_api_key_here
   ```

## Uso
Execute o script principal para iniciar o gerador de nomes:
```bash
python pt_chatbot_gerador_nomes.py
```

O chatbot solicitará informações sobre o tipo de negócio, valores da marca, público-alvo e estilo desejado para gerar sugestões de nomes criativos.

## Exemplo de Uso
1. **Tipo de negócio:** Tecnologia  
2. **Valores da marca:** Inovação, Confiança  
3. **Público-alvo:** Jovens  
4. **Estilo do nome:** Moderno  

Saída esperada:
```
Sugestões de nomes:
1. TechInova
2. FutureCore
3. InovaTech
...
```

## Contribuição
Se desejar contribuir com melhorias, siga os passos:
1. Fork este repositório.
2. Crie um branch com a sua funcionalidade (`git checkout -b minha-funcionalidade`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona minha funcionalidade'`).
4. Envie para o repositório remoto (`git push origin minha-funcionalidade`).
5. Abra um Pull Request.

## Licença
Este projeto está licenciado sob a [MIT License](LICENSE).

