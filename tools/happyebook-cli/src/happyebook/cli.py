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
    
    # 0. Check Required Files
    required_files = ['README.md', 'CITATION.cff', 'LICENSE', 'publication/RELEASE_CHECKLIST.md', 'book/index.md', 'book/preface.md', 'book/myst.yml']
    for req_file in required_files:
        if not os.path.exists(req_file):
            errors.append(f"Missing required file: {req_file}")
            
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
                    
    # 2. Check Placeholders in CITATION.cff
    if os.path.exists("CITATION.cff"):
        with open("CITATION.cff", "r", encoding="utf-8") as f:
            cit_content = f.read()
            for ph in ['YourLastName', 'YourFirstName', 'TODO_FAMILY_NAME', 'TODO_GIVEN_NAME', 'Repo Owner']:
                if ph in cit_content:
                    errors.append(f"Placeholder {ph} found in CITATION.cff.")
    
    # 3. Check Chapters and Linkage
    book_dir = "book/chapters"
    myst_content = ""
    if os.path.exists("book/myst.yml"):
        with open("book/myst.yml", "r", encoding="utf-8") as f:
            myst_content = f.read()
            
    if os.path.exists(book_dir):
        for ch in sorted(os.listdir(book_dir)):
            if not ch.startswith("ch"):
                continue
            
            # Check myst.yml
            if f"{ch}/index.md" not in myst_content:
                errors.append(f"book/myst.yml does not reference {ch}/index.md")
                
            # Check example & test dirs
            chapter_key = ch.split("-")[0] # e.g. 'ch01'
            if not os.path.exists(f"examples/{chapter_key}"):
                errors.append(f"Missing example directory for {chapter_key} at examples/{chapter_key}")
                
            test_exists = any(f.startswith(f"test_{chapter_key}") for f in os.listdir("tests")) if os.path.exists("tests") else False
            if not test_exists:
                errors.append(f"Missing test file for {chapter_key} under tests/")

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
                    
            if req_code and "請在專案根目錄執行" not in content:
                msg = f"Chapter {ch} is missing root execution instruction ('run in project root')."
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
                    
    # 4. Run Pytest
    click.secho("Running pytest...", fg="blue")
    pytest_res = subprocess.run([sys.executable, "-m", "pytest", "-q", "-ra"])
    if pytest_res.returncode != 0:
        errors.append("Pytest suite failed.")
                    
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
