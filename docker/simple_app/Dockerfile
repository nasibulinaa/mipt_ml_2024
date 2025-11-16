FROM python:3.12.3-alpine3.20 AS builder

# ONLINE step, download dependencies
COPY requirements.txt .
RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip \
    pip wheel -r requirements.txt -w wheels/

# OFFLINE step, install dependencies and copy app files
FROM python:3.12.3-alpine3.20
# Do not trigger rebuild of this layers if requirements was not changed
COPY requirements.txt .
RUN --mount=type=bind,from=builder,source=wheels,target=/wheels \
    pip install --no-index --find-links /wheels -r requirements.txt  
COPY . .

ENV FLASK_ENV=production

CMD ["python", "app.py"]