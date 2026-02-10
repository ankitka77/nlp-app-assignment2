# Task B: RESTful API Enhancement Plan for Sentiment Analysis Application

## Executive Summary

This document outlines a comprehensive plan to enhance the Sentiment Analysis Application with enterprise-grade RESTful API capabilities. The enhancements will enable external applications to access the sentiment analysis engine through secure, scalable, and well-documented APIs.

---

## 1. Introduction

### 1.1 Purpose
The purpose of this enhancement is to expose the Sentiment Analysis engine as a RESTful API that can be consumed by external applications, mobile clients, and third-party integrations.

### 1.2 Scope
This plan covers:
- API Design and Architecture
- Authentication & Authorization
- Rate Limiting & Quota Management
- API Versioning
- Error Handling & Standardization
- Documentation & Developer Experience
- Monitoring & Analytics
- Deployment & Scalability

### 1.3 Target Users
- Third-party application developers
- Mobile app developers
- Data analysts requiring batch processing
- Enterprise clients needing API integration

---

## 2. Current State Analysis

### 2.1 Existing Implementation
The current application provides:
- **Hybrid NLP Engine**: Combines VADER and TextBlob with custom keyword weighting.
- **Fixed Thresholds**: Improved classification for nuanced/mixed reviews.
- **Batch Processing**: Automatic paragraph detection and multi-topic analysis for files.
- **High Capacity**: Supports up to 50,000 characters and 10MB file uploads.
- **Interactive UI**: Bar charts, loading animations, and batch summaries.
- **Standardized API**: Robust health checks and detailed JSON responses.

### 2.2 Remaining Limitations
- No API-level authentication (JWT/API Keys).
- No per-user rate limiting (Limiter).
- No external webhook support.
- No Swagger/OpenAPI documentation.

---

## 3. Proposed Enhancement Architecture

### 3.1 Core Components

```
┌─────────────────────────────────────────────────────────┐
│                    External Clients                      │
├─────────────────────────────────────────────────────────┤
│              REST API Gateway / Load Balancer            │
├─────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────┐ │
│  │  Auth Service  │  │  Rate Limiter  │  │  Logger    │ │
│  └────────────────┘  └────────────────┘  └────────────┘ │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────┐  │
│  │      Enhanced RESTful API Endpoints (v1)        │  │
│  │  ┌─────────────┐  ┌─────────────────────────┐  │  │
│  │  │ Sentiment   │  │ Batch Processing        │  │  │
│  │  │ Analysis    │  │ Job Management          │  │  │
│  │  └─────────────┘  └─────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────┐   │
│  │  Sentiment Analyzer (NLP Core)                 │   │
│  │  - VADER Analysis                              │   │
│  │  - TextBlob Analysis                           │   │
│  │  - Text Preprocessing                          │   │
│  └────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │
│  │ Database │  │  Cache   │  │ Message Queue    │    │
│  │ (User/   │  │ (Redis)  │  │ (RabbitMQ/      │    │
│  │ Webhooks)│  │          │  │  Celery)         │    │
│  └──────────┘  └──────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### 3.2 API Versioning Strategy

```
/api/v1/                  - Current version
/api/v2/                  - Future version with breaking changes
/api/{version}/sentiment/ - Sentiment analysis endpoints
/api/{version}/models/    - Model management endpoints
/api/{version}/webhooks/  - Webhook management
/api/{version}/auth/      - Authentication endpoints
```

---

## 4. Authentication & Security

### 4.1 JWT-Based Authentication

#### Implementation
```python
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    # Verify credentials
    access_token = create_access_token(identity=user_id)
    return {'access_token': access_token}

@app.route('/api/v1/sentiment/analyze', methods=['POST'])
@jwt_required()
def analyze():
    # Protected endpoint
    pass
```

#### Token Structure
```json
{
    "sub": "user_id",
    "iat": 1234567890,
    "exp": 1234654290,
    "scope": ["sentiment_analysis", "batch_processing"],
    "rate_limit": 1000
}
```

### 4.2 API Key Authentication (Alternative)

For server-to-server communication:
```python
@app.before_request
def verify_api_key():
    api_key = request.headers.get('X-API-Key')
    if not is_valid_api_key(api_key):
        return {'error': 'Unauthorized'}, 401
```

### 4.3 OAuth 2.0 Support

For future social login integration:
```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='...',
    client_secret='...',
    server_metadata_url='...',
    client_kwargs={'scope': 'openid email profile'}
)
```

---

## 5. Rate Limiting & Quota Management

### 5.1 Implementation

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/v1/sentiment/analyze', methods=['POST'])
@jwt_required()
@limiter.limit("30 per hour")
def analyze():
    pass
```

