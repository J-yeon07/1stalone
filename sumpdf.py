import streamlit as st
from PyPDF2 import PdfReader, PdfMerger
import io

st.set_page_config(page_title="PDF 병합기", page_icon="📎")
st.title("📎 PDF 병합기 - 순서 조정 + 페이지 선택")

uploaded_files = st.file_uploader("📄 PDF 파일 업로드", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.markdown("### 🔢 병합할 순서와 페이지 범위를 선택하세요")

    file_options = []
    page_ranges = {}

    for i, uploaded_file in enumerate(uploaded_files):
        pdf_reader = PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        file_label = f"{i+1}. {uploaded_file.name} ({num_pages} page{'s' if num_pages > 1 else ''})"

        col1, col2 = st.columns([2, 2])
        with col1:
            new_order = st.number_input(f"👉 병합 순서 - {uploaded_file.name}", min_value=1, max_value=len(uploaded_files), value=i+1, key=f"order_{i}")
        with col2:
            page_input = st.text_input(f"📃 포함할 페이지 (예: 1-2, 4)", value=f"1-{num_pages}", key=f"pages_{i}")

        file_options.append({
            "file": uploaded_file,
            "order": new_order,
            "pages": page_input
        })

    filename = st.text_input("💾 저장할 파일 이름을 입력하세요 (확장자 제외)", value="merged_pdf")

    if st.button("📚 PDF 병합하기"):
        try:
            # 순서대로 정렬
            sorted_files = sorted(file_options, key=lambda x: x["order"])
            merger = PdfMerger()

            for item in sorted_files:
                file = item["file"]
                page_range_text = item["pages"]
                pdf_reader = PdfReader(file)
                num_pages = len(pdf_reader.pages)

                # 페이지 번호 파싱 (1부터 시작하는 것을 0부터 인덱싱 처리)
                pages_to_merge = []
                for part in page_range_text.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = part.split('-')
                        pages_to_merge.extend(range(int(start)-1, int(end)))
                    else:
                        pages_to_merge.append(int(part)-1)

                # 새 PDF에 해당 페이지만 추가
                temp_writer = PdfMerger()
                for i in pages_to_merge:
                    if 0 <= i < num_pages:
                        merger.append(file, pages=(i, i+1))  # append 한 페이지씩

            merged_pdf = io.BytesIO()
            merger.write(merged_pdf)
            merger.close()
            merged_pdf.seek(0)

            st.success("✅ 병합 완료! 아래에서 다운로드하세요.")
            st.download_button(
                label="📥 병합된 PDF 다운로드",
                data=merged_pdf,
                file_name=filename.strip() + ".pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
