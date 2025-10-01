import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Body na kružnici", layout="wide")

# Sidebar - vstupy
st.sidebar.header("Parametry kružnice")
x_center = st.sidebar.number_input("Střed X [m]", value=0.0)
y_center = st.sidebar.number_input("Střed Y [m]", value=0.0)
radius = st.sidebar.number_input("Poloměr [m]", min_value=0.1, value=5.0)
num_points = st.sidebar.slider("Počet bodů", min_value=1, max_value=50, value=8)
point_color = st.sidebar.color_picker("Barva bodů", value="#FF0000")

st.sidebar.header("Vaše údaje")
author_name = st.sidebar.text_input("Jméno autora", "Jan Novák")
author_contact = st.sidebar.text_input("Kontakt (email/telefon)", "jan.novak@email.cz")

# Generování bodů
angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
points_x = x_center + radius * np.cos(angles)
points_y = y_center + radius * np.sin(angles)

# Vykreslení grafu
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.plot(points_x, points_y, 'o', color=point_color, label='Body')
ax.plot([x_center], [y_center], 'x', color='black', label='Střed')
for i, (x, y) in enumerate(zip(points_x, points_y), start=1):
    ax.text(x, y, str(i), fontsize=10, ha='right')
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Informace o aplikaci
if st.button("O aplikaci"):
    st.info("""
    **Body na kružnici - Streamlit aplikace**  
    Autor: ChatGPT  
    Technologie: Python, Streamlit, Matplotlib, NumPy, FPDF  
    Funkce: generování bodů, vykreslení grafu, export do PDF
    """)

# Funkce pro PDF
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Body na kružnici", ln=True, align="C")
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Autor: {author_name}", ln=True)
    pdf.cell(0, 10, f"Kontakt: {author_contact}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"Střed: ({x_center}, {y_center}) m", ln=True)
    pdf.cell(0, 10, f"Poloměr: {radius} m", ln=True)
    pdf.cell(0, 10, f"Počet bodů: {num_points}", ln=True)
    pdf.cell(0, 10, f"Barva bodů: {point_color}", ln=True)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    pdf.image(buf, x=10, y=80, w=180)
    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return output

st.download_button(
    "Stáhnout PDF",
    data=create_pdf(),
    file_name="kruzice.pdf",
    mime="application/pdf"
)
