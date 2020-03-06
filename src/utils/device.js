async function getOrientationPermissions() {
  return new Promise(resolve => {
    if (typeof DeviceOrientationEvent.requestPermission !== "function") {
      // handle regular non iOS 13+ devices
      resolve(true);
    }
    DeviceOrientationEvent.requestPermission()
      .then(permissionState => {
        if (permissionState === "granted") {
          resolve(true);
        } else {
          resolve(false);
        }
      })
      .catch(console.error);
  });
}

class MotionSender {
  constructor() {
    this.intervalometer_id = null;
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
      let dataBytes = new Float64Array(this.motionData.orientation);
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
    this.intervalometer_id = setInterval(this.sendData, 1000 / fps);
    this.isSending = true;
  }
  stop() {
    clearInterval(this.intervalometer_id);
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
