"""
Sentiment Analysis Application
Author: Student Assignment
Date: 2025
Description: This module provides sentiment analysis functionality using NLTK and TextBlob
"""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import re
import string

# Download required NLTK data
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


class SentimentAnalyzer:
    """
    A comprehensive sentiment analysis class that uses multiple NLP techniques
    including VADER (Valence Aware Dictionary and sEntiment Reasoner) and TextBlob
    """
    
    def __init__(self):
        """Initialize the sentiment analyzer with necessary NLTK models"""
        self.sia = SentimentIntensityAnalyzer()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text):
        """
        Preprocess the input text by:
        1. Converting to lowercase
        2. Removing special characters and extra whitespace
        3. Tokenization
        4. Removing stopwords
        5. Lemmatization
        
        Args:
            text (str): Raw input text
            
        Returns:
            list: Processed tokens
            str: Cleaned text for analysis
        """
        # Convert to lowercase
        text_lower = text.lower()
        
        # Remove URLs
        text_cleaned = re.sub(r'http\S+|www\S+|https\S+', '', text_lower, flags=re.MULTILINE)
        
        # Remove email addresses
        text_cleaned = re.sub(r'\S+@\S+', '', text_cleaned)
        
        # Remove special characters and digits (but keep important punctuation)
        text_cleaned = re.sub(r'[^a-zA-Z\s!?.]', '', text_cleaned)
        
        # Remove extra whitespace
        text_cleaned = ' '.join(text_cleaned.split())
        
        # Tokenization
        tokens = word_tokenize(text_cleaned)
        
        # Remove stopwords and lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token.lower() not in self.stop_words and len(token) > 2
        ]
        
        return processed_tokens, text_cleaned
    
    def analyze_sentiment_vader(self, text):
        """
        Analyze sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)
        VADER is particularly good for social media and short texts
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Sentiment scores including compound score
        """
        scores = self.sia.polarity_scores(text)
        return {
            'positive': round(scores['pos'], 3),
            'negative': round(scores['neg'], 3),
            'neutral': round(scores['neu'], 3),
            'compound': round(scores['compound'], 3)
        }
    
    def analyze_sentiment_textblob(self, text):
        """
        Analyze sentiment using TextBlob
        Provides polarity (-1 to 1) and subjectivity (0 to 1) scores
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Polarity and subjectivity scores
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3)
        }
    
    def classify_sentiment(self, compound_score):
        """
        Classify sentiment based on compound score from VADER
        Uses standard VADER thresholds for individual sentence classification
        
        Args:
            compound_score (float): Compound sentiment score (-1 to 1)
            
        Returns:
            str: Sentiment classification (positive, negative, or neutral)
        """
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def classify_overall_sentiment(self, vader_scores, textblob_scores, sentence_sentiments, text=""):
        """
        Advanced sentiment classification that combines multiple signals:
        1. VADER compound score
        2. TextBlob polarity
        3. Sentence-level sentiment distribution
        4. Intensity of negative sentences (for review-style text)
        5. Keyword-based detection for strong negative/positive phrases VADER misses
        
        This addresses VADER's limitation with mixed-sentiment texts like movie reviews
        where nostalgic positivity can overshadow critical negativity.
        
        Args:
            vader_scores (dict): VADER sentiment scores
            textblob_scores (dict): TextBlob polarity and subjectivity
            sentence_sentiments (list): Per-sentence sentiment analysis
            text (str): Original text for keyword-based analysis
            
        Returns:
            tuple: (sentiment_label, confidence_score)
        """
        compound = vader_scores['compound']
        polarity = textblob_scores['polarity']
        
        # Strong negative phrases that VADER often misses or underweights
        strong_negative_phrases = [
            # Direct negative expressions
            'rubbish', 'utter rubbish', 'complete rubbish', 'total rubbish',
            'hopeless', 'completely hopeless', 'utterly hopeless',
            'waste of', 'waste of time', 'waste of money', 'waste of film',
            'terrible', 'horrible', 'awful', 'dreadful', 'atrocious',
            'error of judgment', 'huge error', 'big mistake', 'disaster',
            'pathetic', 'abysmal', 'appalling', 'disgraceful',
            'should hand in', 'should resign', 'should quit',
            'unacceptable', 'inexcusable', 'unforgivable',
            # Disappointment expressions  
            'disappointing', 'disappointed', 'disappointment', 
            'bitterly disappointing', 'hugely disappointing', 'let down', 'letdown',
            'to my disappointment', 'what a disappointment',
            # Review-specific negative phrases
            'sad sight', 'bad imitation', 'poor imitation',
            'pretty weak', 'very weak', 'quite weak', 'weak storyline', 'weak plot',
            'not very good', 'not that good', 'not so good', 'isnt that good',
            'didn\'t laugh', 'didnt laugh', 'never laughed',
            'boring', 'tedious', 'dull', 'bland', 'mediocre', 'forgettable',
            'wouldn\'t recommend', 'would not recommend', 'cannot recommend',
            'don\'t bother', 'dont bother', 'skip this', 'avoid this',
            'not worth', 'waste your time', 'save your money',
            'fails to', 'failed to', 'lacks', 'lacking',
            # Comparative negatives
            'worse than', 'inferior to', 'pales in comparison',
            'nothing like', 'far from', 'falls short'
        ]
        
        # Strong positive phrases (only if NOT preceded by "hoping for", "expected", etc.)
        strong_positive_phrases = [
            'excellent', 'outstanding', 'brilliant', 'fantastic', 'amazing',
            'masterpiece', 'incredible', 'superb', 'phenomenal', 'extraordinary',
            'highly recommend', 'must see', 'must watch', 'loved it', 'love it',
            'best ever', 'best movie', 'best film', 'thoroughly enjoyed',
            'blown away', 'exceeded expectations', 'pleasantly surprised'
        ]
        
        # Phrases that indicate positive words are being used hypothetically/negatively
        # (e.g., "I was hoping for excellent" means they DIDN'T get excellent)
        hope_disappointment_patterns = [
            'hoping', 'hoped', 'expected', 'expecting', 'wanted', 
            'wished', 'thought it would', 'should have been',
            'could have been', 'was supposed to'
        ]
        
        # Count keyword matches (case-insensitive)
        text_lower = text.lower() if text else ""
        negative_keyword_count = sum(1 for phrase in strong_negative_phrases if phrase in text_lower)
        positive_keyword_count = sum(1 for phrase in strong_positive_phrases if phrase in text_lower)
        
        # Check for hope-disappointment pattern (positive words used in context of letdown)
        has_hope_disappointment = any(pattern in text_lower for pattern in hope_disappointment_patterns)
        if has_hope_disappointment and 'disappointment' in text_lower:
            # The positive words are describing what was expected, not received
            # Reduce positive count and boost negative
            positive_keyword_count = max(0, positive_keyword_count - 2)
            negative_keyword_count += 1
        
        # Calculate keyword adjustment (-0.3 to +0.3 range)
        keyword_adjustment = 0
        if negative_keyword_count > positive_keyword_count:
            keyword_adjustment = -0.1 * min(negative_keyword_count, 3)  # Cap at -0.3
        elif positive_keyword_count > negative_keyword_count:
            keyword_adjustment = 0.1 * min(positive_keyword_count, 3)   # Cap at +0.3
        
        # Count sentence sentiments and their intensities
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        negative_intensity_sum = 0
        positive_intensity_sum = 0
        
        for sent in sentence_sentiments:
            if sent['sentiment'] == 'positive':
                positive_count += 1
                positive_intensity_sum += sent['confidence']
            elif sent['sentiment'] == 'negative':
                negative_count += 1
                negative_intensity_sum += sent['confidence']
            else:
                neutral_count += 1
        
        total_sentences = len(sentence_sentiments) if sentence_sentiments else 1
        
        # Normalize sentence distribution to -1 to 1 scale
        if positive_count + negative_count > 0:
            sentence_balance = (positive_count - negative_count) / (positive_count + negative_count)
        else:
            sentence_balance = 0
        
        # Calculate average intensity for each sentiment type
        avg_negative_intensity = negative_intensity_sum / negative_count if negative_count > 0 else 0
        avg_positive_intensity = positive_intensity_sum / positive_count if positive_count > 0 else 0
        
        # Intensity adjustment: Strong negative sentences should weigh more heavily
        intensity_adjustment = 0
        if avg_negative_intensity > 0.5 and negative_count >= 2:
            intensity_adjustment = -0.15 * (avg_negative_intensity - 0.5)
        elif avg_positive_intensity > 0.5 and positive_count >= 2:
            intensity_adjustment = 0.15 * (avg_positive_intensity - 0.5)
        
        # Combined weighted score with keyword adjustment
        combined_score = (
            compound * 0.30 +              # VADER compound (30%)
            polarity * 0.15 +              # TextBlob polarity (15%)
            sentence_balance * 0.25 +       # Sentence distribution (25%)
            keyword_adjustment +            # Keyword-based adjustment
            intensity_adjustment +
            # Bonus weight for TextBlob when VADER and TextBlob disagree
            (polarity * 0.10 if (compound > 0 and polarity < 0) or (compound < 0 and polarity > 0) else 0)
        )
        
        # Classification with adjusted thresholds
        if combined_score >= 0.12:
            sentiment = 'positive'
        elif combined_score <= -0.08:
            sentiment = 'negative'
        else:
            # For borderline cases, keyword detection takes priority
            if negative_keyword_count > positive_keyword_count:
                sentiment = 'negative'
            elif positive_keyword_count > negative_keyword_count:
                sentiment = 'positive'
            # Then check sentence distribution
            elif negative_count > positive_count and avg_negative_intensity > 0.3:
                sentiment = 'negative'
            elif positive_count > negative_count and avg_positive_intensity > 0.3:
                sentiment = 'positive'
            else:
                sentiment = 'neutral'
        
        # Calculate confidence
        confidence = abs(combined_score)
        # Boost confidence if keyword detection found strong signals
        if negative_keyword_count >= 2 or positive_keyword_count >= 2:
            confidence = min(confidence + 0.2, 1.0)
        # Boost confidence if multiple signals agree
        if (compound > 0 and polarity > 0 and sentence_balance > 0) or \
           (compound < 0 and polarity < 0 and sentence_balance < 0):
            confidence = min(confidence * 1.2, 1.0)
        
        return sentiment, round(confidence, 3)
    
    def get_detailed_analysis(self, text):
        """
        Perform comprehensive sentiment analysis combining multiple methods
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Comprehensive sentiment analysis results
        """
        # Preprocessing
        processed_tokens, cleaned_text = self.preprocess_text(text)
        
        # VADER Analysis
        vader_scores = self.analyze_sentiment_vader(text)
        
        # TextBlob Analysis
        textblob_scores = self.analyze_sentiment_textblob(text)
        
        # Sentence-level analysis (needed for advanced classification)
        sentences = sent_tokenize(text)
        sentence_sentiments = []
        for sentence in sentences:
            sent_scores = self.analyze_sentiment_vader(sentence)
            sentence_sentiments.append({
                'sentence': sentence.strip(),
                'sentiment': self.classify_sentiment(sent_scores['compound']),
                'confidence': abs(sent_scores['compound'])
            })
        
        # Advanced classification using multiple signals
        sentiment, confidence = self.classify_overall_sentiment(
            vader_scores, 
            textblob_scores, 
            sentence_sentiments,
            text  # Pass original text for keyword-based analysis
        )
        
        return {
            'overall_sentiment': sentiment,
            'confidence': confidence,
            'vader_scores': vader_scores,
            'textblob_scores': textblob_scores,
            'processed_tokens': processed_tokens,
            'token_count': len(processed_tokens),
            'sentence_count': len(sentences),
            'sentence_analysis': sentence_sentiments,
            'cleaned_text': cleaned_text
        }
    
    def analyze_multiple_texts(self, texts):
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts (list): List of texts to analyze
            
        Returns:
            list: List of analysis results for each text
        """
        results = []
        for text in texts:
            result = self.get_detailed_analysis(text)
            results.append(result)
        return results


# Utility functions
def extract_key_words(text, analyzer):
    """
    Extract important keywords from text based on sentiment
    
    Args:
        text (str): Input text
        analyzer (SentimentAnalyzer): Sentiment analyzer instance
        
    Returns:
        list: Important keywords
    """
    tokens, _ = analyzer.preprocess_text(text)
    return tokens[:10]  # Return top 10 tokens


def get_sentiment_confidence(score):
    """
    Get confidence level based on sentiment score
    
    Args:
        score (float): Compound sentiment score
        
    Returns:
        str: Confidence level (low, medium, high)
    """
    abs_score = abs(score)
    if abs_score >= 0.5:
        return 'high'
    elif abs_score >= 0.2:
        return 'medium'
    else:
        return 'low'
