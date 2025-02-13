import streamlit as st
import json
import pandas as pd

def load_data(file_path="database.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_top_scores(data, top_n=7):
    scores = {}
    for name, events in data.items():
        top_scores = sorted(events.values(), reverse=True)[:top_n]
        scores[name] = sum(top_scores)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def highlight_best_scores(val, best_scores):
    return "background-color: yellow; font-weight: bold" if val in best_scores else ""

data = load_data()
sorted_scores = calculate_top_scores(data)

st.title("🏆 10-kamp 2025 🏆")

# Podium Display
st.header("Pallen")

if len(sorted_scores) >= 3:
    st.markdown(f"""<h2 style='text-align:center;'>🥇 {sorted_scores[0][0]} - {sorted_scores[0][1]} pts</h2>""", unsafe_allow_html=True)
    st.markdown(f"""<h3 style='text-align:center;'>🥈 {sorted_scores[1][0]} - {sorted_scores[1][1]} pts</h3>""", unsafe_allow_html=True)
    st.markdown(f"""<h4 style='text-align:center;'>🥉 {sorted_scores[2][0]} - {sorted_scores[2][1]} pts</h4>""", unsafe_allow_html=True)
st.text("")
st.text("")
st.text("")

# List of other competitors
st.subheader("Resten av deltagerne")
for i, (name, score) in enumerate(sorted_scores[3:], start=4):
    st.write(f"{i}. {name} - {score} pts")

st.text("")
st.text("")
st.text("")
# Detailed Scores Table
st.subheader("Alle resultater")
df = pd.DataFrame.from_dict(data, orient="index")
for name in df.index:
    best_scores = sorted(df.loc[name], reverse=True)[:7]
    df.loc[name] = df.loc[name].apply(lambda x: f"{x}" if x in best_scores else x)

st.dataframe(df)
