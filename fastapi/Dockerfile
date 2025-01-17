# latest python stable version in a lightweight docker image
FROM python:3.13.1-alpine3.21

# set the working directory
WORKDIR /app

# take advantage of caching to avoid an useless layer creation if nothing changed
COPY requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# take advantage of caching to avoid an useless layer creation if nothing changed
COPY . .

# run the app on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]