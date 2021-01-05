<template>
  <v-app app>
    <v-app-bar app :clipped-left="dashboardMode">
      <v-app-bar-nav-icon
        v-if="dashboardMode"
        @click="toggleLeftNavDrawerState()"
      >
        <span v-if="!this.$vuetify.breakpoint.mobile">
          <v-icon
            v-html="
              leftNavDrawerIsMini ? 'mdi-chevron-right' : 'mdi-chevron-left'
            "
          />
        </span>
      </v-app-bar-nav-icon>

      <v-app-bar-nav-icon
        v-if="!dashboardMode && this.$vuetify.breakpoint.mobile"
        @click="leftNavDrawerIsVisible = !leftNavDrawerIsVisible"
      />

      <v-toolbar-title
        @click="$router.currentRoute.path !== '/' ? $router.push('/') : {}"
        class="font-weight-black"
      >
        {{ appName }}
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <slot name="app-bar"></slot>

      <v-app-bar-nav-icon
        v-if="isLoggedIn"
        @click="rightNavDrawerVisible = !rightNavDrawerVisible"
      >
        <v-btn icon small>
          <v-icon>mdi-account-cog</v-icon>
        </v-btn>
      </v-app-bar-nav-icon>
    </v-app-bar>

    <!-- left navigation drawer -->
    <v-navigation-drawer
      app
      left
      :clipped="dashboardMode"
      :mini-variant="dashboardMode && leftNavDrawerIsMini"
      v-model="leftNavDrawerIsVisible"
      ref="leftNavDrawerRef"
    >
      <template v-slot:prepend>
        <v-toolbar
          elevation="0"
          color="transparent"
          v-if="$vuetify.breakpoint.mobile"
        >
          <v-btn icon @click="toggleLeftNavDrawerState()">
            <v-icon>mdi-close</v-icon>
          </v-btn>

          <v-toolbar-title
            v-text="appName"
            class="font-weight-black"
          ></v-toolbar-title>

          <v-spacer></v-spacer>
        </v-toolbar>
      </template>

      <v-divider v-if="$vuetify.breakpoint.mobile"></v-divider>

      <slot name="left-nav-drawer"></slot>
    </v-navigation-drawer>

    <!-- right navigation drawer -->
    <v-navigation-drawer
      app
      right
      fixed
      temporary
      v-model="rightNavDrawerVisible"
      ref="rightNavigationDrawer"
    >
      <template v-slot:prepend>
        <v-toolbar elevation="0" color="transparent">
          <v-icon large right>mdi-account-cog</v-icon>

          <v-spacer></v-spacer>

          <v-btn icon @click="rightNavDrawerVisible = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
      </template>

      <v-divider></v-divider>

      <v-list subheader>
        <v-subheader> Account </v-subheader>
        <v-list-item to="/account/profile/edit">
          <v-list-item-content>
            <v-list-item-title>Edit Profile</v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-icon>mdi-account-edit</v-icon>
          </v-list-item-action>
        </v-list-item>

        <v-list-item to="/account/profile/password">
          <v-list-item-content>
            <v-list-item-title>Change Password</v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-icon>mdi-key</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>

      <v-list subheader>
        <v-subheader> Settings </v-subheader>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Theme</v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-switch v-model="$vuetify.theme.dark">
              <template v-slot:label>
                <v-icon v-if="$vuetify.theme.dark" class="ml-2">
                  mdi-weather-night
                </v-icon>
                <v-icon v-if="!$vuetify.theme.dark" class="ml-2">
                  mdi-weather-sunny
                </v-icon>
              </template>
            </v-switch>
          </v-list-item-action>
        </v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <v-btn block color="error" @click="logout()"> Logout </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-main app>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
      <notifications-manager></notifications-manager>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue, { VueConstructor } from "vue";
import { store } from "@/store";
import { appName } from "@/env";
import { readIsLoggedIn } from "@/store/main/getters";
import VNavigationDrawer from "../../node_modules/vuetify/types";
import { dispatchUserLogOut } from "@/store/main/actions";
import NotificationsManager from "./NotificationsManager.vue";
import debounce from "debounce";

interface Types {
  $refs: {
    leftNavDrawerRef: VNavigationDrawer & {
      isActive: boolean;
      miniVariant: boolean;
    };
  };
  leftNavDrawerIsVisible: boolean;
  leftNavDrawerIsMini: boolean;
}

export default (Vue as VueConstructor<Vue & Types>).extend({
  components: { NotificationsManager },
  props: {
    dashboardMode: {
      type: Boolean,
      default: false,
    },
  },
  data: () => {
    return {
      appName: appName as string,
      rightNavDrawerVisible: false as boolean,
      leftNavDrawerIsVisible: false as boolean,
      leftNavDrawerIsMini: false as boolean,
    };
  },
  computed: {
    isLoggedIn(): boolean | null {
      return readIsLoggedIn(store);
    },
  },
  methods: {
    async logout() {
      await dispatchUserLogOut(this.$store);
      this.$vuetify.theme.dark = false;
    },
    toggleLeftNavDrawerState() {
      if (this.$vuetify.breakpoint.mobile) {
        this.leftNavDrawerIsVisible = !this.$refs.leftNavDrawerRef.isActive;
        this.leftNavDrawerIsMini = false;
      } else {
        this.leftNavDrawerIsVisible = true;
        this.leftNavDrawerIsMini = !this.$refs.leftNavDrawerRef.miniVariant;
      }
    },
    initDrawerState() {
      if (this.$vuetify.breakpoint.mobile) {
        this.leftNavDrawerIsVisible = false;
      } else if (this.dashboardMode) {
        this.leftNavDrawerIsVisible = true;
      }
    },
    onResized() {
      if (!this.dashboardMode && !this.$vuetify.breakpoint.mobile) {
        this.leftNavDrawerIsVisible = false;
      } else if (this.dashboardMode && !this.$vuetify.breakpoint.mobile) {
        this.leftNavDrawerIsVisible = true;
      }
    },
  },
  mounted() {
    this.initDrawerState();
    window.onresize = debounce(this.onResized, 200);
  },
});
</script>
