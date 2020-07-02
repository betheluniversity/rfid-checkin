import Vue from "vue";
import App from "./App.vue";
import store from './store'
// import vuetify from './plugins/vuetify';
// import store from "./store";

Vue.config.productionTip = false;

new Vue({
  el: "#app",
  store,

  // vuetify,
  // store,
  render: (h) => h(App)
});
