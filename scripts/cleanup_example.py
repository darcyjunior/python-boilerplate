"""
Script para remover os arquivos de exemplo do projeto.

Uso:
  - Dry-run (não remove, só mostra):
      python scripts/cleanup_example.py --dry-run
  - Execução sem prompt:
      python scripts/cleanup_example.py --yes

Este script remove os arquivos relacionados ao exemplo prático de API de Tarefas (To-Do).
"""
import os
import shutil
from pathlib import Path
import argparse


def _is_safe_path(base_dir: Path, target: Path) -> bool:
    """Garante que o caminho alvo está dentro do diretório do projeto."""
    try:
        return target.resolve().is_relative_to(base_dir.resolve())
    except Exception:
        return False


def _targets(base_dir: Path):
    """Retorna tupla (files_to_remove, dirs_to_check)."""
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

    return files_to_remove, dirs_to_check


def remove_example(base_dir: Path, dry_run: bool = True) -> list[str]:
    """Remove os arquivos de exemplo do projeto.

    Se dry_run=True, apenas lista o que seria removido.
    """
    files_to_remove, dirs_to_check = _targets(base_dir)

    # Segurança: todos os alvos devem estar dentro de base_dir
    unsafe = [p for p in (*files_to_remove, *dirs_to_check) if not _is_safe_path(base_dir, p)]
    if unsafe:
        raise RuntimeError(f"Foram detectados caminhos inseguros fora do projeto: {unsafe}")

    planned = [str(p.relative_to(base_dir)) for p in files_to_remove if p.exists()]
    if dry_run:
        return planned

    removed: list[str] = []
    # Remove os arquivos
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
    parser = argparse.ArgumentParser(description="Remove arquivos do exemplo prático (To-Do)")
    parser.add_argument("--dry-run", action="store_true", help="Apenas mostra o que seria removido")
    parser.add_argument("--yes", action="store_true", help="Executa sem pedir confirmação")
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent
    print("📁 Diretório do projeto:", base_dir)

    try:
        plan = remove_example(base_dir, dry_run=True)
    except Exception as e:
        print(f"❌ Erro de segurança: {e}")
        raise SystemExit(2)

    if not plan:
        print("ℹ️ Nenhum arquivo de exemplo encontrado para remoção.")
        raise SystemExit(0)

    print("\n📝 Itens planejados para remoção:")
    for item in plan:
        print(f"- {item}")

    if args.dry_run and not args.yes:
        print("\n✅ Dry-run concluído. Nada foi removido.")
        raise SystemExit(0)

    if not args.yes:
        confirm = input("\nTem certeza que deseja remover os itens acima? (digite 'sim' para confirmar) ").strip().lower()
        if confirm != "sim":
            print("Operação cancelada.")
            raise SystemExit(0)

    print("\n🧹 Removendo arquivos de exemplo...")
    removed = remove_example(base_dir, dry_run=False)

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
