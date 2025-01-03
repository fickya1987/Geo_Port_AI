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

st.markdown(
    """
    <h1 style="text-align: center; font-family: 'Helvetica', sans-serif; font-size: 36px; color: #2E86C1;">
        Pelindo-TKMP AI Route Analysis
    </h1>
    """,
    unsafe_allow_html=True
)

# Define coordinates for the routes
def add_route_to_map(route_map, route_coords, route_name, route_points):
    for coord, point_name in zip(route_coords, route_points):
        folium.Marker(coord, popup=f"{route_name}: {point_name}").add_to(route_map)
    folium.PolyLine(route_coords, color='blue', weight=2.5, opacity=0.8, tooltip=route_name).add_to(route_map)

routes = {
    "China-Indonesia": {
        "coords": [
            (31.2304, 121.4737),  # Shanghai
            (28.1802, 121.2787),  # Ningbo
            (25.7528, 119.3400),  # Fuqing
            (23.3541, 116.6819),  # Shantou
            (22.5431, 114.0579),  # Shekou
            (-6.2088, 106.8456),  # Jakarta
            (-7.2575, 112.7521)   # Surabaya
        ],
        "points": ["Shanghai", "Ningbo", "Fuqing", "Shantou", "Shekou", "Jakarta", "Surabaya"]
    },
    "Middle-East-Southeast Asia": {
        "coords": [
            (26.3927, 50.9775),  # Dammam
            (25.276987, 55.296249),  # Jebel Ali
            (22.3039, 73.1926),  # Mundra
            (19.0760, 72.8777),  # Nhava Sheva
            (13.7234, 100.4762),  # Laem Chabang
            (10.7769, 106.7009),  # Cai Mep
            (1.3521, 103.8198),  # Singapore
            (-6.2088, 106.8456)   # Jakarta
        ],
        "points": ["Dammam", "Jebel Ali", "Mundra", "Nhava Sheva", "Laem Chabang", "Cai Mep", "Singapore", "Jakarta"]
    },
    "Global Direct Call": {
        "coords": [
            (40.7128, -74.0060),  # New York
            (36.8508, -76.2859),  # Norfolk
            (32.0835, -81.0998),  # Savannah
            (22.3964, 114.1095),  # Hong Kong
            (13.7234, 100.4762),  # Laem Chabang
            (1.3521, 103.8198),  # Singapore
            (-6.2088, 106.8456),  # Jakarta
            (-33.8688, 151.2093)  # Sydney
        ],
        "points": ["New York", "Norfolk", "Savannah", "Hong Kong", "Laem Chabang", "Singapore", "Jakarta", "Sydney"]
    }
}

# Streamlit UI
st.markdown(
    """
    <h2 style="text-align: center; font-family: 'Helvetica', sans-serif; font-size: 28px; color: #2874A6;">
        Visualisasi dan Analisis Rute Kapal
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="font-family: 'Arial', sans-serif; font-size: 18px; color: #5D6D7E;">
        Aplikasi ini memvisualisasikan berbagai rute pelayaran dan menyediakan analisis Pelindo AI.
    </p>
    """,
    unsafe_allow_html=True
)

# Route Selection
selected_route = st.selectbox("Pilih rute untuk divisualisasikan:", list(routes.keys()))

# Initialize map
m = folium.Map(location=[0, 100], zoom_start=3)

# Add selected route to the map
if selected_route:
    route_data = routes[selected_route]
    add_route_to_map(m, route_data["coords"], selected_route, route_data["points"])

# Display the map
st_folium(m, width=700, height=500)

# GPT-4 Analysis
st.markdown(
    """
    <h3 style="font-family: 'Arial', sans-serif; font-size: 24px; color: #2E4053;">
        Analisis AI Pelindo
    </h3>
    """,
    unsafe_allow_html=True
)

if st.button("Analisis Pelindo AI"):
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
st.markdown(
    """
    <h3 style="font-family: 'Arial', sans-serif; font-size: 24px; color: #2E4053;">
        Pencarian Global
    </h3>
    """,
    unsafe_allow_html=True
)

