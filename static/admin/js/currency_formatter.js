(function () {
    "use strict";

    function onlyDigits(value) {
        return String(value || "").replace(/\D/g, "");
    }

    function formatCurrency(value) {
        const digits = onlyDigits(value);

        if (!digits) {
            return "";
        }

        const number = parseInt(digits, 10) / 100;

        return number.toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    function cleanCurrencyFields(form) {
        form.querySelectorAll(".brazilian-currency").forEach(function (field) {
            field.value = onlyDigits(field.value);
        });
    }

    // Works for fields that exist now and fields added later
    document.addEventListener("input", function (event) {
        const field = event.target.closest(".brazilian-currency");

        if (!field) {
            return;
        }

        field.value = formatCurrency(field.value);
    });

    document.addEventListener("blur", function (event) {
        const field = event.target.closest(".brazilian-currency");

        if (!field || !field.value) {
            return;
        }

        field.value = formatCurrency(field.value);
    }, true);

    document.addEventListener("submit", function (event) {
        cleanCurrencyFields(event.target);
    });

    // Format existing fields, if there are any
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".brazilian-currency").forEach(function (field) {
            if (field.value) {
                field.value = formatCurrency(field.value);
            }
        });
    });
})();


/*
document.addEventListener('DOMContentLoaded', function() {
    const currencyFields = document.querySelectorAll('.brazilian-currency');

    console.log(currencyFields)
    
    currencyFields.forEach(field => {
        // Format on load
        field.value = formatCurrency(field.value);
        
        // Format on input
        field.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            this.value = formatCurrency(value);
        });
        
        // Clean before submit
        field.form.addEventListener('submit', function() {
            currencyFields.forEach(f => {
                f.value = f.value.replace(/\D/g, '');
            });
        }, { once: true });
    });
});

function formatCurrency(value) {
    if (!value) return '';
    value = value.replace(/\D/g, '');
    
    // Convert to decimal (dividing by 100 for cents)
    const number = parseInt(value) || 0;
    const formatted = (number / 100).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
    
    return formatted;
}

*/
