workflow "Lint" {
  resolves = ["Black Code Formatter"]
  on = "push"
}

action "Black Code Formatter" {
  uses = "lgeiger/black-action@v1.0.1"
}
