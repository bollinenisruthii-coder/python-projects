"""
AI Chatbot Engine using NLP (NLTK + TF-IDF + Cosine Similarity)
Provides intent classification, FAQ matching, and context-aware responses.
"""

import re
import json
import string
import logging
from datetime import datetime

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

# Download required NLTK data
def download_nltk_data():
    packages = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'punkt_tab']
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass

download_nltk_data()

lemmatizer = WordNetLemmatizer()

# ─── Intent Patterns ────────────────────────────────────────────────────────────

INTENT_PATTERNS = {
    'greeting': [
        r'\b(hi|hello|hey|good morning|good afternoon|good evening|howdy|greetings)\b'
    ],
    'farewell': [
        r'\b(bye|goodbye|see you|take care|thanks bye|thank you bye)\b'
    ],
    'thanks': [
        r'\b(thank you|thanks|thank u|thx|appreciate)\b'
    ],
    'admission': [
        r'\b(admission|apply|enroll|join|registration|how to get admission|application form)\b'
    ],
    'fees': [
        r'\b(fee|fees|cost|charges|tuition|payment|how much|price|amount)\b'
    ],
    'courses': [
        r'\b(course|courses|program|programs|branch|branches|department|departments|what do you offer)\b'
    ],
    'exam': [
        r'\b(exam|examination|test|schedule|timetable|date sheet|when is exam)\b'
    ],
    'hostel': [
        r'\b(hostel|accommodation|room|stay|boarding|dormitory|mess)\b'
    ],
    'placement': [
        r'\b(placement|job|package|salary|recruit|company|campus drive|career)\b'
    ],
    'scholarship': [
        r'\b(scholarship|financial aid|fee waiver|stipend|grant|bursary)\b'
    ],
    'transport': [
        r'\b(transport|bus|route|vehicle|travel|commute|pick up|drop)\b'
    ],
    'faculty': [
        r'\b(faculty|teacher|professor|staff|lecturer|instructor)\b'
    ],
    'library': [
        r'\b(library|books|reading room|e-library|digital library)\b'
    ],
    'sports': [
        r'\b(sports|games|gym|fitness|playground|cricket|football|basketball)\b'
    ],
    'contact': [
        r'\b(contact|phone|email|address|location|where|how to reach)\b'
    ],
    'timing': [
        r'\b(timing|time|hours|open|close|when does|college hours)\b'
    ],
    'eligibility': [
        r'\b(eligibility|eligible|criteria|qualification|marks|percentage|requirement)\b'
    ],
    'documents': [
        r'\b(document|documents|certificate|certificates|papers|required documents)\b'
    ],
    'events': [
        r'\b(event|events|fest|festival|cultural|technical|seminar|workshop)\b'
    ],
}

# ─── Static Responses ────────────────────────────────────────────────────────────

STATIC_RESPONSES = {
    'greeting': [
        "Hello! 👋 Welcome to the College Enquiry Chatbot. I'm here to help you with information about admissions, fees, courses, placements, and more. What would you like to know?",
        "Hi there! 😊 I'm your college assistant. Feel free to ask me anything about our college — admissions, courses, fees, hostel, placements, and more!",
        "Hey! Great to see you here. I can help you with all your college-related queries. What's on your mind?"
    ],
    'farewell': [
        "Goodbye! 👋 Feel free to come back anytime you have questions. Best of luck with your studies!",
        "Take care! 😊 If you have more questions later, I'm always here to help. Have a great day!",
        "Bye! Don't hesitate to reach out if you need any more information. All the best! 🎓"
    ],
    'thanks': [
        "You're welcome! 😊 Is there anything else I can help you with?",
        "Happy to help! Feel free to ask if you have more questions.",
        "Glad I could assist! Let me know if you need anything else. 🎓"
    ],
    'unknown': [
        "I'm sorry, I didn't quite understand that. Could you rephrase your question? You can ask me about admissions, fees, courses, hostel, placements, scholarships, transport, and more.",
        "Hmm, I'm not sure about that. Try asking about: admissions, fee structure, courses offered, exam schedule, hostel facilities, placement records, or scholarships.",
        "I don't have information on that specific topic. Please contact our office at info@college.edu or call +91-XXXXXXXXXX for detailed assistance."
    ]
}

# ─── Quick Reply Suggestions ─────────────────────────────────────────────────────

QUICK_REPLIES = {
    'greeting': ['Admission Process', 'Fee Structure', 'Courses Offered', 'Placement Record'],
    'admission': ['Eligibility Criteria', 'Required Documents', 'Last Date', 'Fee Structure'],
    'fees': ['Scholarship Info', 'Payment Modes', 'Hostel Fees', 'Course Fees'],
    'courses': ['B.Tech', 'MBA', 'BCA', 'Admission Process'],
    'placement': ['Top Recruiters', 'Average Package', 'Placement Process', 'Internships'],
    'hostel': ['Hostel Fees', 'Hostel Rules', 'Mess Timings', 'Facilities'],
    'default': ['Admission Process', 'Fee Structure', 'Courses Offered', 'Contact Us']
}


