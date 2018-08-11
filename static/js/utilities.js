$(document).ready(function(){
    var socket = io.connect('https://localhost:5000/test');
    socket.on('message', function(msg) {
        $('#messages').append('<p>Received: ' + msg.text + '</p>');
    });
    $('#send').click(function(event) {
        socket.emit('message', { text : $('#msg').val()});
        return false;
    });
});
