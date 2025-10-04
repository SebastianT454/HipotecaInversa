document.getElementById("calculate").addEventListener("click", async () => {
  const payload = {
    age: document.getElementById("age").value,
    gender: document.getElementById("gender").value,
    marital_status: document.getElementById("marital_status").value,
    spouse_age: document.getElementById("spouse_age").value,
    spouse_gender: document.getElementById("spouse_gender").value,
    property_value: document.getElementById("property_value").value,
    interest_rate: document.getElementById("interest_rate").value
  };
  
  const out = document.getElementById("output");
  out.textContent = "Calculando...";
  
  try {
    const res = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    const data = await res.json();
    if (data.status === 'ok') {
      out.innerHTML = `<strong>Cuota mensual:</strong> ${data.monthly_fee} <br/>
                       <strong>Cuotas (meses):</strong> ${data.quotas} <br/>
                       <strong>Tasa mensual:</strong> ${data.monthly_rate}`;
    } else {
      out.textContent = "Error: " + (data.error || "desconocido");
    }
  } catch(e) {
    out.textContent = "Error de red: " + e.message;
  }
});