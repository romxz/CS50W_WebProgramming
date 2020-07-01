document.addEventListener('DOMContentLoaded', () => {
    
    // connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // grab message template
    const messageTemplate = Handlebars.compile(document.querySelector('#message-template').innerHTML);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Add a "submit message" event to submit button
        const button = document.querySelector('#message-submit');
        button.onclick = function() {
            const message = {
                'from': this.dataset.from, 
                'message': document.querySelector('#message-textarea').value
            };
            socket.emit('submit message', message);
            alert('Emit:' + message.toString());
        };
    });

    // When a message is submitted, add to the queue
    socket.on('announce message', data => {

        // Build from message template
        const newMessage = messageTemplate(data);
        alert('Received:' + newMessage.toString());

        // Append to beginning of message container
        const previousMessages = document.querySelector('#messages-container');
        previousMessages.innerHTML = newMessage + previousMessages.innerHTML;
    });
});