### 5.2 Tiered Pricing Model

| Tier | Requests/Hour | Requests/Day | Batch Size | Cost |
|------|---------------|--------------|-----------|------|
| Free | 10 | 100 | 5 | $0 |
| Basic | 100 | 1000 | 50 | $9/month |
| Professional | 500 | 10000 | 500 | $49/month |
| Enterprise | Unlimited | Unlimited | Unlimited | Custom |

### 5.3 Quota Headers

Response headers include quota information:
```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1234567890
X-RateLimit-Retry-After: 3600
```

---

## 6. Error Handling & Standardization

### 6.1 Standardized Response Format

#### Success Response
```json
{
    "status": "success",
    "code": 200,
    "message": "Operation completed successfully",
    "data": {
        "request_id": "req_12345",
        "sentiment": "positive",
        "confidence": 0.85
    },
    "error": null,
    "timestamp": "2025-01-31T10:30:00Z"
}
```

#### Error Response
```json
{
    "status": "error",
    "code": 400,
    "message": "Invalid request",
    "data": null,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Missing required field: text",
        "details": {
            "field": "text",
            "reason": "required"
        }
    },
    "timestamp": "2025-01-31T10:30:00Z"
}
```

### 6.2 HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful analysis |
| 201 | Created | New webhook registered |
| 202 | Accepted | Batch job queued |
| 400 | Bad Request | Missing required field |
| 401 | Unauthorized | Invalid API key |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Endpoint not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal error |

### 6.3 Error Codes

```python
ERROR_CODES = {
    'VALIDATION_ERROR': 'Invalid input parameters',
    'AUTHENTICATION_ERROR': 'Invalid credentials',
    'AUTHORIZATION_ERROR': 'Insufficient permissions',
    'NOT_FOUND': 'Resource not found',
    'RATE_LIMIT_ERROR': 'Rate limit exceeded',
    'SERVER_ERROR': 'Internal server error',
    'TIMEOUT_ERROR': 'Request timeout',
    'UNSUPPORTED_LANGUAGE': 'Language not supported'
}
```

---

## 7. Endpoint Specifications

### 7.1 Authentication Endpoints

#### POST /api/v1/auth/register
Register new API user
```
Request:
{
    "username": "user@example.com",
    "password": "secure_password",
    "organization": "Acme Corp"
}

Response:
{
    "status": "success",
    "data": {
        "user_id": "usr_12345",
        "api_key": "sk_live_abcd1234...",
        "created_at": "2025-01-31T10:30:00Z"
    }
}
```

#### POST /api/v1/auth/login
Authenticate and get JWT token
```
Request:
{
    "email": "user@example.com",
    "password": "secure_password"
}

Response:
{
    "status": "success",
    "data": {
        "access_token": "eyJhbGc...",
        "token_type": "Bearer",
        "expires_in": 86400
    }
}
```

#### POST /api/v1/auth/refresh
Refresh JWT token
```
Headers:
Authorization: Bearer {refresh_token}

Response:
{
    "status": "success",
    "data": {
        "access_token": "eyJhbGc..."
    }
}
```

### 7.2 Sentiment Analysis Endpoints

#### POST /api/v1/sentiment/analyze
Analyze sentiment of text
```
Headers:
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
    "text": "I absolutely love this product!",
    "include_details": true,
    "model": "vader",
    "language": "en"
}

Response:
{
    "status": "success",
    "data": {
        "request_id": "req_12345",
        "sentiment": "positive",
        "confidence": 0.92,
        "scores": {
            "positive": 0.55,
            "negative": 0.0,
            "neutral": 0.45,
            "compound": 0.87
        },
        "processing_time_ms": 45,
        "processed_at": "2025-01-31T10:30:00Z"
    }
}
```

#### POST /api/v1/sentiment/batch
Batch sentiment analysis with async processing
```
Request:
{
    "texts": [
        "I love this!",
        "This is awful",
        "It's okay"
    ],
    "callback_url": "https://webhook.site/unique-id",
    "metadata": {
        "project_id": "proj_123",
        "batch_name": "Feb_2025"
    }
}

Response (202 Accepted):
{
    "status": "success",
    "code": 202,
    "data": {
        "batch_id": "batch_12345",
        "status": "queued",
        "total_items": 3,
        "status_url": "/api/v1/sentiment/batch/batch_12345",
        "webhook_url": "https://webhook.site/unique-id"
    }
}
```

