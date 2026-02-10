# Sentiment Analysis Application - Complete Implementation

## Overview

This is a comprehensive Sentiment Analysis application that leverages Natural Language Processing (NLP) techniques to analyze the sentiment of user-provided text. Developed for **Assignment 2** by **Group #37**, the application combines multiple NLP engines (VADER, TextBlob) with custom keyword detection and contextual patterns to provide highly accurate results even for nuanced texts.

## Project Structure

```
sentiment-analysis-app/
├── app.py                          # Flask backend application
├── sentiment_analyzer.py            # NLP sentiment analysis module
├── index.html                       # Frontend web interface
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── uploads/                         # Directory for file uploads (auto-created)
```

## Features

### 1. Web Interface
- **Optimized 3-Column Dashboard**: Clean, responsive layout with synchronized top/bottom alignment and fixed height (720px) for a desktop-app feel.
- **Two Input Methods**:
  - Direct text input with expanded textarea (Limit: 50,000 chars)
  - Bulk file upload functionality (.txt files up to 10MB)
- **Advanced Loading States**: Animated sand-timer SVG for visual feedback during processing.
- **Batch Processing Summary**: Instant breakdown of Positive, Negative, and Neutral paragraphs for uploaded files.
- **Interactive Topic Navigator**: Browse individual paragraph analyses from a single file with one click.
- **Improved Visualization**: High-contrast Bar Chart with percentage scaling for intuitive score comparison.
- **Responsive Design**: Mobile-friendly breakpoints and adaptive grid system.

### 2. Sentiment Analysis
#### Text Preprocessing
- Lowercase conversion
- URL and email removal
- Special character removal
- Tokenization using NLTK
- Stopword removal
- Lemmatization for word normalization

#### Analysis Methods
- **VADER (Valence Aware Dictionary and sEntiment Reasoner)**:
  - Specifically designed for social media and short texts
  - Provides: positive, negative, neutral, and compound scores
  - Compound score ranges from -1 (most negative) to 1 (most positive)

- **TextBlob**:
  - Provides polarity (-1 to 1) and subjectivity (0 to 1) scores
  - Useful for sentiment classification and opinion mining

#### Sentiment Classification
- **Hybrid Scoring**: Combines VADER (intensity), TextBlob (polarity), and Sentence Balance (context).
- **Keyword Detection**: Integrated 50+ strong sentiment phrases and "hope-disappointment" patterns to fix common misclassifications (e.g., negative reviews masked by positive nostalgia).
- **Adjusted Thresholds**:
  - **Positive**: Combined score >= 0.12
  - **Negative**: Combined score <= -0.08
  - **Neutral**: Borderline cases further validated by keyword weighing and intensity scaling.

### 3. Detailed Metrics
- Character and word counts
- Sentence and token counts
- Confidence scores
- Sentence-level sentiment analysis
- Key phrase extraction

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 2.3.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin resource sharing
- NLTK 3.8.1 - Natural Language Toolkit
- TextBlob 0.17.1 - Simplified text processing
- scikit-learn 1.2.2 - Machine learning library
- NumPy & Pandas - Data processing libraries

### Step 2: Download NLTK Data

The first time you run the application, it will automatically download required NLTK data:
- vader_lexicon
- punkt (tokenizer)
- stopwords
- wordnet (lemmatizer)
- averaged_perceptron_tagger

### Step 3: Run the Backend Server

```bash
python app.py
```

The Flask server will start at `http://127.0.0.1:5000`

Output:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 4: Open the Frontend

Open `index.html` in a web browser (or use a local server):

```bash
# Option 1: Using Python's built-in server
python -m http.server 8000
# Then open http://127.0.0.1:8000/index.html

# Option 2: Using Live Server (VS Code extension)
# Right-click index.html and select "Open with Live Server"

# Option 3: Direct file opening
# Simply drag index.html to your browser
```

## API Endpoints

### 1. Health Check
```
GET /api/health
```

Response:
```json
{
    "status": "healthy",
    "message": "Sentiment Analysis API is running"
}
```

### 2. Analyze Text
```
POST /api/analyze
Content-Type: application/json

{
    "text": "Your text here"
}
```

