import Vue from "vue";
import Vuex from "vuex";
import VuexPersist from "vuex-persist";
import axios from "axios";
import VueAxios from "vue-axios";
import createLogger from "vuex/dist/logger";
import checkins from "./modules/checkins";

const vuexPersist = new VuexPersist({
  key: "checkins",
  storage: window.localStorage,
});

Vue.use(Vuex, VueAxios, axios);

window.axios = axios;
// not sure I need to set this URL since its the same domain
axios.defaults.baseURL = process.env.VUE_APP_API_URL;

const debug = process.env.NODE_ENV !== "production";
var plugins = debug
  ? [createLogger(), vuexPersist.plugin]
  : [vuexPersist.plugin];

export default new Vuex.Store({
  plugins: plugins,
  modules: {
    checkins: checkins,
  },
  strict: debug,
});
