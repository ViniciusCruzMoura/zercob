(function () {
    "use strict";

    function getNumericValue(input) {
        return input.value.replace(/\D/g, "");
    }

    function normalizePercentage(input, displaySymbol = true) {
        let value = getNumericValue(input);

        if (value === "") {
            input.value = "";
            return;
        }

        value = value.replace(/^0+(?=\d)/, "");

        let number = Math.min(Math.max(parseInt(value, 10), 0), 100);

        input.value = displaySymbol
            ? number.toString() + "%"
            : number.toString();
    }

    function initializePercentageInput(input) {
        if (input.dataset.percentageInitialized === "true") {
            return;
        }

        input.dataset.percentageInitialized = "true";

        input.setAttribute("min", "0");
        input.setAttribute("max", "100");
        input.setAttribute("maxlength", "4");
        input.setAttribute("inputmode", "numeric");

        // Show the percentage symbol when the field is not being edited.
        normalizePercentage(input, true);

        input.addEventListener("focus", function () {
            // Remove "%" while editing.
            input.value = getNumericValue(input);
            input.select();
        });

        input.addEventListener("input", function () {
            let value = getNumericValue(input);

            if (value === "") {
                input.value = "";
                return;
            }

            value = value.replace(/^0+(?=\d)/, "");

            let number = Math.min(Math.max(parseInt(value, 10), 0), 100);

            input.value = number.toString();
        });

        input.addEventListener("blur", function () {
            normalizePercentage(input, true);
        });
    }

    function initializePercentageInputs() {
        document
            .querySelectorAll(".percentage-mask")
            .forEach(initializePercentageInput);
    }

    document.addEventListener("DOMContentLoaded", function () {
        initializePercentageInputs();

        // Remove "%" before Django serializes the form.
        document.querySelectorAll("form").forEach(function (form) {
            form.addEventListener("submit", function () {
                form.querySelectorAll(".percentage-mask").forEach(function (input) {
                    normalizePercentage(input, false);
                });
            });
        });
    });

    // Support Django admin inline forms added dynamically.
    document.addEventListener("formset:added", function (event) {
        event.target
            .querySelectorAll(".percentage-mask")
            .forEach(initializePercentageInput);
    });
})();

/*
(function () {
    "use strict";

    function normalizePercentage(input) {
        // Keep digits only.
        let value = input.value.replace(/\D/g, "");

        if (value === "") {
            input.value = "";
            return;
        }

        // Remove leading zeroes, while keeping "0".
        value = value.replace(/^0+(?=\d)/, "");

        let number = parseInt(value, 10);

        // Restrict the value to 0–100.
        number = Math.min(Math.max(number, 0), 100);

        input.value = number.toString();
    }

    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".percentage-mask").forEach(function (input) {
            input.setAttribute("min", "0");
            input.setAttribute("max", "100");
            input.setAttribute("maxlength", "3");
            input.setAttribute("inputmode", "numeric");

            input.addEventListener("input", function () {
                normalizePercentage(input);
            });
        });
    });
})();
*/
