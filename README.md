# LinkedIn Profile Classifier

Classifies professional profiles into categories (for example role, seniority, industry) using supervised NLP. Designed to work only with user-provided or licensed text; does not fetch or scrape data from LinkedIn.

Quick start
- python -m venv .venv && source .venv/bin/activate
- pip install -U pip
- pip install -r requirements.txt
- make help (or see commands below) to train, evaluate, and serve

Goals
- Accurate, auditable text classification with reproducible experiments
- Fast local inference and simple API for integration
- Clear data handling boundaries and privacy by default

Features
- Train with classic ML (scikit-learn) or transformer models (Hugging Face)
- Evaluation with precision/recall/F1 and confusion matrix
- CLI and FastAPI server for inference
- Config-driven experiments (YAML) and tracked artifacts
- Optional Docker image for portable deployment

Data and labeling
- Input formats
    - CSV: columns text,label
    - JSONL: {"text": "...", "label": "..."}
- Label examples (customize as needed): engineering, data, product, design, marketing, sales, operations, finance; junior, mid, senior, lead
- Ethics and compliance
    - Use only user-supplied or licensed text
    - Remove PII that is not required for classification
    - Respect the terms of any platform and local regulations

Repository structure (proposed)
- app/ FastAPI app and routing
- linkedin_classifier/
    - data/ loading, preprocessing, augmentation
    - models/ wrappers for sklearn/transformers
    - training/ train and evaluate loops
    - utils/ metrics, logging, config
    - cli.py CLI entrypoints
- configs/ YAML experiment configs
- tests/ unit and integration tests
- scripts/ convenience scripts (prepare_data, train, evaluate, serve)
- artifacts/ saved models, logs, reports (gitignored)
- requirements.txt dependencies
- pyproject.toml or setup.cfg tooling configuration
- Dockerfile container build
- .github/workflows/ci.yml CI pipeline

Environment variables
- MODEL_DIR path to trained model (default artifacts/models/latest)
- MODEL_NAME HF model id if using transformers (for example distilbert-base-uncased)
- DEVICE cpu or cuda
- API_HOST 0.0.0.0
- API_PORT 8000

Training
- Classical ML
    - python -m linkedin_classifier.training.train --config configs/baseline_sklearn.yaml
- Transformers
    - python -m linkedin_classifier.training.train --config configs/baseline_transformer.yaml
- Outputs
    - artifacts/models/<run_id> model.bin or sklearn.pkl
    - artifacts/reports/<run_id> metrics.json, confusion_matrix.png
- Tips
    - Stratify splits by label
    - Use class weights or focal loss for imbalance
    - Log seed and data snapshot for reproducibility

Evaluation
- python -m linkedin_classifier.training.evaluate --run-id <id>
- Metrics reported: accuracy, macro/micro F1, per-class Precision/Recall, ROC-AUC (if applicable)

Inference
- CLI
    - python -m linkedin_classifier.cli predict --model artifacts/models/latest "Senior data scientist building ML platforms"
- Batch
    - python -m linkedin_classifier.cli predict-file --input data/profiles.csv --text-col text --output artifacts/preds.csv
- API (FastAPI)
    - uvicorn app.main:app --host 0.0.0.0 --port 8000
    - POST /predict body: {"text": "…"} returns {"label": "data", "scores": {"data": 0.92, ...}}

Preprocessing
- Lowercasing and basic normalization (configurable)
- Optional de-duplication and sentence trimming
- Optional PII scrubbing (emails, phones) before training

Configuration (YAML)
- data: paths, splits, text/label columns, preprocess options
- model: type=sklearn|transformer, name, hyperparameters
- train: epochs, batch_size, optimizer/lr, early_stopping, seed
- eval: metrics, thresholds
- output: directories, run_name, save_best_only

Docker
- docker build -t linkedin-profile-classifier .
- docker run -p 8000:8000 -e MODEL_DIR=/models -v $(pwd)/artifacts/models/latest:/models linkedin-profile-classifier

Testing and quality
- pytest -q unit tests
- ruff check . linting
- black . formatting
- mypy . type checks (optional)
- pre-commit hooks recommended

Performance notes
- Use DistilBERT or MiniLM for low-latency CPU inference
- Enable TorchScript or ONNX Runtime for transformers
- Cache tokenizer and model; batch requests on server

Security and privacy
- Do not store raw profiles unless necessary; prefer hashed IDs
- Keep training data and artifacts out of the repo (use .gitignore)
- Review model outputs for bias; include a model card in artifacts/reports

Roadmap
- Semi-supervised learning with weak labels
- Active learning loop for annotator efficiency
- Multi-label support (for example role and seniority jointly)
- Simple web UI for batch uploads and review

Contributing
- Open an issue to discuss significant changes
- Fork and create a feature branch
- Add tests and docs; run lint and tests locally
- Submit a pull request with a clear description

License
- MIT (update if different)

Acknowledgements
- scikit-learn, Hugging Face Transformers, FastAPI, Uvicorn

Appendix: example requirements.txt
- fastapi
- uvicorn
- scikit-learn
- pandas
- numpy
- pydantic
- transformers
- torch
- evaluate
- matplotlib
- pyyaml
- ruff
- black
- pytest
- mypy
- python-dotenv
- typer
- onnxruntime (optional)
- torchmetrics (optional)