"""
Enhanced RESTful API Implementation for Sentiment Analysis
Task B: API Enhancement Plan
Author: Student Assignment
Date: January 31, 2025

This module demonstrates the enhancement of the Sentiment Analysis Application
with RESTful API capabilities, security, and scalability features.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from datetime import datetime, timedelta
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIResponse:
    """Standardized API Response Format"""
    
    @staticmethod
    def success(data, status_code=200, message="Success"):
        """Return standardized success response"""
        return {
            "status": "success",
            "code": status_code,
            "message": message,
            "data": data,
            "error": None,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }, status_code
    
    @staticmethod
    def error(error_message, status_code=400, error_code="BAD_REQUEST"):
        """Return standardized error response"""
        return {
            "status": "error",
            "code": status_code,
            "error": {
                "message": error_message,
                "code": error_code
            },
            "data": None,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }, status_code


def enhanced_app_factory(config=None):
    """
    Enhanced Flask application factory with all improvements
    
    Features:
    - JWT Authentication
    - Rate Limiting
    - Comprehensive Logging
    - Standardized Responses
    - API Versioning
    - Webhook Support
    """
    
    app = Flask(__name__)
    
    # Configuration
    if config is None:
        config = {
            'JWT_SECRET_KEY': 'your-secret-key-change-this-in-production',
            'JWT_ACCESS_TOKEN_EXPIRES': timedelta(hours=24),
            'JSON_SORT_KEYS': False
        }
    
    app.config.update(config)
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # API Versioning
    API_VERSION = "v1"
    
    # ==================== Authentication Endpoints ====================
    
    @app.route(f'/api/{API_VERSION}/auth/register', methods=['POST'])
    @limiter.limit("5 per hour")
    def register():
        """
        Register a new API user.
        
        Request:
        {
            "username": "user@example.com",
            "password": "secure_password"
        }
        
        Response:
        {
            "status": "success",
            "data": {
                "user_id": "uuid",
                "api_key": "generated_key"
            }
        }
        
        Note: This is a demonstration implementation that generates a dummy API key.
        """
        try:
            data = request.get_json()
            
            # Validate input
            if not data or 'username' not in data or 'password' not in data:
                return APIResponse.error(
                    "Missing username or password",
                    400, "VALIDATION_ERROR"
                )
            
            # In production: Hash password and store in database
            # For demo: Generate dummy API key
            api_key = f"sk_{data['username'][:3]}_{int(datetime.utcnow().timestamp())}"
            
            response_data = {
                "user_id": "user_123",
                "username": data['username'],
                "api_key": api_key,
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            
            logger.info(f"New user registered: {data['username']}")
            return APIResponse.success(response_data, 201, "User registered successfully")
        
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return APIResponse.error(
                "Registration failed",
                500, "INTERNAL_ERROR"
            )
    
    @app.route(f'/api/{API_VERSION}/auth/login', methods=['POST'])
    @limiter.limit("10 per hour")
    def login():
        """
        Login and calculate access token.
        
        Request:
        {
            "username": "user@example.com",
            "password": "secure_password"
        }
        
        Response:
        {
            "status": "success",
            "data": {
                "access_token": "jwt_token",
                "token_type": "Bearer",
                "expires_in": 86400
            }
        }
        
        Note: This is a demonstration that accepts any valid JSON structure.
        """
        try:
            data = request.get_json()
            
            if not data or 'username' not in data or 'password' not in data:
                return APIResponse.error(
                    "Missing credentials",
                    400, "VALIDATION_ERROR"
                )
            
            # In production: Verify credentials against database
            # For demo: Accept any username/password combination
            access_token = create_access_token(
                identity=data['username'],
                expires_delta=app.config['JWT_ACCESS_TOKEN_EXPIRES']
            )
            
            response_data = {
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": int(app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
            }
            
            logger.info(f"User logged in: {data['username']}")
            return APIResponse.success(response_data, 200, "Login successful")
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return APIResponse.error(
                "Login failed",
                500, "INTERNAL_ERROR"
            )
    
    # ==================== Enhanced Sentiment Analysis Endpoints ====================
    
    @app.route(f'/api/{API_VERSION}/sentiment/analyze', methods=['POST'])
    @jwt_required()
    @limiter.limit("30 per hour")
    def analyze_sentiment_enhanced():
        """
        Enhanced sentiment analysis with authentication and rate limiting.
        
        Headers:
        Authorization: Bearer {jwt_token}
        
        Request:
        {
            "text": "Your text here",
            "include_details": true,
            "language": "en"
        }
        
        Response:
        {
            "status": "success",
            "code": 200,
            "data": {
                ...
            }
        }
        
        Note: Uses mock sentiment data for demonstration if the analyzer is not connected.
        """
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return APIResponse.error(
                    "Missing text field",
                    400, "VALIDATION_ERROR"
                )
            
            text = data['text'].strip()
            include_details = data.get('include_details', False)
            language = data.get('language', 'en')
            
            # Validate language
            if language != 'en':
                return APIResponse.error(
                    "Currently only English is supported",
                    400, "UNSUPPORTED_LANGUAGE"
                )
            
            # Generate request ID for tracking
            request_id = f"req_{int(datetime.utcnow().timestamp() * 1000)}"
            
            # Perform sentiment analysis (using analyzer module)
            # sentiment_result = analyzer.get_detailed_analysis(text)
            
            # Mock result for demonstration
            sentiment_result = {
                "overall_sentiment": "positive",
                "confidence": 0.85,
                "vader_scores": {
                    "positive": 0.5,
                    "negative": 0.1,
                    "neutral": 0.4,
                    "compound": 0.76
                }
            }
            
            response_data = {
                "request_id": request_id,
                "sentiment": sentiment_result['overall_sentiment'],
                "confidence": sentiment_result['confidence'],
                "processed_at": datetime.utcnow().isoformat() + "Z",
                "text_preview": text[:100] + ("..." if len(text) > 100 else "")
            }
            
            if include_details:
                response_data['analysis'] = sentiment_result
            
            logger.info(f"Analysis completed: {request_id}")
            return APIResponse.success(response_data, 200, "Analysis completed successfully")
        
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return APIResponse.error(
                "Analysis failed",
                500, "ANALYSIS_ERROR"
            )
    
    @app.route(f'/api/{API_VERSION}/sentiment/batch', methods=['POST'])
    @jwt_required()
    @limiter.limit("10 per hour")
    def batch_analyze_enhanced():
        """
        Batch sentiment analysis with job tracking.
        
        Request:
        {
            "texts": ["text1", "text2"],
            "callback_url": "https://your-webhook.com/sentiment",
            "metadata": {"project_id": "123"}
        }
        
        Response:
        {
            "status": "success",
            "data": {
                "batch_id": "batch_123",
                "status": "processing",
                "total_items": 2,
                "webhook_url": "..."
            }
        }
        
        Note: Simulates queuing a batch job without actual background processing.
        """
        try:
            data = request.get_json()
            
            if not data or 'texts' not in data:
                return APIResponse.error(
                    "Missing texts field",
                    400, "VALIDATION_ERROR"
                )
            
            texts = data['texts']
            callback_url = data.get('callback_url')
            metadata = data.get('metadata', {})
            
            if not isinstance(texts, list) or len(texts) > 100:
                return APIResponse.error(
                    "texts must be a list with max 100 items",
                    400, "VALIDATION_ERROR"
                )
            
            # Generate batch ID
            batch_id = f"batch_{int(datetime.utcnow().timestamp() * 1000)}"
            
            response_data = {
                "batch_id": batch_id,
                "status": "queued",
                "total_items": len(texts),
                "processing_url": f"/api/{API_VERSION}/sentiment/batch/{batch_id}",
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            
            if callback_url:
                response_data['webhook_url'] = callback_url
            
            logger.info(f"Batch job created: {batch_id} with {len(texts)} items")
            
            # In production: Queue job with Celery/RQ and process asynchronously
            return APIResponse.success(response_data, 202, "Batch job queued")
        
        except Exception as e:
            logger.error(f"Batch analysis error: {str(e)}")
            return APIResponse.error(
                "Batch analysis failed",
                500, "BATCH_ERROR"
            )
    
    @app.route(f'/api/{API_VERSION}/sentiment/batch/<batch_id>', methods=['GET'])
    @jwt_required()
    def get_batch_status(batch_id):
        """
        Get status of batch processing job.
        
        Response:
        {
            "status": "success",
            "data": {
                "batch_id": "batch_123",
                "status": "completed",
                ...
            }
        }
        
        Note: Always returns a mocking 'completed' status.
        """
        try:
            # In production: Fetch job status from queue/database
            response_data = {
                "batch_id": batch_id,
                "status": "completed",
                "progress": 100,
                "total_items": 2,
                "completed_items": 2,
                "results_url": f"/api/{API_VERSION}/sentiment/batch/{batch_id}/results"
            }
            
            return APIResponse.success(response_data, 200, "Batch status retrieved")
        
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return APIResponse.error(
                "Status check failed",
                500, "STATUS_ERROR"
            )
    
    # ==================== Model Management Endpoints ====================
    
    @app.route(f'/api/{API_VERSION}/models/list', methods=['GET'])
    @jwt_required()
    def list_models():
        """
        List available sentiment analysis models.
        
        Response:
        {
            "status": "success",
            "data": {
                "models": [...]
            }
        }
        
        Note: Returns a static list of models for demonstration.
        """
        models = [
            {
                "id": "vader",
                "name": "VADER Sentiment Analyzer",
                "description": "Valence Aware Dictionary and sEntiment Reasoner",
                "language": "en",
                "accuracy": 0.88,
                "type": "lexicon-based",
                "supported_tasks": ["sentiment_analysis", "intensity_detection"]
            },
            {
                "id": "textblob",
                "name": "TextBlob Sentiment",
                "description": "Simple API for common NLP tasks",
                "language": "en",
                "accuracy": 0.82,
                "type": "machine-learning",
                "supported_tasks": ["sentiment_analysis", "subjectivity_detection"]
            },
            {
                "id": "bert-sentiment",
                "name": "BERT Sentiment (Coming Soon)",
                "description": "Transformer-based deep learning model",
                "language": "en",
                "accuracy": 0.94,
                "type": "deep-learning",
                "status": "coming_soon",
                "supported_tasks": ["sentiment_analysis", "aspect_sentiment"]
            }
        ]
        
        return APIResponse.success({"models": models}, 200, "Models retrieved successfully")
    
    @app.route(f'/api/{API_VERSION}/models/<model_id>/info', methods=['GET'])
    @jwt_required()
    def get_model_info(model_id):
        """
        Get detailed information about a specific model.
        
        Response:
        {
            "status": "success",
            "data": {
                "model": {...},
                "metrics": {...},
                "usage_examples": [...]
            }
        }
        
        Note: Returns mock model information details.
        """
        # Mock model info
        model_info = {
            "id": model_id,
            "name": "VADER Sentiment Analyzer",
            "description": "Valence Aware Dictionary and sEntiment Reasoner",
            "version": "1.0.0",
            "metrics": {
                "accuracy": 0.88,
                "precision": 0.89,
                "recall": 0.87,
                "f1_score": 0.88
            },
            "examples": [
                {
                    "input": "I love this!",
                    "output": {
                        "sentiment": "positive",
                        "confidence": 0.91
                    }
                }
            ]
        }
        
        return APIResponse.success({"model": model_info}, 200)
    
    # ==================== Webhook Management Endpoints ====================
    
    @app.route(f'/api/{API_VERSION}/webhooks/register', methods=['POST'])
    @jwt_required()
    def register_webhook():
        """
        Register a webhook for event notifications.
        
        Request:
        {
            "url": "https://your-server.com/webhook",
            "events": ["batch_completed", "analysis_failed"],
            "active": true
        }
        
        Response:
        {
            "status": "success",
            "data": {
                "webhook_id": "wh_123",
                "url": "...",
                ...
            }
        }
        
        Note: Simulates webhook registration (no database used).
        """
        try:
            data = request.get_json()
            
            if not data or 'url' not in data:
                return APIResponse.error(
                    "Missing webhook URL",
                    400, "VALIDATION_ERROR"
                )
            
            webhook_id = f"wh_{int(datetime.utcnow().timestamp() * 1000)}"
            
            response_data = {
                "webhook_id": webhook_id,
                "url": data['url'],
                "events": data.get('events', ['all']),
                "active": data.get('active', True),
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            
            logger.info(f"Webhook registered: {webhook_id}")
            return APIResponse.success(response_data, 201, "Webhook registered successfully")
        
        except Exception as e:
            logger.error(f"Webhook registration error: {str(e)}")
            return APIResponse.error(
                "Webhook registration failed",
                500, "WEBHOOK_ERROR"
            )
    
    # ==================== Error Handlers ====================
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return APIResponse.error(
            f"Endpoint not found",
            404, "NOT_FOUND"
        )
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return APIResponse.error(
            "Internal server error",
            500, "INTERNAL_ERROR"
        )
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        """Handle rate limit errors"""
        return APIResponse.error(
            "Rate limit exceeded",
            429, "RATE_LIMIT_EXCEEDED"
        )
    
    return app


# Example Usage
if __name__ == '__main__':
    config = {
        'JWT_SECRET_KEY': 'your-secret-key-change-this',
        'JSON_SORT_KEYS': False
    }
    
    app = enhanced_app_factory(config)
    app.run(debug=True, host='127.0.0.1', port=5000)
