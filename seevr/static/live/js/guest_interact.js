$(document).ready(function () {

    var DEBUG = true;
    var guest_socket = null;
    var motion_sender = null;
    var motion_sender_intervalometer_id = null;
    console.log(document.getElementById("context_json").textContent.toString());
    context_data = JSON.parse(document.getElementById("context_json").textContent);
    console.log(context_data.toString());
    console.log(context_data.feature_slug);
    console.log(context_data.guest_name);
    $("#guest_name").append("<b>Name: </b>" + context_data.guest_name);

    var ws_scheme = "wss://";
    if (window.location.protocol == "http:") {
        ws_scheme = "ws://";
    }

    class MotionCollector {
        constructor() {
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
                console.log(latest.alpha, latest.beta, latest.gamma);
                return [latest.alpha, latest.beta, latest.gamma];
            };
        }
    }


    class MotionSender {
        constructor(socket) {
            var motion_collector = new MotionCollector();

            this.send_latest = function () {
                var motion_state = motion_collector.get_state();
                if (!motion_state.includes(null)) {
                    var motion_bytes = new Float64Array(motion_state);
                    socket.send(motion_bytes);
                    debug_interface.update_motion_data_readout(motion_state);
                } else {
                    console.log("No motion data available.")
                }
            };

            this.start = function (fps) {
                console.log('START SENDING GYRONORM MOTION STATE');
                if (fps == null) {
                    fps = 30;
                }
                motion_collector.register();
                motion_sender_intervalometer_id = setInterval(this.send_latest, 1000 / fps);
            };

            this.stop = function () {
                console.log('STOP SENDING MOTION STATE');
                clearInterval(motion_sender_intervalometer_id);
                motion_collector.unregister();
            };
        }
    }


    guest_socket = new WebSocket(ws_scheme + window.location.host + "/ws/guest/");
    guest_socket.onopen = function (event) {
        console.log('guest_socket.onopen', event);
    };
    guest_socket.onmessage = function (event) {
        console.log('guest_socket.onmessage', event);
        received_data = JSON.parse(event.data);
        console.log(received_data.feature.presenter_channel);

        if (!received_data.feature.presenter_channel || 0 === received_data.feature.presenter_channel) {
            var msg = "Feature unavailable."
            $("#message_display").show()
            $("#message_display").text(msg);
        } else if (received_data.guest_queue[0].session_key === context_data.session_key) {
            console.log('Enabling interact mode', received_data.guest_queue[0]);
            enableInteractMode(received_data.guest_queue);
        } else {
            console.log('Enabling waiting mode', received_data.guest_queue);
            enableWaitingMode(received_data.guest_queue);
        }
    };
    guest_socket.onclose = function (event) {
        console.log('guest_socket.onclose', event);
        window.location.href = "/exit/";
    };
    guest_socket.onerror = function (event) {
        console.log('guest_socket.onerror', event);
    };


    function enableWaitingMode(guest_queue) {
        $("#interact_ui").hide();
        $("#waiting_ui").show();
        $("#exit_waiting_button").click(function (e) {
            close_session(guest_socket);
        });

        populateWaitingTable(guest_queue);
    }


    function enableInteractMode() {
        $("#waiting_ui").hide();

        motion_sender = new MotionSender(guest_socket);
        console.log("PERMISSION GRANTED");
        $("#start_interact_button").click(function (e) {
            // feature detect
            if (typeof DeviceOrientationEvent.requestPermission === 'function') {
                DeviceOrientationEvent.requestPermission()
                    .then(permissionState => {
                        if (permissionState === 'granted') {
                            motion_sender.start();
                        }
                    })
                    .catch(console.error);
            } else {
                // handle regular non iOS 13+ devices
                motion_sender.start();
            }
            $(this).hide();
            $("#stop_button").show();
        });

        $("#stop_interact_button").click(function (e) {
            $(this).hide();
            $("#start_button").show();

            motion_sender.stop();
        });

        $("#exit_interact_button").click(function (e) {
            close_session(guest_socket)
        });

        $("#message_display").hide();
        $("#interact_ui").show();

        $("#debug_send_current_state").click(function () {
            console.log('CLICKED');
            motion_sender.send_latest();
        });
    };


    function close_session(guest_socket) {
        console.log("CLOSE SESSION");
        guest_socket.send(JSON.stringify({
            "type": "close_session", "message": { "close_code": 4150 }
        }));
    }


    function populateWaitingTable(guest_queue) {
        table_body = $("#guest_queue_table_body");
        table_body.empty();
        for (var index in guest_queue) {
            var item = guest_queue[index];
            var row = $("<tr/>");
            row.append("<td>" + index + "</td>");
            row.append("<td>" + item.guest_name + "</td>");
            row.append("<td>" + item.session_key + "</td>");
            row.append("</tr>");
            table_body.append(row);
        }
    }


    class DebugInterface {
        constructor(enable) {
            this.update_motion_data_readout = function (data) { };

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
    }
    debug_interface = new DebugInterface(DEBUG);

});