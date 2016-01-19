/*global google:false, Firebase:false, $:false*/

var map;
var currentPosition;
var gpsFixed = true;
var watchPositionID;
var currentMarker;
var firebase = new Firebase("https://glaring-torch-4222.firebaseio.com/accident/");
var infoWindow;
var situation_marker_icon = [
    'img/red-dot.png',
    'img/blue-dot.png',
    'img/purple-dot.png',
    'img/yellow-dot.png'
];
var accidentMarkers = [];
var accidentInfo = [];
var accidentType = [
    '事故',
    '施工',
    '管制',
    '障礙'
];

function applyPosition(position) {
    'use strict';
    currentPosition = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };
    currentMarker.setPosition(currentPosition);
    if (gpsFixed) {
        map.panTo(currentPosition);
    }
}

function positionErrorHandler(positionError) {
    'use strict';
    window.alert('Error: (' + positionError.code + ')' + positionError.message);
}

function mapsAPILoaded() {
    'use strict';
    var defaultPosition = {
        lat: 25.039820,
        lng: 121.512001
    };
    map = new google.maps.Map(document.getElementById('map'), {
        center: defaultPosition,
        zoom: 16
    });
    if (navigator.geolocation) {
        watchPositionID = navigator.geolocation.watchPosition(applyPosition, positionErrorHandler);
    } else {
        window.alert('Navigator is unusable!');
    }
    map.addListener('dragstart', function () {
        gpsFixed = false;
        $('#gps-fixed-btn').fadeIn('fast');
    });
    currentMarker = new google.maps.Marker({
        map: map,
        zIndex: google.maps.Marker.MAX_ZINDEX + 1,
        icon: 'img/1452554285_car.png'
    });
    infoWindow = new google.maps.InfoWindow({
        maxWidth: 200
    });
    firebase.on('child_added', function (snapshot) {
        var data = snapshot.val(),
            marker = new google.maps.Marker({
                position: {
                    lat: data.latitude,
                    lng: data.longitude
                },
                map: map,
                animation: google.maps.Animation.DROP,
                icon: situation_marker_icon[data.type]
            });
        marker.addListener('click', function () {
            infoWindow.setContent(
                '<h4>' + accidentType[accidentInfo[accidentMarkers.indexOf(this)].type] + '</h4>' +
                    '<p>' + accidentInfo[accidentMarkers.indexOf(this)].description + '</p>'
            );
            infoWindow.open(map, this);
        });
        accidentInfo.push(data);
        accidentMarkers.push(marker);
    });
}

function accidentReport(type, desc) {
    'use strict';
    /*
    var lat = currentPosition.lat + 0.000001 * Math.ceil(Math.random() * 8948),
        lng = currentPosition.lng + 0.000001 * Math.ceil(Math.random() * 13239);
    */
    $.get('https://roads.googleapis.com/v1/snapToRoads', {
        key: 'AIzaSyCquZV94BIFX8D4J75AG8ZWGICNOJOGb60',
        path: currentPosition.lat + ',' + currentPosition.lng
    }, function (data) {
        firebase.push({
            timestamp: Math.ceil(Date.now() / 1000),
            latitude: data.snappedPoints[0].location.latitude,
            longitude: data.snappedPoints[0].location.longitude,
            description: desc,
            type: type
        });
    });
}

function removeAllOpenClass() {
    'use strict';
    $('#report-toggle-btn').removeClass('open');
    $('#situation-group-ul > li > button').removeClass('open');
    $('#report-form').removeClass('open');
}

$(document).ready(function () {
    'use strict';
    $('#report-toggle-btn').click(function () {
        $(this).toggleClass('open');
        $('#situation-group-ul > li > button').toggleClass('open');
    });
    $('#gps-fixed-btn').click(function () {
        gpsFixed = true;
        navigator.geolocation.getCurrentPosition(applyPosition, positionErrorHandler);
        $(this).fadeOut('fast');
    });
    $('#situation-group-ul > li > button').click(function () {
        $('#report-form').toggleClass('open');
        $('#report-confirm').val($(this).val());
        $('#report-form h2').html($(this).html());
        $('#desc').val('');
    });
    $('#report-cancel').click(function () {
        removeAllOpenClass();
    });
    $('#report-confirm').click(function () {
        accidentReport(Number($(this).val()), $('#desc').val());
        removeAllOpenClass();
    });
});