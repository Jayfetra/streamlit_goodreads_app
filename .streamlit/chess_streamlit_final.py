import streamlit as st
import plotly.express as px
import pandas as pd
import openai

from chess_com_download import (
    get_overall_stats,
    get_color_stats,
    get_elo_trend,
    get_termination_stats,
    get_opening_performance,
    get_opponent_analysis,
    get_time_of_day_performance,
)

# ============ CONFIG ============
st.set_page_config(page_title="DeepSeek Chess Coach", layout="wide")
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store API key in .streamlit/secrets.toml

# ============ APP TITLE ============
st.title("♟️ DeepSeek Chess Coach")
username = st.text_input("Enter your Chess.com username:")

if username:
    # 1st section - Overall stats
    st.header("1. Overall Stats")
    overall_stats = get_overall_stats(username)
    st.write(overall_stats)

    # 2nd section - Overall stats Black & White
    st.header("2. Color Stats (White vs Black)")
    color_stats = get_color_stats(username)
    st.bar_chart(color_stats.set_index("color")["win_rate"])

    # 3rd section - Elo rating over time
    st.header("3. Elo Rating Over Time")
    elo_df = get_elo_trend(username)
    fig_elo = px.line(elo_df, x="date", y="elo", color="time_control", title="Elo Rating Over Time")
    fig_elo.update_layout(title_font_size=22)
    st.plotly_chart(fig_elo, use_container_width=True)

    # 4th section - Termination types
    st.header("4. Game Termination Types")
    term_df = get_termination_stats(username)
    st.bar_chart(term_df.set_index("termination")["count"])

    # 5th section - Chess Opening Performance
    st.header("5. Chess Opening Performance")
    opening_df = get_opening_performance(username)
    fig_opening = px.bar(opening_df, x="opening", y="win_rate", title="Win Rate by Opening")
    fig_opening.update_layout(title_font_size=22, xaxis_tickangle=-45)
    st.plotly_chart(fig_opening, use_container_width=True)

    # 6th section - Stronger/Weaker Opponent Analysis
    st.header("6. Stronger vs Weaker Opponent")
    opp_df = get_opponent_analysis(username)
    st.write(opp_df)

    # 7th section - Time of Day Performance
    st.header("7. Time of Day Performance")
    tod_df = get_time_of_day_performance(username)
    fig_tod = px.bar(tod_df, x="time_of_day", y="win_rate", title="Performance by Time of Day")
    st.plotly_chart(fig_tod, use_container_width=True)

    # 8th section - Personalized ChatGPT Advice
    st.header("8. AI-Powered Chess Improvement Advice")

    if st.button("Generate Advice"):
        # Prepare insights from sections 1-7
        context = f"""
        Overall stats: {overall_stats.to_dict() if isinstance(overall_stats, pd.DataFrame) else overall_stats}
        Color stats: {color_stats.to_dict()}
        Elo trend: {elo_df.tail(5).to_dict()}
        Termination types: {term_df.to_dict()}
        Opening performance: {opening_df.sort_values('win_rate', ascending=False).head(5).to_dict()}
        Opponent analysis: {opp_df.to_dict()}
        Time of day performance: {tod_df.to_dict()}
        """

        prompt = f"""
        You are a chess coach. Based only on the data below (no external knowledge), give the user 3-5 actionable
        suggestions to improve their chess. Focus on weaknesses and opportunities.

        DATA:
        {context}
        """

        with st.spinner("Analyzing your games..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful chess coach analyzing player statistics."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=400,
            )

            advice = response["choices"][0]["message"]["content"]
            st.subheader("Your Personalized Advice:")
            st.write(advice)
