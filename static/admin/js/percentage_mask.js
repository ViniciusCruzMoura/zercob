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

