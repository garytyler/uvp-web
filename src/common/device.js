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
    if (!this.socket || !this.motionData.orientation) {
      // console.log("No orientation data available.");
    } else {
      let dataBytes = new Float64Array(this.motionData.orientation);
      if (dataBytes) {
        this.socket.send(dataBytes);
      } else {
        // console.log(`No data found: ${dataBytes}`);
      }
    }
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
  orientation: new MotionSender()
};
