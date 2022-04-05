venv:
	python3 -m venv $@

.PHONY: init
init:
	python3 -m pip install -U -r requirements.txt

.PHONY: clean
clean:
	rm -rf venv
