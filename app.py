import streamlit as st
from pdf_generator import generate_quotation_pdf
from calculator import calculate_standard_cut
from offcut import split_remaining_sheet, evaluate_offcut


st.set_page_config(
    page_title="Fabrication Quotation Calculator",
    page_icon="📐",
    layout="centered",
)

st.title("Fabrication Quotation Calculator")
st.caption("Create customer fabrication quotations.")


# --------------------------------------------------
# QUOTATION STORAGE
# --------------------------------------------------

if "quotation_items" not in st.session_state:
    st.session_state.quotation_items = []


# --------------------------------------------------
# CUSTOMER DETAILS
# --------------------------------------------------

st.subheader("Customer Details")

customer_name = st.text_input("Customer Name")

customer_phone = st.text_input(
    "Phone Number",
    placeholder="Optional"
)


# --------------------------------------------------
# ORDER ITEM
# --------------------------------------------------

st.subheader("Add Order Item")

thickness = st.selectbox(
    "Material Thickness",
    ["1.5mm", "1.8mm", "2mm", "2.5mm"],
)

col1, col2 = st.columns(2)

with col1:
    length = st.number_input(
        "Length (inches)",
        min_value=1.0,
        value=55.0,
    )

with col2:
    width = st.number_input(
        "Width (inches)",
        min_value=1.0,
        value=39.0,
    )

quantity = st.number_input(
    "Quantity",
    min_value=1,
    value=1,
    step=1,
)


# --------------------------------------------------
# OFFCUT METHOD
# --------------------------------------------------

st.write("### Offcut Method")

calculation_method = st.radio(
    "Remaining material:",
    [
        'Automatic — Standard 4" belts',
        "Manual — Enter offcut value",
    ],
)

manual_offcut_value = None

if calculation_method == "Manual — Enter offcut value":

    manual_offcut_value = st.number_input(
        "Usable remaining material value (₦)",
        min_value=0.0,
        value=0.0,
        step=100.0,
    )


# --------------------------------------------------
# PREVIEW / ADD ITEM
# --------------------------------------------------

try:

    preview = calculate_standard_cut(
        length=length,
        width=width,
        thickness=thickness,
        quantity=quantity,
        offcut_value_override=manual_offcut_value,
    )

    st.write("### Price Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Unit Price",
            f'₦{preview["unit_price"]:,.0f}',
        )

    with col2:
        st.metric(
            "Line Total",
            f'₦{preview["total_price"]:,.0f}',
        )


    with st.expander("Calculation Details"):

        st.write(
            f'Normalized size: '
            f'{preview["length"]:g}" × '
            f'{preview["width"]:g}"'
        )

        st.write(
            f'Material price: '
            f'₦{preview["raw_price"]:,.0f}'
        )

        st.write(
            f'Standard 4" belts: '
            f'{preview["total_belts"]}'
        )

        st.write(
            f'Standard offcut value: '
            f'₦{preview["standard_offcut_value"]:,.0f}'
        )

        st.write(
            f'Final offcut value: '
            f'₦{preview["final_offcut_value"]:,.0f}'
        )


    if st.button(
        "➕ Add Item to Quotation",
        type="primary",
        use_container_width=True,
    ):

        item = {
            "original_length": length,
            "original_width": width,
            "length": preview["length"],
            "width": preview["width"],
            "thickness": thickness,
            "quantity": quantity,
            "unit_price": preview["unit_price"],
            "total_price": preview["total_price"],
            "offcut_value": preview["final_offcut_value"],
            "calculation_mode": preview["calculation_mode"],
        }

        st.session_state.quotation_items.append(item)

        st.success("Item added to quotation.")

        st.rerun()


except ValueError as error:

    st.error(str(error))


# --------------------------------------------------
# CURRENT QUOTATION
# --------------------------------------------------

st.divider()

st.subheader("Current Quotation")

if not st.session_state.quotation_items:

    st.info("No items added yet.")

else:

    grand_total = 0

    for index, item in enumerate(
        st.session_state.quotation_items
    ):

        grand_total += item["total_price"]

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(
                f'**{index + 1}. '
                f'{item["original_length"]:g}" × '
                f'{item["original_width"]:g}" '
                f'({item["thickness"]})**'
            )

            st.write(
                f'Qty {item["quantity"]} × '
                f'₦{item["unit_price"]:,.0f} '
                f'= **₦{item["total_price"]:,.0f}**'
            )

        with col2:

            if st.button(
                "Remove",
                key=f"remove_{index}",
            ):

                st.session_state.quotation_items.pop(index)

                st.rerun()

        st.divider()


    st.metric(
        "Grand Total",
        f"₦{grand_total:,.0f}",
    )

    st.metric(
        "Grand Total",
        f"₦{grand_total:,.0f}",
    )

    # --------------------------------------------------
    # PDF QUOTATION
    # --------------------------------------------------

    pdf_data, quotation_number = generate_quotation_pdf(
        customer_name=customer_name,
        customer_phone=customer_phone,
        items=st.session_state.quotation_items,
    )

    st.download_button(
        label="📄 Download Quotation PDF",
        data=pdf_data,
        file_name=f"{quotation_number}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    if st.button(
        "Clear Quotation",
        use_container_width=True,
    ):

        st.session_state.quotation_items = []

        st.rerun()