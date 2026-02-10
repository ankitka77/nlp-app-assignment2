"""
Flask Backend for Sentiment Analysis Application
Provides REST endpoints for sentiment analysis
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from sentiment_analyzer import SentimentAnalyzer
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize sentiment analyzer
analyzer = SentimentAnalyzer()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main HTML interface"""
    return send_file('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Sentiment Analysis API is running'
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Analyze sentiment of provided text
    
    Request JSON:
    {
        "text": "Your text here"
    }
    
    Response:
    {
        "overall_sentiment": "positive",
        "confidence": 0.85,
        "vader_scores": {...},
        "textblob_scores": {...},
        "sentence_analysis": [...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field in request'
            }), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                'error': 'Text field cannot be empty'
            }), 400
        
        if len(text) > 50000:
            return jsonify({
                'error': 'Text exceeds maximum length of 50000 characters'
            }), 400
        
        # Perform sentiment analysis
        result = analyzer.get_detailed_analysis(text)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error analyzing text: {str(e)}'
        }), 500


@app.route('/api/analyze-file', methods=['POST'])
def analyze_file():
    """
    Analyze sentiment from uploaded file
    Supports .txt files
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file part in request'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'No selected file'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'File type not allowed. Allowed types: txt'
            }), 400
        
        # Read file content
        if file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')
        else:
            return jsonify({
                'error': 'Currently only .txt files are supported'
            }), 400
        
        if len(content) > 50000: # Increased limit for larger files
            return jsonify({
                'error': 'File content exceeds maximum length of 50000 characters'
            }), 400
        
        # Robust splitting logic
        # Try double newline first (typical paragraph separation)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        # If only one paragraph found, check if it has single newlines and use those
        if len(paragraphs) <= 1:
            split_by_single = [p.strip() for p in content.split('\n') if p.strip()]
            if len(split_by_single) > 1:
                paragraphs = split_by_single
        
        if not paragraphs:
            return jsonify({
                'error': 'No valid content found in file'
            }), 400

        # Perform sentiment analysis for each paragraph
        results = []
        for p in paragraphs:
            analysis = analyzer.get_detailed_analysis(p)
            results.append({
                'text_preview': p[:100] + ('...' if len(p) > 100 else ''),
                'analysis': analysis
            })
        
        return jsonify({
            'success': True,
            'filename': secure_filename(file.filename),
            'is_batch': len(results) > 1,
            'data': results if len(results) > 1 else results[0]['analysis'],
            'batch_results': results if len(results) > 1 else None
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error analyzing file: {str(e)}'
        }), 500


@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    """
    Analyze sentiment for multiple texts
    
    Request JSON:
    {
        "texts": ["text1", "text2", "text3"]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({
                'error': 'Missing texts field in request'
            }), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list):
            return jsonify({
                'error': 'texts field must be a list'
            }), 400
        
        if len(texts) > 10:
            return jsonify({
                'error': 'Maximum 10 texts allowed per batch'
            }), 400
        
        # Filter empty texts
        texts = [t.strip() for t in texts if t.strip()]
        
        if not texts:
            return jsonify({
                'error': 'No valid texts provided'
            }), 400
        
        # Perform batch analysis
        results = []
        for text in texts:
            result = analyzer.get_detailed_analysis(text)
            results.append({
                'text': text[:100] + ('...' if len(text) > 100 else ''),
                'analysis': result
            })
        
        return jsonify({
            'success': True,
            'batch_count': len(results),
            'data': results
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error analyzing batch: {str(e)}'
        }), 500


@app.route('/api/stats', methods=['POST'])
def get_stats():
    """
    Get statistics for sentiment analysis results
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field'
            }), 400
        
        text = data['text'].strip()
        result = analyzer.get_detailed_analysis(text)
        
        # Calculate statistics
        stats = {
            'character_count': len(text),
            'word_count': len(text.split()),
            'sentence_count': result['sentence_count'],
            'token_count': result['token_count'],
            'sentiment_breakdown': {
                'positive': result['vader_scores']['positive'],
                'negative': result['vader_scores']['negative'],
                'neutral': result['vader_scores']['neutral']
            },
            'dominant_sentiment': result['overall_sentiment'],
            'confidence': result['confidence']
        }
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Error getting stats: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run Flask app in debug mode
    app.run(debug=True, host='127.0.0.1', port=5000)
