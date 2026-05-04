import click
import subprocess
import sys
import os
import re

try:
    import tomllib
except ImportError:
    import tomli as tomllib

def load_config():
    """Load config from pyproject.toml if available."""
    pyproject_path = "pyproject.toml"
    default_config = {
        "strict_mode": True,
        "min_word_count": 2000,
        "require_code_blocks": True
    }
    
    if not os.path.exists(pyproject_path):
        return default_config
        
    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            config = data.get("tool", {}).get("happyebook", {})
            default_config.update(config)
    except Exception as e:
        click.secho(f"Warning: Failed to parse pyproject.toml: {e}", fg="yellow")
        
    return default_config

@click.group()
def main():
    """Happy eBook CLI tool for building and verifying publications."""
    pass

@main.command()
def build():
    """Build the Jupyter Book."""
    click.secho("Building Jupyter Book...", fg="blue")
    
    env = os.environ.copy()
    # We could set BASE_URL here if needed, but normally CI sets it
    
    result = subprocess.run(
        [sys.executable, "-m", "jupyter_book", "build", "--html", "book"],
        env=env
    )
    
    if result.returncode != 0:
        click.secho("Build failed!", fg="red")
        sys.exit(1)
    
    click.secho("Build successful!", fg="green")

@main.command()
def check():
    """Run all pre-publication checks."""
    click.secho("Running Happy eBook checks...", fg="blue")
    config = load_config()
    strict = config.get("strict_mode", True)
    min_words = config.get("min_word_count", 2000)
    req_code = config.get("require_code_blocks", True)
    
    errors = []
    warnings = []
    
    # 1. Check Checklist
    checklist_path = "publication/RELEASE_CHECKLIST.md"
    if os.path.exists(checklist_path):
        with open(checklist_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "[ ]" in content:
                msg = f"Unchecked items found in {checklist_path}."
                if strict:
                    errors.append(msg)
                else:
                    warnings.append(msg)
    
    # 2. Check Chapters
    book_dir = "book/chapters"
    if os.path.exists(book_dir):
        for ch in os.listdir(book_dir):
            index_path = os.path.join(book_dir, ch, "index.md")
            if not os.path.exists(index_path):
                continue
                
            with open(index_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Check code block
            if req_code and "```python" not in content:
                msg = f"Chapter {ch} is missing a python code block."
                if strict:
                    errors.append(msg)
                else:
                    warnings.append(msg)
            
            # Word count
            if min_words > 0:
                text_only = re.sub(r'```python.*?```', '', content, flags=re.DOTALL)
                word_count = len(text_only)
                if word_count < min_words:
                    warnings.append(f"Chapter {ch} word count ({word_count}) is below {min_words}.")
                    
    # Print results
    for w in warnings:
        click.secho(f"WARNING: {w}", fg="yellow")
        
    for e in errors:
        click.secho(f"ERROR: {e}", fg="red")
        
    if errors:
        click.secho("Checks failed!", fg="red")
        sys.exit(1)
        
    click.secho("All checks passed!", fg="green")

if __name__ == "__main__":
    main()
