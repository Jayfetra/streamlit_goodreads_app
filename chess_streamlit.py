import urllib.request

import gender_guesser.detector as gender
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import xmltodict
from pandas import json_normalize
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_lottie import st_lottie


st.set_page_config(page_title="Goodreads Analysis App", layout="wide")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

row0_1.title("Analyzing Your Chess Habits")

with row0_2:
    add_vertical_space()

row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

with row1_1:
    st.markdown(
        "This is a website to hopefully make you suck less and screw your opponent. Beat the idiot who keeps beating you in chess"    
        )
    st.markdown(
        "**Enter your chess.com user_id** 👇"
    )

row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))
with row2_1:
    
    user_input = st.text_input(
        "Input your own chess.com user_id (e.g. jay_fh)"
    )

    st.warning(
        """For now we only can get data from chess.com, 
        so please enter your chess.com user_id. If you don't have one, 
        you can create one [here](https://www.chess.com/register)."""
    )


line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))

with line1_1:
    st.markdown(
        "this is line1_1"
    )

st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row3_1:
    st.subheader("Win Rate Per Time Control")
    year_df = pd.DataFrame(df["read_at_year"].dropna().value_counts()).reset_index()
    year_df.columns = ["Year", "Count"]

    year_df = year_df.sort_values(by="Year")
    fig = px.bar(
        year_df,
        x="Year",
        y="Count",
        title="Win rate per time control",
        color_discrete_sequence=["#9EE6CF"],
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "It looks like you've read a grand total of **{} books with {} authors,** with {} being your most read author! That's awesome. Here's what your reading habits look like since you've started using Goodreads.".format(
            u_books, u_authors, df["book.authors.author.name"].mode()[0]
        )
    )


with row3_2:
    st.subheader("Detail")
    # plots a bar chart of the dataframe df by book.publication year by count in plotly. columns are publication year and count
    age_df = pd.DataFrame(df["book.publication_year"].value_counts()).reset_index()
    age_df.columns = ["publication_year", "count"]
    age_df = age_df.sort_values(by="publication_year")
    fig = px.bar(
        age_df,
        x="publication_year",
        y="count",
        title="Books Read by Publication Year",
        color_discrete_sequence=["#9EE6CF"],
    )
    fig.update_xaxes(title_text="Publication Year")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    avg_book_year = str(int(np.mean(pd.to_numeric(df["book.publication_year"]))))
    row_young = df.sort_values(by="book.publication_year", ascending=False).head(1)
    youngest_book = row_young["book.title_without_series"].iloc[0]
    row_old = df.sort_values(by="book.publication_year").head(1)
    oldest_book = row_old["book.title_without_series"].iloc[0]

    st.markdown(
        "Looks like the average publication date is around **{}**, with your oldest book being **{}** and your youngest being **{}**.".format(
            avg_book_year, oldest_book, youngest_book
        )
    )
    st.markdown(
        "Note that the publication date on Goodreads is the **last** publication date, so the data is altered for any book that has been republished by a publisher."
    )

add_vertical_space()

# df = pd.read_csv("jay_fh_historical_data.txt", sep='\t')
# df = df_chess_game_all.copy()

# display (df.head())
analysis_results = analyze_chess_games(df, 'jay_fh')
# display (analysis_results)
# print (analysis_results)
# Print the analysis results
for color, color_data in analysis_results.items():
    print(f"\n--- {color.title()} ---")
    for key, value in color_data.items():
        # print (1)
        print(f"\n--- {key.replace('_', ' ').title()} ---")
        if isinstance(value, dict):
            for index, data in value.items():
                print(f"{index}: {data}")
        else:
            print(value)