$(document).ready(function () {

    // Predefined globals
    // if (DEBUG == null) {
    //     DEBUG = false;
    // }
    var DEBUG = true;
    var guest_socket = null;
    var motion_socket = null;
    var motion_sender = null;
    var motion_sender_intervalometer_id = null;

    guest_data = JSON.parse(document.getElementById("guest_json").textContent);
    $("#guest_guest_name").append("<b>Name: </b>" + guest_data.guest_name);

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


    // var gyronormMotionEventCaller = {
    //     gn: new GyroNorm(),
    //     init: function (handler) {
    //         this.handler = handler;
    //         this.gn.init({});
    //         return this; // Used by factory
    //     },
    //     start: function (handler) {
    //         this.gn.start(function (data) {
    //             handler(data.do);
    //         });
    //     },
    //     stop: function () {
    //         this.gn.stop();
    //     },
    // };

    // function MotionCollector() {
    //     var gn = new GyroNorm();

    //     var latest = {
    //         alpha: 0,
    //         beta: 0,
    //         gamma: 0
    //     };

    //     var handle_motion_event = function (event) {
    //         latest = event;
    //     };

    //     this.register = function () {

    //         // window.ondeviceorientation = handle_motion_event;
    //         gn.start(handle_motion_event);
    //     };

    //     this.unregister = function () {
    //         // window.ondeviceorientation = null;
    //         gn.stop();
    //     };

    //     this.get_state = function () {
    //         // console.log(latest.alpha, latest.beta, latest.gamma);
    //         return [latest.alpha, latest.beta, latest.gamma];
    //     };

    // }
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
                motion_bytes = new Float64Array(motion_state);
                socket.send(motion_bytes);
                debug_interface.update_motion_data_readout(motion_state);
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
        data = JSON.parse(event.data);

        if (data.current_guests_state[0].session_key === guest_data.session_key) {
            console.log('Enabling interact mode', data.current_guests_state[0]);
            enableInteractMode(data.current_guests_state);
        } else {
            console.log('Enabling waiting mode', data.current_guests_state);
            enableWaitingMode(data.current_guests_state);
        }
    };
    guest_socket.onclose = function (event) {
        console.log('GUEST_ON_CLOSE');
        console.log('guest_socket.onclose', event);
        //TODO Pass an exit code for messaging
        shutdown_and_exit();
    };
    guest_socket.onerror = function (event) {
        console.log('guest_socket.onerror', event);
    };


    function enableWaitingMode(current_guests_state) {
        $("#interact_ui").hide();
        $("#waiting_ui").show();

        $("#exit_waiting_button").click(function (e) {
            request_force_remove_guest();
        });

        populateWaitingTable(current_guests_state);
    }


    function enableInteractMode(current_guests_state) {
        $("#waiting_ui").hide();

        motion_socket = new WebSocket(ws_scheme + window.location.host + "/ws/motion/");
        motion_socket.onopen = function (event) {
            console.log('motion_socket.onopen:', event);
        };
        motion_socket.onmessage = function (event) {
            data = JSON.parse(event.data);
            console.log('motion_socket.onmessage:', data);

            if (data.method == "permission_granted") {
                fps = data.args.fps;
                media_title = data.args.media_title;
                allowed_time = data.args.allowed_time;

                motion_sender = new MotionSender(motion_socket);
                console.log("PERMISSION GRANTED");
                $("#start_button").click(function (e) {
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

                $("#stop_button").click(function (e) {
                    $(this).hide();
                    $("#start_button").show();

                    motion_sender.stop();
                });

                $("#exit_interact_button").click(function (e) {
                    console.log("EXIT_INTERACT_BUTTON");
                    // request_force_remove_guest();
                });

                $("#message_display").hide();
                $("#interact_ui").show();

                $("#debug_send_current_state").click(function () {
                    console.log('CLICKED');
                    motion_sender.send_latest();
                });

            } else if (data.method == "permission_denied") {
                $("#interact_ui").hide();
                $("#message_display").append("<h3>" + data.args.reason + "</h3>");
            }
        };
        motion_socket.onerror = function (event) {
            console.log('motion_socket.onerror', event);
        };
        motion_socket.onclose = function (event) {
            console.log("ONCLOSE");
            console.log('motion_socket.onclose', event);
            shutdown_and_exit();
        };

    }


    function request_force_remove_guest() {
        console.log("FORCE_REMOVE_GUEST");
        guest_socket.send(JSON.stringify({
            "method": "force_remove_guest"
        }));
    }


    function shutdown_and_exit() {

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


    function populateWaitingTable(current_guests_state) {
        table_body = $("#current_guests_table_body");
        table_body.empty();
        for (var index in current_guests_state) {
            var item = current_guests_state[index];
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