class CollegeChatbot:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
        self.faq_questions = []
        self.faq_answers = []
        self.faq_categories = []
        self.faq_ids = []
        self.is_trained = False
        self.conversation_context = {}  # session_id -> context

    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 1]
        return ' '.join(tokens)

    def train(self, faqs: list):
        """Train the chatbot with FAQ data."""
        if not faqs:
            logger.warning("No FAQs provided for training.")
            return

        self.faq_questions = []
        self.faq_answers = []
        self.faq_categories = []
        self.faq_ids = []

        for faq in faqs:
            # Add main question
            self.faq_questions.append(self.preprocess_text(faq.question))
            self.faq_answers.append(faq.answer)
            self.faq_categories.append(faq.category)
            self.faq_ids.append(faq.faq_id)

            # Add keyword variants
            if faq.keywords:
                keywords = [k.strip() for k in faq.keywords.split(',')]
                for kw in keywords:
                    if kw:
                        self.faq_questions.append(self.preprocess_text(kw + ' ' + faq.question))
                        self.faq_answers.append(faq.answer)
                        self.faq_categories.append(faq.category)
                        self.faq_ids.append(faq.faq_id)

        if self.faq_questions:
            self.vectorizer.fit(self.faq_questions)
            self.tfidf_matrix = self.vectorizer.transform(self.faq_questions)
            self.is_trained = True
            logger.info(f"Chatbot trained with {len(faqs)} FAQs ({len(self.faq_questions)} vectors).")

    def detect_intent(self, text: str) -> str:
        """Detect the intent of the user's message."""
        text_lower = text.lower()
        for intent, patterns in INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        return 'unknown'

    def find_best_faq(self, query: str, threshold: float = 0.3):
        """Find the best matching FAQ using TF-IDF cosine similarity."""
        if not self.is_trained:
            return None, 0.0

        processed_query = self.preprocess_text(query)
        if not processed_query.strip():
            return None, 0.0

        query_vec = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        if best_score >= threshold:
            return {
                'answer': self.faq_answers[best_idx],
                'category': self.faq_categories[best_idx],
                'faq_id': self.faq_ids[best_idx],
            }, best_score

        return None, best_score

    def get_response(self, user_message: str, session_id: str = None, user_id: int = None) -> dict:
        """Generate a response for the user's message."""
        if not user_message or not user_message.strip():
            return {
                'response': "Please type a question. I'm here to help! 😊",
                'intent': 'empty',
                'confidence': 0.0,
                'quick_replies': QUICK_REPLIES['default'],
                'source': 'static'
            }

        intent = self.detect_intent(user_message)

        # Handle static intents
        if intent in ('greeting', 'farewell', 'thanks'):
            import random
            responses = STATIC_RESPONSES[intent]
            return {
                'response': random.choice(responses),
                'intent': intent,
                'confidence': 1.0,
                'quick_replies': QUICK_REPLIES.get(intent, QUICK_REPLIES['default']),
                'source': 'static'
            }

        # Try FAQ matching
        faq_result, confidence = self.find_best_faq(user_message)

        if faq_result:
            category = faq_result['category'].lower()
            quick_replies = QUICK_REPLIES.get(category, QUICK_REPLIES.get(intent, QUICK_REPLIES['default']))
            return {
                'response': faq_result['answer'],
                'intent': intent,
                'confidence': round(confidence, 3),
                'quick_replies': quick_replies,
                'source': 'faq',
                'faq_id': faq_result['faq_id'],
                'category': faq_result['category']
            }

        # Fallback
        import random
        return {
            'response': random.choice(STATIC_RESPONSES['unknown']),
            'intent': 'unknown',
            'confidence': round(confidence, 3),
            'quick_replies': QUICK_REPLIES['default'],
            'source': 'fallback'
        }

    def get_suggestions(self, partial_text: str, limit: int = 5) -> list:
        """Return autocomplete suggestions based on partial input."""
        if not self.is_trained or len(partial_text) < 2:
            return []

        partial_lower = partial_text.lower()
        suggestions = []
        seen = set()

        for i, q in enumerate(self.faq_questions):
            original_q = q  # already preprocessed
            if partial_lower in original_q and original_q not in seen:
                suggestions.append(self.faq_answers[i][:80] + '...' if len(self.faq_answers[i]) > 80 else self.faq_answers[i])
                seen.add(original_q)
                if len(suggestions) >= limit:
                    break

        return suggestions


# Global chatbot instance
chatbot_instance = CollegeChatbot()


def get_chatbot() -> CollegeChatbot:
    return chatbot_instance


def retrain_chatbot():
    """Retrain chatbot with latest FAQs from database."""
    try:
        from models.faq import FAQ
        faqs = FAQ.query.filter_by(is_active=True).all()
        chatbot_instance.train(faqs)
        return True
    except Exception as e:
        logger.error(f"Error retraining chatbot: {e}")
        return False
