import streamlit as st
import requests
import pandas as pd
import time
import datetime

st.set_page_config(page_title="European Leagues Live Scores", layout="wide")
st.title("⚽ European Major Leagues - Live Score Panel")

def get_live_scores():
    url = "https://v3.football.api-sports.io/fixtures"
    raw_key = "0f006a6e45f9c3502c156a1c08bfe68b"
    clean_key = str(raw_key).strip().encode('utf-8').decode('latin-1')

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': clean_key
    }

    today_date = datetime.date.today().strftime('%Y-%m-%d')
    query_params = {"date": today_date}

    try:
        response = requests.get(url, headers=headers, params=query_params)
        data = response.json()

        match_list = []

        for item in data.get('response', []):
            home_goals = item['goals']['home'] if item['goals']['home'] is not None else 0
            away_goals = item['goals']['away'] if item['goals']['away'] is not None else 0
            elapsed_time = f"{item['fixture']['status']['elapsed']}'" if item['fixture']['status']['elapsed'] else "Not Started"

            match_list.append({
                "Lig": str(item['league']['name']),
                "Ülke": str(item['league']['country']),
                "Ev Sahibi": str(item['teams']['home']['name']),
                "Deplasman": str(item['teams']['away']['name']),
                "Skor": f"{home_goals} - {away_goals}",
                "Süre / Durum": str(elapsed_time)
            })

        return match_list

    except Exception as e:
        st.error(f"API Error: {e}")
        return []

# Verileri çek ve listele
match_list = get_live_scores()

if match_list:
    df = pd.DataFrame(match_list)
    st.subheader("🔥 Today's Live & Upcoming Football Matches Across Leagues")
    st.metric(label="Total Matches Today", value=len(df))
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("There are no matches scheduled or playing right now.")

st.caption(f"Last Updated At: {time.strftime('%H:%M:%S')}")

if st.button("🔄 Refresh Scores"):
    st.rerun()