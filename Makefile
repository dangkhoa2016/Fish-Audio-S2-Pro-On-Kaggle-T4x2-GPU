SHELL := /bin/bash

.PHONY: audit json shell python links weights status

audit: shell python json links weights
	@git diff --check
	@echo "REPOSITORY_AUDIT=PASS"

shell:
	@for f in scripts/*.sh; do bash -n "$$f"; done
	@echo "SHELL_SYNTAX=PASS"

python:
	@python3 -m compileall -q scripts
	@rm -rf scripts/__pycache__
	@echo "PYTHON_COMPILE=PASS"

json:
	@python3 -c 'from pathlib import Path; import json; [json.loads(p.read_text()) for p in Path(".").rglob("*.json") if ".git" not in p.parts]; print("JSON_VALIDATION=PASS")'

links:
	@python3 -c 'from pathlib import Path; import re,urllib.parse; bad=[(str(p),t) for p in Path(".").rglob("*.md") for _,t in re.findall(r"\[([^\]]+)\]\(([^)]+)\)",p.read_text(errors="ignore")) if not t.startswith(("http://","https://","#","mailto:")) and (u:=urllib.parse.unquote(t.split("#",1)[0])) and not (p.parent/u).resolve().exists()]; print("MARKDOWN_LINKS=PASS" if not bad else bad); raise SystemExit(bool(bad))'

weights:
	@! git ls-files | grep -Ei '\.(safetensors|pth|pt|ckpt|bin)$$'
	@echo "MODEL_WEIGHT_POLICY=PASS"

status:
	@git status --short
