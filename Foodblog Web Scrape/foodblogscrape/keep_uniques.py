import pandas as pd

#read in desired data
df_new_scrape=pd.read_json("C:/Users/lowzh/Desktop/Portfolio/Web Scraper/foodblogscrape/foodinfo.json")

#Note: need  keep_default_na=False, otherwise by default empty fields will be read in as NaN in df
df_active=pd.read_csv("C:/Users/lowzh/Desktop/Portfolio/Web Scraper/foodblogscrape/foodinfo_active_file.csv", keep_default_na=False)
df_historical=pd.read_csv("C:/Users/lowzh/Desktop/Portfolio/Web Scraper/foodblogscrape/foodinfo_full_historical_data.csv", keep_default_na=False)

#union new scrape with active file
active_result=pd.concat([df_active,df_new_scrape])

#remove duplicates 
active_result.drop_duplicates(inplace=True)

#keep only top MAX_RECORDS 
MAX_RECORDS: int = 50
if active_result.shape[0] > MAX_RECORDS:
    active_result=active_result.tail(MAX_RECORDS)

active_result.to_csv("C:/Users/lowzh/Desktop/Portfolio/Web Scraper/foodblogscrape/foodinfo_active_file.csv",sep=',',index=False)

#union new scrape with historical data 
hist_result=pd.concat([df_historical,df_new_scrape])

#remove duplicates and save to csv
hist_result.drop_duplicates(inplace=True)
hist_result.to_csv("C:/Users/lowzh/Desktop/Portfolio/Web Scraper/foodblogscrape/foodinfo_full_historical_data.csv",sep=',',index=False)

