from flask import Flask, render_template, request
import pandas as pd
import joblib
from datetime import datetime

from reorder_logic import (
    calculate_reorder_point,
    check_reorder
)


# ==================================================
# Flask Application
# ==================================================

app = Flask(__name__)


# ==================================================
# Load Trained Model
# ==================================================

model = joblib.load(
    "models/sales_forecasting_model.joblib"
)


# ==================================================
# Load Preprocessor
# ==================================================

preprocessor = joblib.load(
    "models/preprocessor.joblib"
)


# ==================================================
# Load Model Evaluation Results
# ==================================================

evaluation_results = joblib.load(
    "models/evaluation_results.joblib"
)


# ==================================================
# Home Page
# ==================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==================================================
# Prediction Route
# ==================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # ==========================================
        # Get Store Information
        # ==========================================

        store = int(
            request.form["store"]
        )

        store_type = request.form[
            "store_type"
        ]

        assortment = request.form[
            "assortment"
        ]

        competition_distance = float(
            request.form[
                "competition_distance"
            ]
        )


        # ==========================================
        # Get Date Information
        # ==========================================

        day_of_week = int(
            request.form[
                "day_of_week"
            ]
        )

        day = int(
            request.form["day"]
        )

        month = int(
            request.form["month"]
        )

        year = int(
            request.form["year"]
        )

        week_of_year = int(
            request.form[
                "week_of_year"
            ]
        )


        # ==========================================
        # Get Promotion / Holiday Information
        # ==========================================

        promo = int(
            request.form["promo"]
        )

        promo2 = int(
            request.form["promo2"]
        )

        school_holiday = int(
            request.form[
                "school_holiday"
            ]
        )

        state_holiday = request.form[
            "state_holiday"
        ]

        promo_interval = request.form[
            "promo_interval"
        ]


        # ==========================================
        # Get Competition Information
        # ==========================================

        competition_open_month = int(
            request.form[
                "competition_open_month"
            ]
        )

        competition_open_year = int(
            request.form[
                "competition_open_year"
            ]
        )

        promo2_since_week = int(
            request.form[
                "promo2_since_week"
            ]
        )

        promo2_since_year = int(
            request.form[
                "promo2_since_year"
            ]
        )


        # ==========================================
        # Get Inventory Information
        # ==========================================

        current_inventory = float(
            request.form[
                "current_inventory"
            ]
        )

        lead_time = float(
            request.form[
                "lead_time"
            ]
        )

        safety_stock = float(
            request.form[
                "safety_stock"
            ]
        )


        # ==========================================
        # Input Validation
        # ==========================================

        if store <= 0:

            raise ValueError(
                "Store ID must be greater than 0."
            )


        if day_of_week < 1 or day_of_week > 7:

            raise ValueError(
                "Day of Week must be between 1 and 7."
            )


        if day < 1 or day > 31:

            raise ValueError(
                "Day must be between 1 and 31."
            )


        if month < 1 or month > 12:

            raise ValueError(
                "Month must be between 1 and 12."
            )


        if year < 2013:

            raise ValueError(
                "Please enter a valid year."
            )


        if competition_distance < 0:

            raise ValueError(
                "Competition distance cannot be negative."
            )


        if current_inventory < 0:

            raise ValueError(
                "Current inventory cannot be negative."
            )


        if lead_time < 0:

            raise ValueError(
                "Lead time cannot be negative."
            )


        if safety_stock < 0:

            raise ValueError(
                "Safety stock cannot be negative."
            )


        # ==========================================
        # Validate Date
        # ==========================================

        try:

            input_date = datetime(
                year,
                month,
                day
            )

        except ValueError:

            raise ValueError(
                "The entered date is not valid."
            )


        # ==========================================
        # Create Input DataFrame
        # ==========================================

        input_data = pd.DataFrame({

            "Store": [store],

            "DayOfWeek": [
                day_of_week
            ],

            "Open": [1],

            "Promo": [promo],

            "SchoolHoliday": [
                school_holiday
            ],

            "CompetitionDistance": [
                competition_distance
            ],

            "CompetitionOpenSinceMonth": [
                competition_open_month
            ],

            "CompetitionOpenSinceYear": [
                competition_open_year
            ],

            "Promo2": [promo2],

            "Promo2SinceWeek": [
                promo2_since_week
            ],

            "Promo2SinceYear": [
                promo2_since_year
            ],

            "Year": [year],

            "Month": [month],

            "Day": [day],

            "WeekOfYear": [
                week_of_year
            ],

            "StateHoliday": [
                str(state_holiday)
            ],

            "StoreType": [
                str(store_type)
            ],

            "Assortment": [
                str(assortment)
            ],

            "PromoInterval": [
                str(promo_interval)
            ]

        })


        # ==========================================
        # Convert Categorical Columns to String
        # ==========================================

        categorical_columns = [

            "StateHoliday",

            "StoreType",

            "Assortment",

            "PromoInterval"

        ]


        for column in categorical_columns:

            input_data[column] = (
                input_data[column].astype(str)
            )


        # ==========================================
        # Preprocess Input
        # ==========================================

        processed_input = (
            preprocessor.transform(
                input_data
            )
        )


        # ==========================================
        # Predict Daily Sales
        # ==========================================

        predicted_sales = model.predict(
            processed_input
        )[0]


        # Make sure prediction is not negative

        predicted_sales = max(
            0,
            float(predicted_sales)
        )


        # ==========================================
        # Calculate Expected Demand
        # ==========================================

        expected_demand = (
            predicted_sales * lead_time
        )


        # ==========================================
        # Calculate Reorder Point
        # ==========================================

        reorder_point = (
            calculate_reorder_point(

                predicted_sales,

                lead_time,

                safety_stock

            )
        )


        # ==========================================
        # Check Reorder Requirement
        # ==========================================

        recommendation = check_reorder(

            current_inventory,

            reorder_point

        )


        # ==========================================
        # Calculate Recommended Order Quantity
        # ==========================================

        recommended_order_quantity = max(

            0,

            reorder_point - current_inventory

        )


        # ==========================================
        # Get Model Evaluation Metrics
        # ==========================================

        mae = evaluation_results[
            "MAE"
        ]

        rmse = evaluation_results[
            "RMSE"
        ]

        r2 = evaluation_results[
            "R2"
        ]


        # ==========================================
        # Display Results
        # ==========================================

        return render_template(

            "result.html",


            # Sales Prediction
            predicted_sales=round(
                predicted_sales,
                2
            ),


            # Expected Demand
            expected_demand=round(
                expected_demand,
                2
            ),


            # Reorder Point
            reorder_point=round(
                reorder_point,
                2
            ),


            # Current Inventory
            current_inventory=round(
                current_inventory,
                2
            ),


            # Lead Time
            lead_time=round(
                lead_time,
                2
            ),


            # Safety Stock
            safety_stock=round(
                safety_stock,
                2
            ),


            # Recommended Order Quantity
            recommended_order_quantity=round(
                recommended_order_quantity,
                2
            ),


            # Recommendation
            recommendation=recommendation,


            # Prediction Date
            prediction_date=input_date.strftime(
                "%d-%m-%Y"
            ),


            # Model Metrics
            mae=round(
                mae,
                2
            ),

            rmse=round(
                rmse,
                2
            ),

            r2=round(
                r2,
                4
            )

        )


    # ==================================================
    # Handle Invalid Input
    # ==================================================

    except ValueError as error:

        return render_template(

            "index.html",

            error=str(error)

        )


    # ==================================================
    # Handle Other Errors
    # ==================================================

    except Exception as error:

        return render_template(

            "index.html",

            error=(
                "An error occurred while "
                "making the prediction: "
                + str(error)
            )

        )


# ==================================================
# Run Flask Application
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )