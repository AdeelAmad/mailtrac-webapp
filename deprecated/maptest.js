//define all location package has been
var citycoords = [
      {lat: 37.93414, lng: -121.696744},
      {lat: 37.739651, lng: -121.425223},
      {lat: 34.07029, lng: -117.39588},
    ];
//create map
function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: citycoords[0],
  });

  //create polyline using citycoords
  var travelPath = new google.maps.Polyline({
    path: citycoords,
    geodesic: true,
    strokeColor: '#00a8b8',
    strokeOpacity: 1.0,
    strokeWeight: 1
  });
  travelPath.setMap(map);

  //add all markers
  for (var city in citycoords) {
    var marker = new google.maps.Marker({
      position: citycoords[city],
      map: map,
    });
  };
}


function changeText(){
    var btn = document.getElementById("togglemap");

    if (btn.innerHTML == "Show Map"){
        btn.innerHTML = "Hide Map"
    } else {
        btn.innerHTML = "Show Map"
    }
}