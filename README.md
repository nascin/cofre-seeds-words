# Cofre de Seed Words de Blockchain
O Cofre de Seed Words de Blockchain é uma aplicação segura e confiável para armazenar suas seed words (palavras-chave de recuperação) de carteiras de blockchain. Este aplicativo foi desenvolvido para fornecer uma solução conveniente e protegida para garantir que suas seed words não sejam perdidas, danificadas ou acessadas por terceiros não autorizados

# Recursos
- Segurança Avançada: Todas as seed words são criptografadas e protegidas por senha antes de serem armazenadas no aplicativo.
- Organização de Carteiras: Organize suas seed words por carteiras, facilitando o acesso e a gestão de várias contas de blockchain.
- Pesquisa Rápida: Localize rapidamente suas seed words usando a funcionalidade de pesquisa integrada.
- Interface Amigável: Uma interface intuitiva e fácil de usar, projetada para oferecer uma experiência de usuário agradável.
- Gere um executável: Ótima para salvar em um pendrive e iniciar a partir dele.

# Uso
Após iniciar o aplicativo, você será recebido com uma interface de linha de comando fácil de usar. Siga as instruções exibidas na tela para criar uma nova conta, adicionar suas seed words e protegê-las com uma senha forte.

# Instalação
- Baixe ou clone este repositório para o seu ambiente local.
- Navegue até o diretório do projeto e crie um ambiente virtual: `python3 -m venv env`
- Ative com `env/Scripts/activate`, e depois instale a dependências com `pip install -r requirements.txt`
- Por fim, digite o terminal o seguinte comando: `pyinstaller --exclude-module tests -n Cofre --onefile main.py`