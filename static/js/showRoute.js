'use strict';

const form = document.querySelector('#routeinfo');


// form.addEventListener("submit", (evt) => {
//     evt.preventDefault();
//     const routeZipCode = document.querySelector('#route-zipcode').value
//     console.log(routeZipCode)
//     if (routeZipCode) {
//         fetch(`/api/routes/${routeZipCode}`)
//             .then((response) => response.json())
//             .then((responseJSON => {
//                 console.log(responseJSON)
//             }
//             ))
//     }
// }
// );

function initMap() {
    const routeCoords = [];
    // const humphreyCoords = {
    //     lat: 37.75303451932446,
    //     lng: -122.41187293853972,
    // };
    // routeCoords.push(humphreyCoords);

    // const biRiteCoords = {
    //     lat: 37.76175113473264,
    //     lng: -122.42566335756337,
    // };

    // routeCoords.push(biRiteCoords);
    // const houseOfPancakesCoords = {
    //     lat: 37.7430759633752,
    //     lng: -122.47613712502925,
    // };
    // routeCoords.push(houseOfPancakesCoords);


    // const burmaSuperStarCoords = {
    //     lat: 37.7837765579607,
    //     lng: -122.46273936046609,
    // };
    // routeCoords.push(burmaSuperStarCoords);


    // const yankSingCoords = {
    //     lat: 37.79279235853008,
    //     lng: -122.39297750174063,
    // };
    // routeCoords.push(yankSingCoords);


    // const cords = [humphreyCoords, biRiteCoords, houseOfPancakesCoords, burmaSuperStarCoords, yankSingCoords];
    form.addEventListener("submit", (evt) => {
        evt.preventDefault();
        const routeZipCode = document.querySelector('#route-zipcode').value
        console.log(routeZipCode)
        if (routeZipCode) {
            fetch(`/api/routes/${routeZipCode}`)
                .then((response) => response.json())
                .then((responseJSON => {
                    console.log(responseJSON)
                    const map = new google.maps.Map(document.querySelector('#map'), {
                        center: { placeId: responseJSON["place_ids"][0] },
                        zoom: 13,
                    });
                
                
                    const directionsService = new google.maps.DirectionsService();
                
                    // Directions Renderer draws directions on the map
                    const directionsRenderer = new google.maps.DirectionsRenderer();
                    directionsRenderer.setMap(map);

                    const place_ids = responseJSON["place_ids"]
                    
                    const first_stop = place_ids[0]
                    const last_stop = place_ids[place_ids.length - 1]
                    const waypoints = []
                    for (let i = 1; i < (place_ids.length - 1); i += 1) {
                        let new_waypoint = {}
                        new_waypoint["location"] = {placeId: place_ids[i]}
                        waypoints.push(new_waypoint)
                        console.log(waypoints)
                    };
                
                    const crawlRoute = {
                        origin: { placeId: first_stop },
                        destination: { placeId: last_stop },
                        waypoints: waypoints,
                        travelMode: 'DRIVING',
                    }
                    // const crawlRoute = {
                    //     origin: { placeId: responseJSON["place_ids"][0] },
                    //     destination: { placeId: responseJSON["place_ids"][2] },
                    //     waypoints: [{ location:  {placeId: responseJSON["place_ids"][1]}}],
                    //     travelMode: 'DRIVING',
                    // }
                    console.log(crawlRoute)
                
                    directionsService.route(crawlRoute, (response, status) => {
                        if (status === 'OK') {
                            directionsRenderer.setDirections(response);
                        }
                        else {
                            alert(`Directions request unsuccessful due to ${status}`)
                        }
                    });
                    
                }
                ))
        }
    }
    );

    // const map = new google.maps.Map(document.querySelector('#map'), {
    //     center: { placeId: "ChIJVSvIaJiAhYARwg6LgKkXkB0" },
    //     zoom: 13,
    // });

    // // const markers = []
    // // for (const cord of cords) {
    // //     markers.push(
    // //         new google.maps.Marker({
    // //             position: cord,
    // //             map: map,
    // //         })
    // //     )

    // // }

    // // for (const marker of markers) {
    // //     const markerInfo = `
    // //     <p>
    // //         Coordinates of this test marker:
    // //         ${marker.position.lat()}
    // //         ${marker.position.lng()}
    // //     </p>
    // //     `
    // //         ;


    // //     const infoWindow = new google.maps.InfoWindow({
    // //         content: markerInfo,
    // //         maxWidth: 200,
    // //     });

    // //     marker.addListener('click', () => {
    // //         infoWindow.open(map, marker)
    // //     })
    // // }

    // const directionsService = new google.maps.DirectionsService();

    // // Directions Renderer draws directions on the map
    // const directionsRenderer = new google.maps.DirectionsRenderer();
    // directionsRenderer.setMap(map);

    // // const crawlRoute = {
    // //     origin: humphreyCoords,
    // //     destination: biRiteCoords,
    // //     waypoints: [{location: burmaSuperStarCoords}, {location: houseOfPancakesCoords}, {location: yankSingCoords}],
    // //     travelMode: 'DRIVING',
    // // }

    // const crawlRoute = {
    //     origin: { placeId: "ChIJVSvIaJiAhYARwg6LgKkXkB0" },
    //     destination: { placeId: "ChIJTbUmE5qAhYAR3Pp-88HmmFc" },
    //     waypoints: [{ location:  {placeId: "ChIJa3aIDJyAhYARMPjFJtHsI5I"}}],
    //     travelMode: 'DRIVING',
    // }

    // directionsService.route(crawlRoute, (response, status) => {
    //     if (status === 'OK') {
    //         directionsRenderer.setDirections(response);
    //     }
    //     else {
    //         alert(`Directions request unsuccessful due to ${status}`)
    //     }
    // });





}