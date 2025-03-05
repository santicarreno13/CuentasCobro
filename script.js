document.getElementById("invoiceForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const data = {
        fecha: new Date().toLocaleDateString(),
        cliente: document.getElementById("cliente").value,
        cliente_nit: document.getElementById("cliente_nit").value,
        descripcion: document.getElementById("descripcion").value,
        valor_total: document.getElementById("valor_total").value,
        abono: document.getElementById("abono").value,
        saldo: document.getElementById("valor_total").value - document.getElementById("abono").value,
        material: document.getElementById("material").value,
        empresa_nit: "79864703-4",
        remitente: "Luis Antonio Carreño Gonzales",
        cedula_remitente: "79864703",
        celular_remitente: "3125915013"
    };
    
    fetch("https://cuentascobro.onrender.com/generate_pdf", { //http://127.0.0.1:5000/generate_pdf" Para servidor local
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "Cuenta_de_Cobro.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
    });
});