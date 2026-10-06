from pricing import RAW_MATERIALS, OFFCUT_PRODUCTS


PAN_LENGTH = 96
PAN_WIDTH = 48
HALF_PAN_WIDTH = 24
STANDARD_BELT_WIDTH = 4


def normalize_dimensions(length, width):
    """
    Rotate the customer piece automatically when necessary.

    Example:
    33 × 86 becomes 86 × 33.
    """

    if length <= PAN_LENGTH and width <= PAN_WIDTH:
        return length, width

    if width <= PAN_LENGTH and length <= PAN_WIDTH:
        return width, length

    return length, width


def calculate_standard_cut(
    length,
    width,
    thickness,
    quantity=1,
    raw_price_override=None,
    offcut_value_override=None,
):
    """
    Calculate quotation using Diamond Pans pricing rules.

    Confirmed standard-sheet rules:
    - 96" × 48" = full 4ft × 8ft sheet -> zero belts.
    - 96" × 24" = half 2ft × 8ft sheet -> zero belts.
      Two 2ft × 8ft sheets make one 4ft × 8ft sheet.
    - Other custom cuts use the standard 4-inch
      belt recovery calculation.
    """

    length, width = normalize_dimensions(length, width)

    if length > PAN_LENGTH or width > PAN_WIDTH:
        raise ValueError(
            "This order is larger than one standard 4ft × 8ft pan."
        )

    # --------------------------------------------------
    # STANDARD 4FT × 8FT FULL SHEET
    # --------------------------------------------------

    if length == PAN_LENGTH and width == PAN_WIDTH:

        raw_price = RAW_MATERIALS["4x8"]["prices"].get(thickness)

        if raw_price is None:
            raise ValueError(
                f"No 4ft × 8ft price available for {thickness}."
            )

        if raw_price_override is not None:
            raw_price = raw_price_override

        unit_price = raw_price
        total_price = unit_price * quantity

        return {
            "length": length,
            "width": width,
            "thickness": thickness,
            "quantity": quantity,

            "raw_price": raw_price,

            "remaining_length": 0,
            "remaining_width": 0,

            "length_belts": 0,
            "width_belts": 0,
            "total_belts": 0,
            "belt_price": 0,

            "standard_offcut_value": 0,
            "final_offcut_value": 0,

            "calculation_mode": "Standard 4ft × 8ft full sheet — no belt",

            "unit_price": unit_price,
            "total_price": total_price,
        }

    # --------------------------------------------------
    # STANDARD 2FT × 8FT HALF SHEET
    # --------------------------------------------------

    if length == PAN_LENGTH and width == HALF_PAN_WIDTH:

        raw_price = RAW_MATERIALS["2x8"]["prices"].get(thickness)

        if raw_price is None:
            raise ValueError(
                f"No 2ft × 8ft price available for {thickness}."
            )

        if raw_price_override is not None:
            raw_price = raw_price_override

        unit_price = raw_price
        total_price = unit_price * quantity

        return {
            "length": length,
            "width": width,
            "thickness": thickness,
            "quantity": quantity,

            "raw_price": raw_price,

            "remaining_length": 0,
            "remaining_width": 0,

            "length_belts": 0,
            "width_belts": 0,
            "total_belts": 0,
            "belt_price": 0,

            "standard_offcut_value": 0,
            "final_offcut_value": 0,

            "calculation_mode": "Standard 2ft × 8ft half sheet — no belt",

            "unit_price": unit_price,
            "total_price": total_price,
        }

    # --------------------------------------------------
    # CUSTOM CUT — STANDARD 4-INCH BELT RECOVERY
    # --------------------------------------------------

    raw_price = RAW_MATERIALS["4x8"]["prices"].get(thickness)

    if raw_price is None:
        raise ValueError(
            f"No 4ft × 8ft price available for {thickness}."
        )

    if raw_price_override is not None:
        raw_price = raw_price_override

    belt_price = OFFCUT_PRODUCTS["4_belt"]["prices"].get(thickness)

    if belt_price is None:
        raise ValueError(
            f'No 4" belt price available for {thickness}.'
        )

    remaining_length = PAN_LENGTH - length
    remaining_width = PAN_WIDTH - width

    length_belts = int(
        remaining_length // STANDARD_BELT_WIDTH
    )

    width_belts = int(
        remaining_width // STANDARD_BELT_WIDTH
    ) * 2

    total_belts = length_belts + width_belts

    standard_offcut_value = total_belts * belt_price

    # Use manual business decision when supplied.
    if offcut_value_override is not None:
        final_offcut_value = offcut_value_override
        calculation_mode = "Manual offcut value"
    else:
        final_offcut_value = standard_offcut_value
        calculation_mode = 'Standard 4" belt calculation'

    unit_price = raw_price - final_offcut_value
    total_price = unit_price * quantity

    return {
        "length": length,
        "width": width,
        "thickness": thickness,
        "quantity": quantity,

        "raw_price": raw_price,

        "remaining_length": remaining_length,
        "remaining_width": remaining_width,

        "length_belts": length_belts,
        "width_belts": width_belts,
        "total_belts": total_belts,
        "belt_price": belt_price,

        "standard_offcut_value": standard_offcut_value,
        "final_offcut_value": final_offcut_value,

        "calculation_mode": calculation_mode,

        "unit_price": unit_price,
        "total_price": total_price,
    }