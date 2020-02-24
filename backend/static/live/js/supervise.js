$(document).ready(function () {

    var ws_scheme = 'wss://';
    if (window.location.protocol == 'http:') {
        ws_scheme = 'ws://';
    }

    function send_request(method, args) {
        console.log("SEND REQUEST", method, args);
        supervisor_socket.send(JSON.stringify({ method: method, args: args }));
    }

    function remove_guest(session_key) {
        method = 'remove_guest';
        args = { 'session_key': session_key };
        send_request(method, args);
    }

    var supervisor_socket = new WebSocket(ws_scheme + window.location.host + '/ws/supervisor/');
    supervisor_socket.onmessage = function (event) {
        console.log('supervisor_socket.onmessage:', event);
        var data = JSON.parse(event.data);
        // $('#supervisor_ui').show();
        buildQueueMonitor(data.queue_state);
    };
    supervisor_socket.onclose = function (event) {
        console.log('supervisor_socket.close', event);
    };
    supervisor_socket.onclose = function (event) {
        console.log('supervisor_socket.onclose', event);
    };
    supervisor_socket.onerror = function (event) {
        console.log('supervisor_socket.onerror', event);
    };

    function createHeaderRow(labels) {
        var head_row = $('<tr/>');
        for (var index in labels) {
            head_row.append('<th>' + labels[index] + '</th>');
        }
        return head_row;
    }

    function createDataRow(index, queue_item) {
        var row = $('<tr/>');
        row.attr('id', queue_item.session_key);

        rem_button = $('<button>');
        rem_button.append('Remove');
        rem_button.on('click', function () {
            remove_guest(queue_item.session_key);
        });

        row.append(rem_button);
        row.append('<td>' + index + '</td>');
        row.append('<td>' + queue_item.guest_name + '</td>');
        row.append('<td>' + queue_item.session_key + '</td>');
        row.append('<td>' + queue_item.channel_names.join('\n') + '</td>');

        // Support multi-line data cells
        row.css('white-space', 'pre-wrap');
        row.css('word-wrap', 'break-word');

        return row;
    }

    function buildQueueMonitor(queue_state) {
        console.log("BUILD QUEUE MONITOR", queue_state);

        var table = $('#queue_monitor_table');
        var labels = Array("", 'Pos.', 'Name', 'Session', 'Sockets');

        var thead = $('<thead/>').append(createHeaderRow(labels));
        var tbody = $('<tbody/>');
        for (var index in queue_state) {
            tbody.append(createDataRow(index, queue_state[index]));
        }

        table.empty();
        table.append(thead);
        table.append(tbody);
    }

});