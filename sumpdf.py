import streamlit as st
from PyPDF2 import PdfReader, PdfMerger
import io

st.set_page_config(page_title="PDF 병합기", page_icon="📎")
st.title("📎 PDF 병합기 - 순서 선택 & 페이지 범위 지정")

uploaded_files = st.file_uploader("📄 PDF 파일 업로드", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.markdown("### 🔢 병합할 순서와 페이지 범위를 선택하세요")

    n_files = len(uploaded_files)
    selected_orders = {}
    page_ranges = {}

    order_choices = list(range(1, n_files + 1))

    for i, uploaded_file in enumerate(uploaded_files):
        pdf_reader = PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)

        col1, col2 = st.columns([2, 3])
        with col1:
            # 사용자가 선택한 순서를 추적하며 중복을 방지
            available_orders = [o for o in order_choices if o not in selected_orders.values()]
            default_order = i + 1 if i + 1 in available_orders else available_orders[0]
            selected_order = st.selectbox(
                f"📑 병합 순서 - {uploaded_file.name}",
                options=available_orders,
                index=available_orders.index(default_order),
                key=f"order_{i}"
            )
            selected_orders[i] = selected_order

        with col2:
            page_range = st.text_input(
                f"📃 포함할 페이지 (예: 1-2, 4) - {uploaded_file.name}",
                value=f"1-{num_pages}",
                key=f"pages_{i}"
            )
            page_ranges[i] = page_range

    filename = st.text_input("💾 저장할 파일 이름을 입력하세요 (확장자 제외)", value="merged_pdf")

    if st.button("📚 PDF 병합하기"):
        try:
            # 병합 순서대로 정렬
            merge_plan = sorted([
                {
                    "order": selected_orders[i],
                    "file": uploaded_files[i],
                    "pages": page_ranges[i]
                }
                for i in range(n_files)
            ], key=lambda x: x["order"])

            merger = PdfMerger()

            for item in merge_plan:
                file = item["file"]
                page_range_text = item["pages"]
                pdf_reader = PdfReader(file)
                num_pages = len(pdf_reader.pages)

                # 페이지 파싱
                pages_to_merge = []
                for part in page_range_text.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages_to_merge.extend(range(start - 1, end))
                    else:
                        pages_to_merge.append(int(part) - 1)

                for i in pages_to_merge:
                    if 0 <= i < num_pages:
                        merger.append(file, pages=(i, i + 1))  # 한 페이지씩 추가

            # 저장
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
            st.error(f"❌ 오류 발생: {e}")
