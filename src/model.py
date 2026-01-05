import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
from scipy.special import softmax

class SentimentAnalyzer:
    """
    Wrapper class for the Twitter-RoBERTa sentiment model.
    """
    
    # Using the specific model from Hugging Face Hub
    MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    def __init__(self):
        print(f"Loading model: {self.MODEL_NAME}...")
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.config = AutoConfig.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME)
        print("Model loaded successfully.")

    def predict(self, text: str):
        """
        Analyzes the sentiment of the input text.
        Returns: label (str), confidence (float)
        """
        # Encode input text
        encoded_input = self.tokenizer(text, return_tensors='pt')
        
        # Perform inference
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores) # Convert logits to probabilities

        # Get the highest scoring label
        ranking = np.argsort(scores)
        ranking = ranking[::-1] # Sort descending
        
        top_label_id = ranking[0]
        top_label = self.config.id2label[top_label_id]
        confidence = float(scores[top_label_id])

        return top_label, confidence