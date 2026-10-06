# pricing.py

# --------------------------------------------------
# RAW MATERIALS
# --------------------------------------------------

RAW_MATERIALS = {
    "4x8": {
        "name": "4ft × 8ft",
        "length": 96,
        "width": 48,
        "prices": {
            "1.5mm": 48000,
            "1.8mm": 63000,
            "2mm": 70000,
            "2.5mm": 85000,
        },
    },

    "2x8": {
        "name": "2ft × 8ft",
        "length": 96,
        "width": 24,
        "prices": {
            "1.5mm": 23000,
            "1.8mm": 33000,
            "2mm": 35000,
            "2.5mm": 42500,
        },
    },
}


# --------------------------------------------------
# PRODUCTS THAT CAN COME FROM OFFCUTS
# --------------------------------------------------

OFFCUT_PRODUCTS = {
    "4_belt": {
        "name": '4" × 1m Belt',
        "width": 4,
        "length": 39.37,
        "prices": {
            "1.5mm": 1200,
            "1.8mm": 1300,
            "2mm": 1300,
        },
    },

    "5_belt": {
        "name": '5" × 1m Belt',
        "width": 5,
        "length": 39.37,
        "prices": {
            "1.5mm": 2500,
            "1.8mm": 2500,
            "2mm": 2500,
            "2.5mm": 2500,
        },
    },

    "6_belt": {
        "name": '6" × 1m Belt',
        "width": 6,
        "length": 39.37,
        "prices": {
            "1.5mm": 3000,
            "1.8mm": 3000,
            "2mm": 3000,
            "2.5mm": 3000,
        },
    },

    "8_belt": {
        "name": '8" × 1m Belt',
        "width": 8,
        "length": 39.37,
        "prices": {
            "1.5mm": 4300,
            "1.8mm": 4300,
            "2mm": 4300,
            "2.5mm": 4300,
        },
    },

    "12x12": {
        "name": '12" × 12" Design',
        "width": 12,
        "length": 12,
        "prices": {
            "1.5mm": 2500,
            "1.8mm": 2800,
            "2mm": 2800,
        },
    },

    "16x16": {
        "name": '16" × 16" Design',
        "width": 16,
        "length": 16,
        "prices": {
            "1.5mm": 3000,
            "1.8mm": 3300,
            "2mm": 3500,
        },
    },

    "1m_x_1m": {
        "name": "1m × 1m Design",
        "width": 39.37,
        "length": 39.37,
        "prices": {
            "1.5mm": 18000,
            "1.8mm": 25000,
            "2mm": 30000,
        },
    },
}