document.addEventListener('DOMContentLoaded', function() {
    const currencyFields = document.querySelectorAll('.brazilian-currency');
    
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
