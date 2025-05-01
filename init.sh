#!/bin/bash

# Cria diretórios
mkdir -p app gui resources

# Cria arquivos Python
touch app/__init__.py
touch app/idevice.py
touch app/config.py
touch app/logger.py
touch app/utils.py

touch gui/__init__.py
touch gui/main_window.py
touch gui/about_dialog.py
touch gui/settings_dialog.py

# Cria o arquivo principal
cat <<EOF > main.py
#!/usr/bin/env python3

def main():
    print("Bem-vindo ao libimobiledevice GUI!")

if __name__ == "__main__":
    main()
EOF

# Cria arquivos auxiliares
cat <<EOF > requirements.txt
# Dependências do projeto
# Exemplo: PyQt5 ou Tkinter, subprocess
EOF

touch README.md
touch LICENSE

# Mensagem de sucesso
echo "✅ Estrutura de projeto criada com sucesso em $(pwd)"
