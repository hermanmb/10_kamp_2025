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

def get_podium(sorted_scores):
    podium = {1: [], 2: [], 3: []}
    if not sorted_scores:
        return podium

    current_place = 1
    last_score = None
    place_count = 0  # how many distinct score levels we’ve used

    for name, score in sorted_scores:
        if last_score is None:
            podium[current_place].append((name, score))
            last_score = score
            place_count = 1
        elif score == last_score:
            podium[current_place].append((name, score))
        else:
            place_count += 1
            current_place = place_count
            if current_place > 3:
                break
            podium[current_place].append((name, score))
            last_score = score

    # If two players share 2nd place → no 3rd place
    if len(podium[2]) > 1:
        podium[3] = []

    return podium

data = load_data()
sorted_scores = calculate_top_scores(data)

st.title("🏆 10-kamp 2025 🏆")

# Podium Display
st.header("Pallen")
podium = get_podium(sorted_scores)

max_place_used = max([place for place, players in podium.items() if players], default=0)
start_rank = max_place_used + 1

if podium[1]:
    st.markdown("<h2 style='text-align:center;'>🥇 " + 
                ", ".join([f"{n} - {s} pts" for n, s in podium[1]]) + 
                "</h2>", unsafe_allow_html=True)
if podium[2]:
    st.markdown("<h3 style='text-align:center;'>🥈 " + 
                ", ".join([f"{n} - {s} pts" for n, s in podium[2]]) + 
                "</h3>", unsafe_allow_html=True)
if podium[3]:
    st.markdown("<h4 style='text-align:center;'>🥉 " + 
                ", ".join([f"{n} - {s} pts" for n, s in podium[3]]) + 
                "</h4>", unsafe_allow_html=True)
st.text("")
st.text("")
st.text("")

# List of other competitors
st.subheader("Resten av deltagerne")
for i, (name, score) in enumerate(sorted_scores[sum(len(p) for p in podium.values()):], start=start_rank):
    st.write(f"{i+1}. {name} - {score} pts")

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
