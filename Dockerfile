ARG PYTHON_VERSION=3.11.10
FROM python:${PYTHON_VERSION}-slim as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN python -m pip install uv
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
     uv pip install -r requirements.txt --system
COPY . .
EXPOSE 8501
CMD streamlit run main_app.py 
