import streamlit as st
from PyPDF2 import PdfMerger
import io

st.set_page_config(page_title="PDF 병합기", page_icon="📎")

st.title("📎 여러 개의 PDF를 하나로 병합하기")
st.markdown("여러 개의 PDF 파일을 선택해 주세요. 업로드 순서대로 병합됩니다.")

# 파일 업로드
uploaded_files = st.file_uploader("📄 PDF 파일 업로드", type="pdf", accept_multiple_files=True)

# 병합된 PDF 이름 입력
filename = st.text_input("💾 저장할 파일 이름을 입력하세요 (확장자 제외)", value="merged_pdf")

if uploaded_files:
    if st.button("📚 PDF 병합하기"):
        # PDF 병합
        merger = PdfMerger()
        for file in uploaded_files:
            merger.append(file)

        # 병합된 PDF 저장
        merged_pdf = io.BytesIO()
        merger.write(merged_pdf)
        merger.close()
        merged_pdf.seek(0)

        st.success("✅ 병합 완료! 아래에서 다운로드하세요.")

        # 파일명 확장자 붙이기
        download_filename = filename.strip() + ".pdf"

        # 다운로드 버튼
        st.download_button(
            label="📥 병합된 PDF 다운로드",
            data=merged_pdf,
            file_name=download_filename,
            mime="application/pdf"
        )
