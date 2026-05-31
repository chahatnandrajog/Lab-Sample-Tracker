async function loadDashboard() {
    const response = await fetch("/dashboard/summary");
    const data = await response.json();

    document.getElementById("total-samples").textContent = data.total_samples;

    const statusSummary = document.getElementById("status-summary");
    statusSummary.innerHTML = "";

    for (const status in data.status_counts) {
        const li = document.createElement("li");
        li.textContent = `${status}: ${data.status_counts[status]}`;
        statusSummary.appendChild(li);
    }
}

async function loadSamples() {
    const response = await fetch("/samples/");
    const samples = await response.json();

    const table = document.getElementById("samples-table");
    table.innerHTML = "";

    samples.forEach(sample => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${sample.sample_id}</td>
            <td>${sample.sample_type}</td>
            <td>${sample.status}</td>
            <td>${sample.storage_location}</td>
            <td>${sample.owner}</td>
            <td>${sample.temperature}</td>
        `;

        table.appendChild(row);
    });
}

loadDashboard();
loadSamples();