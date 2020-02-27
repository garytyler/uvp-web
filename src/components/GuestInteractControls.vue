<template>
  <v-row>
    <!-- <v-dialog
      persistent
      no-click-animation
      class="elevation-12"
      v-model="dialog"
    >
      <v-card>
        {{ status }}
        <v-card-actions> -->
    <v-container fluid>
      {{ status }}
      <v-row justify="center">
        <v-col cols="10">
          <v-row rows="3">
            <v-btn
              block
              align="stretch"
              style="height: 100px;"
              :color="isSending ? 'accent' : 'primary'"
              @click="isSending ? stop() : start()"
            >
              <span class="headline">
                {{ isSending ? "Pause" : "Start" }}
              </span>
            </v-btn>
          </v-row>
        </v-col>
      </v-row>

      <v-row justify="center" class="mt-12">
        <v-col cols="6">
          <v-row>
            <v-btn
              block
              align="stretch"
              color="accent darken-4"
              @click="stop()"
            >
              Exit
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
    <!-- </v-card-actions>
      </v-card>
    </v-dialog> -->
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
import Vue from "vue";
import device from "@/utils/device.js";

export default {
  data() {
    return {
      isSending: false,
      dialog: true,
      status: "NO STATUS"
    };
  },
  computed: {
    ...mapGetters("guest_app", [
      "featurePresenterChannel",
      "sessionGuestId",
      "featureGuests"
    ])
  },

  methods: {
    start() {
      if (typeof DeviceOrientationEvent.requestPermission === "function") {
        DeviceOrientationEvent.requestPermission()
          .then(permissionState => {
            this.status = "permissionState:" + permissionState;
            if (permissionState === "granted") {
              window.addEventListener("deviceorientation", () => {});
            }
          })
          .catch((this.status = "granted:" + console.error));
      } else {
        // handle regular non iOS 13+ devices
      }

      // // console.log(DeviceOrientationEvent.requestPermission);
      // // console.log(DeviceOrientationEvent.permission);
      // this.status =
      //   " permission:" +
      //   DeviceOrientationEvent.permission +
      //   " requestPermission:" +
      //   DeviceOrientationEvent.requestPermission;
      // if (typeof DeviceOrientationEvent.requestPermission === "function") {
      //   // handle iOS 13+ devices
      //   // console.log(DeviceOrientationEvent.permission);
      //   // if (DeviceOrientationEvent.permission === "granted") {
      //   //   console.log("not granted");
      //   //   this.startSendingDeviceOrientation();
      //   // } else {
      //   this.status =
      //     "DeviceOrientationEvent.requestPermission:" +
      //     DeviceOrientationEvent.requestPermission;
      //   DeviceOrientationEvent.requestPermission()
      //     .then(permissionState => {
      //       this.status = "permissionState:" + this.status;
      //       if (permissionState === "granted") {
      //         this.startSendingDeviceOrientation();
      //       }
      //     })
      //     .catch((this.status = console.error));
      // } else {
      //   // handle regular non iOS 13+ devices
      //   this.startSendingDeviceOrientation();
      // }
    },
    stop() {
      this.stopSendingDeviceOrientation();
    },
    startSendingDeviceOrientation() {
      device.orientation.start(Vue.prototype.$socket, 30, true);
      this.isSending = device.orientation.isSending;
    },
    stopSendingDeviceOrientation() {
      device.orientation.stop();
      this.isSending = device.orientation.isSending;
    }
  }
};
</script>

<style scoped>
.v-btn {
  width: 100%;
}
</style>
