"""
Script para remover os arquivos de exemplo do projeto.

Este script remove os arquivos relacionados ao exemplo prático de API de Tarefas (To-Do).
"""
import os
import shutil
from pathlib import Path

def remove_example():
    """Remove os arquivos de exemplo do projeto."""
    # Diretório base do projeto
    base_dir = Path(__file__).parent.parent
    src_dir = base_dir / "src" / "boilerplate"
    
    # Lista de arquivos e diretórios a serem removidos
    files_to_remove = [
        # Arquivos da API
        src_dir / "models" / "todo.py",
        src_dir / "services" / "todo.py",
        src_dir / "api" / "v1" / "endpoints" / "todos.py",
        src_dir / "api" / "v1" / "api.py",
        
        # Arquivos da interface web
        src_dir / "templates" / "todos.html",
        src_dir / "static" / "js" / "todos.js",
        src_dir / "static" / "css" / "styles.css",
        
        # Arquivos de teste
        base_dir / "tests" / "unit" / "test_todo_service.py",
        base_dir / "tests" / "integration" / "test_todo_api.py",
        
        # Outros arquivos relacionados ao exemplo
        src_dir / "static" / "js" / "main.js",
        src_dir / "static" / "images" / "favicon.ico",
    ]
    
    # Diretórios que podem ficar vazios após a remoção
    dirs_to_check = [
        # Diretórios da API
        src_dir / "models",
        src_dir / "services",
        src_dir / "api" / "v1" / "endpoints",
        src_dir / "api" / "v1",
        src_dir / "api",
        
        # Diretórios da interface web
        src_dir / "templates",
        src_dir / "static" / "js",
        src_dir / "static" / "css",
        src_dir / "static" / "images",
        src_dir / "static" / "img",
        src_dir / "static",
        
        # Diretórios de teste
        base_dir / "tests" / "unit",
        base_dir / "tests" / "integration",
        base_dir / "tests",
        
        # Diretório de relatórios de teste
        base_dir / "htmlcov",
        
        # Diretório de cache do Python
        base_dir / "__pycache__",
        base_dir / ".pytest_cache",
    ]
    
    # Remove os arquivos
    removed = []
    for file_path in files_to_remove:
        if file_path.exists():
            try:
                if file_path.is_file():
                    file_path.unlink()
                    removed.append(str(file_path.relative_to(base_dir)))
                else:
                    shutil.rmtree(file_path)
                    removed.append(f"{str(file_path.relative_to(base_dir))}/ (diretório)")
            except Exception as e:
                print(f"Erro ao remover {file_path}: {e}")
    
    # Remove diretórios vazios (em ordem reversa para garantir que subdiretórios sejam removidos primeiro)
    for dir_path in reversed(dirs_to_check):
        try:
            if dir_path.exists() and dir_path.is_dir() and not any(dir_path.iterdir()):
                dir_path.rmdir()
                removed.append(f"{str(dir_path.relative_to(base_dir))}/ (diretório vazio)")
        except Exception as e:
            print(f"Erro ao remover diretório vazio {dir_path}: {e}")
    
    return removed

if __name__ == "__main__":
    print("Removendo arquivos de exemplo...")
    removed = remove_example()
    
    if removed:
        print("\n✅ Arquivos removidos com sucesso:")
        for item in removed:
            print(f"- {item}")
        
        print("\n📝 Ações manuais necessárias:")
        print("1. Remova as rotas relacionadas ao exemplo do arquivo main.py")
        print("2. Remova as importações não utilizadas no main.py")
        print("3. Atualize o arquivo README.md removendo as referências ao exemplo")
        print("4. Remova as dependências de desenvolvimento não utilizadas do pyproject.toml")
        print("5. Remova as configurações de teste do pytest.ini se não for mais necessário")
        print("6. Se estiver usando controle de versão, faça commit das alterações")
    else:
        print("ℹ️ Nenhum arquivo de exemplo encontrado para remoção.")
    
    # Sugestão de comandos para limpar o cache do navegador
    print("\n💡 Dica: Limpe o cache do seu navegador para garantir que as alterações tenham efeito.")
