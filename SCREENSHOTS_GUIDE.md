# Application Flow & Screenshots Guide

## Overview
This document describes the screenshots that should be included in the final report to demonstrate the complete application flow.

---

## Screenshot 1: Application Home Page

**Description**: Initial state of the Sentiment Analysis Application

**Elements to Show**:
- Header with title and tagline
- Input area with text input field
- Two tabs: "Direct Text" and "Upload File"
- "Analyze" and "Clear" buttons
- "Results Card" area (empty/hidden initially)
- Clean, modern gradient background (purple gradient)

**What Users See**:
- Professional header: "💬 Sentiment Analysis Application"
- Subheader: "Analyze the sentiment of your text using advanced NLP techniques"
- Input textarea with placeholder text
- File upload tab alternative
- Loading and error message areas (hidden)

**Key Features Visible**:
- Tab-based navigation
- Input validation helpers
- Character limit indicator (5000 characters max)

---

## Screenshot 2: Positive Sentiment Example

**Description**: Application displaying analysis results for positive text

**Input Text**: "I absolutely love this product! It's amazing and exceeded my expectations."

**Elements to Show**:
- Text input area with the positive text entered
- Results section now visible with:
  - Sentiment badge (GREEN background with "POSITIVE" label)
  - Confidence meter showing ~90% (green progress bar)
  - Statistics grid showing:
    * Overall Sentiment: POSITIVE
    * Confidence: 0.92
    * Sentences: 1
    * Tokens: 6
  - Doughnut chart showing:
    * Positive segment (large, green)
    * Negative segment (small/none, red)
    * Neutral segment (moderate, blue)

**What This Demonstrates**:
- Successful sentiment analysis
- Visual feedback with colors (positive = green)
- Confidence scoring
- Real-time chart generation

---

## Screenshot 3: Detailed Analysis Tab

**Description**: Showing the detailed analysis breakdown

**Visible Information**:
- Three tabs: "Sentiment Scores", "Processed Tokens", "Sentence Analysis"
- **Sentiment Scores Tab** (active):
  * Positive Score: 0.55
  * Negative Score: 0.0
  * Neutral Score: 0.45
  * Compound Score: 0.87
  * Polarity: 0.88
  * Subjectivity: 0.62

**What This Demonstrates**:
- Multiple NLP metrics (VADER + TextBlob)
- Detailed breakdown of sentiment components
- Tab-based navigation for organized information

---

## Screenshot 4: Processed Tokens Tab

**Description**: Showing preprocessed and lemmatized tokens

**Elements to Show**:
- Tokens displayed as badges/pills with different colors
- Example tokens for the positive text:
  * "absolutely" (blue badge)
  * "love" (blue badge)
  * "product" (blue badge)
  * "amazing" (blue badge)
  * "exceeded" (blue badge)
  * "expectations" (blue badge)

**What This Demonstrates**:
- Text preprocessing results
- Lemmatization in action
- Removal of stopwords
- Visual token representation

---

## Screenshot 5: Sentence Analysis Tab

**Description**: Breaking down sentiment by individual sentence

**Elements to Show**:
- For the positive text example:
  * Sentence 1: "I absolutely love this product!"
    - Sentiment badge: POSITIVE (green)
    - Confidence: 91%
  * Sentence 2: "It's amazing and exceeded my expectations."
    - Sentiment badge: POSITIVE (green)
    - Confidence: 85%

**What This Demonstrates**:
- Sentence-level sentiment analysis
- Individual sentence confidence scores
- Granular sentiment breakdown

---

## Screenshot 6: Negative Sentiment Example

**Description**: Application analyzing negative sentiment text

**Input Text**: "This is terrible and I hate it. Worst purchase ever."

**Elements to Show**:
- Text input with negative text
- Results section with:
  - Sentiment badge (RED background with "NEGATIVE" label)
  - Confidence meter showing ~95% (red progress bar)
  - Statistics grid updated with negative values
  - Doughnut chart showing:
    * Positive segment (none/minimal, green)
    * Negative segment (large, red)
    * Neutral segment (minimal, blue)

**What This Demonstrates**:
- Correct identification of negative sentiment
- Color-coded feedback (negative = red)
- Handling of strong sentiment language
- High confidence for clear sentiment

---

## Screenshot 7: Neutral Sentiment Example

**Description**: Application analyzing neutral/factual text

**Input Text**: "The product is available in stores and has a size of 10 inches."

**Elements to Show**:
- Text input with neutral text
- Results section with:
  - Sentiment badge (BLUE background with "NEUTRAL" label)
  - Confidence meter showing ~10-20% (low confidence, balanced bar)
  - Statistics grid showing balanced positive/neutral scores
  - Doughnut chart showing:
    * Positive segment (small, green)
    * Negative segment (small/none, red)
    * Neutral segment (large, blue)

**What This Demonstrates**:
- Correct identification of neutral sentiment
- Lower confidence for factual text
- Balanced sentiment distribution
- Proper handling of informational content

---

## Screenshot 8: File Upload Feature

**Description**: Demonstrating file upload functionality

**Elements to Show**:
- File upload tab active
- File input area with text "Click to select file"
- File selected: "sample_text.txt"
- File size displayed: "1.2 KB"
- "Analyze File" button ready to click

**What This Demonstrates**:
- Alternative input method (file upload)
- Tab switching capability
- File validation UI

