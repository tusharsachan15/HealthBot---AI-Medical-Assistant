import streamlit as st
import time
from config import Config, PAGE_CONFIG, SYSTEM_PROMPTS
from utils.symptom_matcher import load_medical_data, load_doctor_data, match_symptoms, suggest_doctors
from utils.web_search import web_search
from utils.rag import retrieve, truncate_text
from models.llm import get_chatgroq_model

st.set_page_config(**PAGE_CONFIG)
Config.validate_config()

if "medical_df" not in st.session_state:
    st.session_state.medical_df = load_medical_data()
if "doctors" not in st.session_state:
    st.session_state.doctors = load_doctor_data()  

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "stop_generating" not in st.session_state:
    st.session_state.stop_generating = False

# UI
st.title("🏥 HealthBot - AI Medical Assistant")

mode = st.sidebar.radio("Response Style:", ["Concise", "Detailed"])
use_web = st.sidebar.checkbox("Enable Web Search", value=True)

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# User input

if prompt := st.chat_input("💬 Ask about symptoms or health queries..."):

    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.stop_generating = False

    with st.chat_message("assistant"):
        placeholder = st.empty()
        stop_button = st.button("⏹️ Stop Generating", key=f"stop_{len(st.session_state.chat_history)}")

        response_parts = []

        # Symptom matcher
        matches = match_symptoms(prompt, st.session_state.medical_df)
        if matches:
            for disease in matches:
                # Detailed vs Concise
                if mode == "Detailed":
                    response_parts.append(f"🦠 **Possible Condition**: {disease['Disease']}")
                    response_parts.append(f"📖 {disease['Description']}")
                    response_parts.append(f"💊 Suggested (general): {disease['Medicines']}")
                    response_parts.append(f"👨‍⚕️ Advice: {disease['Consultation']}")
                else:
                    response_parts.append(f"🦠 {disease['Disease']} - {disease['Consultation']}")

                # Doctor recommendations
                doctors_list = suggest_doctors(disease['Disease'], st.session_state.doctors)
                if doctors_list:
                    for doctor in doctors_list:
                        if mode == "Detailed":
                            response_parts.append(
                                f"👨‍⚕️ **Doctor Recommendation**: {doctor['name']} ({doctor['specialty']})\n"
                                f"🏥 {doctor['hospital']}\n"
                                f"📞 {doctor['contact']}"
                            )
                        else:
                            response_parts.append(f"👨‍⚕️ Doctor: {doctor['name']} ({doctor['specialty']})")
                else:
                    response_parts.append("👨‍⚕️ Doctor: No specialist found for this condition.")

        #  RAG knowledge retrieval
        rag_docs = retrieve(prompt)
        if rag_docs:
            if mode == "Detailed":
                response_parts.append("📚 **Related Knowledge:**")
                for doc in rag_docs:
                    text = truncate_text(doc, limit=500)
                    response_parts.append(f"- {text}")
            else:
                response_parts.append("📚 Related Knowledge:")
                for doc in rag_docs[:3]:
                    first_sentence = doc.split(".")[0]
                    response_parts.append(f"- {first_sentence}.")

        if use_web:
            results = web_search(prompt)
            if results:
                if mode == "Detailed":
                    response_parts.append("🌐 **Web Search Results:**")
                    for r in results:
                        response_parts.append(f"- {r}")
                else:
                    response_parts.append("🌐 Web Search Results:")
                    for r in results[:3]:  # limit in concise mode
                        response_parts.append(f"- {r}")

        response_parts.append(
            "⚠️ *This information is for educational purposes only. Please consult a licensed doctor for medical advice.*"
        )

        bot_reply = "\n\n".join(response_parts)
        typed_text = ""
        for char in bot_reply:
            if stop_button or st.session_state.stop_generating:
                st.session_state.stop_generating = True
                break
            typed_text += char
            placeholder.markdown(typed_text)
            time.sleep(0.01)

    st.session_state.chat_history.append({"role": "assistant", "content": typed_text})
