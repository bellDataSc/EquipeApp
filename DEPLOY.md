# 📖 Guia Completo de Deploy

## 🚀 Opção 1: Deploy Direto no GitHub + Streamlit Cloud

### Passo 1: Subir para o GitHub
```bash
# No diretório EquipeApp
git init
git add .
git commit -m "Primeiro commit - Sistema de Controle de Equipe"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/EquipeApp.git
git push -u origin main
```

### Passo 2: Deploy no Streamlit Cloud
1. Acesse https://share.streamlit.io
2. Faça login com GitHub
3. Clique em "New app"
4. Selecione seu repositório "EquipeApp"
5. Arquivo principal: `app.py`
6. Clique em "Deploy"

## ⚡ Opção 2: Fork deste Projeto
1. Faça fork deste repositório
2. Acesse https://share.streamlit.io
3. Conecte com GitHub
4. Deploy automático!

## 🔧 Personalização Rápida

### Alterar Cores do Tema
Edite as variáveis CSS no início do `app.py`:
- `#667eea` - Cor primária (azul-roxo)
- `#764ba2` - Cor secundária (roxo)
- `#e74c3c` - Prioridade alta (vermelho)
- `#f39c12` - Prioridade média (laranja)
- `#27ae60` - Prioridade baixa (verde)

### Adicionar Novos Campos
No arquivo `app.py`, procure por `CREATE TABLE` e adicione campos conforme necessário.

## 📱 Teste Local Antes do Deploy
```bash
streamlit run app.py
```
Acesse http://localhost:8501

## 🛡️ Segurança para Produção
- O banco SQLite é local ao contêiner
- Para dados persistentes, considere PostgreSQL
- Para equipes maiores, adicione autenticação

---
✅ **Seu app estará online em poucos minutos!**