---

## Screenshot 9: File Analysis Results

**Description**: Results from analyzing uploaded file

**Elements to Show**:
- Input textarea now populated with file contents
- Results displayed below
- Same analysis structure as text input
- File name displayed in success message: "Successfully analyzed: sample_text.txt"

**What This Demonstrates**:
- File upload works correctly
- Content is properly extracted
- Analysis flows the same for both input methods
- User feedback about file processing

---

## Screenshot 10: Error Handling

**Description**: Demonstrating error messages

**Scenario 1 - Empty Input**:
- Error message: "Please enter some text to analyze"
- Red error box displayed
- Error message automatically disappears after analysis attempt

**Scenario 2 - Text Too Long**:
- Error message: "Text exceeds maximum length of 5000 characters"
- Character count shown: 5001 characters
- Input area highlighted (red border)

**Scenario 3 - Invalid File**:
- Error message: "File type not allowed. Allowed types: txt"
- File name shown: "document.pdf"
- File input remains visible for retry

**What This Demonstrates**:
- Input validation
- User-friendly error messages
- Graceful error handling
- Clear guidance for correction

---

## Screenshot 11: Mobile Responsive View

**Description**: Application on mobile device (320px width)

**Elements to Show**:
- Stacked layout (single column)
- Input card on top
- Results card below
- Full-width buttons
- Readable font sizes
- Proper spacing maintained

**What This Demonstrates**:
- Responsive design
- Mobile-friendly interface
- Touch-friendly buttons
- Proper breakpoints

---

## Screenshot 12: API Testing with cURL

**Description**: Backend API endpoint test

**Terminal Output**:
```
$ curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this!"}'

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
    ...
  }
}
```

**What This Demonstrates**:
- Backend API functionality
- JSON response format
- Successful API communication
- Integration testing capability

---

## Screenshot 13: Loading State

**Description**: Application during analysis processing

**Elements to Show**:
- Spinner animation (rotating circle)
- Loading message: "Analyzing sentiment..."
- Disabled analyze button (grayed out)
- Input field still visible
- Timestamp showing loading started

**What This Demonstrates**:
- User feedback during processing
- UI responsiveness
- Asynchronous operation handling
- Professional loading indicator

---

## Screenshot 14: Success Message

**Description**: Confirmation message after successful analysis

**Elements to Show**:
- Green success box
- Message: "Analysis complete!"
- Success icon (or green highlight)
- Message visible for 5 seconds then fades
- Results displayed below

**What This Demonstrates**:
- Positive user feedback
- Operation confirmation
- Professional UX pattern

---

## Screenshot 15: Browser Console Logs

**Description**: Developer tools showing logging

**Elements to Show**:
- Network tab showing API calls
- Request to `http://127.0.0.1:5000/api/analyze`
- Response status: 200 OK
- Request payload visible
- Response JSON visible
- No CORS errors
- No JavaScript errors

**What This Demonstrates**:
- Proper API communication
- No frontend/backend issues
- Successful data transmission
- Debugging capability

---

## Recommended Report Structure

### Page 1-2: Introduction & Overview
- Application description
- Features and capabilities
- Technology stack

### Page 3-4: Home Page & Interface (Screenshots 1-2)
- Initial application state
- First user interaction

### Page 5-6: Positive Sentiment (Screenshots 2-4)
- Analysis example with positive input
- Detailed breakdown

### Page 7: Negative Sentiment (Screenshot 6)
- Analysis example with negative input
- Comparison with positive sentiment

### Page 8: Neutral Sentiment (Screenshot 7)
- Analysis example with neutral input
- Balanced sentiment case

### Page 9: Alternative Input Methods (Screenshots 8-9)
- File upload feature
- Multiple input options

### Page 10: Error Handling (Screenshot 10)
- Input validation
- User-friendly errors

### Page 11: Mobile & API (Screenshots 11-13)
- Responsive design
- API testing

### Page 12: Loading & Feedback (Screenshots 13-14)
- User experience elements
- Feedback mechanisms

### Page 13: Developer Testing (Screenshot 15)
- API verification
- Network inspection

### Page 14-15: Conclusion
- Design decisions
- Challenges faced
- Future improvements

---

## How to Create Screenshots

### Using Windows
1. Press `Win + Shift + S` to open Snip & Sketch
2. Select area to capture
3. Save as PNG
4. Insert into document

### Using Mac
1. Press `Cmd + Shift + 4` for selection screenshot
2. Click and drag to select area
3. Screenshot saved to Desktop
4. Open in word processor to insert

### Using Browser DevTools
1. Press `F12` to open DevTools
2. Use Device Toolbar for mobile view
3. Use Print (`Ctrl + P`) for full page capture

---

## Tips for Professional Documentation

1. **Consistency**: Use same window size for all screenshots
2. **Clarity**: Ensure text is readable (at least 12pt font)
3. **Captions**: Add descriptive captions under each screenshot
4. **Highlighting**: Use arrows/circles to highlight key features
5. **Resolution**: Save at 1920x1080 or higher
6. **Format**: Use PNG for lossless quality
7. **Annotations**: Add labels to important elements

---

**Note**: This is a guide for creating screenshots. Your actual screenshots will vary based on your text inputs and system. Follow this guide to ensure comprehensive documentation of your application's functionality.

---

**Document Version**: 1.0
**Last Updated**: January 31, 2025
