var socket=Nil;
var x;
var y;
var width;
var height;
var radius;
var max_distance = 10;

$(document).ready(function(){
    socket = io.connect('http://localhost:5000/mrl');
    // socket.on('message', function(msg) {
    //     $('#messages').append('<p>Received: ' + msg.text + '</p>');
    // });
    // $('#send').click(function(event) {
    //     socket.emit('message', { text : $('#msg').val()});
    //     return false;
    // });
});

function setup() {
  width = 400; // TODO: THIS NEEDS TO BE TAKEN FROM THE DOCUMENT AND TREATED AS DYNAMIC
  height = 400;
  radius = width/2;
  var canvas = createCanvas(width, height);
  canvas.parent('p5-controls');
  canvas.mousePressed( function() {
    // TODO: CONVERT FROM CARTESIAN TO POLAR
    var max_radius = radius - 10;
    var dx = mouseX - (width/2);
    var dy = mouseY - (height/2);
    var r = Math.min(max_radius, Math.sqrt(dx*dx + dy*dy));
    var alpha = Math.atan2(dy, dx);
    var rads = alpha;
    var power = 100;
    x = r * Math.cos(rads) + (width/2);
    y = r * Math.sin(rads) + (height/2);
    console.log( "r = " + r + "x = " + dx + ", y = " + dy);
    distance = (max_distance * r ) / max_radius;
    cmd = {distance:distance, rads:rads, power:power};
    socket.emit('move', cmd)
  });
  background(0, 0, 0, 0);
}

function draw() {
  noStroke();
  // TODO: THE BACKGROUND SHOULD BE AN IMAGE
  fill('blue');
  ellipse(width/2, height/2, width, height);
  fill('white');
  ellipse(x, y, 10);
  fill('yellow');
  ellipse(width/2, height/2, width/10, height/10);
}
