# Build and push the container
# gcloud builds submit --tag gcr.io/book-loan-david-yalin/book-loan-app

# Build locally
# docker build -t gcr.io/book-loan-david-yalin/book-loan-app .
docker buildx build \
  --platform linux/amd64 \
  -t gcr.io/book-loan-david-yalin/book-loan-app \
  --push .
# Push to Container Registry
docker push gcr.io/book-loan-david-yalin/book-loan-app

# Deploy to Cloud Run
gcloud run deploy book-loan-service \
  --image gcr.io/book-loan-david-yalin/book-loan-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080