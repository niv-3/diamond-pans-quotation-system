import streamlit as st

from calculator import calculate_standard_cut
from pdf_generator import generate_quotation_pdf


st.set_page_config(
    page_title="Diamond Pans Quotation Calculator",
    page_icon="📐",
    layout="centered",
)

st.title("Diamond Pans Quotation Calculator")
st.caption("Create customer fabrication quotations.")


# ==================================================
# SESSION STATE
# ==================================================

if "quotation_items" not in st.session_state:
    st.session_state.quotation_items = []

if "total_calculated" not in st.session_state:
    st.session_state.total_calculated = False


# ==================================================
# CUSTOMER DETAILS
# ==================================================

st.subheader("Customer Details")

customer_name = st.text_input("Customer Name")

customer_phone = st.text_input(
    "Phone Number",
    placeholder="Optional",
)


# ==================================================
# ADD ORDER ITEM
# ==================================================

st.subheader("Add Order Item")

col1, col2 = st.columns(2)

with col1:
    thickness = st.selectbox(
        "Material Thickness",
        [
            "1.5mm",
            "1.8mm",
            "2mm",
            "2.5mm",
        ],
    )

with col2:
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1,
        step=1,
    )


col3, col4 = st.columns(2)

with col3:
    length = st.number_input(
        "Length (inches)",
        min_value=1.0,
        value=55.0,
    )

with col4:
    width = st.number_input(
        "Width (inches)",
        min_value=1.0,
        value=39.0,
    )


# ==================================================
# OFFCUT METHOD
# ==================================================

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
        "Usable remaining material value per item (₦)",
        min_value=0.0,
        value=0.0,
        step=100.0,
    )


# ==================================================
# ADD ITEM
# ==================================================

if st.button(
    "➕ Add Item",
    type="primary",
    use_container_width=True,
):

    try:

        result = calculate_standard_cut(
            length=length,
            width=width,
            thickness=thickness,
            quantity=quantity,
            offcut_value_override=manual_offcut_value,
        )

        item = {
            "original_length": length,
            "original_width": width,

            "length": result["length"],
            "width": result["width"],

            "thickness": thickness,
            "quantity": quantity,

            # Keep original business calculation
            "calculated_unit_price":
                result["unit_price"],

            # Editable customer selling price
            "unit_price":
                result["unit_price"],

            "total_price":
                result["total_price"],

            "raw_price":
                result["raw_price"],

            "total_belts":
                result["total_belts"],

            "standard_offcut_value":
                result["standard_offcut_value"],

            "offcut_value":
                result["final_offcut_value"],

            "calculation_mode":
                result["calculation_mode"],
        }

        st.session_state.quotation_items.append(
            item
        )

        # A new item means the total must
        # be calculated again.
        st.session_state.total_calculated = False

        st.rerun()

    except ValueError as error:

        st.error(str(error))


# ==================================================
# QUOTATION
# ==================================================

st.divider()

st.subheader("Quotation")


if not st.session_state.quotation_items:

    st.info("No items added yet.")


else:

    # ==================================================
    # QUOTATION ITEMS
    # ==================================================

    for index, item in enumerate(
        st.session_state.quotation_items
    ):

        st.write(
            f'**{index + 1}. '
            f'{item["original_length"]:g}" × '
            f'{item["original_width"]:g}" '
            f'| {item["thickness"]} '
            f'| Qty {item["quantity"]}**'
        )


        # --------------------------------------------------
        # EDITABLE PRICE
        # --------------------------------------------------

        selling_price = st.number_input(
            "Price per item (₦)",
            min_value=0.0,
            value=float(item["unit_price"]),
            step=100.0,
            key=f"selling_price_{index}",
        )


        # If she changes the selling price,
        # hide the old total until Calculate Total
        # is pressed again.
        if selling_price != item["unit_price"]:

            item["unit_price"] = selling_price

            st.session_state.total_calculated = False


        # --------------------------------------------------
        # CALCULATION DETAILS
        # --------------------------------------------------

        with st.expander(
            "View calculation details"
        ):

            st.write(
                'Raw pan: '
                '4ft × 8ft '
                '(96" × 48")'
            )

            st.write(
                f'Thickness: '
                f'{item["thickness"]}'
            )

            st.write(
                f'Material price: '
                f'₦{item["raw_price"]:,.0f}'
            )

            st.write(
                f'Standard 4" belts recovered: '
                f'{item["total_belts"]}'
            )

            st.write(
                f'Standard offcut value: '
                f'₦{item["standard_offcut_value"]:,.0f}'
            )

            st.write(
                f'Final offcut value used: '
                f'₦{item["offcut_value"]:,.0f}'
            )

            st.write(
                f'System calculated price: '
                f'₦{item["calculated_unit_price"]:,.0f}'
            )

            st.write(
                f'Current selling price: '
                f'₦{item["unit_price"]:,.0f}'
            )

            st.write(
                f'Method: '
                f'{item["calculation_mode"]}'
            )


        # --------------------------------------------------
        # REMOVE ITEM
        # --------------------------------------------------

        if st.button(
            "Remove Item",
            key=f"remove_{index}",
        ):

            st.session_state.quotation_items.pop(
                index
            )

            st.session_state.total_calculated = False

            st.rerun()

        st.divider()


    # ==================================================
    # CALCULATE TOTAL
    # ==================================================

    if st.button(
        "🧮 Calculate Total",
        type="primary",
        use_container_width=True,
    ):

        for item in st.session_state.quotation_items:

            item["total_price"] = (
                item["unit_price"]
                * item["quantity"]
            )

        st.session_state.total_calculated = True

        st.rerun()


    # ==================================================
    # RESULTS ONLY AFTER CALCULATE TOTAL
    # ==================================================

    if st.session_state.total_calculated:

        st.subheader("Calculated Total")

        grand_total = 0


        for index, item in enumerate(
            st.session_state.quotation_items
        ):

            grand_total += item["total_price"]

            st.write(
                f'**{index + 1}. '
                f'{item["original_length"]:g}" × '
                f'{item["original_width"]:g}" '
                f'({item["thickness"]})**'
            )

            st.write(
                f'Qty {item["quantity"]} × '
                f'₦{item["unit_price"]:,.0f} '
                f'= '
                f'**₦{item["total_price"]:,.0f}**'
            )


        # ==================================================
        # GRAND TOTAL
        # ==================================================

        st.metric(
            "Grand Total",
            f"₦{grand_total:,.0f}",
        )


        # ==================================================
        # PDF
        # ==================================================

        pdf_data, quotation_number = (
            generate_quotation_pdf(
                customer_name=customer_name,
                customer_phone=customer_phone,
                items=st.session_state.quotation_items,
            )
        )

        st.download_button(
            label="📄 Download / Print Quotation PDF",
            data=pdf_data,
            file_name=f"{quotation_number}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


    # ==================================================
    # CLEAR
    # ==================================================

    if st.button(
        "Clear Quotation",
        use_container_width=True,
    ):

        st.session_state.quotation_items = []

        st.session_state.total_calculated = False

        st.rerun()