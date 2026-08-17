(function () {
  function onlyDigits(s) {
    return (s || "").replace(/\D/g, "");
  }

  function maskCPF(v) {
    v = onlyDigits(v).slice(0, 11);
    const p1 = v.slice(0, 3);
    const p2 = v.slice(3, 6);
    const p3 = v.slice(6, 9);
    const p4 = v.slice(9, 11);
    let out = p1;
    if (p2) out += "." + p2;
    if (p3) out += "." + p3;
    if (p4) out += "-" + p4;
    return out;
  }

  function maskCNPJ(v) {
    v = onlyDigits(v).slice(0, 14);
    const p1 = v.slice(0, 2);
    const p2 = v.slice(2, 5);
    const p3 = v.slice(5, 8);
    const p4 = v.slice(8, 12);
    const p5 = v.slice(12, 14);
    let out = p1;
    if (p2) out += "." + p2;
    if (p3) out += "." + p3;
    if (p4) out += "/" + p4;
    if (p5) out += "-" + p5;
    return out;
  }

  function maskCPF_CNPJ(el) {
    const digits = onlyDigits(el.value);
    if (digits.length <= 11) el.value = maskCPF(digits);
    else el.value = maskCNPJ(digits);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("input.cpf-cnpj-mask").forEach(function (el) {
      el.addEventListener("input", function () {
        maskCPF_CNPJ(el);
      });

      // If there's already a value (e.g., browser autofill), mask it:
      if (el.value) maskCPF_CNPJ(el);
    });
  });
})();

/** 
(function () {
  function onlyDigits(s) {
    return (s || "").replace(/\D/g, "");
  }

  function maskCPF(v) {
    // 000.000.000-00 (11 digits)
    v = onlyDigits(v).slice(0, 11);
    const p1 = v.slice(0, 3);
    const p2 = v.slice(3, 6);
    const p3 = v.slice(6, 9);
    const p4 = v.slice(9, 11);

    let out = p1;
    if (p2) out += "." + p2;
    if (p3) out += "." + p3;
    if (p4) out += "-" + p4;
    return out;
  }

  function maskCNPJ(v) {
    // 00.000.000/0000-00 (14 digits)
    v = onlyDigits(v).slice(0, 14);
    const p1 = v.slice(0, 2);
    const p2 = v.slice(2, 5);
    const p3 = v.slice(5, 8);
    const p4 = v.slice(8, 12);
    const p5 = v.slice(12, 14);

    let out = p1;
    if (p2) out += "." + p2;
    if (p3) out += "." + p3;
    if (p4) out += "/" + p4;
    if (p5) out += "-" + p5;
    return out;
  }

  function maskCPF_CNPJ(el) {
    const raw = el.value;
    const digits = onlyDigits(raw);

    // Decide based on length (11 -> CPF, 14 -> CNPJ)
    if (digits.length <= 11) {
      el.value = maskCPF(digits);
    } else {
      el.value = maskCNPJ(digits);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    // Change this selector to match your input id/name
    // If your field is "cpf_cnpj", Django admin input id will usually be:
    // id_cpf_cnpj
    const el = document.querySelector("input#id_cpf_cnpj");
    if (!el) return;

    // Format on input and also handle pasted content
    el.addEventListener("input", function () {
      maskCPF_CNPJ(el);
    });
  });
})();
*/
