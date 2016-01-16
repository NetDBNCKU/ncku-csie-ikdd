/*global google:false, Firebase:false, $:false*/

var map;
var watchPositionID;
var currentMarker;
var currentPosition;
var autoMove = true;
var accidentMarkers = [];
var accidentInfo = [];
var firebase = new Firebase("https://glaring-torch-4222.firebaseio.com/accident/");
var infoWindow;
var accidentType = [
    '事故',
    '施工',
    '管制',
    '障礙'
];
var situation_marker_icon = [
    'img/red-dot.png',
    'img/blue-dot.png',
    'img/purple-dot.png',
    'img/yellow-dot.png'
];

function applyPosition(position) {
    'use strict';
    var latlng = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };
    currentMarker.setPosition(latlng);
    currentPosition = latlng;
    if (autoMove) {
        map.panTo(latlng);
        map.setZoom(16);
    }
}

function positionErrorHandler(positionError) {
    'use strict';
    window.console.log('Error: (' + positionError.code + ')' + positionError.message);
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

function relocate() {
    'use strict';
    autoMove = true;
    $('#position-btn').fadeOut();
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

$(document).ready(function () {
    'use strict';
    if (navigator.geolocation) {
        watchPositionID = navigator.geolocation.watchPosition(applyPosition, positionErrorHandler);
    } else {
        window.alert('Navigator is unusable!');
    }
    $('#situation-btn-0').click(function () {
        $(this).toggleClass('open');
        if (window.innerHeight > window.innerWidth) {
            $('.situation-btn').toggleClass('scaleY');
        } else {
            $('.situation-btn').toggleClass('scaleX');
        }
    });
    $('.situation-btn').click(function () {
        $('#report-form').toggleClass('scale');
        $('#report-confirm').val($(this).val());
        $('#report-form h2').html($(this).html());
    });
    $('#report-cancel').click(function () {
        $('#report-form').toggleClass('scale');
    });
    $('#report-confirm').click(function () {
        accidentReport(Number($(this).val()), $('#desc').val());
        $('#report-form').toggleClass('scale');
        $('#situation-btn-0').click();
    });
});