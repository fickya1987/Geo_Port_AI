import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

openai.api_key = openai_api_key

# Add company logo
st.image("pelindo_logo.jfif", use_container_width=True)

st.title("Pelindo-TKMP AI Shipping Route Analysis")

# Define coordinates for the routes
def add_route_to_map(route_map, route_coords, route_name):
    for coord in route_coords:
        folium.Marker(coord, popup=f"{route_name}").add_to(route_map)
    folium.PolyLine(route_coords, color='blue', weight=2.5, opacity=0.8, tooltip=route_name).add_to(route_map)

routes = {
    "China-Indonesia": [
        (31.2304, 121.4737),  # Shanghai
        (28.1802, 121.2787),  # Ningbo
        (25.7528, 119.3400),  # Fuqing
        (23.3541, 116.6819),  # Shantou
        (22.5431, 114.0579),  # Shekou
        (-6.2088, 106.8456),  # Jakarta
        (-7.2575, 112.7521)   # Surabaya
    ],
    "Middle-East-Southeast Asia": [
        (26.3927, 50.9775),  # Dammam
        (25.276987, 55.296249),  # Jebel Ali
        (22.3039, 73.1926),  # Mundra
        (19.0760, 72.8777),  # Nhava Sheva
        (13.7234, 100.4762),  # Laem Chabang
        (10.7769, 106.7009),  # Cai Mep
        (1.3521, 103.8198),  # Singapore
        (-6.2088, 106.8456)   # Jakarta
    ],
    "Global Direct Call": [
        (40.7128, -74.0060),  # New York
        (36.8508, -76.2859),  # Norfolk
        (32.0835, -81.0998),  # Savannah
        (22.3964, 114.1095),  # Hong Kong
        (13.7234, 100.4762),  # Laem Chabang
        (1.3521, 103.8198),  # Singapore
        (-6.2088, 106.8456),  # Jakarta
        (-33.8688, 151.2093)  # Sydney
    ]
}

# Streamlit UI
st.title("Ship Route Visualization and Analysis")
st.markdown("This app visualizes various shipping routes and provides analysis using GPT-4o.")

# Route Selection
selected_route = st.selectbox("Select a route to visualize:", list(routes.keys()))

# Initialize map
m = folium.Map(location=[0, 100], zoom_start=3)

# Add selected route to the map
if selected_route:
    add_route_to_map(m, routes[selected_route], selected_route)

# Display the map
st_folium(m, width=700, height=500)

# GPT-4 Analysis
st.subheader("Analisis Pelindo AI")
if st.button("Pelindo AI"):
    prompt = (
        f"Rute yang dipilih adalah: {selected_route}. Berikan analisis mendalam tentang bagaimana rute ini memengaruhi efisiensi logistik untuk PT Pelindo. Sertakan dampak ekonomi, potensi kemacetan pelabuhan, dan peluang optimalisasi rute yang dapat meningkatkan efisiensi operasional."
    )

    # GPT-4 API call
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Anda adalah ahli analisis logistik dan pelabuhan."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=1.0
        )
        st.write(response.choices[0].message["content"].strip())
    except Exception as e:
        st.error(f"Error berkomunikasi dengan GPT-4: {e}")

# GPT-4 Custom Query
st.subheader("Global Search")
custom_query = st.text_area("Masukkan pertanyaan atau analisis yang Anda perlukan:")
if st.button("Search GPT-4"):
    if custom_query:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Anda adalah ahli analisis data dan logistik."},
                    {"role": "user", "content": custom_query}
                ],
                max_tokens=2048,
                temperature=1.0
            )
            st.write(response.choices[0].message["content"].strip())
        except Exception as e:
            st.error(f"Error berkomunikasi dengan GPT-4: {e}")
    else:
        st.warning("Mohon masukkan pertanyaan atau analisis yang diinginkan.")