#### GET /api/v1/sentiment/batch/{batch_id}
Get batch processing status
```
Response:
{
    "status": "success",
    "data": {
        "batch_id": "batch_12345",
        "status": "processing",
        "progress": 33,
        "total_items": 3,
        "processed_items": 1,
        "failed_items": 0,
        "estimated_completion": "2025-01-31T10:35:00Z",
        "results_url": "/api/v1/sentiment/batch/batch_12345/results"
    }
}
```

#### GET /api/v1/sentiment/batch/{batch_id}/results
Retrieve batch results
```
Response:
{
    "status": "success",
    "data": {
        "batch_id": "batch_12345",
        "results": [
            {
                "index": 0,
                "text": "I love this!",
                "sentiment": "positive",
                "confidence": 0.92
            },
            ...
        ]
    }
}
```

### 7.3 Model Management Endpoints

#### GET /api/v1/models
List available models
```
Response:
{
    "status": "success",
    "data": {
        "models": [
            {
                "id": "vader",
                "name": "VADER Sentiment Analyzer",
                "accuracy": 0.88,
                "supported_languages": ["en"],
                "tasks": ["sentiment_analysis"]
            },
            {
                "id": "bert-sentiment",
                "name": "BERT Sentiment Analyzer",
                "accuracy": 0.94,
                "status": "coming_soon"
            }
        ]
    }
}
```

#### GET /api/v1/models/{model_id}
Get model details and metrics
```
Response:
{
    "status": "success",
    "data": {
        "model": {
            "id": "vader",
            "name": "VADER Sentiment Analyzer",
            "accuracy": 0.88,
            "metrics": {
                "precision": 0.89,
                "recall": 0.87,
                "f1_score": 0.88
            },
            "examples": [...]
        }
    }
}
```

### 7.4 Webhook Management Endpoints

#### POST /api/v1/webhooks
Register webhook
```
Request:
{
    "url": "https://your-server.com/webhooks/sentiment",
    "events": ["batch_completed", "analysis_failed"],
    "active": true,
    "headers": {
        "Authorization": "Bearer your-token"
    }
}

Response:
{
    "status": "success",
    "code": 201,
    "data": {
        "webhook_id": "wh_12345",
        "url": "https://your-server.com/webhooks/sentiment",
        "events": ["batch_completed", "analysis_failed"],
        "created_at": "2025-01-31T10:30:00Z",
        "secret": "whsec_123..." // For HMAC verification
    }
}
```

#### GET /api/v1/webhooks
List webhooks
```
Response:
{
    "status": "success",
    "data": {
        "webhooks": [
            {
                "webhook_id": "wh_12345",
                "url": "https://your-server.com/webhooks/sentiment",
                "active": true,
                "last_triggered": "2025-01-31T10:25:00Z"
            }
        ]
    }
}
```

#### PUT /api/v1/webhooks/{webhook_id}
Update webhook
```
Request:
{
    "active": false,
    "events": ["batch_completed"]
}

Response:
{
    "status": "success",
    "data": {
        "webhook_id": "wh_12345",
        "updated_at": "2025-01-31T10:30:00Z"
    }
}
```

#### DELETE /api/v1/webhooks/{webhook_id}
Delete webhook
```
Response:
{
    "status": "success",
    "message": "Webhook deleted successfully"
}
```

---

## 8. Webhook Events

### 8.1 Event Types

#### batch_completed
Triggered when batch processing completes
```json
{
    "event_type": "batch_completed",
    "event_id": "evt_12345",
    "timestamp": "2025-01-31T10:30:00Z",
    "data": {
        "batch_id": "batch_12345",
        "total_items": 3,
        "processed_items": 3,
        "failed_items": 0
    }
}
```

#### analysis_failed
Triggered when analysis fails
```json
{
    "event_type": "analysis_failed",
    "event_id": "evt_12346",
    "timestamp": "2025-01-31T10:30:00Z",
    "data": {
        "batch_id": "batch_12345",
        "item_index": 1,
        "error": "Text exceeds maximum length"
    }
}
```

### 8.2 Webhook Verification

HMAC-SHA256 signature verification:
```python
import hmac
import hashlib

webhook_secret = "whsec_..."
signature = request.headers.get('X-Webhook-Signature')

body = request.get_data()
computed_signature = hmac.new(
    webhook_secret.encode(),
    body,
    hashlib.sha256
).hexdigest()

assert signature == computed_signature
```

---

## 9. Implementation Plan

### 9.1 Phase 1: Core NLP & UI Optimization (COMPLETED)
- [x] Implement hybrid sentiment logic (VADER + TextBlob + Keywords).
- [x] Add multi-paragraph batch detection for file uploads.
- [x] Standardize internal JSON response formats.
- [x] Create 3-column interactive responsive dashboard.
- [x] Implement loading indicators and summary stats.

