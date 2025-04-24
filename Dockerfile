FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install spaCy model explicitly
RUN python -m spacy download en_core_web_sm

COPY --chown=user . /app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
