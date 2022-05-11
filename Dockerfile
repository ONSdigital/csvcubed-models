FROM gsscogs/pythonversiontesting:v1.0.1

RUN pyenv global 3.10.0

WORKDIR /

# Install all dependencies for project
COPY poetry.lock /
COPY pyproject.toml /

RUN poetry export --format requirements.txt --output /requirements.txt --without-hashes --dev
# Install all dependencies listed in text file to the test environment.
RUN pip install --requirement /requirements.txt

# Patch behave
RUN bash -c 'export python_dir=$(python -c "import site; print(site.getsitepackages()[0])") && patch -Nf -d "$python_dir/behave/formatter" -p1 < /cucumber-format.patch || true'

RUN rm /poetry.lock /pyproject.toml /requirements.txt

WORKDIR /workspace