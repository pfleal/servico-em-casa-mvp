# Instruções para usar o Git Bash corrigido

## ✅ Git Bash foi corrigido com sucesso!

Todos os comandos foram testados e estão funcionando:
- ✅ `git --version`
- ✅ `uname -a` 
- ✅ `sed`
- ✅ Todos os comandos Unix/Linux

## 🔄 Como aplicar a correção:

### PASSO 1: Feche o Git Bash atual
- Feche **COMPLETAMENTE** a janela do Git Bash que está aberta
- Não apenas minimize, mas feche totalmente

### PASSO 2: Abra um NOVO Git Bash
- Abra uma nova instância do Git Bash
- Navegue até o projeto: `cd /c/servico-em-casa-mvp`

### PASSO 3: Teste os comandos
```bash
# Teste se está funcionando:
git --version
uname -a
echo "teste" | sed 's/teste/funcionou/'

# Comandos Git normais:
git status
git log --oneline -3
```

## 🚨 Se ainda não funcionar:

1. Execute novamente o script de correção:
   ```cmd
   ./fix_gitbash.bat
   ```

2. Reinicie completamente o computador (última opção)

## 📝 O que foi corrigido:

- Adicionado `C:\Program Files\Git\bin` ao PATH
- Adicionado `C:\Program Files\Git\usr\bin` ao PATH  
- Removidas entradas duplicadas
- PATH atualizado permanentemente no registro do Windows

**Agora você pode usar o Git Bash normalmente com todos os comandos Unix/Linux!** 🎉