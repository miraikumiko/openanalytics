FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN <<EOF
pip install ".[dev]"
pyproject-build
EOF

EXPOSE 8000

CMD ["openanalytics"]