Response:
```json
{
    "success": true,
    "data": {
        "overall_sentiment": "positive",
        "confidence": 0.85,
        "vader_scores": {
            "positive": 0.5,
            "negative": 0.1,
            "neutral": 0.4,
            "compound": 0.76
        },
        "textblob_scores": {
            "polarity": 0.75,
            "subjectivity": 0.6
        },
        "processed_tokens": ["amazing", "great", "wonderful"],
        "token_count": 3,
        "sentence_count": 1,
        "sentence_analysis": [
            {
                "sentence": "This is amazing!",
                "sentiment": "positive",
                "confidence": 0.76
            }
        ],
        "cleaned_text": "this is amazing"
    }
}
```

### 3. Analyze File
```
POST /api/analyze-file
Content-Type: multipart/form-data

File: (binary .txt file)
```

Response: Same as /api/analyze with filename field

### 4. Batch Analysis
```
POST /api/analyze-batch
Content-Type: application/json

{
    "texts": ["text1", "text2", "text3"]
}
```

Response:
```json
{
    "success": true,
    "batch_count": 3,
    "data": [
        {
            "text": "text1",
            "analysis": { ... }
        },
        ...
    ]
}
```

### 5. Get Statistics
```
POST /api/stats
Content-Type: application/json

{
    "text": "Your text here"
}
```

Response:
```json
{
    "success": true,
    "data": {
        "character_count": 15,
        "word_count": 3,
        "sentence_count": 1,
        "token_count": 3,
        "sentiment_breakdown": {
            "positive": 0.5,
            "negative": 0.1,
            "neutral": 0.4
        },
        "dominant_sentiment": "positive",
        "confidence": 0.76
    }
}
```

## Usage Examples

### Example 1: Positive Sentiment
**Input:** "I absolutely love this product! It's amazing and exceeded my expectations."

**Output:**
- Overall Sentiment: POSITIVE
- Confidence: 0.87
- Positive Score: 0.55
- Negative Score: 0.0
- Neutral Score: 0.45
- Compound: 0.87

### Example 2: Negative Sentiment
**Input:** "This is terrible and I hate it. Worst purchase ever."

**Output:**
- Overall Sentiment: NEGATIVE
- Confidence: 0.92
- Positive Score: 0.0
- Negative Score: 0.62
- Neutral Score: 0.38
- Compound: -0.92

### Example 3: Neutral Sentiment
**Input:** "The product is available in stores."

**Output:**
- Overall Sentiment: NEUTRAL
- Confidence: 0.0
- Positive Score: 0.0
- Negative Score: 0.0
- Neutral Score: 1.0
- Compound: 0.0

## UI Components

### Input Section
- Text area for direct text input (max 5000 characters)
- File upload for .txt files
- Tab-based navigation between input methods
- Clear and Analyze buttons

### Results Display
- **Sentiment Badge**: Color-coded visual representation
- **Confidence Meter**: Visual progress bar
- **Statistics Grid**: Shows key metrics (sentiment, confidence, sentences, tokens)
- **Sentiment Chart**: Doughnut chart of positive/negative/neutral distribution

### Detailed Analysis Tabs
1. **Sentiment Scores**: Detailed breakdown of all sentiment metrics
2. **Processed Tokens**: Display of preprocessed and lemmatized tokens
3. **Sentence Analysis**: Sentiment analysis for individual sentences

## Design Choices & Architecture

### Backend Architecture
- **Flask Framework**: Lightweight, scalable HTTP server
- **Modular Design**: Separated sentiment analysis logic from API endpoints
- **Error Handling**: Comprehensive error checking and user-friendly messages
- **CORS Support**: Allows frontend to communicate with backend

### NLP Techniques
- **VADER**: Best for social media and informal text due to emoji/punctuation handling
- **TextBlob**: Good for standard text sentiment and subjectivity analysis
- **Dual Approach**: Combines multiple methods for robust sentiment detection
- **Preprocessing**: Ensures clean data for accurate analysis

### Frontend Design
- **Responsive Grid Layout**: Adapts to different screen sizes
- **Modern Styling**: Gradient backgrounds, smooth animations, visual feedback
- **Chart.js Integration**: Dynamic, responsive charts
- **Tab-based Navigation**: Organized information presentation
- **Real-time Feedback**: Loading states, error/success messages

## Challenges & Solutions

### Challenge 1: Handling Diverse Text Types
**Solution**: Used VADER which handles emojis, punctuation, and informal text better than traditional methods.

