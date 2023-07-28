import streamlit as st
import pandas as pd
import numpy as np
import os
from witmotion_converter import WitMotionConverter

st.title('Witmotion Binary Converter')
st.caption('This Tool converts the output of witmotion Offline Dataloggers (WT901SD*) to a csv File.')
uploaded_file = st.file_uploader("Input File")
if uploaded_file is not None:
    st.write("uploaded file")
    basename = os.path.splitext(uploaded_file.name)[0]
    newName = basename+'.csv'
    bytes_data = uploaded_file.getvalue()
    conv = WitMotionConverter()
    data = conv.get_accelectaions(bytes_data)
    chart_data = pd.DataFrame(
        data,
        columns=['i', 't', 'x', 'y', 'z'])
    #time_data = chart_data.drop(['x', 'y', 'z', 'i'], axis=1)
    chart_data = chart_data.drop(['i', 't'], axis=1)
    #chart_data.set_axis(['i', 't'], axis='columns')

    st.line_chart(chart_data)
    csv = conv.toCsv(data)
    st.download_button('Download CSV', csv, mime="text/csv", file_name=newName)
