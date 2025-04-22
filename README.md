title: ' akaike-email-classifier_'
sdk: docker
app_file: app.py
app_port: 7860
emoji: 🏃
colorFrom: red
colorTo: red

## Setup
```bash
pip install -r requirements.txt
```

## Train the Model
Place your dataset in the same directory and name it `combined_emails_with_natural_pii.csv`


```bash
python models.py
```
now u will get 2 files that must be present before running the python app.py command

## Run the API
```bash
uvicorn app:app --reload
```

## Endpoint
**POST /classify_email**
