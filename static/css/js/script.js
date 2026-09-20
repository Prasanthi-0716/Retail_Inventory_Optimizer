document.addEventListener("DOMContentLoaded", function () {

    const dateInput = document.getElementById("prediction_date");

    const dayOfWeekInput = document.getElementById("day_of_week");
    const dayInput = document.getElementById("day");
    const monthInput = document.getElementById("month");
    const yearInput = document.getElementById("year");
    const weekInput = document.getElementById("week_of_year");


    // Check that all elements exist
    if (
        !dateInput ||
        !dayOfWeekInput ||
        !dayInput ||
        !monthInput ||
        !yearInput ||
        !weekInput
    ) {
        console.error("Date form elements not found.");
        return;
    }


    // Calculate ISO week number
    function getWeekNumber(date) {

        const tempDate = new Date(date.getTime());

        // Thursday determines the ISO week
        tempDate.setHours(0, 0, 0, 0);

        tempDate.setDate(
            tempDate.getDate() + 3 -
            (tempDate.getDay() + 6) % 7
        );

        const week1 = new Date(
            tempDate.getFullYear(),
            0,
            4
        );

        return (
            1 +
            Math.round(
                (
                    (
                        tempDate - week1
                    ) / 86400000 -
                    3 +
                    (
                        week1.getDay() + 6
                    ) % 7
                ) / 7
            )
        );
    }


    // Update all date fields
    function updateDateFields() {

        const selectedValue = dateInput.value;

        if (!selectedValue) {

            dayOfWeekInput.value = "";
            dayInput.value = "";
            monthInput.value = "";
            yearInput.value = "";
            weekInput.value = "";

            return;
        }


        // HTML date input always gives YYYY-MM-DD
        const parts = selectedValue.split("-");

        if (parts.length !== 3) {
            return;
        }


        const year = parseInt(parts[0], 10);
        const month = parseInt(parts[1], 10);
        const day = parseInt(parts[2], 10);


        const selectedDate = new Date(
            year,
            month - 1,
            day
        );


        if (isNaN(selectedDate.getTime())) {
            return;
        }


        /*
         * JavaScript:
         * Sunday = 0
         * Monday = 1
         *
         * Rossmann:
         * Monday = 1
         * Sunday = 7
         */

        let dayOfWeek = selectedDate.getDay();

        if (dayOfWeek === 0) {
            dayOfWeek = 7;
        }


        // Fill the fields
        dayOfWeekInput.value = dayOfWeek;

        dayInput.value = day;

        monthInput.value = month;

        yearInput.value = year;

        weekInput.value = getWeekNumber(selectedDate);


        console.log("Date information updated:");
        console.log("Day of Week:", dayOfWeek);
        console.log("Day:", day);
        console.log("Month:", month);
        console.log("Year:", year);
        console.log("Week:", weekInput.value);
    }


    // When date changes
    dateInput.addEventListener(
        "change",
        updateDateFields
    );


    // Also handle input event
    dateInput.addEventListener(
        "input",
        updateDateFields
    );


    // Update immediately if a date already exists
    updateDateFields();

});