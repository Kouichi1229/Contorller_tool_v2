import pandas as pd
import streamlit as st
from io import  StringIO
from strsimpy.jaro_winkler import JaroWinkler
from String_clean import *
from action import *
from TAKE_OUT_TYPE import *
import time

endcoding = 'utf-8-sig'
data_DB=pd.read_excel('./清單.xlsx')
#df = pd.read_csv("./測試樣本.csv",encoding=encoding)

upload_type= st.radio(
     "請選擇上傳檔案類型",
     ('Csv', 'Excel'))

if upload_type == 'Csv':
     st.write('上傳CSV檔')
     uploaded_file = st.file_uploader("清選擇清洗目標比對檔案 CSV檔")
     if uploaded_file is not None:
     # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
     #st.write(bytes_data)

     # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode(encoding))
     #st.write(stringio)

     # To read file as string:
        string_data = stringio.read()
     #st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file,encoding=encoding)
        #st.write(df)

        option_df = st.selectbox(
        '選擇要比對的欄位',
        (df.columns))

        st.write('你的比對欄位', df[option_df])

        
    #DB音便字體轉英文
        term_DB_list=[]
        for i in range(0,len(data_DB['AC'])):
            trem_string = (data_DB['AC'][i])
            term_DB_list.append(trem_string)
        data_DB['Assignee_Name_regex']=pd.Series(term_DB_list)

#音便字體轉英文
        term_list=[]
        for i in range(0,len(df[option_df])):
            trem_string = (df[option_df][i])
            term_list.append(trem_string)

        df['Assignee_Name_regex']=pd.Series(term_list)

        option = st.selectbox(
        '請選擇清洗方式',
        ('轉大寫 & 去除所有Corp及LLC及LTD型態(包含THE、AND)', 
        '轉大寫 & 去除所有Corp及LLC及LTD型態 & 德國類型公司(gmbh & co. kg...)(包含THE、AND)',
        '轉大寫 & 去除所有Corp及LLC及LTD型態(包含THE、AND 及 錯字)',
        '轉大寫 & 去除所有Corp及LLC及LTD型態 & 德國類型公司(gmbh & co. kg...)(包含THE、AND 及 錯字)',
        ''))



        time.sleep(3)

        if option=='轉大寫 & 去除所有Corp及LLC及LTD型態(包含THE、AND)':
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].astype(str).str.upper()
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].astype(str).str.partition(',')[0]
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].apply(lambda x:' '.join(word.upper() for word in x.split() if word not in TAKE_OUT_CORP_LLC_LTD))
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)

        elif option=='轉大寫 & 去除所有Corp及LLC及LTD型態 & 德國類型公司(gmbh & co. kg...)(包含THE、AND)':
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].astype(str).str.upper()
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].astype(str).str.partition(',')[0]
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].apply(lambda x:' '.join(word.upper() for word in x.split() if word not in TAKE_OUT_CORP_LLC_LTD_GERMANY))
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)


        elif option=='轉大寫 & 去除所有Corp及LLC及LTD型態(包含THE、AND 及 錯字)':
            WROG_WORDS=WRONG_WORDS_ALL()
            TAKE_OUT_CORP_LLC_LTD.append(WROG_WORDS)

            df['Assignee_Name_regex']=df['Assignee_Name_regex'].astype(str).str.upper()
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].astype(str).str.partition(',')[0]
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].apply(lambda x:' '.join(word.upper() for word in x.split() if word not in TAKE_OUT_CORP_LLC_LTD))
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)

        elif option=='轉大寫 & 去除所有Corp及LLC及LTD型態 & 德國類型公司(gmbh & co. kg...)(包含THE、AND 及 錯字)':
            WROG_WORDS=WRONG_WORDS_ALL()
            TAKE_OUT_CORP_LLC_LTD_GERMANY.append(WROG_WORDS)

            df['Assignee_Name_regex']=df['Assignee_Name_regex'].astype(str).str.upper()
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].astype(str).str.partition(',')[0]
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].apply(lambda x:' '.join(word.upper() for word in x.split() if word not in TAKE_OUT_CORP_LLC_LTD_GERMANY))
            df['Assignee_Name_regex']=df['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)
    
    #印出正規化後資料
        st.write(df[[option_df,'Assignee_Name_regex']])

        if st.button('比對'):
            if option=='轉大寫 & 去除所有Corp及LLC及LTD型態(包含THE、AND)':
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].astype(str).str.upper()
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].astype(str).str.partition(',')[0]
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].apply(lambda x:' '.join(word.upper() for word in x.split() if word not in TAKE_OUT_CORP_LLC_LTD))
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)

            elif option=='轉大寫 & 去除所有Corp及LLC及LTD型態 & 德國類型公司(gmbh & co. kg...)(包含THE、AND)':
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].astype(str).str.upper()
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].astype(str).str.partition(',')[0]
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].apply(lambda x:' '.join(word.upper() for word in x.split() if word not in TAKE_OUT_CORP_LLC_LTD_GERMANY))
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)


            elif option=='轉大寫 & 去除所有Corp及LLC及LTD型態(包含THE、AND 及 錯字)':
                WROG_WORDS=WRONG_WORDS_ALL()
                TAKE_OUT_CORP_LLC_LTD.append(WROG_WORDS)

                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].astype(str).str.upper()
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].astype(str).str.partition(',')[0]
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].apply(lambda x:' '.join(word.upper() for word in x.split() if word not in TAKE_OUT_CORP_LLC_LTD))
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)

            elif option=='轉大寫 & 去除所有Corp及LLC及LTD型態 & 德國類型公司(gmbh & co. kg...)(包含THE、AND 及 錯字)':
                WROG_WORDS=WRONG_WORDS_ALL()
                TAKE_OUT_CORP_LLC_LTD_GERMANY.append(WROG_WORDS)

                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].astype(str).str.upper()
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].astype(str).str.partition(',')[0]
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].apply(lambda x:' '.join(word.upper() for word in x.split() if word not in TAKE_OUT_CORP_LLC_LTD_GERMANY))
                data_DB['Assignee_Name_regex']=data_DB['Assignee_Name_regex'].replace('[^A-Za-z0-9]+','',regex=True)


            data_DB= data_DB.drop_duplicates(subset=None,keep="first",inplace=False)
            dic={}
            for i in range(0,len(data_DB['AC'])):
                dic[data_DB['Assignee_Name_regex'][i]]=data_DB['AC'][i]
        
   
            df['AC']=df['Assignee_Name_regex'].map(dic)

            not_Null= pd.notnull(df['AC'])
     
            st.write("總共有",len(df[option_df]),"與資料庫配對到的有",len(df[not_Null]))
            st.write(df[[option_df,'AC']])



#item_choice = st.radio(
     #"選擇項目",
     #('群組資料', '配對資料庫資料'))

#if item_choice == '群組資料':
    #group_df=df.groupby(['Assignee_Name_regex'])
    #st.write(group_df.size())
#else:
    #st.write("You didn't select comedy.")


    