from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1]

def wrap_pre(text: str, title: str) -> str:
    return f"""<!doctype html>
<html><head><meta charset='utf-8'><title>{title}</title></head>
<body><h1>{title}</h1><pre style='white-space:pre-wrap'>{text}</pre></body></html>"""

def main():
    # Flake8
    f_flake = BASE / 'analysis_flake8.txt'
    if f_flake.exists():
        content = f_flake.read_bytes().decode('utf-8', errors='replace')
        (BASE / 'report_flake8.html').write_text(wrap_pre(content, 'Flake8 Report'), encoding='utf-8')
        print('Generated report_flake8.html')

    # Pylint
    f_pylint = BASE / 'analysis_pylint.txt'
    if f_pylint.exists():
        content = f_pylint.read_bytes().decode('utf-8', errors='replace')
        (BASE / 'report_pylint.html').write_text(wrap_pre(content, 'Pylint Report'), encoding='utf-8')
        print('Generated report_pylint.html')

    # Bandit JSON -> pretty
    f_bandit = BASE / 'analysis_bandit.json'
    if f_bandit.exists():
        data = json.loads(f_bandit.read_bytes().decode('utf-8', errors='replace'))
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        (BASE / 'report_bandit.html').write_text(wrap_pre(pretty, 'Bandit Report (JSON)'), encoding='utf-8')
        print('Generated report_bandit.html')

if __name__ == '__main__':
    main()
