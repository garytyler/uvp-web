$(document).ready(function () {

    // Predefined globals
    if (DEBUG == null) {
        DEBUG = false;
    }
    var guest_socket = null;
    var motion_socket = null;
    var motion_sender_intervalometer_id = null;

    guest = JSON.parse(document.getElementById("guest_json").textContent);
    $("#guest_display_name").append("<b>Name: </b>" + guest.display_name);

    var ws_scheme = "wss://";
    if (window.location.protocol == "http:") {
        ws_scheme = "ws://";
    }


    /*
    //TODO Gyronorm is no longer maintained. Look at FULLTILT, a dependency of gyronorm.

    var gyronormMotionEventCaller = {
        gn: new GyroNorm(),
        init: function (handler) {
            this.handler = handler;
            this.gn.init({});
            return this; // Used by factory
        },
        start: function (handler) {
            this.gn.start(function (data) {
                handler(data.do);
            });
        },
        stop: function () {
            this.gn.stop();
        },
    };
    */


    function MotionCollector() {

        var latest = {
            alpha: 0,
            beta: 0,
            gamma: 0
        };

        var handle_motion_event = function (event) {
            latest = event;
        };

        this.register = function () {
            window.ondeviceorientation = handle_motion_event;
        };

        this.unregister = function () {
            window.ondeviceorientation = null;
        };

        this.get_state = function () {
            return [latest.alpha, latest.beta, latest.gamma];
        };

    }


    function MotionSender(socket) {

        var motion_collector = new MotionCollector();

        var send_latest = function () {
            var motion_state = motion_collector.get_state();
            motion_bytes = new Float64Array(motion_state);
            socket.send(motion_bytes);
            debug_interface.update_motion_data_readout(motion_state);
        };

        this.start = function (fps) {
            console.log('START SENDING MOTION STATE');
            if (fps == null) {
                fps = 30;
            }
            motion_collector.register();
            motion_sender_intervalometer_id = setInterval(send_latest, 1000 / fps);
        };

        this.stop = function () {
            console.log('STOP SENDING MOTION STATE');
            clearInterval(motion_sender_intervalometer_id);
            motion_collector.unregister();
        };

    }


    guest_socket = new WebSocket(ws_scheme + window.location.host + "/ws/guest/");
    guest_socket.onopen = function (event) {
        console.log('guest_socket.onopen', event);
    };
    guest_socket.onmessage = function (event) {
        console.log('guest_socket.onmessage', event);
        data = JSON.parse(event.data);

        if (data.queue_state[0].session_key === guest.session_key) {
            console.log('Enabling interact mode', data.queue_state[0]);
            enableInteractMode(data.queue_state);
        } else {
            console.log('Enabling queue mode', data.queue_state);
            enableQueueMode(data.queue_state);
        }
    };
    guest_socket.onclose = function (event) {
        console.log('guest_socket.onclose', event);
        //TODO Pass an exit code for messaging
        shutdown_client();
    };
    guest_socket.onerror = function (event) {
        console.log('guest_socket.onerror', event);
    };


    function enableQueueMode(queue_state) {
        $("#interact_ui").hide();
        $("#queue_ui").show();

        $("#exit_queue_button").click(function (e) {
            request_force_dequeue();
        });

        populateQueueTable(queue_state);
    }


    function enableInteractMode(queue_state) {
        $("#queue_ui").hide();

        motion_socket = new WebSocket(ws_scheme + window.location.host + "/ws/motion/");
        motion_socket.onopen = function (event) {
            console.log('motion_socket.onopen:', event);

            motion_sender = new MotionSender(motion_socket);

            $("#start_button").click(function (e) {
                $(this).hide();
                $("#stop_button").show();

                motion_sender.start();
            });

            $("#stop_button").click(function (e) {
                $(this).hide();
                $("#start_button").show();

                motion_sender.stop();
            });

            $("#exit_interact_button").click(function (e) {
                request_force_dequeue();
            });

            $("#interact_ui").show();

        };
        motion_socket.onmessage = function (event) {
            data = JSON.parse(event.data);
            console.log('motion_socket.onmessage:', data);

            // if (data.method == "start_interacting") {
            //     time_limit = data.args.time_limit;
            //     fps = data.args.fps;
            // }

        };
        motion_socket.onerror = function (event) {
            console.log('motion_socket.onerror', event);
        };
        motion_socket.onclose = function (event) {
            console.log('motion_socket.onclose', event);
            shutdown_client();
        };

    }


    function request_force_dequeue() {
        guest_socket.send(JSON.stringify({
            "method": "force_dequeue"
        }));
    }


    function shutdown_client() {

        if (motion_sender != null) {
            motion_sender.stop();
        }

        if (motion_socket != null) {
            motion_socket.close();
        }

        if (guest_socket != null) {
            guest_socket.close();
        }

        window.location.href = "/exit/";
    }


    function populateQueueTable(queue_state) {
        table_body = $("#queue_table_body");
        table_body.empty();
        for (var index in queue_state) {
            var item = queue_state[index];
            var row = $("<tr/>");
            row.append("<td>" + index + "</td>");
            row.append("<td>" + item.display_name + "</td>");
            row.append("<td>" + item.session_key + "</td>");
            row.append("</tr>");
            table_body.append(row);
        }
    }


    function DebugInterface(enable) {
        this.update_motion_data_readout = function (data) {};

        if (enable) {
            this.update_motion_data_readout = function (data) {

                console.log(data);

                if (data instanceof Array) {
                    data = {
                        alpha: data[0],
                        beta: data[1],
                        gamma: data[2]
                    };
                }
                for (var key in (data)) {
                    if (typeof data[key] == 'number') {
                        $("#motiondata_" + key).text(data[key].toFixed(2));
                    } else {
                        $("#motiondata_" + key).text(data[key]);
                    }
                }
            };
        }
        $("#debug").css('display', 'inline');
        $("#debug").show();
    }
    debug_interface = new DebugInterface(DEBUG);

});