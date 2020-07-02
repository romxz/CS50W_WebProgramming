"use strict";

document.addEventListener('DOMContentLoaded', function () {
  // Request messages for this topic
  var request = new XMLHttpRequest();
  request.open('POST', '/rooms/messages'); // Callback for when message request completes

  request.onload = function () {
    // Extract JSON data from request
    var data = JSON.parse(request.responseText); // Load all messages if successful

    if (data.success) {
      //alert('Message request success!');
      load_all_messages(data.messages);
    } else {} //alert('Couldn\'t load messages');
    // Once loaded, connect to allow furthe messages


    messageSocket();
  }; // Send request


  var topic = document.querySelector('#message-submit').dataset.topic;
  var requestData = new FormData();
  requestData.append('topic', topic); //alert('First message request sent');

  request.send(requestData);
  var maxNumMessages = 10;
  var messageNum = 0;
  var messageContainer = document.querySelector('#messages-container'); // Loads a list of messages

  function load_all_messages(messages) {
    for (var i = Math.min(messages.length - 1, maxNumMessages - 1); i >= 0; i--) {
      load_message(messages[i]);
    }
  } // Compile message template


  var messageTemplate = Handlebars.compile(document.querySelector('#message-template').innerHTML); // Loads a single message

  function load_message(messageData) {
    var div = document.createElement('div');
    div.innerHTML = messageTemplate(messageData);
    div.setAttribute('id', 'message-' + messageNum);
    messageContainer.prepend(div);
    messageNum++;

    if (messageNum > maxNumMessages) {
      messageContainer.removeChild(messageContainer.lastChild);
    }
  } // Creates websocket connection to post messages in current channel


  function messageSocket() {
    // connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port); // When connected, configure buttons

    socket.on('connect', function () {
      // Add a "submit message" event to submit button
      var button = document.querySelector('#message-submit');

      button.onclick = function () {
        var message = {
          'from': this.dataset.from,
          'topic': this.dataset.topic,
          'message': document.querySelector('#message-textarea').value
        };
        socket.emit('submit message', message); //alert(`Emit::\nfrom:${message.from};\ntopic:${message.topic};\nmessage:${message.message}`);
      };
    }); // When a message is submitted, add to the queue

    socket.on('announce message', function (data) {
      //alert(`Received message!\nSuccess: ${data.success}`);
      if (data.success) {
        load_message(data.message);
      } // else { alert(`Errors:\n${data.errors}`); }

    });
  }
});