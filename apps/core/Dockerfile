FROM rasa/rasa:3.1.0-spacy-en
WORKDIR /app

USER root
RUN pip install --no-cache-dir pipenv
COPY Pipfile* ./
RUN pipenv install --skip-lock --system
RUN python -m spacy download en_core_web_sm

WORKDIR /app/apps/core

COPY --chown=1001:1001 apps/core .
RUN rasa train
RUN mv endpoints.docker.yml endpoints.yml

ARG FINNHUB_API_KEY
ENV FINNHUB_API_KEY=${FINNHUB_API_KEY}
ARG POLYGON_API_KEY
ENV POLYGON_API_KEY=${POLYGON_API_KEY}
ARG WEATHER_API_KEY
ENV WEATHER_API_KEY=${WEATHER_API_KEY}
ARG NEWS_API_KEY
ENV NEWS_API_KEY=${NEWS_API_KEY}

USER 1001
