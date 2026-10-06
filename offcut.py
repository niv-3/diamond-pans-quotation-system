from pricing import OFFCUT_PRODUCTS


def product_fits(space_length, space_width, product):
    """
    Check whether a product can fit inside a rectangular
    remaining space.

    Rotation is allowed.
    """

    product_length = product["length"]
    product_width = product["width"]

    # Normal orientation
    normal_fit = (
        product_length <= space_length
        and product_width <= space_width
    )

    # Rotated orientation
    rotated_fit = (
        product_width <= space_length
        and product_length <= space_width
    )

    return normal_fit or rotated_fit


def find_fitting_products(space_length, space_width, thickness):
    """
    Find all known products that can physically fit
    inside a remaining rectangular space.
    """

    fitting_products = []

    for product_id, product in OFFCUT_PRODUCTS.items():

        # Some products do not have a known price
        # for every thickness.
        price = product["prices"].get(thickness)

        if price is None:
            continue

        if product_fits(space_length, space_width, product):
            fitting_products.append({
                "id": product_id,
                "name": product["name"],
                "price": price,
                "length": product["length"],
                "width": product["width"],
            })

def calculate_product_capacity(
    space_length,
    space_width,
    product,
    thickness
):
    """
    Calculate how many identical copies of a product
    can fit inside a rectangular offcut.

    Both normal and rotated orientations are tested.
    """

    product_length = product["length"]
    product_width = product["width"]

    price = product["prices"].get(thickness)

    if price is None:
        return None

    # Normal orientation
    normal_count = (
        int(space_length // product_length)
        * int(space_width // product_width)
    )

    # Rotated orientation
    rotated_count = (
        int(space_length // product_width)
        * int(space_width // product_length)
    )

    count = max(normal_count, rotated_count)

    if count == 0:
        return None

    return {
        "count": count,
        "unit_price": price,
        "total_value": count * price,
    }


def evaluate_offcut(space_length, space_width, thickness):
    """
    Evaluate the possible uses of a rectangular offcut.
    """

    options = []

    for product_id, product in OFFCUT_PRODUCTS.items():

        result = calculate_product_capacity(
            space_length,
            space_width,
            product,
            thickness
        )

        if result is None:
            continue

        options.append({
            "id": product_id,
            "name": product["name"],
            "count": result["count"],
            "unit_price": result["unit_price"],
            "total_value": result["total_value"],
        })

    # Highest-value option first
    options.sort(
        key=lambda option: option["total_value"],
        reverse=True
    )

    return options

def split_remaining_sheet(
    customer_length,
    customer_width,
    sheet_length=96,
    sheet_width=48
):
    """
    Split the material remaining after a rectangular
    customer piece is cut from one corner of the sheet.

    Returns non-overlapping rectangles so material
    is never counted twice.
    """

    if customer_length > sheet_length:
        raise ValueError("Customer length exceeds sheet length.")

    if customer_width > sheet_width:
        raise ValueError("Customer width exceeds sheet width.")

    if customer_length <= 0 or customer_width <= 0:
        raise ValueError("Dimensions must be greater than zero.")

    offcuts = []

    # Rectangle remaining beside the customer piece.
    side_length = sheet_length - customer_length

    if side_length > 0:
        offcuts.append({
            "name": "Side remainder",
            "length": side_length,
            "width": customer_width,
        })

    # Long strip remaining across the unused width.
    bottom_width = sheet_width - customer_width

    if bottom_width > 0:
        offcuts.append({
            "name": "Width remainder",
            "length": sheet_length,
            "width": bottom_width,
        })

    return offcuts

def calculate_standard_belt_recovery(
    customer_length,
    customer_width,
    thickness
):
    """
    Implements the company's confirmed standard
    4-inch belt recovery calculation.
    """

    remaining_length = 96 - customer_length
    remaining_width = 48 - customer_width

    if remaining_length < 0 or remaining_width < 0:
        raise ValueError(
            "Customer piece exceeds the standard 4ft × 8ft pan."
        )

    belt_product = OFFCUT_PRODUCTS["4_belt"]

    belt_price = belt_product["prices"].get(thickness)

    if belt_price is None:
        raise ValueError(
            f'No 4" belt price available for {thickness}.'
        )

    length_belts = int(remaining_length // 4)

    width_belts = int(remaining_width // 4) * 2

    total_belts = length_belts + width_belts

    return {
        "remaining_length": remaining_length,
        "remaining_width": remaining_width,
        "length_belts": length_belts,
        "width_belts": width_belts,
        "total_belts": total_belts,
        "belt_price": belt_price,
        "recovery_value": total_belts * belt_price,
    }


    return fitting_products