// Initialize the map and set its view to a geographical center of India
const mymap = L.map('mapid').setView([23.5, 80], 5);

// Add a tile layer (the base map style)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(mymap);

// Data structure to store artisan traditions for each state
// NOTE: The state names here MUST exactly match the names in your GeoJSON file.
const artisanData = {
    "Rajasthan": "Tie-Dye (Bandhani), Block Printing, Blue Pottery",
    "Gujarat": "Patola Silk, Kutch Embroidery, Rogan Art",
    "Kerala": "Kathakali Masks, Aranmula Kannadi, Coir Products",
    "Goa": "Terracotta and Clay Work, Coir Craft, Wood Carving",
    "Bihar": "Madhubani Painting, Sujini Embroidery, Stonecraft",
    "West Bengal": "Kantha Embroidery, Terracotta, Dokra Art",
    "Odisha": "Pattachitra Paintings, Appliqué Work, Silver Filigree",
    "Uttar Pradesh": "Chikankari Embroidery, Pottery, Metalware",
    "Jammu and Kashmir": "Pashmina Shawls, Walnut Wood Carving, Paper Mache"
    // Add more states and their traditions here
};

// Function to style the GeoJSON states
function style(feature) {
    return {
        fillColor: '#ffffff', // Default color for all states
        weight: 2,
        opacity: 1,
        color: 'gray',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

// Function to handle interactions (hover, click)
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: function(e) {
            const layer = e.target;
            layer.setStyle({
                weight: 4,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.9,
                fillColor: '#f1c40f' // Highlight color on hover
            });
            // Display a tooltip with the state name
            layer.bindTooltip(feature.properties.name, {permanent: true, direction: "top"}).openTooltip();
        },
        mouseout: function(e) {
            // Revert to original style on mouse out
            geojson.resetStyle(e.target);
            // Close the tooltip
            mymap.closeTooltip(e.target);
        },
        // Add a click function to show artisan details
        click: function(e) {
            const stateName = feature.properties.name;
            const traditions = artisanData[stateName] || "No data available.";
            
            // Create a pop-up with the traditions list
            layer.bindPopup(`
                <h3>${stateName}</h3>
                <p>Traditional Crafts: ${traditions}</p>
            `).openPopup();
        }
    });
}

// Load the GeoJSON file
let geojson;
fetch('india_states.geojson')
    .then(response => response.json())
    .then(data => {
        geojson = L.geoJson(data, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(mymap);
    });