### Challenge 2: Balancing Accuracy with Performance
**Solution**: Implemented efficient preprocessing and used pre-trained models instead of training from scratch.

### Challenge 3: Cross-origin Requests
**Solution**: Implemented Flask-CORS to handle frontend-backend communication across different origins.

### Challenge 4: File Upload Handling
**Solution**: Implemented secure file upload with validation and appropriate error messages.

### Challenge 5: UI Responsiveness
**Solution**: Used CSS Grid and Media Queries for flexible, responsive design.

## Limitations & Future Enhancements

### Current Status
- ✅ English language support
- ✅ 50,000 character limit per analysis
- ✅ 10MB file upload limit
- ✅ Multi-paragraph (batch) file analysis

### Future Enhancements
1. **Multi-language Support**: Implement language detection and multilingual NLP models
2. **Advanced Models**: Integrate transformer-based models (BERT, RoBERTa) for better accuracy
3. **User Authentication**: Add user accounts and history tracking
4. **Database Integration**: Store analysis history and enable data export
5. **Advanced Visualizations**: Add word clouds, sentiment trends over time
6. **API Authentication**: Implement JWT-based authentication for RESTful APIs
7. **Deployment**: Docker containerization and cloud deployment (AWS, GCP, Azure)
8. **Performance**: Implement caching and async processing for batch operations

## RESTful API Enhancement (Task B)

### Proposed Enhancement Plan

#### 1. API Security
```python
# Implement JWT token-based authentication
from flask_jwt_extended import JWTManager, jwt_required

@app.route('/api/token', methods=['POST'])
def get_token():
    # Generate JWT token for API access
    pass

@app.route('/api/analyze', methods=['POST'])
@jwt_required()
def analyze_text():
    # Protected endpoint
    pass
```

#### 2. Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.headers.get('X-API-Key'))

@app.route('/api/analyze', methods=['POST'])
@limiter.limit("10/minute")
def analyze_text():
    pass
```

#### 3. API Versioning
```python
/api/v1/analyze
/api/v1/analyze-batch
/api/v1/models/list
```

#### 4. Response Standardization
```python
{
    "status": "success|error",
    "code": 200,
    "data": {...},
    "error": null,
    "timestamp": "2025-01-31T10:30:00Z"
}
```

#### 5. Webhook Support
```python
@app.route('/api/analyze/async', methods=['POST'])
def analyze_async():
    # Store callback URL and process asynchronously
    task = process_sentiment.apply_async(
        args=[text],
        callback_url=request.json['callback_url']
    )
    return {'task_id': task.id}
```

#### 6. Documentation
- Swagger/OpenAPI documentation
- Interactive API explorer
- Code examples for various languages

## Testing

### Unit Tests
```python
def test_vader_analysis():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_sentiment_vader("I love this!")
    assert result['positive'] > 0.5

def test_preprocessing():
    analyzer = SentimentAnalyzer()
    tokens, text = analyzer.preprocess_text("Hello, World!")
    assert len(tokens) > 0
```

### API Tests
```bash
# Health check
curl http://127.0.0.1:5000/api/health

# Text analysis
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this!"}'
```

## Performance Metrics

- **Response Time**: < 500ms for text analysis
- **Max Throughput**: 10+ requests per second
- **Memory Usage**: ~200MB at startup
- **Processing Speed**: 1000+ tokens per second

## License

This project is provided as part of BITS WILP M.Tech AIML Course Assignment 2.

## Support & Contact

For any queries regarding this assignment, please contact:
- **Course LF**: Vasugi I (vasugii@wilp.bits-pilani.ac.in)

## References

1. VADER Sentiment Analysis: https://github.com/cjhutto/vaderSentiment
2. NLTK Documentation: https://www.nltk.org/
3. TextBlob Documentation: https://textblob.readthedocs.io/
4. Flask Documentation: https://flask.palletsprojects.com/
5. Sentiment Analysis Survey: https://arxiv.org/abs/2005.00357

---

## Group Information (Group #37)
- **Ankit Kumar Agarwal** (2024aa05560)
- **Chandrababu Yelamuri** (2024aa05820)
- **Deepan KG** (2024aa05755)
- **Preety Gupta** (2023ac05892)
- **Srithin Nair** (2024ab05197)

## Version Info
- **Version**: 2.0.0 (Enhanced Edition)  
- **Last Updated**: February 9, 2025  
- **Status**: Deployment Ready
