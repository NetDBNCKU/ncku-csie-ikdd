/*global google:false, Firebase:false, $:false*/

var map;
var watchPositionID;
var currentMarker;
var autoMove = true;
var accidentMarkers = [];
var firebase = new Firebase("https://glaring-torch-4222.firebaseio.com/accident/");
var COLOR_ARR = [
    '0x1F77B4',
    '0xFF7F0E',
    '0x2CA02C',
    '0xD62728',
    '0x9467BD',
    '0x8C564B',
    '0xE377C2',
    '0x7F7F7F',
    '0xBCBD22',
    '0x17BECF'
];

function applyPosition(position) {
    'use strict';
    var latlng = {lat: position.coords.latitude, lng: position.coords.longitude};
    currentMarker.setPosition(latlng);
    if (autoMove) {
        map.panTo(latlng);
        map.setZoom(16);
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
    map.addListener('dragstart', function () {
        autoMove = false;
        $('#position-btn').fadeIn();
    });
    currentMarker = new google.maps.Marker({
        position: defaultPosition,
        map: map,
        zIndex: google.maps.Marker.MAX_ZINDEX + 1,
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

function relocate() {
    'use strict';
    autoMove = true;
    $('#position-btn').fadeOut();
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

$(document).ready(function () {
    'use strict';
    if (navigator.geolocation) {
        watchPositionID = navigator.geolocation.watchPosition(applyPosition, positionErrorHandler);
    } else {
        window.alert('Navigator is unusable!');
    }
    $('#situation-btn-0').click(function () {
        $(this).toggleClass('open');
        $('.situation-btn').toggleClass('scale');
    });
});