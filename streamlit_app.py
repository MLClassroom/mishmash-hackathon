import shutil
import streamlit as st
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from configparser import ConfigParser
from os import environ,mkdir
from uuid import uuid4
from shutil import rmtree
from os.path import join as pjoin
from os.path import exists
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
# from src.utils.utils import *


#env vars
try :
    conf = ConfigParser()
    conf.read('config.ini')
    blob_conn_string = conf['azblob']['conn_string']
    container_name = conf['azblob']['container_name']

except FileNotFoundError:
    blob_conn_string = environ['blob_conn_string']
    contrainer_name = environ['contrainer_name']

blob_service_client = BlobServiceClient.from_connection_string(blob_conn_string)

# ALL functions
def create_folders():
    """function init session"""
    temp_path = "temp"
    input_path = pjoin(temp_path,"input")
    output_path = pjoin(temp_path,"output")
    if not exists("temp"):
        mkdir("temp")
    if not exists(input_path):
        mkdir(input_path)
    if not exists(output_path):
        mkdir(output_path)
    return temp_path,input_path, output_path

def delete_folders():
    """function to cleanup session """
    temp_path = "temp",
    rmtree(temp_path)


@st.cache
def filters(df):
    # all columns
    all_columns = df.columns.values.tolist()

    # column sets
    column_sets = {}

    # price column subset
    column_sets['price_columns'] = ['Competitor1_RPI', 'Competitor2_RPI', 'Competitor3_RPI', 'Competitor4_RPI',
                                'RPI_Category', 'RPI_Subcategory', 'Avg_EQ_Price', 'EQ_Base_Price']

    # volume column subset
    column_sets['volume_columns'] = ['EQ_Category', 'EQ_Subcategory', 'Est_ACV_Selling', 'pct_ACV']

    # macro-economic variables
    column_sets['macro_columns'] = ['Median_Temp', 'Median_Rainfall', 'Fuel_Price', 'Inflation',
                                'Trade_Invest', 'Brand_Equity']

    # cost variables
    column_sets['cost_columns'] = ['Social_Search_Working_cost', 'Digital_Working_cost', 'Print_Working_Cost.Ads50',
                                'OOH_Working_Cost']

    # percent cost variables
    column_sets['percent_cost_columns'] = ['SOS_pct', 'Digital_Impressions_pct', 'pct_PromoMarketDollars_Category',
                                        'pct_PromoMarketDollars_Subcategory', 'Magazine_Impressions_pct']

    # impression count variables
    column_sets['impression_columns'] = ['Social_Search_Impressions', 'Digital_Impressions', 'Print_Impressions.Ads40',
                                        'OOH_Impressions']

    # other columns
    column_sets['other_columns'] = ['Any_Promo_pct_ACV', 'Any_Feat_pct_ACV', 'Any_Disp_pct_ACV', 'CCFOT',
                                'Avg_no_of_Items', 'TV_GRP']
    return column_sets


@st.cache
def key_pplot(key,column_sets):
    target_var ="EQ"
    col_set = column_sets[key] + [target_var]
    corr_mat = df[col_set].corr()

    # setup figure and axes
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_axes()

    # generate heatmap
    ax = sns.heatmap(corr_mat, vmin=-1, vmax=1, center=0,
                     cmap=sns.diverging_palette(20, 220, n=200),
                     square=True)

    # setup labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45,
                       horizontalalignment='right')

    # setup suptitle
    fig.suptitle(f'Column Set: {key}', fontsize=18)

    # show the plot
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


    return fig

def randplot():
    f = plt.figure()
    arr = np.random.normal(1, 1, size=100)
    plt.hist(arr, bins=20)
    return f

st.title("MishMash Hackathon")
"""
## Team-GEP
"""

@st.cache
def load_df(input_path,uploaded_file):
    filename = "rand.csv"
    local_file_name = pjoin(input_path, filename)
    with open(local_file_name,"w") as wfile:
        # wfile.write(uploaded_file)
        uploaded_file.seek(0)
        shutil.copyfileobj(uploaded_file,wfile)
    df =pd.read_csv(local_file_name)
    return df


# block to take file as input and upload it to blob
uploaded_file = st.file_uploader("Choose a csv file", type=["csv"])
# sess_id = str(uuid4())
temp_path,input_path, output_path = create_folders()
if st.button('print_df'):
    if uploaded_file is not None:
        df = load_df(input_path,uploaded_file)
        st.write(df)


df = pd.read_csv('temp/input/rand.csv')
cols = ["EQ","Digital_Impressions"]
st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)
st.write(df[st_ms])

filter_sets = filters(df)
pic = st.selectbox("choose column_keys", list(filter_sets.keys()), 0)
# st.pyplot(key_pplot(pic,filter_sets))
st.pyplot(randplot())



if st.button('upload to blob'):
    if uploaded_file is not None:
        #upload file to blob
        # st.write(pd.read_csv(uploaded_file))       
        local_file_name = pjoin(input_path, "rand.csv")

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
        with open(local_file_name, "rb") as data:
            blob_client.upload_blob(data,overwrite = True)

    st.write("uploading file to blob done")
    




