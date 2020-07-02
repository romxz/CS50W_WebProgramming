document.addEventListener('DOMContentLoaded', () => {
    
    
    // Request messages for this topic
    const request = new XMLHttpRequest();
    request.open('POST', '/rooms/messages');

    // Callback for when message request completes
    request.onload = () => {    
        // Extract JSON data from request
        const data = JSON.parse(request.responseText);
        // Load all messages if successful
        if (data.success) {
            //alert('Message request success!');
            load_all_messages(data.messages);
        } else {
            //alert('Couldn\'t load messages');
        }
        // Once loaded, connect to allow furthe messages
        messageSocket();
    }

    // Send request
    const topic = document.querySelector('#message-submit').dataset.topic;
    const requestData = new FormData();
    requestData.append('topic', topic);
    //alert('First message request sent');
    request.send(requestData);

    var maxNumMessages = 10;
    var messageNum = 0;
    const messageContainer = document.querySelector('#messages-container');

    // Loads a list of messages
    function load_all_messages(messages) {
        for (let i = Math.min(messages.length-1, maxNumMessages-1); i >= 0; i--) {
            load_message(messages[i]);
        }
    }

    // Compile message template
    const messageTemplate = Handlebars.compile(document.querySelector('#message-template').innerHTML);
    
    // Loads a single message
    function load_message(messageData) {
        const div = document.createElement('div');
        div.innerHTML = messageTemplate(messageData);
        div.setAttribute('id', 'message-'+messageNum);
        messageContainer.prepend(div);
        messageNum++;
        if (messageNum > maxNumMessages) {
            messageContainer.removeChild(messageContainer.lastChild);
        }
    }

    // Creates websocket connection to post messages in current channel
    function messageSocket() {
        // connect to websocket
        var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

        // When connected, configure buttons
        socket.on('connect', () => {

            // Add a "submit message" event to submit button
            const button = document.querySelector('#message-submit');
            button.onclick = function() {
                const message = {
                    'from': this.dataset.from,
                    'topic': this.dataset.topic,
                    'message': document.querySelector('#message-textarea').value
                };
                socket.emit('submit message', message);
                //alert(`Emit::\nfrom:${message.from};\ntopic:${message.topic};\nmessage:${message.message}`);
            };
        });

        // When a message is submitted, add to the queue
        socket.on('announce message', data => {
            //alert(`Received message!\nSuccess: ${data.success}`);
            if (data.success) {
                load_message(data.message);
            } // else { alert(`Errors:\n${data.errors}`); }
        });
    }
    
});