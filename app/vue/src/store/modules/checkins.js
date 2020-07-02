import axios from "axios";

const state = () => ({
  visibility: "all",
  checkins: [],
});

const getters = {
  // Here we will create a getter
};

const mutations = {
  setVisibility(state, visibility) {
    state.visibility = visibility;
  },

  saveCheckins(state, checkins) {
    state.checkins = checkins;
  },

  updateCheckin(state, checkin) {
    var oldCheckin = state.checkins.find(function (element) {
      return element.id === checkin.id;
    });
    var index = state.checkins.indexOf(oldCheckin);
    // state.todos[index] = todo;
    state.checkins.splice(index, 1, checkin);
  },
};

const actions = {
  setVisibility(context, visibility) {
    context.commit("setVisibility", visibility);
  },

  // loadCheckins(context, session) {
  loadCheckins(context) {
    var u = new URL(location.href);
    var session = u.href.split("/").slice(-1)[0];
    axios
      .get("/get-checkins/" + session)
      .then((result) => {
        context.commit("saveCheckins", result.data.checkins);
      })
      .catch((error) => {
        throw new Error(`API ${error}`);
      });
  },

  updateCheckin(context, checkin) {
    axios
      .post("/update-checkin", {
        id: parseInt(checkin.id),
        completed: checkin.completed,
      })
      .then((result) => {
        // todo: less lazy way
        // dispatch("loadItems");
        context.commit("updateCheckin", result.data);
      })
      .catch((error) => {
        throw new Error(`API ${error}`);
      });
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
