/*global google:false, Firebase:false, $:false*/

var map;
var currentPosition;
var gpsFixed = true;
var watchPositionID;
var currentMarker;
var FIREBASE = new Firebase("https://glaring-torch-4222.firebaseio.com/");
var infoWindow;
var accidents = {};
var SITUATION_MARKER_ICON = [
    'img/red-dot.png',
    'img/blue-dot.png',
    'img/purple-dot.png',
    'img/yellow-dot.png'
];
var ACCIDENT_TYPE = [
    '事故',
    '施工',
    '管制',
    '障礙'
];
var CREATE_NEW_RADIUS = 50;
var DURIATION = 60 * 60;

var degreesToRadians = function (degrees) {
    'use strict';
    return (degrees * Math.PI / 180);
};

function distance(pos1, pos2) {
    'use strict';
    var a, c,
        latDelta = degreesToRadians(pos2.lat - pos1.lat),
        lonDelta = degreesToRadians(pos2.lng - pos1.lng),
        radius = 6371; // Earth's radius in kilometers

    a = (Math.sin(latDelta / 2) * Math.sin(latDelta / 2)) +
        (Math.cos(degreesToRadians(pos1.lat)) * Math.cos(degreesToRadians(pos2.lat)) *
            Math.sin(lonDelta / 2) * Math.sin(lonDelta / 2));

    c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return radius * c * 1000; // kilometer -> meter
}

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
    window.alert('無法取得位置，請開啟定位及WiFi並重新整理！');
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
        maxWidth: 300
    });
    FIREBASE.child('accident').orderByChild('timestamp').startAt(Math.ceil(Date.now() / 1000) - DURIATION).on('child_added', function (snapshot) {
        var data = snapshot.val(),
            marker = new google.maps.Marker({
                position: data.position,
                map: map,
                animation: google.maps.Animation.DROP,
                icon: SITUATION_MARKER_ICON[data.type],
                title: snapshot.key()
            });
        marker.addListener('click', function () {
            infoWindow.setContent(
                '<h4>' + ACCIDENT_TYPE[accidents[this.getTitle()].info.type] + '</h4>' +
                    '<p>' +
                        '<strong>更新時間</strong>: ' + (new Date(accidents[this.getTitle()].info.timestamp * 1000)).toLocaleString() +
                        '<br>' +
                        '<strong>路況敘述</strong>: ' + accidents[this.getTitle()].info.description +
                    '</p>'
            );
            infoWindow.open(map, this);
        });
        accidents[snapshot.key()] = {
            marker: marker,
            info: data
        };
    });
    FIREBASE.child('accident').orderByChild('timestamp').startAt(Math.ceil(Date.now() / 1000) - DURIATION).on('child_changed', function (snapshot) {
        accidents[snapshot.key()].marker.setPosition(snapshot.val().position);
        accidents[snapshot.key()].marker.setIcon(SITUATION_MARKER_ICON[snapshot.val().type]);
        accidents[snapshot.key()].info = snapshot.val();
    });
}

function accidentReport(type, desc) {
    'use strict';
    var id, identifier = '', position = $.extend({}, currentPosition);
    for (id in accidents) {
        if (accidents.hasOwnProperty(id)) {
            if (distance(currentPosition, accidents[id].info.position) < CREATE_NEW_RADIUS) {
                identifier = id;
                position.lat = (position.lat + accidents[id].info.position.lat) / 2;
                position.lng = (position.lng + accidents[id].info.position.lng) / 2;
                desc = accidents[id].info.description + '\n' + desc;
                break;
            }
        }
    }
    $.get('https://roads.googleapis.com/v1/snapToRoads', {
        key: 'AIzaSyCquZV94BIFX8D4J75AG8ZWGICNOJOGb60',
        path: position.lat + ',' + position.lng
    }, function (data) {
        if (identifier === '') {
            FIREBASE.child('accident').push({
                timestamp: Math.ceil(Date.now() / 1000),
                position: {
                    lat: data.snappedPoints[0].location.latitude,
                    lng: data.snappedPoints[0].location.longitude
                },
                description: desc,
                type: type
            });
        } else {
            FIREBASE.child('accident').child(identifier).update({
                timestamp: Math.ceil(Date.now() / 1000),
                position: {
                    lat: data.snappedPoints[0].location.latitude,
                    lng: data.snappedPoints[0].location.longitude
                },
                description: desc,
                type: type
            });
        }
    });
}

function removeAllOpenClass() {
    'use strict';
    $('#report-toggle-btn').removeClass('open');
    $('#situation-group-ul > li > button').removeClass('open');
    $('#report-form').removeClass('open');
    $('#feedback-form').removeClass('open');
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
        if ($(this).val() === '4') {
            $('#feedback-form').toggleClass('open');
        } else {
            $('#report-form').toggleClass('open');
            $('#report-confirm').val($(this).val());
            $('#report-form h2').html($(this).html());
            $('#desc').val('');
        }
    });
    $('#report-cancel, #feedback-cancel').click(function () {
        removeAllOpenClass();
    });
    $('#report-confirm').click(function () {
        accidentReport(Number($(this).val()), $('#desc').val());
        removeAllOpenClass();
    });
    $('#feedback-confirm').click(function () {
        FIREBASE.child('opinion').push({
            timestamp: Math.ceil(Date.now() / 1000),
            content: $('#opinion').val()
        });
        removeAllOpenClass();
    });
});