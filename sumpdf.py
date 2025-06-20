import streamlit as st
from PyPDF2 import PdfMerger
import io

st.set_page_config(page_title="PDF 병합기", page_icon="📎")

st.title("📎 여러 개의 PDF를 하나로 병합하기")
st.markdown("여러 개의 PDF 파일을 선택해 주세요. 업로드 순서대로 병합됩니다.")

uploaded_files = st.file_uploader("PDF 파일 선택", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if st.button("📚 PDF 병합하기"):
        merger = PdfMerger()

        for file in uploaded_files:
            merger.append(file)

        merged_pdf = io.BytesIO()
        merger.write(merged_pdf)
        merger.close()
        merged_pdf.seek(0)

        st.success("병합 완료! 아래에서 다운로드하세요.")

        st.download_button(
            label="📥 병합된 PDF 다운로드",
            data=merged_pdf,
            file_name="merged.pdf",
            mime="application/pdf"
        )
