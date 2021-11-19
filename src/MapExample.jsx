import React, { useState, useEffect } from "react";
import {
  GoogleMap,
  DirectionsRenderer,
  useJsApiLoader,
  // InfoWindow,
  Marker,
} from "@react-google-maps/api";
import Loading from "./Loading";
// https://react-google-maps-api-docs.netlify.app/#

export default function MapExample() {
  const [mapData, setMapData] = useState([]);
  const [loading, setLoading] = useState(false);
  const { isLoaded, loadError } = useJsApiLoader({
    googleMapsApiKey: "",
  });

  // useEffect(() => {
  //   setLoading(true);
  //   fetch("/api/map_data")
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setMapData(data);
  //       setLoading(false);
  //     });
  // }, []);
  const routeZipCode = "94110"
  useEffect(() => {
    setLoading(true);
    fetch(`/api/routes/${routeZipCode}`)
      .then((response) => response.json())
      .then((responseJSON) => {
        setMapData(responseJSON);
        setLoading(false);
      });
  }, []);

  if (loadError) {
    return <h3>There was an error loading the map</h3>;
  }

  if (loading || !isLoaded) {
    return <Loading />;
  }

  return (
    <GoogleMap
      center={{ lat: 72, lng: -140 }}
      mapContainerStyle={{ width: "400px", height: "400px" }}
      zoom={5}
    >
      {mapData.map((dataPoint) => (
        <Marker
          key={dataPoint}
          position={{ placeId: dataPoint, lng: dataPoint}}
        />
      ))}
    </GoogleMap>
  );
}
