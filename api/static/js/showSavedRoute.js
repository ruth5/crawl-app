'use strict';



function initMap() {
    const routeCoords = [];

    let map = new google.maps.Map(document.querySelector('#map'), {
        center: {
            "lat": 37.77361,
            "lng": -122.421622
        },

        zoom: 13,
    });
    var buttons = document.getElementsByTagName("button");
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click',
            () => {
                let buttonID = buttons[i].id
                console.log(buttonID)
                fetch(`/api/saved-routes/${buttonID}`)
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
                        map = new google.maps.Map(document.querySelector('#map'), {
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
    

                        const places = responseJSON["locations"]
    
                        
                        const first_stop = places[0]["place_id"]
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

                        console.log(crawlRoute)
                    
                        directionsService.route(crawlRoute, (response, status) => {
                            if (status === 'OK') {
                                directionsRenderer.setDirections(response);
                                const stopInfo = new google.maps.InfoWindow()

                                for (let i=0; i < places.length; i++) {

                                const stopMarker = new google.maps.Marker({
                                    position: places[i]["coords"],
                                    label: `${i + 1}`,
                                    map: map,
                                    });
                                

                                stopMarker.addListener('click', () => {
                                    stopInfo.close();
                                    stopInfo.setContent(`<h5> Crawl Stop #${i + 1} </h5> <p class="info-window-name"> ${places[i]["name"]} </p>`);
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
        )

    }

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



}

// function saveRoute() {
//     saveRouteForm = document.querySelector('#save-crawl');

//     saveRouteForm.addEventListener("submit", (evt) => {
//         evt.preventDefault();
//         const crawlName = document.querySelector('#crawl-name').value;
//         if (crawlName) {

//         }


//     })
// }