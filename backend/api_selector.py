# backend/api_selector.py

import re

# -----------------------------
# Static Database of Payment APIs Info
# (Later you can load this from a JSON if you want)
payment_api_info = {
    "stripe": {
        "name": "Stripe",
        "pros": [
            "Easy and fast setup for developers",
            "Supports 135+ currencies and payment methods",
            "Great documentation and SDKs",
            "Powerful fraud detection (Stripe Radar)"
        ],
        "cons": [
            "Slightly higher fees for international transactions",
            "Limited customization in some regions"
        ],
        "best_for": [
            "Startups",
            "Quick go-to-market",
            "Businesses focused on North America and Europe"
        ]
    },
    "adyen": {
        "name": "Adyen",
        "pros": [
            "Unified global payments platform",
            "Direct acquiring licenses in many countries",
            "Better for scaling large enterprise businesses",
            "Advanced risk management and local compliance support"
        ],
        "cons": [
            "Complex setup compared to Stripe",
            "Better suited for larger companies"
        ],
        "best_for": [
            "Enterprises",
            "Global merchants",
            "Businesses operating across multiple continents"
        ]
    }
}
# -----------------------------

def recommend_payment_apis(user_query):
    """
    Basic logic to suggest payment APIs based on user query keywords.
    (Later we can make this smarter using LLM too!)
    """
    user_query = user_query.lower()

    recommendations = []

    # Very simple keyword matching for now
    if any(word in user_query for word in ["startup", "fast", "simple", "quick", "easy"]):
        recommendations.append("stripe")
    if any(word in user_query for word in ["global", "international", "multi-currency", "enterprise", "scaling"]):
        recommendations.append("adyen")

    # If no strong match, suggest both
    if not recommendations:
        recommendations = ["stripe", "adyen"]

    return recommendations

def format_recommendations(recommendations):
    """
    Given list of API keys, return nicely formatted text to show user.
    """
    output = ""

    for api_key in recommendations:
        info = payment_api_info.get(api_key)
        if info:
            output += f"\n\n**{info['name']}**\n"
            output += f"**Best For:** {', '.join(info['best_for'])}\n"
            output += f"**Pros:** {', '.join(info['pros'])}\n"
            output += f"**Cons:** {', '.join(info['cons'])}\n"

    return output

def get_api_info(api_key):
    """Helper to fetch info of a single API when user picks one."""
    return payment_api_info.get(api_key)

# -----------------------------
# Example Usage
if __name__ == "__main__":
    query = input("Tell me your payment setup needs: ")
    recs = recommend_payment_apis(query)
    print(format_recommendations(recs))
