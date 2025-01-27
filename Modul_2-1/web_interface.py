#!/usr/bin/env python
# coding: utf-8

# In[18]:


import streamlit as st
import pyterrier as pt
import pickle

if not pt.started():
    pt.init()


# In[19]:


with open("/home/tim/Schreibtisch/2024-25-Data_Librarian-Reschop_Tim/Modul_2-1/violence_pubs.pkl", "rb") as f:
    data = pickle.load(f)
    # Überprüfen auf null-Werte
    data = data.replace('null', None)
    st.session_state["data"] = data


# In[20]:


def init():
    index = pt.IndexFactory.of("/home/tim/Schreibtisch/2024-25-Data_Librarian-Reschop_Tim/Modul_2-1/violece_index_mult/data.properties")
    st.session_state["engine"] = pt.BatchRetrieve(index, wmodel="TF_IDF")
    st.session_state["data"] = pickle.load(open("/home/tim/Schreibtisch/2024-25-Data_Librarian-Reschop_Tim/Modul_2-1/violence_pubs.pkl", "rb"))


# In[21]:


def search(query):
    res = st.session_state["engine"].search(query)
    fields_to_show = ['text', 'tags', 'url', 'author', 'description']
    
    for _, row in res.iterrows():
        score = round(row['score'], 2)
        entry = st.session_state["data"][st.session_state["data"]['docno'] == row['docno']].iloc[0]
        
        for field in fields_to_show:
            if field == "text":
                st.title(entry[field])
            else:
                st.write(f"{field.capitalize()}: \t {entry[field]}")
                
        st.write(f"Score: {score}")
        st.divider()


# In[22]:


if not "engine" in st.session_state:
    init()

query = st.sidebar.text_input("Query")
st.sidebar.button("Search", on_click=search, args=(query,))


# In[ ]:





# In[ ]:




