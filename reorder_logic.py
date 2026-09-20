def calculate_reorder_point(
    predicted_daily_sales,
    lead_time_days,
    safety_stock
):
    """
    Calculate inventory reorder point.

    Formula:
    Reorder Point =
    Predicted Daily Sales × Lead Time + Safety Stock
    """

    reorder_point = (
        predicted_daily_sales * lead_time_days
        + safety_stock
    )

    return reorder_point


def check_reorder(
    current_inventory,
    reorder_point
):
    """
    Decide whether inventory should be reordered.
    """

    if current_inventory <= reorder_point:
        return "REORDER"

    return "NO REORDER"


def calculate_order_quantity(
    current_inventory,
    reorder_point
):
    """
    Calculate how many units should be ordered.
    """

    quantity = (
        reorder_point - current_inventory
    )

    return max(0, quantity)


if __name__ == "__main__":

    predicted_sales = 500
    lead_time = 3
    safety_stock = 200
    current_inventory = 1200

    reorder_point = calculate_reorder_point(
        predicted_sales,
        lead_time,
        safety_stock
    )

    recommendation = check_reorder(
        current_inventory,
        reorder_point
    )

    order_quantity = calculate_order_quantity(
        current_inventory,
        reorder_point
    )

    print("Predicted Daily Sales:", predicted_sales)
    print("Lead Time:", lead_time)
    print("Safety Stock:", safety_stock)
    print("Reorder Point:", reorder_point)
    print("Current Inventory:", current_inventory)
    print("Recommendation:", recommendation)
    print("Recommended Order Quantity:", order_quantity)