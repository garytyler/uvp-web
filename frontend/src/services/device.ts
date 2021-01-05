const getOrientationPermissions = async (): Promise<boolean> => {
  return new Promise((resolve) => {
    if (typeof DeviceOrientationEvent.requestPermission === "function") {
      DeviceOrientationEvent.requestPermission()
        .then((permissionState) => {
          if (permissionState === "granted") {
            resolve(true);
          } else {
            resolve(false);
          }
        })
        .catch(console.error);
    } else {
      // handle regular non iOS 13+ devices
      resolve(true);
    }
  });
};

class MotionSender {
  orientation: Float64Array = new Float64Array();
  isSending = false;
  intervalometerId: number | undefined;
  socket: WebSocket | undefined;
  constructor() {
    this.sendData = this.sendData.bind(this);
    this.handleOrientationEvent = this.handleOrientationEvent.bind(this);
  }
  start(socket: WebSocket, fps: number) {
    this.socket = socket;
    this.isSending = true;
    this.intervalometerId = window.setInterval(this.sendData, 1000 / fps);
    window.addEventListener("deviceorientation", this.handleOrientationEvent);
  }
  sendData() {
    if (this.socket && this.orientation) {
      this.socket.send(this.orientation);
    }
  }
  handleOrientationEvent(event: DeviceOrientationEvent) {
    this.orientation = new Float64Array([
      event.alpha || 0,
      event.beta || 0,
      event.gamma || 0,
    ]);
  }
  stop() {
    window.clearInterval(this.intervalometerId);
    window.removeEventListener(
      "deviceorientation",
      this.handleOrientationEvent
    );
    this.isSending = false;
  }
}

export default {
  motionSender: new MotionSender(),
  getOrientationPermissions: getOrientationPermissions,
};
