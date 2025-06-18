import streamlit as st
from parser_script import parse_companies, get_max_page
import io
import pandas as pd

st.set_page_config(page_title="Парсер Made-in-China", layout="centered")

st.markdown(
    "<h1 style='white-space: nowrap;'>🌏 Парсер компаний с Made-in-China</h1>",
    unsafe_allow_html=True
)

search_query = st.text_input("🔍 Введите, что искать (например: conveyor belting)", value="conveyor belting")

if search_query:
    max_pages = get_max_page(search_query)
    st.markdown(f"Максимально доступно страниц для парсинга: **{max_pages}**")

    start_page = st.number_input(
        "▶️ Начать с страницы",
        min_value=1,
        max_value=max_pages,
        value=1
    )

    pages = st.number_input(
        "📄 Количество страниц для парсинга",
        min_value=1,
        max_value=max_pages - start_page + 1,
        value=1
    )

    # ✅ ДОБАВЛЕНО: контейнер для отображения прогресса
    progress_placeholder = st.empty()

    # ✅ ДОБАВЛЕНО: функция обновления прогресса
    def show_current_page(p):
        progress_placeholder.info(f"🔄 Обработка страницы: {p}")

    if st.button("🚀 Запустить парсинг"):
        with st.spinner("Парсинг данных..."):
            try:
                data_list, last_page = parse_companies(
                    query=search_query,
                    start_page=start_page,
                    page_count=pages,
                    progress_callback=show_current_page  # ✅ ДОБАВЛЕНО: передача колбэка
                )
                df = pd.DataFrame(data_list)
            except Exception as e:
                st.error(f"Ошибка при парсинге: {e}")
                df = pd.DataFrame()
                last_page = 0

        if not df.empty:
            st.success(f"Готово! Найдено компаний: {len(df)}")
            st.info(f"Успешно обработано страниц: {last_page - start_page + 1} из {pages}")
            st.dataframe(df)

            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            st.download_button(
                label="📥 Скачать Excel-файл",
                data=output,
                file_name="made_in_china_companies.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Данные не найдены или произошла ошибка.")