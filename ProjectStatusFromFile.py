from sqlalchemy import null
import streamlit as st
import pandas as pd
import plotly_express as px


def addData(data, series, name):
    table = []
    for s in series:
        s = data.loc[data[name[0]] == s].groupby(name).count()['ID']
        for i, v in s.iteritems():
            item = {}
            for index, val in enumerate(name):
                if(len(name) > 1):
                    item[val] = i[index]
                else:
                    item[val] = i
            item['Counts'] = v
            table.append(item)

    return pd.DataFrame(table).sort_values(by="Counts", ascending=False)


st.title("Project Status Report")
st.header(
    "Choose the project status file...")
st.text("Export from QP with ID, Status, Owner, Deadline")
file = st.file_uploader("")
if file is not None:
    ext = file.name.split(".")[1]
    # st.text(ext)
    data = None
    if(ext == 'csv'):
        data = pd.read_csv(file)
    elif ext == 'xlsx' or ext == 'xls':
        data = pd.read_excel(file)
    else:
        st.error("Please choose a 'csv' or 'xlsx' or 'xls' file type")
    if data is not None:
        data = data.drop(columns=['Deadline'])
        data = data.dropna(subset=['ID'], how='all')

        stats = data['Status'].unique()
        stats_table = addData(data, stats, ['Status'])
        st.subheader("Outstanding items total:")
        st.table(stats_table)
        stat_fig = px.bar(stats_table, x='Status', y='Counts')
        st.plotly_chart(stat_fig, use_container_width=True)

        people = data['Owner'].unique()
        people_table = addData(data, people, ['Owner', 'Status'])
        st.subheader("Outstanding items per preson:")
        st.table(people_table)
        people_fig = px.bar(people_table, x='Owner',
                            y='Counts', color="Status", barmode='stack')
        st.plotly_chart(people_fig, use_container_width=True)
        # st.dataframe(data)
