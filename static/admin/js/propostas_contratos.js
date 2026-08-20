(function () {
    function init() {
        const devedorField = document.getElementById("id_devedor");

        if (!devedorField) {
            return;
        }

        const contratosUrl = devedorField.dataset.contratosUrl;

        if (!contratosUrl) {
            return;
        }

        let requestNumber = 0;

        async function carregarContratos(limparSelecionado) {
            const devedorId = devedorField.value;
            const currentRequest = ++requestNumber;

            const contratoFields = document.querySelectorAll(
                'select[name$="-contrato"]'
            );

            if (!devedorId) {
                contratoFields.forEach(function (select) {
                    select.innerHTML =
                        '<option value="">---------</option>';
                });

                return;
            }

            const response = await fetch(
                `${contratosUrl}?devedor_id=${encodeURIComponent(devedorId)}`,
                {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                }
            );

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            if (currentRequest !== requestNumber) {
                return;
            }

            contratoFields.forEach(function (select) {
                const valorAtual = limparSelecionado
                    ? ""
                    : select.value;

                select.innerHTML = "";

                select.add(
                    new Option("---------", "")
                );

                data.results.forEach(function (contrato) {
                    select.add(
                        new Option(
                            contrato.text,
                            contrato.id
                        )
                    );
                });

                const contratoAindaExiste = data.results.some(
                    function (contrato) {
                        return String(contrato.id) ===
                            String(valorAtual);
                    }
                );

                if (contratoAindaExiste) {
                    select.value = valorAtual;
                } else {
                    select.value = "";
                }
            });
        }

        /*
         * Changed debtor:
         * clear any previous contract and load only contracts
         * belonging to the newly selected debtor.
         */
        devedorField.addEventListener("change", function () {
            carregarContratos(true);
        });

        /*
         * Django admin inline dynamically added.
         */
        document.addEventListener("formset:added", function () {
            carregarContratos(false);
        });

        /*
         * Change page or pre-populated debtor.
         */
        if (devedorField.value) {
            carregarContratos(false);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            init
        );
    } else {
        init();
    }
})();
