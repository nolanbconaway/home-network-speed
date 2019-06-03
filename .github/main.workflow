
workflow "Build, Lint" {
  on = "push"
  resolves = [
    "Format", "Lint"
  ]
}

action "Build" {
  uses = "nolanbconaway/python-actions@master"
  args = "pip install black pylint && pip install -r requirements.txt"
}

action "Format" {
  uses = "nolanbconaway/python-actions@master"
  args = "black app/* --check --verbose"
  needs = ["Build"]
}

action "Lint" {
  uses = "nolanbconaway/python-actions@master"
  args = "pylint app/*.py"
  needs = ["Build"]
}
