name: Main Workflow

on: push

jobs:
  build:
    name: Main Workflow

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: 3.7

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v1
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Dependencies
        run: |
          pip install --upgrade pip
          pip install black

      - name: Lint with Black
        run: black app --check --verbose