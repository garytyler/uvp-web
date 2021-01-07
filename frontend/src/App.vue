<template>
  <v-app>
    <div>
      <router-view />
    </div>
  </v-app>
</template>


<style>
/* Unset background-color change on app-bar buttons when active */
.v-app-bar .v-btn--active:before {
  background-color: unset;
}
.v-card__title {
  word-break: break-word !important;
}
</style>
