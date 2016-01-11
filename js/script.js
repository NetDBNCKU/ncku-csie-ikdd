/*global google:false*/

function mapsAPILoaded() {
    'use strict';
    var map = new google.maps.Map(document.getElementById('map'), {
        center: (function () {
            if (navigator.geolocation) {
                var position = navigator.geolocation.getCurrentPosition();
                return {lat: position.coords.latitude, lng: position.coords.longitude};
            }
            return {lat: 25.039820, lng: 121.512001};
        }()),
        zoom: 8
    });
}