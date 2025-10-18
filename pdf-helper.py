import streamlit as st
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import io

st.set_page_config(page_title="PDF 도우미☺️", page_icon="📄")
st.title("📄 PDF 도우미☺️")
st.markdown("병합기와 추출기, 두 가지 기능을 한 곳에서 사용할 수 있어요!")

# 기능 선택
mode = st.radio("🔧 기능을 선택하세요", ["📎 PDF 병합기", "✂️ PDF 추출기"])

# 작성자 이름 입력
user_name = st.text_input("👤 이름을 입력하세요 (결과 PDF에 기록됩니다)", value="")

st.divider()

# ---------------------------
# 📎 PDF 병합기
# ---------------------------
if mode == "📎 PDF 병합기":
    uploaded_files = st.file_uploader("📄 여러 개의 PDF 파일을 업로드하세요", type="pdf", accept_multiple_files=True)

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
                            merger.append(file, pages=(i, i + 1))

                merged_pdf = io.BytesIO()
                merger.write(merged_pdf)
                merger.close()
                merged_pdf.seek(0)

                st.success("✅ 병합 완료! 아래에서 다운로드하세요.")
                st.download_button(
                    label="📥 병합된 PDF 다운로드",
                    data=merged_pdf,
                    file_name=f"{filename.strip()}.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")

# ---------------------------
# ✂️ PDF 추출기
# ---------------------------
elif mode == "✂️ PDF 추출기":
    uploaded_file = st.file_uploader("📄 PDF 파일을 업로드하세요", type="pdf")

    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        st.info(f"이 PDF에는 총 **{num_pages}쪽**이 있습니다.")

        page_input = st.text_input(
            "📃 추출할 페이지를 입력하세요 (예: 1-3, 5, 7-9)",
            value="1"
        )

        filename = st.text_input("💾 저장할 파일 이름을 입력하세요 (확장자 제외)", value="extracted_pages")

        if st.button("✨ 페이지 추출하기"):
            try:
                writer = PdfWriter()
                pages_to_extract = []

                for part in page_input.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages_to_extract.extend(range(start - 1, end))
                    else:
                        pages_to_extract.append(int(part) - 1)

                for i in pages_to_extract:
                    if 0 <= i < num_pages:
                        writer.add_page(pdf_reader.pages[i])

                # 이름(작성자)을 메타데이터로 저장
                if user_name.strip():
                    writer.add_metadata({
                        "/Author": user_name.strip(),
                        "/Producer": "PDF 도우미☺️"
                    })

                extracted_pdf = io.BytesIO()
                writer.write(extracted_pdf)
                extracted_pdf.seek(0)

                st.success("✅ 페이지 추출 완료!")
                st.download_button(
                    label="📥 추출된 PDF 다운로드",
                    data=extracted_pdf,
                    file_name=f"{filename.strip()}.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")
