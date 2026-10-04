# Abgabe – Projektarbeit Tag 5

## Pipeline-Architektur

| Job | Zweck | Trigger / Bedingung | braucht (`needs`) | Environment | Artifact |
|---|---|---|---|---|---|
| `test` | Dependencies installieren (mit Cache), Tests ausführen | `push` auf `main`, `pull_request` | – | – | – |
| `build` | ZIP-Paket bauen | nach grünem `test` | `test` | – | Upload `temperatur-konverter` |
| `deploy` | Release mit Paket erstellen | `if: github.event_name == 'push' && github.ref == 'refs/heads/main'` | `build` | `production` (Required reviewers, Branch `main`) | Download `temperatur-konverter` |

**Leitfragen:**
- *Welche Jobs braucht man mindestens?* `test` und `deploy`. `build` ist als eigener Job abgetrennt, damit die Rollen sauber getrennt sind.
- *Was wird zum Artifact?* Das ZIP aus `src/`. `deploy` lädt es herunter und baut nicht ein zweites Mal.
- *Wo greift eine Bedingung?* Im `deploy`-Job: nur bei Push auf `main`, nicht bei Pull Requests.
- *Welche Rechte braucht welcher Job?* `test` und `build` brauchen nur `contents: read`. `deploy` braucht zusätzlich `contents: write` und `actions: read`.
- *Woher kommen Zugangsdaten?* Aus Repository-Secrets und `GITHUB_TOKEN`. Sichtbar sind sie nur für Admins des Repos, im Log werden sie maskiert.

## Abschluss-Challenge: die 6 Probleme

| # | Symptom / Risiko | Ursache | Fix |
|---|---|---|---|
| 1 | `setup-python` sucht Version `3.1`, Run bricht ab | `python-version: 3.10` ohne Anführungszeichen. YAML liest das als Zahl `3.1` | `python-version: "3.10"` bzw. `${{ env.PYTHON_VERSION }}` |
| 2 | `No module named pytest` / `pytest: command not found` | Test-Step steht **vor** dem Install-Step | Erst `pip install -r requirements.txt`, dann testen |
| 3 | `Could not open requirements file ... 'requirement.txt'` | Tippfehler im Dateinamen (fehlendes `s`) | `requirements.txt` |
| 4 | `build` bricht ab (`No such file or directory: 'src/'`) und läuft auch bei roten Tests | Kein `actions/checkout@v4` im Job und kein `needs: test` | `checkout` ergänzen und `needs: test` setzen |
| 5 | Deployment läuft bei jedem Push/PR ohne Freigabe und schreibt das Secret direkt in `run` (Risiko: Leak, z. B. bei Teilstrings oder Umformungen) | Keine `if`-Bedingung, kein `needs`, kein `environment`, Secret direkt im Skript verwendet | `needs`, `if: github.ref == 'refs/heads/main'`, `environment: production`; Secret nur über `env:` übergeben und nur die Länge ausgeben |
| 6 | Cache wird nie erneuert, Installationen nutzen dauerhaft alte Pakete | Statischer Key `pip-cache` ohne `hashFiles()` | `key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}` plus `restore-keys` |

**Weitere Auffälligkeiten (nicht Teil der sechs):**
- `release` hat kein `download-artifact`, deshalb existiert `build/app.zip` dort nicht.
- Der Cache steht im `release`-Job, wo gar nichts installiert wird. Er gehört in den `test`-Job.
- Ohne `checkout` braucht `gh release create` die Angabe `GH_REPO: ${{ github.repository }}` bzw. `--repo`, sonst fehlt der Repo-Kontext. Das betrifft auch die Musterlösung A2.

Alle Punkte sind in [`.github/workflows/pipeline.yml`](../.github/workflows/pipeline.yml) behoben.

## Definition of Done

- [x] Eigenes Repository mit `src/`, `tests/`, `requirements.txt`, `README.md`
- [x] Anwendung mit 7 automatisierten Tests, lokal grün
- [x] Workflow startet bei `push` und `pull_request`
- [x] Drei Jobs, verbunden über `needs`
- [x] Dependencies werden erst installiert, dann wird getestet
- [x] Build erzeugt ein ZIP-Paket
- [x] Artifact wird in `build` hochgeladen und in `deploy` heruntergeladen
- [x] Cache mit `hashFiles()` im Key
- [x] Secret `DEPLOY_TOKEN` wird verwendet, im Log steht nur die Länge
- [ ] Environment `production` mit Required reviewers und Branch-Regel *(in den GitHub-Settings anlegen)*
- [x] `permissions: contents: read` global, im Deploy-Job erweitert
- [x] `if`-Bedingung am Deploy-Job
- [x] Deployment nur auf `main` und nur nach grünen Tests
- [ ] Release mit Paket als Asset automatisch entstanden *(nach dem ersten Push prüfen)*
- [x] README erklärt Zweck, Pipeline, Trigger, Secrets, Deployment und lokales Ausführen
- [x] Keine Secret-Werte in Logs, README, Commits oder Artifacts
- [x] Alle sechs Challenge-Probleme dokumentiert und behoben

## Links (nach dem Push ausfüllen)
- Repository: `https://github.com/<user>/mein-projekt`
- Release: `https://github.com/<user>/mein-projekt/releases/tag/v1.0.<n>`
