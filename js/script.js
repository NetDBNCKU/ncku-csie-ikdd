/*global google:false, Firebase:false, $:false*/

var map;
var watchPositionID;
var currentMarker;
var autoMove = true;
var accidentMarkers = [];
var firebase = new Firebase("https://glaring-torch-4222.firebaseio.com/accident/");

function applyPosition(position) {
    'use strict';
    var latlng = {lat: position.coords.latitude, lng: position.coords.longitude};
    currentMarker.setPosition(latlng);
    if (autoMove) {
        map.setCenter(latlng);
    }
}

function positionErrorHandler(positionError) {
    'use strict';
    window.alert('Error: ' + positionError.message);
}

function mapsAPILoaded() {
    'use strict';
    var defaultPosition = {lat: 25.039820, lng: 121.512001};
    map = new google.maps.Map(document.getElementById('map'), {
        center: defaultPosition,
        zoom: 16
    });
    currentMarker = new google.maps.Marker({
        position: defaultPosition,
        map: map,
        icon: 'img/1452554285_car.png'
    });
    firebase.on('child_added', function (snapshot) {
        var data = snapshot.val();
        accidentMarkers.push(new google.maps.Marker({
            position: {lat: data.latitude, lng: data.longitude},
            map: map,
            animation: google.maps.Animation.DROP
        }));
    });
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

(function () {
    'use strict';
    if (navigator.geolocation) {
        watchPositionID = navigator.geolocation.watchPosition(applyPosition, positionErrorHandler);
    } else {
        window.alert('Navigator is unusable!');
    }
}());