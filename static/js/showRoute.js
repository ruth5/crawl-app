'use strict';

function initMap() {
    const humphreyCoords = {
        lat: 37.75303451932446, 
        lng: -122.41187293853972,
    };

    const biRiteCoords = {
        lat: 37.76175113473264, 
        lng: -122.42566335756337,
    };

    const houseOfPancakesCoords = {
        lat: 37.7430759633752, 
        lng: -122.47613712502925,
    };

    const burmaSuperStarCoords = {
        lat: 37.7837765579607, 
        lng: -122.46273936046609,
    };

    const yankSingCoords = {
        lat: 37.79279235853008, 
        lng: -122.39297750174063,
    };

    const cords = [humphreyCoords, biRiteCoords, houseOfPancakesCoords, burmaSuperStarCoords, yankSingCoords];

    const map = new google.maps.Map(document.querySelector('#map'), {
        center: humphreyCoords,
        zoom: 13,
    });

    const markers = []
    for (const cord of cords) {
        markers.push(
            new google.maps.Marker({
                position: cord
            })
        )
        console.log(cord);
    }
    console.log(markers);

    for (const marker of markers) {
        const markerInfo = `
        <p>
            Hi
            ${marker.position.lat()}
            ${marker.position.lng()}
        </p>
        `
        ;
    

    const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        maxWidth: 200,
    });

    marker.addListener('click', () => {
        infoWindow.open(map, marker)
    })
}





}