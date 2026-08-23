from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=11)
pdf.multi_cell(0, 6, "A"*200)
pdf.ln(5)
try:
    pdf.multi_cell(0, 6, "A")
    print("A worked with ln(5)")
except Exception as e:
    print(f"Error on A with ln(5): {e}")

pdf.set_x(pdf.l_margin)
try:
    pdf.multi_cell(0, 6, "A")
    print("A worked with set_x")
except Exception as e:
    print(f"Error on A with set_x: {e}")
