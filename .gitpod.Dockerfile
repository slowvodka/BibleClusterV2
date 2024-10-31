FROM gitpod/workspace-python

RUN pyenv install 3.12 \
    && pyenv global 3.12