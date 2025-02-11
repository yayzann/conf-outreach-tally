let aurora, edmonds, newWest, pacificSpirit, richmond, southCambie, totalRegistrations;
async function fetchSheetData() {
    try {
        const response = await fetch("https://conf-outreach-tally.onrender.com/get-conf-data");
        const data = await response.json();    
        aurora = data.Aurora;
        edmonds = data.Edmonds;
        newWest = data["New West"];
        pacificSpirit = data["Pacific Spirit"];
        richmond = data.Richmond;
        southCambie = data["South Cambie"];
        totalRegistrations = data["Total Registrations"];
        makeBubbles(data);
    } catch (error) {
        console.error('Error fetching data:',error)
    }
}
async function main() {
    await fetchSheetData();
}
function makeBubbles(data) {
    const bubbleContainer = document.getElementById("bubble-container");
    bubbleContainer.innerHTML = "";
    
    Object.entries(data).forEach(([region, count]) => {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        bubble.textContent = `${region}: ${count}`;
        let size = count * 5 + 65;
        if (region === "Total Registrations") size += 50;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        let fontSize = Math.max(10, size * 0.15);
        bubble.style.fontSize = `${fontSize}px`;
        bubbleContainer.appendChild(bubble);
    });
}
main();