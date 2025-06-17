import streamlit as st
import pandas as pd
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Dict, Any

# Konfigurasi halaman
st.set_page_config(
    page_title="Pencarian Naskah Lontara",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Embedded CSS styling
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@300;400;500;600;700&family=Noto+Serif:wght@400;500;600&display=swap');
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        font-family: 'Noto Serif', serif;
    }
    
    .description {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
        font-family: 'Noto Sans', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #2c3e50;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .lontara-text {
        font-family: 'Noto Sans', sans-serif;
        font-size: 1.8rem;
        font-weight: 500;
        color: #2c3e50;
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 2px solid #e8b86d;
        line-height: 1.8;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        letter-spacing: 0.5px;
    }
    
    .latin-text {
        font-family: 'Noto Sans', sans-serif;
        font-size: 1.3rem;
        font-weight: 500;
        color: #34495e;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 2px solid #90caf9;
        line-height: 1.6;
        font-style: italic;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .translation-text {
        font-family: 'Noto Serif', serif;
        font-size: 1.2rem;
        font-weight: 400;
        color: #2e7d32;
        background: linear-gradient(135deg, #f1f8e9 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 2px solid #81c784;
        line-height: 1.7;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .footer {
        text-align: center;
        color: #7f8c8d;
        font-style: italic;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 2px solid #ecf0f1;
        font-family: 'Noto Sans', sans-serif;
    }
    
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .lontara-text { font-size: 1.4rem; padding: 0.75rem; }
        .latin-text { font-size: 1.1rem; padding: 0.75rem; }
        .translation-text { font-size: 1rem; padding: 0.75rem; }
        .description { font-size: 1rem; padding: 1rem; }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_sample_data():
    """Membuat data sample jika file tidak ditemukan"""
    data = {
        'type': ['Class', 'Class', 'Class', 'Class', 'Class', 'Paragraf', 'Kalimat', 'Kata', 'Kata', 'Kata', 'Kata', 'Kata', 'Kata', 'Kata', 'Kata', 'Kata'],
        'name': ['Kata', 'Kalimat', 'Paragraf', 'latin', 'terjemahan', 'Paragraf1', 'Kalimat1_1', 'Maeki', 'namassing', 'Ni', 'tingkatkan', 'iman', 'taqwata', 'Ri', 'Allah', 'Taala'],
        'aksara': ['', '', '', '', '', 'ᨆᨕᨙᨀᨗ ᨊᨆᨔᨗᨂ ᨊᨗ tingkatkan iman dan taqwata ᨑᨗ ᨕᨒᨙ ᨈᨕᨒᨕ  ᨅᨈᨘᨓᨀᨊ ᨕᨈᨚᨍᨙᨂᨛᨀᨗ ᨈᨄ ᨔᨒᨁᨂ ᨕᨈᨚᨍᨙᨂ-ᨈᨚᨍᨙᨂᨛᨀᨗ ᨕᨁᨘᨀᨘᨂᨗ ᨄᨔᨘᨑᨚᨕᨊᨙ, ᨕᨈᨚᨍᨙᨂ-ᨈᨚᨍᨙᨂᨛᨀᨗ ᨆᨒᨑ ᨕᨒᨒᨗᨕᨂᨗ ᨄᨄᨗᨔᨂᨀᨊ', 'ᨆᨕᨙᨀᨗ ᨊᨆᨔᨗᨂ ᨊᨗ tingkatkan iman dan taqwata ᨑᨗ ᨕᨒᨙ ᨈᨕᨒᨕ', 'ᨆᨕᨙᨀᨗ', 'ᨊᨆᨔᨗᨂ', 'ᨊᨗ', 'ᨈᨗᨂᨙᨈᨀᨈᨊ', 'ᨕᨗᨆᨊ', 'ᨈᨀᨓᨈ', 'ᨑᨗ', 'ᨕᨒᨒᨗ', 'ᨈᨕ\'ᨒ'],
        'latin': ['', '', '', 'Transliterasi Teks', 'Terjemahan Teks', 'Maeki namassing ni tingkatkan iman dan taqwata ri Alé Ta\'ala. Battuwakana Attojengki Tappa Salagang Attojeng-Tojengki Aggaukangi Passuroanna, Attojeng-Tojengki Malla\' Allaliangi Papisangkana.', 'Maeki namassing ni tingkatkan iman dan taqwata ri Allah Ta\'ala', 'Maeki', 'namassing', 'ni', 'tingkatkan', 'iman', 'taqwata', 'ri', 'Allah', 'Ta\'ala'],
        'terjemahan': ['', '', '', 'Transliterasi Teks', 'Terjemahan Teks', 'Marilah (kita) bersungguh-sungguh dalam meningkatkan iman dan ketakwaan kita kepada Allah Ta\'ala. Hadapilah dengan hati nuranimu sebelum satu per satu hati nuranimu sungguh-sungguh mengerjakan perbuatannya, hati nuranimu akan menilai pertimbangannya.', 'Marilah (kita) bersungguh-sungguh dalam meningkatkan iman dan ketakwaan kita kepada Allah Ta\'ala.', 'Marilah kita', 'bersungguh-sungguh', 'Dalam hal/terhadap/untuk/oleh', 'meningkatkan', 'iman', 'ketakwaan', 'Kepada', 'Allah', 'Ta\'ala (Yang Maha Tinggi)'],
        'kategori': ['', '', '', '', '', '', '', 'perintah', 'kata sifat', 'kata penghubung', 'kata kerja', 'kata benda', 'kata benda', 'preposisi', 'kata benda', 'kata sifat']
    }
    return pd.DataFrame(data)

@st.cache_data
def load_data_from_sparql(endpoint_url: str) -> pd.DataFrame:
    sparql_query = """
    PREFIX lontara: <http://naskahlontara.org/lontara/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?s ?type ?label ?kategori ?aksara ?latin ?terjemahan
    WHERE {
        {
            # --- BAGIAN 1: Mengambil data Paragraf dan Kalimat ---
            # Di sini, semua info ada di dalam satu 'label'
            ?s a ?type .
            FILTER(?type IN (lontara:Paragraf, lontara:Kalimat))
            ?s rdfs:label ?label .
        }
        UNION
        {
            # --- BAGIAN 2: Mengambil data Kata melalui 'Latin' ---
            # Kita mulai dari 'Latin' sebagai pusat data kata
            ?s a lontara:Latin .
            BIND(lontara:Kata as ?type) # Kita tandai sebagai tipe 'Kata' untuk aplikasi

            # Ambil semua data dengan mengikuti relasi properti
            ?s rdfs:label ?latin .         # Label dari 'Latin' adalah teks latin itu sendiri
            BIND(?latin as ?label)         # Gunakan juga sebagai ?label agar konsisten

            OPTIONAL { ?s lontara:kategori ?kategori . }
            OPTIONAL {
                ?s lontara:memilikiTerjemahan ?terjemahanNode .
                ?terjemahanNode rdfs:label ?terjemahan .
            }
            OPTIONAL {
                ?s lontara:memilikiKata ?kataNode .
                ?kataNode rdfs:label ?aksara .
            }
        }
    }
    """

    sparql = SPARQLWrapper(endpoint_url)

    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader("Accept", "application/sparql-results+json")
    sparql.addCustomHttpHeader("Content-Type", "application/sparql-query")


    
    try:
        results = sparql.query().convert()
        data = []
        for result in results["results"]["bindings"]:
            
            type_uri = result["type"]["value"]
            type_label = type_uri.split("/")[-1]

            # --- LOGIKA KONDISIONAL YANG BARU DAN BENAR ---
            if type_label in ["Paragraf", "Kalimat"]:
                # Kasus 1: Parsing dari 'label' untuk Paragraf/Kalimat
                label_text = result["label"]["value"]
                name = result["s"]["value"].split("/")[-1]
                
                aksara_match = re.search(r'Aksara:\s*(.*?)\n', label_text, re.DOTALL)
                latin_match = re.search(r'Latin:\s*(.*?)\n', label_text, re.DOTALL)
                arti_match = re.search(r'Arti:\s*(.*)', label_text, re.DOTALL)
                
                aksara = aksara_match.group(1).strip() if aksara_match else ""
                latin = latin_match.group(1).strip() if latin_match else ""
                terjemahan = arti_match.group(1).strip() if arti_match else ""
                kategori = "" 
            
            else: # Kasus 2: 'Kata', ambil data langsung dari variabelnya
                name = result.get("label", {}).get("value", "")
                aksara = result.get("aksara", {}).get("value", "")
                latin = result.get("latin", {}).get("value", "")
                terjemahan = result.get("terjemahan", {}).get("value", "")
                kategori = result.get("kategori", {}).get("value", "")
            
            # --- Membuat baris untuk DataFrame ---
            row = {
                'type': type_label,
                'name': name,
                'aksara': aksara,
                'latin': latin,
                'terjemahan': terjemahan,
                'kategori': kategori
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        print("DEBUG: Berhasil terhubung ke SPARQL endpoint.")
        return df
    
    except Exception as e:
        st.error(f"❌ Gagal mengambil data dari SPARQL endpoint: {e}")
        # --- PERUBAHAN DI SINI ---
        st.warning("⚠️ Endpoint tidak dapat diakses. Menampilkan data sampel lokal sebagai gantinya.")
        return create_sample_data() # Ganti DataFrame kosong dengan data sampel


def search_in_data(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Pencarian dalam data berdasarkan latin atau terjemahan"""
    if not query.strip():
        return pd.DataFrame()
    
    query = query.lower().strip()
    
    # Pencarian di kolom latin dan terjemahan
    mask = (
        df['latin'].str.lower().str.contains(query, na=False, regex=False) |
        df['terjemahan'].str.lower().str.contains(query, na=False, regex=False) |
        df['name'].str.lower().str.contains(query, na=False, regex=False)
    )
    
    return df[mask]

def display_search_results(results: pd.DataFrame):
    """Menampilkan hasil pencarian dalam format yang rapi"""
    if results.empty:
        st.warning("Tidak ada hasil ditemukan untuk pencarian tersebut.")
        return
    
    st.success(f"Ditemukan {len(results)} hasil pencarian")
    
    # Group results by type
    for result_type in ['Paragraf', 'Kalimat', 'Kata']:
        type_results = results[results['type'] == result_type]
        if not type_results.empty:
            st.subheader(f"📋 {result_type} ({len(type_results)} hasil)")
            
            for idx, row in type_results.iterrows():
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.markdown(f"**{row['name']}**")
                        if row['kategori']:
                            st.caption(f"Kategori: {row['kategori']}")
                    
                    with col2:
                        # Aksara Lontara
                        if row['aksara']:
                            st.markdown("📜 Aksara Lontara:")
                            st.markdown(f'<div class="lontara-text">{row["aksara"]}</div>', 
                                        unsafe_allow_html=True)
                        
                        # Transliterasi Latin
                        if row['latin']:
                            st.markdown("🔤 Transliterasi Latin:")
                            st.markdown(f'<div class="latin-text">{row["latin"]}</div>', 
                                        unsafe_allow_html=True)
                        
                        # Terjemahan Indonesia
                        if row['terjemahan']:
                            st.markdown("🇮🇩 Terjemahan Indonesia:")
                            st.markdown(f'<div class="translation-text">{row["terjemahan"]}</div>', 
                                        unsafe_allow_html=True)
                
                st.divider()

def display_browse_data(df: pd.DataFrame, selected_type: str):
    """Menampilkan data berdasarkan tipe yang dipilih"""
    filtered_data = df[df['type'] == selected_type]
    
    if filtered_data.empty:
        st.warning(f"Tidak ada data {selected_type} ditemukan.")
        return
    
    st.subheader(f"📊 Data {selected_type} ({len(filtered_data)} item)")
    
    for idx, row in filtered_data.iterrows():
        with st.expander(f"{row['name']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                if row['aksara']:
                    st.markdown("📜 Aksara Lontara:")
                    st.markdown(f'<div class="lontara-text">{row["aksara"]}</div>', 
                                unsafe_allow_html=True)
                
                if row['latin']:
                    st.markdown("🔤 Transliterasi Latin:")
                    st.markdown(f'<div class="latin-text">{row["latin"]}</div>', 
                                unsafe_allow_html=True)
            
            with col2:
                if row['terjemahan']:
                    st.markdown("🇮🇩 Terjemahan Indonesia:")
                    st.markdown(f'<div class="translation-text">{row["terjemahan"]}</div>', 
                                unsafe_allow_html=True)
                
                if row['kategori']:
                    st.markdown(f"*Kategori:* `{row['kategori']}`")

def main():
    """Fungsi utama aplikasi"""
    # Load CSS (embedded)
    load_css()
    
    # URL endpoint default
    endpoint_lokal = "http://localhost:7200" # <-- GANTI DENGAN URL ENDPOINT LOKAL ANDA
    repository_name = "ontology-lontara"

    endpoint_url = f"{endpoint_lokal}/repositories/{repository_name}"

    # Load data from SPARQL (dengan fallback ke data sampel jika gagal)
    df = load_data_from_sparql(endpoint_url)

    # Header
    st.markdown('<div class="main-header">🏛 Pencarian Naskah Lontara</div>', 
                unsafe_allow_html=True)

    st.markdown("""
    <div class="description">
    Aplikasi ini memungkinkan Anda untuk mencari dan menjelajahi naskah dalam aksara Lontara 
    beserta transliterasi dan terjemahannya. Gunakan kotak pencarian untuk menemukan kata atau frasa 
    dalam transliterasi Latin atau terjemahan Bahasa Indonesia.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 Baca tentang asal-usul naskah ini"):
        st.write("""
            Naskah Lontara ini memiliki topik **"Perjalanan Isra' Mi'raj Nabi Muhammad SAW"** dan ditulis dalam aksara Lontara. 
            Naskah asli dimiliki oleh **Nasir Kula** dan disimpan di Kabupaten Takalar, Sulawesi Selatan.
            
            Naskah ini ditemukan pada tahun **1780** dan kemudian disalin kembali sekitar tahun **1890-an**. 
            Gunakan mode "Jelajahi Data" untuk mengenal isi naskah lebih lanjut!
        """)
    st.markdown("---")
    
    # Sidebar untuk navigasi
    with st.sidebar:
        st.header("🔍 Panel Navigasi")
        
        # Mode selection
        mode = st.radio(
            "Pilih Mode:",
            ["🔍 Pencarian", "📚 Jelajahi Data"],
            index=0
        )
        
        # Statistics
        # Cek dulu apakah df tidak kosong sebelum menghitung statistik
        if not df.empty:
            st.subheader("📊 Statistik Data")
            total_items = len(df)
            paragraf_count = len(df[df['type'] == 'Paragraf'])
            kalimat_count = len(df[df['type'] == 'Kalimat'])
            kata_count = len(df[df['type'] == 'Kata'])
            
            st.metric("Total Item", total_items)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Paragraf", paragraf_count)
                st.metric("Kalimat", kalimat_count)
            with col2:
                st.metric("Kata", kata_count)
        else:
            st.subheader("📊 Statistik Data")
            st.info("Data tidak dapat dimuat.")

    # Main content area
    if mode == "🔍 Pencarian":
        st.subheader("🔍 Pencarian Teks")
        
        # Search input
        search_query = st.text_input(
            "Masukkan kata kunci pencarian:",
            placeholder="Contoh: Allah, maeki, tingkatkan, iman...",
            help="Cari berdasarkan transliterasi Latin atau terjemahan Bahasa Indonesia"
        )
        
        # Search options
        col1, col2, col3 = st.columns(3)
        with col1:
            search_paragraf = st.checkbox("Cari di Paragraf", value=True)
        with col2:
            search_kalimat = st.checkbox("Cari di Kalimat", value=True)
        with col3:
            search_kata = st.checkbox("Cari di Kata", value=True)
        
        if search_query:
            # Filter by selected types
            search_types = []
            if search_paragraf:
                search_types.append('Paragraf')
            if search_kalimat:
                search_types.append('Kalimat')
            if search_kata:
                search_types.append('Kata')
            
            if search_types and not df.empty:
                filtered_df = df[df['type'].isin(search_types)]
                results = search_in_data(filtered_df, search_query)
                display_search_results(results)
            elif df.empty:
                 st.error("Data tidak tersedia untuk melakukan pencarian.")
            else:
                st.warning("Pilih minimal satu tipe pencarian.")
    
    else:  # Browse mode
        st.subheader("📚 Jelajahi Data")
        
        # Type selection for Browse
        browse_type = st.selectbox(
            "Pilih tipe data untuk dijelajahi:",
            ["Paragraf", "Kalimat", "Kata"],
            index=0
        )
        
        if not df.empty:
            display_browse_data(df, browse_type)
        else:
            st.error("Data tidak tersedia untuk dijelajahi.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
    📜 Aplikasi Pencarian Naskah Lontara - Preservasi Warisan Budaya Sulawesi Selatan
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()