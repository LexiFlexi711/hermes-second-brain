# Raw note — Hermes YAML fix

Datum: 2026-05-17

Context:
Hermes gaf deze fout bij opstart:
Failed to parse /home/sjoe/.hermes/config.yaml: expected '<document start>', but found '<scalar>'
line 10, column 5.

Oorzaak:
config.yaml bevatte per ongeluk gekopieerde prefixes zoals `1|`, `2|`, `10|`.

Fix:
De prefixes zijn verwijderd met een Python-regex.
Daarna gaf yaml.safe_load() de melding: YAML OK.

Status:
Hermes v0.14.0 is up-to-date.
De YAML-config is opnieuw leesbaar.
Environment check toonde geen zichtbare OPENROUTER/HERMES/ANTHROPIC/OPENAI API key in de shell.

Belangrijk:
Hermes negeerde door de YAML-fout alle eigen overrides.
Na de fix zou Hermes de custom config opnieuw moeten kunnen laden.
