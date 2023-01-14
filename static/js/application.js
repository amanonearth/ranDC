
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }            
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p> <ul> <li>' + numbers_received[i].toString() + '</li> </ul></p>';
        }
        $('#log').html(numbers_string);
    });

    socket.on('result', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }            
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = numbers_received.length-2; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p> <ul> <li>' + numbers_received[i].toString() + '</li> </ul></p>';
        }
        $('#result').html(numbers_string);
    });

});