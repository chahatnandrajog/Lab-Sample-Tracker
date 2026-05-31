let allSamples = [];

async function loadDashboard() {
    const response = await fetch("/dashboard/summary");
    const data = await response.json();

    document.getElementById("total-samples").textContent = data.total_samples;

    const statusSummary = document.getElementById("status-summary");
    statusSummary.innerHTML = "";

    const statusFilter = document.getElementById("status-filter");
    statusFilter.innerHTML = `<option value="">All statuses</option>`;

    for (const status in data.status_counts) {
        const li = document.createElement("li");
        li.textContent = `${status}: ${data.status_counts[status]}`;
        statusSummary.appendChild(li);

        const option = document.createElement("option");
        option.value = status;
        option.textContent = status;
        statusFilter.appendChild(option);
    }
}

async function loadSamples() {
    const response = await fetch("/samples/");
    allSamples = await response.json();
    renderSamples(allSamples);
    await loadDashboard();
}

function renderSamples(samples) {
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

function applyControls() {
    const searchValue = document.getElementById("search-input").value.toLowerCase();
    const statusValue = document.getElementById("status-filter").value;
    const sortValue = document.getElementById("sort-select").value;

    let filtered = [...allSamples];

    if (searchValue) {
        filtered = filtered.filter(sample =>
            sample.sample_id.toLowerCase().includes(searchValue) ||
            sample.sample_type.toLowerCase().includes(searchValue) ||
            sample.owner.toLowerCase().includes(searchValue) ||
            sample.storage_location.toLowerCase().includes(searchValue)
        );
    }

    if (statusValue) {
        filtered = filtered.filter(sample => sample.status === statusValue);
    }

    if (sortValue) {
        filtered.sort((a, b) => {
            if (sortValue === "temperature") {
                return a.temperature - b.temperature;
            }

            return String(a[sortValue]).localeCompare(String(b[sortValue]));
        });
    }

    renderSamples(filtered);
}

function resetControls() {
    document.getElementById("search-input").value = "";
    document.getElementById("status-filter").value = "";
    document.getElementById("sort-select").value = "";

    renderSamples(allSamples);
}

function openModal() {
    document.getElementById("modal").classList.remove("hidden");
}

function closeModal() {
    document.getElementById("modal").classList.add("hidden");
    document.getElementById("form-message").textContent = "";
}

document.getElementById("sample-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    const sample = {
        sample_id: formData.get("sample_id"),
        sample_type: formData.get("sample_type"),
        collection_date: formData.get("collection_date"),
        status: formData.get("status"),
        storage_location: formData.get("storage_location"),
        owner: formData.get("owner"),
        temperature: Number(formData.get("temperature")),
        notes: formData.get("notes")
    };

    const response = await fetch("/samples/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(sample)
    });

    const message = document.getElementById("form-message");

    if (response.ok) {
        message.textContent = "Sample added successfully.";
        event.target.reset();
        await loadSamples();
    } else {
        const error = await response.json();
        message.textContent = error.detail || "Failed to add sample.";
    }
});

loadSamples();