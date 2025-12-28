import streamlit as st
import pandas as pd
import time

# --- CONFIGURATION (THE BRAND) ---
st.set_page_config(page_title="LITHOMANCER PRO", page_icon="💎", layout="centered")

# --- THE DATABASE (THE BRAIN) ---
# We structure this as a DataFrame for professional display
MINERAL_DATA = {
    "Material": ["HEMATITE (Real Iron)", "GALENA (Lead Ore)", "GOLD (24k)", "DIAMOND", "QUARTZ", "OPALITE (Glass)", "RESIN/PLASTIC", "SLAG (Industrial)"],
    "Type": ["ORE", "ORE", "PRECIOUS", "PRECIOUS", "COMMON", "FAKE", "FAKE", "WASTE"],
    "SG_Low": [5.0, 7.4, 19.0, 3.50, 2.60, 2.4, 1.0, 2.8],
    "SG_High": [5.3, 7.6, 19.3, 3.53, 2.70, 2.5, 1.3, 3.2],
    "Value_Est_Per_Gram": ["R 0.50", "R 0.20", "R 1400.00", "R 50000+", "R 0.10", "R 0.00", "R 0.00", "R 0.00"]
}
df = pd.DataFrame(MINERAL_DATA)

# --- THE LOGIC (THE CALCULUS) ---
def calculate_sg(air, water):
    if air <= water or water <= 0:
        return 0.0
    return air / (air - water)

def get_verdict(sg):
    # Filter the database for matches
    match = df[(df['SG_Low'] <= sg) & (df['SG_High'] >= sg)]
    return match

# --- THE INTERFACE (THE TRAP) ---
def main():
    # 1. HEADER
    st.title("💎 LITHOMANCER ASSAY TOOL")
    st.caption("FIELD UNIT: HAZYVIEW // AUTH: A. THORNE")
    st.markdown("---")

    # 2. INPUT SECTOR (The Ritual)
    col1, col2 = st.columns(2)
    with col1:
        w_air = st.number_input("Weight in AIR (g)", min_value=0.0, step=0.01, format="%.2f")
    with col2:
        w_water = st.number_input("Weight in WATER (g)", min_value=0.0, step=0.01, format="%.2f")

    # 3. THE EXECUTION
    if st.button("RUN FORENSIC ANALYSIS", type="primary"):
        if w_air > 0 and w_water > 0:
            with st.spinner('CALCULATING DENSITY MATRIX...'):
                time.sleep(1) # Dramatic pause for client perception
                sg_result = calculate_sg(w_air, w_water)

            # 4. THE REVEAL
            st.markdown(f"### 🔬 SPECIFIC GRAVITY: `{sg_result:.2f}`")

            matches = get_verdict(sg_result)

            if not matches.empty:
                st.success("MATCH CONFIRMED IN DATABASE")
                for index, row in matches.iterrows():
                    # This card is the "Product"
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color:#1E1E1E; padding:20px; border-radius:10px; border-left: 5px solid #00FF00;">
                            <h2 style="color:white;">{row['Material']}</h2>
                            <p style="color:#CCCCCC; font-size: 1.2em;">TYPE: {row['Type']}</p>
                            <p style="color:#00FF00; font-weight: bold; font-size: 1.5em;">EST. VALUE: {row['Value_Est_Per_Gram']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("NO DATABASE MATCH. UNKNOWN MATERIAL OR ALLOY.")
                st.warning("RECOMMENDATION: ACID TEST OR XRF SCAN REQUIRED.")

if __name__ == "__main__":
    main()
