from time import perf_counter

from fastapi import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUESTS = Counter('prediction_requests', 'Prediction HTTP responses', ['status_class'])
LATENCY = Histogram('prediction_duration_seconds', 'Prediction endpoint response time')
PREDICTIONS = Histogram('model_prediction', 'Distribution of model outputs', buckets=[0.5, 1, 2, 3, 5, 8, 12, 20, 35])
AGE = Histogram('input_age_years', 'Age in successful requests, years', buckets=[2, 5, 8, 12, 16, 25])


def observe(prediction, age):
    PREDICTIONS.observe(prediction)
    AGE.observe(age)


def instrument(app):
    for status in ('2xx', '4xx', '5xx'):
        REQUESTS.labels(status)

    @app.middleware('http')
    async def measure(request, call_next):
        if request.url.path != '/api/prediction':
            return await call_next(request)
        start = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            REQUESTS.labels('5xx').inc()
            raise
        else:
            REQUESTS.labels(f'{response.status_code // 100}xx').inc()
            return response
        finally:
            LATENCY.observe(perf_counter() - start)

    @app.get('/metrics', include_in_schema=False)
    def metrics():
        return Response(generate_latest(), headers={'Content-Type': CONTENT_TYPE_LATEST})
