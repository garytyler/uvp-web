async function getOrientationPermissions() {
  return new Promise(resolve => {
    if (typeof DeviceOrientationEvent.requestPermission === "function") {
      DeviceOrientationEvent.requestPermission()
        .then(permissionState => {
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
}

class MotionSender {
  constructor() {
    this.intervalometerId = null;
    this.isSending = false;
    this.socket = null;
    this.motionData = {
      orientation: null
    };
    this.sendData = this.sendData.bind(this);
    this.handleOrientationEvent = this.handleOrientationEvent.bind(this);
  }
  sendData() {
    if (this.socket || !this.motionData.orientation) {
      const dataBytes = new Float64Array(this.motionData.orientation);
      if (dataBytes) {
        this.socket.send(dataBytes);
      }
    }
    // TODO: Handle an else case here
  }
  handleOrientationEvent(e) {
    this.motionData.orientation = [e.alpha, e.beta, e.gamma];
  }
  start(socket, fps) {
    this.socket = socket;
    window.addEventListener("deviceorientation", this.handleOrientationEvent);
    this.intervalometerId = setInterval(this.sendData, 1000 / fps);
    this.isSending = true;
  }
  stop() {
    clearInterval(this.intervalometerId);
    window.removeEventListener(
      "deviceorientation",
      this.handleOrientationEvent
    );

    this.isSending = false;
  }
}

export default {
  motionSender: new MotionSender(),
  getOrientationPermissions: getOrientationPermissions
};
