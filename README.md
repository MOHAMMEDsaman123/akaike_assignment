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
POST /classify_email

## Input Img
![image](https://github.com/user-attachments/assets/b22fd351-2dd7-4fb4-b47c-0f383698f04c)

## Output Img
![image](https://github.com/user-attachments/assets/9bf6d9d4-e98d-4ca1-a0de-a14854f918ae)

