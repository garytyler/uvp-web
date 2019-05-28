$(document).ready(function () {

    guest = JSON.parse(document.getElementById("guest_json").textContent);
    $("#guest_display_name").append("<b>Name: </b>" + guest.display_name);

    var ws_scheme = "wss://";
    if (window.location.protocol == "http:") {
        ws_scheme = "ws://";
    }

    var gyronormMotionEventCaller = {
        gn: new GyroNorm(),
        init: function (handler) {
            this.handler = handler;
            this.gn.init({});
            return this; // Used by factory
        },
        start: function () {
            this.gn.start(function (data) {
                this.handler(data.do);
            });
        },
        stop: function () {
            this.gn.stop();
        },
    };

    var nativeMotionEventCaller = {
        init: function () {
            return this; // Used by factory
        },
        start: function () {
            window.ondeviceorientation = handler;
        },
        stop: function () {
            window.ondeviceorientation = null;
        }
    };

    function MotionManager() {
        getEventCaller = function (handler, motion_type) {
            switch (motion_type) {
                case "native_euler":
                    return nativeMotionEventCaller.init();
                case "gyronorm_euler":
                    return gyronormMotionEventCaller.init(handler);
                default:
                    return nativeMotionEventCaller.init();
            }
        };

        handler = function (data) {
            console.log(data);
            motion_socket.send(JSON.stringify({
                // guest: { display_name: guest.display_name },
                euler: {
                    alpha: data.alpha,
                    beta: data.beta,
                    gamma: data.gamma
                }
            }));
            debug_interface.update_motion_data(data);
        };
        var event_caller = getEventCaller(handler);

        this.start = function () {
            event_caller.start();
        };
        this.stop = function () {
            event_caller.stop();
        };

    }


    // Predefined globals
    var DEBUG = true;
    motion_socket = null;


    var guest_socket = new WebSocket(ws_scheme + window.location.host + "/ws/guest/");
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
            console.log('motion_socket.onopen', event);

            motion_sender = new MotionManager();

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
            console.log('motion_socket.onmessage:', event);
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
        guest_socket.send(JSON.stringify({ "method": "force_dequeue" }));
    }
    function shutdown_client() {
        if (motion_sender != null) { motion_sender.stop(); }
        if (motion_socket != null) { motion_socket.close(); }
        if (guest_socket != null) { guest_socket.close(); }
        window.location.href = "/exit/";
    }

    function populateQueueTable(queue_state) {
        console.log(queue_state);
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
        this.update_motion_data = function (data) { };
        this.reveal_queue = function (queue_state) { };
        if (enable) {
            // API
            this.update_motion_data = function (data) {
                for (var key in (data)) {
                    if (typeof data[key] == 'number') {
                        $("#motiondata_" + key).text(data[key].toFixed(2));
                    } else {
                        $("#motiondata_" + key).text(data[key]);
                    }
                }
            };
        }

        this.reveal_queue_ui = function (queue_state) {
            populateQueueTable(queue_state);
            $("#queue_ui").show();
        };

        // UI
        $("#queue_ui_button").click(function () {
            $("#queue_ui").show();
        });
        $("#interact_ui_button").click(function () {
            enableQueueMode();
        });
        $("#debug").css('display', 'inline');
        $("#debug").show();
    }

    debug_interface = new DebugInterface(DEBUG);
});