"use strict";

document.addEventListener('DOMContentLoaded', function () {
  // connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port); // grab message template

  var messageTemplate = Handlebars.compile(document.querySelector('#message-template').innerHTML); // When connected, configure buttons

  socket.on('connect', function () {
    // Add a "submit message" event to submit button
    var button = document.querySelector('#message-submit');

    button.onclick = function () {
      var message = {
        'from': this.dataset.from,
        'message': document.querySelector('#message-textarea').value
      };
      socket.emit('submit message', message);
      alert('Emit:' + message.toString());
    };
  }); // When a message is submitted, add to the queue

  socket.on('announce message', function (data) {
    // Build from message template
    var newMessage = messageTemplate(data);
    alert('Received:' + newMessage.toString()); // Append to beginning of message container

    var previousMessages = document.querySelector('#messages-container');
    previousMessages.innerHTML = newMessage + previousMessages.innerHTML;
  });
});