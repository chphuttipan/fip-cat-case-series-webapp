import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Molnupiravir FIP case-series',
                   page_icon=":cat:", layout='wide', initial_sidebar_state='expanded')

st.title(':cat: Case series project: The efficacy of molnupiravir for management of the effusive feline infectious peritonitis in cats')
st.markdown("##")

# Import DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/chphuttipan/data/main/mu_fip_project4.csv')
df.drop(df.columns[0], axis = 1, inplace=True)

# Change feature in week column
df['week'] = df['week'].replace(4, 3)

st.markdown('##')

# Main Descriptive Stat
df_w0 = df[df['week'] == 0]
total_case = int(df_w0['case_number'].max())
med_molnu_dose = (df_w0['dose_monu'].median())
med_bw = df_w0['bw'].median()

left_col, middle_col, right_col = st.columns(3)
with left_col:
    st.subheader("Total Cases:")
    st.subheader(f"😺 :violet[{total_case}] cats")

with middle_col:
    st.subheader("Median Dose of Molnupiravir:")
    st.subheader(f"💉 :violet[{med_molnu_dose}] mg/kg")

with right_col:
    st.subheader("Median Body Weights:")
    st.subheader(f"🏋 :violet[{med_bw}] kg")

st.markdown("---")

left_col, right_col = st.columns([6,4])
with right_col:
    # Plot pie-chart by cat breed
    st.subheader("Cat Breed Distribution:")
    breed_counts = df_w0.groupby('breed').size().reset_index(name='counts')

    fig, ax = plt.subplots()
    ax.pie(breed_counts['counts'], labels=breed_counts['breed'], autopct='%1.1f%%')
    st.pyplot(fig)

with left_col:
    # Plot bar-chart by clinical signs
    week = st.sidebar.selectbox("Please Select Week of Clinical Signs Observation", df['week'].unique())
    df_select = df.query(
        "week == @week"
    )
    st.subheader("Clinical Signs Distribution")
    st.write(f"Select Week {week}")
    merge_counts = pd.DataFrame(columns=['sign'])

    for col in df_select.columns[7:11]:
        col_counts = df_select[col].value_counts().reset_index()
        col_counts.columns = ['sign', f'count_{col}']
        merge_counts = merge_counts.merge(col_counts, how='outer', on='sign', suffixes=('', f'_{col}')).fillna(0)

    merge_counts['total_count'] = merge_counts.iloc[:, 1:5].sum(axis=1)
    merge_counts.sort_values('total_count', ascending=False, inplace=True)

    fig, ax = plt.subplots()
    ax.bar(merge_counts['sign'], merge_counts['total_count'])
    ax.set_xlabel('Clinical Sign')
    ax.set_ylabel('Number of Occurrences')
    plt.xticks(rotation=90)
    st.pyplot(fig)
