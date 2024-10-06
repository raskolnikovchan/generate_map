import streamlit as st
import pandas as pd
import folium
import googlemaps
import os

if "excel_path" not in st.session_state:
    st.session_state.excel_path = ""
if "map_path" not in st.session_state:
    st.session_state.map_path = ""


#住所を渡して緯度と経度を受け取る
def get_lat_lng(address_input:str, gmaps):
    try:
        geocode_result = gmaps.geocode(address_input)
        location = geocode_result[0]["geometry"]["location"]
        lat = location["lat"]
        lng = location["lng"]
        return (lat, lng)
    except:
        return (None, None)

st.title("Generate Map")
st.write("エクセルファイルを入れて作成してください。")
with st.form("data_to_map", clear_on_submit=True):
    title = st.text_input("title")
    api_key = st.text_input("your api_key")
    center_loc = st.text_input("address of a center location")
    file = st.file_uploader("excel file", type="xlsx")
    excel_submit = st.form_submit_button("マップを作成する")

    if excel_submit:
        gmaps = googlemaps.Client(key=api_key)
        df = pd.read_excel(file, header=2, usecols=[1, 2, 3])
        df = df.dropna()
        center_lat, center_lng = get_lat_lng(center_loc, gmaps)
        center = [center_lat, center_lng]
        folium_map = folium.Map(location=center, )

        for data in df.itertuples():
            lat, lng = get_lat_lng(data.住所, gmaps)
            df.at[data.Index, "緯度"] = lat
            df.at[data.Index, "経度"] = lng
            if lat == None or lng == None:
                continue
            try:
                folium.Marker(
                    location=[lat, lng],
                    popup=[data.地名, data.住所],
                    icon=folium.Icon(color="red")
                    ).add_to(folium_map)
            except:
                pass
        
        excel_path = f"{title}.xlsx"
        df.to_excel(excel_path)
        map_path = f"{title}.html"
        folium_map.save(map_path)
        


        st.session_state.excel_path = excel_path
        st.session_state.map_path = map_path
        




if st.session_state.excel_path:  
    with open(st.session_state.excel_path, "rb") as f:
        st.download_button(
            label="EXCELログダウンロード",
            data=f,
            file_name=os.path.basename(st.session_state.excel_path),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

if st.session_state.map_path:  
    with open(st.session_state.map_path, "rb") as f:
        st.download_button(
            label="マップダウンロード",
            data=f,
            file_name=os.path.basename(st.session_state.map_path),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

