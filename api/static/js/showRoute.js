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
        const routeKeyword = document.querySelector('#route-keyword').value
        const placeType = document.querySelector('#place-type').value
        const radius = document.querySelector('#radius').value
        const numStops = document.querySelector('#num-stops').value

        if (routeZipCode) {
            const queryString = new URLSearchParams({location: routeZipCode, radius: radius, keyword: routeKeyword, place_type: placeType, stops: numStops}).toString();
            console.log(queryString)
            fetch(`/api/routes?${queryString}`)
                .then((response) => response.json())
                .then((responseJSON => {
                    if ("status" in responseJSON) {
                        if (responseJSON["status"] === "error") {
                            console.log("there was an error");
                            const map_placeholder = document.querySelector('#map');
                            map_placeholder.innerHTML = "<p> There were not enough places with your criteria for us to make a crawl route. Please try another search. </p>";
                        }
                        
                    }
                    else {
                        console.log(responseJSON)
                        const map = new google.maps.Map(document.querySelector('#map'), {
                            // center: { placeId: responseJSON["place_ids"][0] },
                            center: responseJSON["locations"][0]["coords"],
    
                            zoom: 13,
                        });
                    
                    
                        const directionsService = new google.maps.DirectionsService();
                    
                        // Directions Renderer draws directions on the map
                        const directionsRenderer = new google.maps.DirectionsRenderer(
                            {
                                suppressMarkers: true
                            }
                        );
                        directionsRenderer.setMap(map);
    
                        // const place_ids = responseJSON["place_ids"]
                        const places = responseJSON["locations"]
    
                        
                        const first_stop = places[0]["place_id"]
                        // const last_stop = place_ids[place_ids.length - 1]
                        const last_stop = places[places.length - 1]["place_id"]
    
                        const waypoints = []
                        for (let i = 1; i < (places.length - 1); i += 1) {
                            let new_waypoint = {}
                            new_waypoint["location"] = {placeId: places[i]["place_id"]}
                            waypoints.push(new_waypoint)
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
                                const stopInfo = new google.maps.InfoWindow()
                                // addMarker(`placeId: ${responseJSON["place_ids"][0]}`, map)
                                for (let i=0; i < places.length; i++) {
                                // const stopMarker = addMarker(
                                //     places[i]["coords"]
                                // , map);
                                const stopMarker = new google.maps.Marker({
                                    position: places[i]["coords"],
                                    label: `${i + 1}`,
                                    map: map,
                                    });
                                

                                stopMarker.addListener('click', () => {
                                    stopInfo.close();
                                    stopInfo.setContent(`<h3> Crawl Stop #${i + 1} </h3> <p> ${places[i]["name"]} </p>`);
                                    stopInfo.open(map, stopMarker);
                                });
                            }



    
                            }
                            else {
                                alert(`Directions request unsuccessful due to ${status}`)
                            }
                        });
                    }

                    
                }
                ))
        }
    }
    );
        // Adds a marker to the map.
    function addInfoWindow(content) {
        new google.maps.InfoWindow({
            content: content,
        });
    }
    function addMarker(location, map) {
        new google.maps.Marker({
        position: location,
        map: map,
        });
    }

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