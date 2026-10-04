# Temperatur-Konverter

## Was macht das Projekt?
Eine kleine Python-Bibliothek, die Temperaturen zwischen Celsius, Fahrenheit und Kelvin umrechnet und Werte unter dem absoluten Nullpunkt ablehnt. Die Anwendung ist bewusst klein gehalten. Sie dient als Testfall für eine vollständige CI/CD-Pipeline mit GitHub Actions: Tests, Build, Artifact und automatisches Release.

## Pipeline im Überblick
Workflow: [`.github/workflows/pipeline.yml`](.github/workflows/pipeline.yml)

```
test ──> build ──> deploy (Environment: production)
           │          ▲
           └─> Artifact ┘
```

| Job | Zweck | Trigger / Bedingung | braucht (`needs`) | Environment | Artifact |
|---|---|---|---|---|---|
| `test` | Code auschecken, Python einrichten, pip-Cache, Dependencies installieren, `pytest` ausführen | jeder Push auf `main` und jeder Pull Request | – | – | – |
| `build` | ZIP-Paket aus `src/` bauen und hochladen | nur wenn `test` grün ist | `test` | – | lädt `temperatur-konverter` hoch |
| `deploy` | Paket herunterladen, Secret prüfen, GitHub-Release mit dem ZIP erstellen | nur bei Push auf `main` (`if`), nach Freigabe | `build` | `production` (Required reviewer, nur Branch `main`) | lädt `temperatur-konverter` herunter |

## Trigger
- `push` auf den Branch `main`: Die komplette Pipeline läuft, inklusive Deployment.
- `pull_request` (auf jeden Branch): `test` und `build` laufen, `deploy` wird **übersprungen** (`skipped`).

## Secrets und Environment
| Name | Art | Verwendung |
|---|---|---|
| `DEPLOY_TOKEN` | Repository-Secret | wird im Deploy-Job geprüft, ausgegeben wird nur die Länge |
| `DEPLOY_TARGET` | Repository-Variable (z. B. `staging`) | wird als Deployment-Ziel im Log angezeigt |
| `GITHUB_TOKEN` | automatisch von GitHub | erstellt das Release (`gh release create`) |

Secret-Werte stehen **nie** im Code, in der README oder im Log.

**Environment `production`:**
- Schutzregel *Required reviewers*: Der Deploy-Job wartet auf eine manuelle Freigabe.
- *Deployment branches*: nur `main`.

**Permissions:** Global gilt nur `contents: read`. Ausschließlich der Deploy-Job bekommt zusätzlich `contents: write` (für das Release) und `actions: read` (für das Artifact).

## Deployment
Nach einem Push auf `main` mit grünen Tests und erteilter Freigabe erstellt der Deploy-Job automatisch ein GitHub-Release `v1.0.<run_number>`, mit `temperatur-konverter.zip` als Asset.

So prüfst du es:
1. Unter **Actions** den Run öffnen, `deploy` freigeben (*Review deployments → Approve*)
2. Unter **Releases** (rechte Spalte im Repository) erscheint die neue Version mit dem ZIP-Paket

## Lokal ausführen
```bash
git clone https://github.com/S-max-ui-star/mein-projekt.git
cd mein-projekt

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

python -m pip install -r requirements.txt
python -m pytest -v                # Tests

mkdir -p build
python -m zipfile -c build/temperatur-konverter.zip src/   # Build

python -m src.konverter            # Beispielausgabe
```

