/*global google:false, Firebase:false, $:false*/

var map;
var markers = [];
var firebase = new Firebase("https://glaring-torch-4222.firebaseio.com/accident/");

function applyPosition(position) {
    'use strict';
    var latlng = {lat: position.coords.latitude, lng: position.coords.longitude}, marker;
    map.setCenter(latlng);
    map.setZoom(16);
    marker = new google.maps.Marker({
        position: latlng,
        map: map,
        icon: 'img/1452554285_car.png'
    });
    firebase.on('child_added', function (snapshot) {
        var data = snapshot.val();
        markers.push(new google.maps.Marker({
            position: {lat: data.latitude, lng: data.longitude},
            map: map,
            animation: google.maps.Animation.DROP
        }));
    });
}

function mapsAPILoaded() {
    'use strict';
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 25.039820, lng: 121.512001},
        zoom: 8
    });
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(applyPosition);
    }
}

function accidentReport() {
    'use strict';
    var lat = 22.988287 + 0.000001 * Math.ceil(Math.random() * 8948),
        lng = 120.212102 + 0.000001 * Math.ceil(Math.random() * 13239);
    $.get('https://roads.googleapis.com/v1/snapToRoads', {
        key: 'AIzaSyCquZV94BIFX8D4J75AG8ZWGICNOJOGb60',
        path: lat + ',' + lng
    }, function (data) {
        firebase.push({
            timestamp: Math.ceil(Date.now() / 1000),
            latitude: data.snappedPoints[0].location.latitude,
            longitude: data.snappedPoints[0].location.longitude,
            type: 0,
            step: 1
        });
    });
}
