(function () {
    "use strict";

    function formatPhone(value) {
        let digits = value.replace(/\D/g, "");

        // Remove Brazil's country code if it is already present
        if (digits.startsWith("55")) {
            digits = digits.substring(2);
        }

        // Maximum: DDD + 9-digit mobile number
        digits = digits.substring(0, 11);

        // Nothing typed yet
        if (!digits) {
            return "+55 ";
        }

        // Only one DDD digit typed
        if (digits.length === 1) {
            return `+55 ${digits}`;
        }

        const ddd = digits.substring(0, 2);
        const phone = digits.substring(2);

        // DDD only
        if (!phone) {
            return `+55 ${ddd} `;
        }

        // Landline format:
        // +55 11 2345-6789
        if (phone.length <= 8) {
            const firstPart = phone.substring(0, 4);
            const secondPart = phone.substring(4);

            return `+55 ${ddd} ${firstPart}${
                secondPart ? "-" + secondPart : ""
            }`;
        }

        // Mobile format:
        // +55 11 91234-5678
        const firstPart = phone.substring(0, 5);
        const secondPart = phone.substring(5);

        return `+55 ${ddd} ${firstPart}${
            secondPart ? "-" + secondPart : ""
        }`;
    }

    function initializePhoneMask(input) {
        input.addEventListener("input", function () {
            this.value = formatPhone(this.value);

            // Put the cursor at the end after formatting
            this.setSelectionRange(this.value.length, this.value.length);
        });

        input.addEventListener("focus", function () {
            if (!this.value) {
                this.value = "+55 ";
                this.setSelectionRange(this.value.length, this.value.length);
            }
        });
    }

    function initialize() {
        document
            .querySelectorAll("input.phone-mask")
            .forEach(initializePhoneMask);
    }

    document.addEventListener("DOMContentLoaded", initialize);
})();

