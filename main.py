import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt


class WebContentCurationSystem:
    def __init__(self, user_preferences):
        self.user_preferences = user_preferences
        self.content_data = []
        self.recommendations = []

    def gather_content(self):
        for keyword in self.user_preferences["keywords"]:
            url = f"https://www.examplewebsite.com/search?query={keyword}"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                articles = soup.find_all("article")
                for article in articles:
                    title = article.find("h2").text
                    content = article.find("div", class_="content").text
                    self.content_data.append({"title": title, "content": content})
        if len(self.content_data) == 0:
            raise ValueError("No content found.")

    def analyze_content(self):
        content_texts = [content["content"] for content in self.content_data]
        vectorizer = CountVectorizer()
        vectorized_content = vectorizer.fit_transform(content_texts)
        similarity_matrix = cosine_similarity(vectorized_content)
        for i, content in enumerate(self.content_data):
            scores = list(enumerate(similarity_matrix[i]))
            sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
            recommendation_indices = [idx for idx, _ in sorted_scores[1:4]]
            content["recommendations"] = [
                self.content_data[idx]["title"] for idx in recommendation_indices
            ]

    def personalize_recommendations(self):
        user_history = self.user_preferences["history"]
        for content in self.content_data:
            if content["title"] in user_history:
                self.recommendations.extend(content["recommendations"])

    def visualize_recommendations(self):
        sentiment_scores = []
        for recommendation in self.recommendations:
            sentiment_analyzer = SentimentIntensityAnalyzer()
            sentiment_scores.append(
                sentiment_analyzer.polarity_scores(recommendation)["compound"]
            )
        plt.hist(sentiment_scores, bins=10)
        plt.title("Sentiment Distribution of Recommendations")
        plt.xlabel("Sentiment Score")
        plt.ylabel("Count")
        plt.show()

    def run(self):
        self.gather_content()
        self.analyze_content()
        self.personalize_recommendations()
        self.visualize_recommendations()


if __name__ == "__main__":
    user_preferences = {
        "keywords": ["technology", "science"],
        "history": ["article1", "article2"],
    }
    curation_system = WebContentCurationSystem(user_preferences)
    curation_system.run()