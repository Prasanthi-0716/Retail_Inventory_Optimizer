/* ==========================================
   INVENTORY COMPARISON BAR CHART
   ========================================== */


document.addEventListener("DOMContentLoaded", function () {

    // Get the three bars
    const currentInventoryBar =
        document.getElementById("currentInventoryBar");

    const reorderPointBar =
        document.getElementById("reorderPointBar");

    const leadTimeDemandBar =
        document.getElementById("leadTimeDemandBar");


    // Make sure the bars exist
    if (
        !currentInventoryBar ||
        !reorderPointBar ||
        !leadTimeDemandBar
    ) {
        return;
    }


    // Get values from HTML data attributes
    const currentInventory =
        parseFloat(
            currentInventoryBar.dataset.value
        );

    const reorderPoint =
        parseFloat(
            reorderPointBar.dataset.value
        );

    const leadTimeDemand =
        parseFloat(
            leadTimeDemandBar.dataset.value
        );


    // Find the largest value
    const maximumValue = Math.max(
        currentInventory,
        reorderPoint,
        leadTimeDemand
    );


    // Calculate percentage
    function calculatePercentage(value) {

        if (
            !Number.isFinite(value) ||
            maximumValue <= 0
        ) {
            return 0;
        }

        return (value / maximumValue) * 100;
    }


    // Set Current Inventory bar
    currentInventoryBar.style.width =
        calculatePercentage(currentInventory) + "%";


    // Set Reorder Point bar
    reorderPointBar.style.width =
        calculatePercentage(reorderPoint) + "%";


    // Set Lead-Time Demand bar
    leadTimeDemandBar.style.width =
        calculatePercentage(leadTimeDemand) + "%";

});