custom_query = st.text_area("Masukkan pertanyaan atau analisis yang Anda perlukan:")
if st.button("Pelindo AI"):
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
            st.markdown(
                f"""<p style='font-family: Arial; font-size: 16px; color: #1F618D;'>{response.choices[0].message['content'].strip()}</p>""",
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error berkomunikasi dengan GPT-4: {e}")
    else:
        st.warning("Mohon masukkan pertanyaan atau analisis yang diinginkan.")

# Add Route Images and Descriptions
st.markdown(
    """
    <h3 style="font-family: 'Arial', sans-serif; font-size: 24px; color: #2E4053;">
        Gambar dan Deskripsi Rute
    </h3>
    """,
    unsafe_allow_html=True
)

st.image("Ship-route-description-from-Asia-to-Northern-Europe.png", caption="Rute Busan ke Hamburg")
st.markdown(
    """<div style="font-family: 'Arial'; font-size: 16px; color: #34495E; line-height: 1.6;">
    Berdasarkan peta yang Anda unggah, berikut adalah pelabuhan-pelabuhan yang dilewati oleh kapal dari Asia menuju Eropa Utara:
    - <strong>Busan (Korea Selatan)</strong>: Pelabuhan awal di Asia Timur.
    - <strong>Qingdao (China)</strong>: Pelabuhan di Tiongkok Timur.
    - <strong>Shanghai (China)</strong>: Salah satu pelabuhan terbesar di dunia.
    - <strong>Yantian (China)</strong>: Pelabuhan di wilayah Shenzhen.
    - <strong>Singapore</strong>: Pelabuhan penghubung utama di Asia Tenggara.
    - <strong>Algeciras (Spanyol)</strong>: Pelabuhan di pintu masuk ke Eropa melalui Selat Gibraltar.
    - <strong>Le Havre (Prancis)</strong>: Pelabuhan utama di Eropa Barat.
    - <strong>Rotterdam (Belanda)</strong>: Salah satu pelabuhan terbesar di Eropa.
    - <strong>Hamburg (Jerman)</strong>: Pelabuhan akhir di Eropa Utara.
    </div>""",
    unsafe_allow_html=True
)

st.image("attacks-redsea-trade-routes-map-POL3820.jpg", caption="Dampak Perubahan Rute Perdagangan Laut Merah")
st.markdown(
    """<div style="font-family: 'Arial'; font-size: 16px; color: #34495E; line-height: 1.6;">
    Peta ini mengilustrasikan bagaimana serangan terhadap kapal dagang di Laut Merah memengaruhi rute perdagangan:
    - <strong>Sebelum Perang Gaza</strong>: Rute utama mencakup Selat Hormuz, Selat Bab al-Mandab, dan Terusan Suez.
    - <strong>Selama Perang Gaza</strong>: Rute alternatif digunakan untuk menghindari area berisiko tinggi, memperpanjang waktu perjalanan secara signifikan.
    - <strong>Potensi Pengalihan Rute Minyak Teluk</strong>: Kapal menghindari seluruh wilayah Teluk Persia, menggunakan rute yang lebih panjang dan aman melalui Tanjung Harapan.
    <strong>Implikasi Strategis:</strong>
    - Biaya lebih tinggi karena rute yang lebih panjang.
    - Peningkatan biaya bahan bakar dan operasional.
    - Premi keamanan dan asuransi meningkat.
    </div>""",
    unsafe_allow_html=True
)

st.image("1500img-4.jpg", caption="Rute Jakarta ke Shanghai dan Kembali")
st.markdown(
    """<div style="font-family: 'Arial'; font-size: 16px; color: #34495E; line-height: 1.6;">
    <strong>Rute Hijau (Jakarta ke Shanghai)</strong>:
        - Jakarta (Indonesia), Surabaya, Shekou (China), Shantou, Fuqing, Shanghai-Ningbo (China).
    <strong>Rute Merah (Shanghai ke Jakarta)</strong>:
        - Shanghai-Ningbo, Fuqing, Shantou, Shekou, Manila (Filipina), Davao, Jakarta.
    <strong>Sorotan:</strong>
    - Menghubungkan Asia Tenggara dengan Tiongkok secara efisien.
    - Hub perdagangan regional Manila memainkan peran penting.
    </div>""",
    unsafe_allow_html=True
)

st.image("Direct-Call.jpg", caption="Rute Direct Call dari Tanjung Priok")
st.markdown(
    """<div style="font-family: 'Arial'; font-size: 16px; color: #34495E; line-height: 1.6;">
    Rute dari Tanjung Priok menghubungkan Indonesia langsung ke:
    - <strong>Amerika Serikat</strong>: Pelabuhan-pelabuhan di pantai timur seperti New York dan Norfolk.
    - <strong>Eropa</strong>: Pelabuhan seperti Rotterdam dan Hamburg.
    - <strong>Intra-Asia</strong>: Hub utama seperti Singapura dan Hong Kong.
    - <strong>Australia</strong>: Brisbane, Adelaide, Sydney, dan Melbourne.
    <strong>Manfaat:</strong>
    - Mengurangi waktu transit.
    - Rute ekspor yang kompetitif.
    </div>""",
    unsafe_allow_html=True
)



