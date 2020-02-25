<template>
  <v-row>
    <v-dialog
      persistent
      no-click-animation
      class="elevation-12"
      v-model="dialog"
    >
      <v-card>
        <v-card-actions>
          <v-container fluid>
            <v-row justify="center">
              <v-col cols="10">
                <v-row rows="3">
                  <v-btn
                    block
                    align="stretch"
                    style="height: 100px;"
                    :color="isSending ? 'accent' : 'primary'"
                    @click="isSending ? stopSending() : startSending()"
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
                    @click="stopSending()"
                  >
                    Exit
                  </v-btn>
                </v-row>
              </v-col>
            </v-row>
          </v-container>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
      dialog: true
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
    startSending() {
      console.log(Vue.prototype.$socket);
      device.orientation.start(Vue.prototype.$socket, 30, true);
      this.isSending = device.orientation.isSending;
    },
    stopSending() {
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
