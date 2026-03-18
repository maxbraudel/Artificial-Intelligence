# Interview Simulator Bot

Bot Telegram qui simule un entretien d'embauche de A à Z, propulsé par un LLM (via OpenRouter).

## Ce que fait le bot

1. **Collecte du CV** — L'utilisateur envoie son CV en texte, en PDF ou en DOCX. Le bot l'analyse via le LLM et le reformate en interne.
2. **Description du poste** — L'utilisateur décrit l'entreprise et le poste visé (ou colle directement une offre d'emploi).
3. **Entretien** — Le bot pose une série de questions d'entretien (10 par défaut, configurable). Chaque question est générée par le LLM en fonction du CV, du poste et des échanges précédents. La dernière question est toujours « Avez-vous une remarque ou une question avant de finir cet entretien ? ».
4. **Bilan** — Une fois l'entretien terminé, le bot génère un compte rendu détaillé : impression générale, analyse question par question, forces, points positifs, axes d'amélioration et note sur 10.
5. **Beast Mode** — Si l'utilisateur est offensant ou provocateur à n'importe quel moment de la conversation, le bot bascule en mode clash et utilise le CV du candidat contre lui.

## Architecture

```
bot.py                  Point d'entrée, lance le polling Telegram
config.py               Chargement des variables d'environnement
prompts.py              Templates de prompts envoyés au LLM
handlers/
  conversation.py       Logique de conversation (états, handlers)
services/
  llm.py                Client OpenAI (OpenRouter), appels au LLM
  document.py           Extraction de texte depuis PDF / DOCX
  memory.py             Persistance des sessions en JSON (dossier memory/)
```

## Configuration

Créer un fichier `.env` à la racine :

```
TELEGRAM_TOKEN=<token du bot Telegram>
OPENROUTER_KEY=<clé API OpenRouter>
NUMBER_OF_INTERVIEW_QUESTIONS=10
```

Le modèle LLM est configuré dans `config.py`.

## Installation et lancement

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bot.py
```

## Dépendances

- `python-telegram-bot` — Interface avec l'API Telegram
- `python-dotenv` — Chargement des variables d'environnement depuis `.env`
- `openai` — Client API pour OpenRouter (compatible OpenAI)
- `pdfplumber` — Extraction de texte depuis les fichiers PDF
- `python-docx` — Extraction de texte depuis les fichiers DOCX
- `fpdf2` — Génération du bilan d'entretien en PDF

## Commandes Telegram

- `/start` — Démarre un nouvel entretien
- `/cancel` — Annule l'entretien en cours
