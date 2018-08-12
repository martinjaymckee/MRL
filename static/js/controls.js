var socket=null;
var x;
var y;
var width;
var height;
var radius;
var max_distance = 10;
var canvas;

$(document).ready(function(){
    socket = io.connect('http://localhost:5000/mrl');

    $('#success-alert').hide();
    $('#info-alert').hide();
    $('#danger-alert').hide();

    socket.on('status', function(status) {
      if(status.id == 0) {
        $('#success-alert').show();
        $('#info-alert').hide();
        $('#danger-alert').hide();
      } else if (status.id == 1) {
        $('#success-alert').hide();
        $('#info-alert').show();
        $('#danger-alert').hide();
      } else {
        $('#success-alert').hide();
        $('#info-alert').hide();
        $('#danger-alert').show();
      }
    });

});

function updateControlDimensions() {
  height = windowHeight;
  width = windowWidth;
  width = 0.75 * Math.min(width, height);
  height = width;
  radius = width/2;
}

function setup() {
  updateControlDimensions();
  canvas = createCanvas(width, height);
  canvas.parent('p5-controls');
  canvas.mousePressed( function() {
    // TODO: CONVERT FROM CARTESIAN TO POLAR
    var max_radius = radius - 10;
    var dx = mouseX - (width/2);
    var dy = mouseY - (height/2);
    var r = Math.sqrt(dx*dx + dy*dy);
    if(r <= max_radius) {
      var alpha = Math.atan2(dy, dx);
      var rads = alpha;
      var power = 100;
      x = r * Math.cos(rads) + (width/2);
      y = r * Math.sin(rads) + (height/2);
      // TODO: NEED TO MAKE THIS CALCULATE THE CORRECT "TURN" ANGLE
      //console.log( "r = " + r + "x = " + dx + ", y = " + dy);
      distance = (max_distance * r ) / max_radius;
      cmd = {distance:distance, rads:rads, power:power};
      console.log(cmd);
      socket.emit('move', cmd);
    } else {
      // TODO: THIS IS NOT ON THE CONTROL GRID
    }
  });
  background(0, 0, 0, 0);
}

function polygon(x, y, radius, npoints) {
  var angle = TWO_PI / npoints;
  beginShape();
  for (var a = 0; a < TWO_PI; a += angle) {
    var sx = x + cos(a) * radius;
    var sy = y + sin(a) * radius;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}

function draw() {
  noStroke();
  // TODO: THE BACKGROUND SHOULD BE AN IMAGE
  // TODO: DRAW AN ARROW AND, POTENTIALLY, FILL BASED ON PROGRESS
  // TODO: THE CONTROLS SHOULD BE DRAWN HERE
  fill('blue');
  ellipse(width/2, height/2, width, height);
  fill('white');
  ellipse(x, y, 10);
  fill('yellow');
  ellipse(width/2, height/2, width/10, height/10);

  fill('green');
  poly = polygon(width/10, width/10, width/11, 3);
}

function windowResized() {
  updateControlDimensions();
  resizeCanvas(width, height);
  background(0, 0, 0, 0);
}