### 9.2 Phase 2: Security & Rate Limiting (NEXT)
- [ ] Set up Flask-JWT-Extended for token authentication.
- [ ] Implement per-client request throttling with Flask-Limiter.
- [ ] Standardize HTTP error codes (401, 403, 429).

### 9.3 Phase 3: Documentation & Testing (Week 5-6)
- [ ] Write comprehensive API documentation
- [ ] Create Swagger/OpenAPI spec
- [ ] Write unit tests
- [ ] Write integration tests

### 9.4 Phase 4: Deployment & Monitoring (Week 7-8)
- [ ] Set up logging and monitoring
- [ ] Deploy to staging
- [ ] Performance testing
- [ ] Deploy to production

---

## 10. Technology Stack

### Backend
- **Framework**: Flask 2.3.0
- **Authentication**: Flask-JWT-Extended
- **Rate Limiting**: Flask-Limiter
- **Database**: PostgreSQL (for user/webhook storage)
- **Cache**: Redis (for rate limiting, caching)
- **Task Queue**: Celery + RabbitMQ (for batch processing)

### Monitoring & Logging
- **Logging**: Python logging + ELK Stack
- **Monitoring**: Prometheus + Grafana
- **Error Tracking**: Sentry
- **APM**: New Relic or DataDog

### Documentation
- **OpenAPI**: Swagger/OpenAPI 3.0
- **Documentation**: ReDoc, Swagger UI
- **SDKs**: Python, JavaScript, Java

---

## 11. Security Considerations

### 11.1 HTTPS/TLS
- All API endpoints must use HTTPS
- TLS 1.2 minimum
- Certificate pinning for mobile clients

### 11.2 Data Protection
- Encrypt sensitive data in transit and at rest
- PII should be hashed or encrypted
- GDPR compliance

### 11.3 API Security
- CORS restrictions
- CSRF protection
- SQL injection prevention
- XSS protection

### 11.4 Audit Logging
```python
logger.info(f"User {user_id} analyzed text: {request_id}")
logger.warning(f"Rate limit exceeded for user {user_id}")
logger.error(f"Analysis failed for batch {batch_id}")
```

---

## 12. Monitoring & Analytics

### 12.1 Metrics to Track
- API response time
- Request throughput
- Error rate
- Cache hit ratio
- Batch processing queue size
- User engagement metrics

### 12.2 Alerting Rules
- Response time > 1000ms
- Error rate > 5%
- Queue size > 1000 items
- Webhook delivery failures

---

## 13. API Documentation Example

### 13.1 Swagger/OpenAPI Specification

```yaml
openapi: 3.0.0
info:
  title: Sentiment Analysis API
  version: 1.0.0
  description: RESTful API for sentiment analysis

servers:
  - url: https://api.sentimentanalyzer.com/api/v1

paths:
  /sentiment/analyze:
    post:
      summary: Analyze sentiment of text
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                text:
                  type: string
                  maxLength: 5000
              required:
                - text
      responses:
        '200':
          description: Successful analysis
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AnalysisResponse'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

---

## 14. Cost Estimation

| Component | Cost/Month | Notes |
|-----------|-----------|-------|
| Hosting (AWS) | $500-2000 | Auto-scaling |
| Database | $100-300 | RDS Multi-AZ |
| Cache (Redis) | $50-200 | Elasticache |
| CDN | $100-500 | CloudFront |
| Monitoring | $200-500 | Datadog/New Relic |
| **Total** | **$950-3500** | Depends on scale |

---

## 15. Success Metrics

- API uptime > 99.9%
- Average response time < 200ms
- Support ticket resolution < 24 hours
- Developer adoption (SDK downloads, API calls)
- Customer satisfaction score > 4.5/5

---

## 16. Future Enhancements

1. **Multi-language Support**: Expand beyond English
2. **Advanced Models**: Integration with BERT, GPT models
3. **Real-time Streaming**: WebSocket support for live sentiment analysis
4. **Aspect-based Sentiment**: Analyze sentiment for specific aspects
5. **Mobile SDKs**: Native iOS and Android SDKs
6. **GraphQL API**: Alternative to REST
7. **Plugin Ecosystem**: Community-built extensions

---

## Conclusion

This enhancement plan transforms the Sentiment Analysis Application into an enterprise-grade API platform. By implementing industry-standard practices for authentication, rate limiting, error handling, and monitoring, the API will be secure, scalable, and maintainable.

The phased approach allows for iterative development and testing while the comprehensive documentation ensures good developer experience.

---

**Document Version**: 2.0  
**Last Updated**: February 9, 2025  
**Author**: Group #37 (BITS WILP M.Tech AIML)  
**Status**: Revised (Phase 1 Complete)
