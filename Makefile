.PHONY: sim

CWD=${CURDIR}

ifeq ($(OS), Windows_NT)
VENV=.venv_windows
PYTHON=python
VENVBIN=./${VENV}/Scripts
else ifneq ("$(wildcard /.dockerenv)","")
VENV=.venv_docker
PYTHON=python3
VENVBIN=./${VENV}/bin
else
VENV=.venv_osx
PYTHON=python3
VENVBIN=./${VENV}/bin
endif

default: help 
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## This list of Makefile targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

sim: setup_${VENV} ## Performs coverage tests and then runs the simulator
	${VENVBIN}/${PYTHON} -m robot coverage sim

run: ## Runs the robot
	${PYTHON} -m robot run

${VENV}:
	${PYTHON} -m venv ${VENV}

lint: ## Runs the linter(s)
	# From CI pipeline. We are more strict in our local check
	# --select=E9,F6,F7,F8,F4,W1,W2,W4,W5,W6,E11 --ignore W293
	${VENVBIN}/flake8 . --count --select=E9,F6,F7,F8,F4,W1,W2,W4,W5,W6,E11 --ignore W293,W503 --show-source --statistics --exclude */tests/pyfrc*,utils/yaml/*,.venv*/,venv*/

test: setup_${VENV} lint  ## Does a lint and then test
	${VENVBIN}/${PYTHON} robot.py test

coverage: setup_${VENV} test
	${VENVBIN}/${PYTHON} robot.py coverage test

setup_${VENV}: ${VENV}
	${VENVBIN}/${PYTHON} -m pip install --upgrade pip setuptools
	${VENVBIN}/pip install --pre -r ${CWD}/requirements.txt
	$(file > setup_${VENV})

clean:
	rm -f setup setup_${VENV}

realclean: clean
	rm -fr ${VENV}

docker: docker_build
	docker run --rm -ti -v $$(PWD):/src raptacon2022_build bash

docker_build:
	docker build . --tag raptacon2022_build

deploy:
	${PYTHON} robot.py deploy --no-resolve --robot 10.32.0.2
