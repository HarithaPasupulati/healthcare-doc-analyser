import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

def get_client():
    key = os.getenv("AZURE_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

def get_safety_flag(negative_score):
    if negative_score > 0.70:
        return "⚠️ HIGH RISK — Review required", "error"
    elif negative_score > 0.40:
        return "⚡ MEDIUM RISK — Monitor", "warning"
    else:
        return "✅ SAFE", "success"

def analyse(client, text):
    docs = [text]
    sentiment = client.analyze_sentiment(documents=docs)[0]
    entities = client.recognize_entities(documents=docs)[0]
    keyphrases = client.extract_key_phrases(documents=docs)[0]
    language = client.detect_language(documents=docs)[0]
    return sentiment, entities, keyphrases, language

st.title("🏥 Healthcare Document Analyser")
st.markdown("*Powered by Azure AI Language*")
st.divider()

text_input = st.text_area(
    "Enter a clinical note or patient feedback:",
    height=150,
    placeholder="e.g. Patient John Smith was admitted with severe chest pain..."
)

if st.button("🔍 Analyse Document"):
    if not text_input.strip():
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Analysing with Azure AI..."):
            client = get_client()
            sentiment, entities, keyphrases, language = analyse(client, text_input)

            st.divider()
            st.subheader("📊 Analysis Results")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Language", sentiment.sentiment.upper())
                flag_text, flag_type = get_safety_flag(
                    sentiment.confidence_scores.negative
                )
                if flag_type == "error":
                    st.error(flag_text)
                elif flag_type == "warning":
                    st.warning(flag_text)
                else:
                    st.success(flag_text)

            with col2:
                st.metric("Detected Language",
                    language.primary_language.name)
                st.metric("Confidence",
                    f"{language.primary_language.confidence_score:.0%}")

            st.divider()
            st.subheader("😊 Sentiment Scores")
            score_col1, score_col2, score_col3 = st.columns(3)
            score_col1.metric("Positive",
                f"{sentiment.confidence_scores.positive:.0%}")
            score_col2.metric("Neutral",
                f"{sentiment.confidence_scores.neutral:.0%}")
            score_col3.metric("Negative",
                f"{sentiment.confidence_scores.negative:.0%}")

            st.divider()
            st.subheader("🏷️ Named Entities")
            if entities.entities:
                entity_data = [
                    {
                        "Entity": e.text,
                        "Category": e.category,
                        "Confidence": f"{e.confidence_score:.0%}"
                    }
                    for e in entities.entities
                ]
                st.table(entity_data)
            else:
                st.info("No entities detected")

            st.divider()
            st.subheader("🔑 Key Phrases")
            if keyphrases.key_phrases:
                phrases = " • ".join(keyphrases.key_phrases)
                st.info(phrases)
            else:
                st.info("No key phrases detected")