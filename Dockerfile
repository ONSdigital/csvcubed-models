FROM gsscogs/pythonversiontesting:v1.0.1

RUN pyenv global 3.10.0

RUN mkdir -p /workspace

WORKDIR /workspace

# Install all dependencies for project
COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-root

# Patch behave
RUN bash -c 'poetry run export python_dir=$(python -c "import site; print(site.getsitepackages()[0])") && patch -Nf -d "$python_dir/behave/formatter" -p1 < /cucumber-format.patch || true'

RUN rm -rf /workspace/*

WORKDIR /workspace

ENTRYPOINT poetry config virtualenvs.create false && poetry install && bash