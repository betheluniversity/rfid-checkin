(function (t) {
  function e(e) {
    for (
      var n, s, o = e[0], l = e[1], a = e[2], d = 0, f = [];
      d < o.length;
      d++
    )
      (s = o[d]),
        Object.prototype.hasOwnProperty.call(c, s) && c[s] && f.push(c[s][0]),
        (c[s] = 0);
    for (n in l) Object.prototype.hasOwnProperty.call(l, n) && (t[n] = l[n]);
    u && u(e);
    while (f.length) f.shift()();
    return r.push.apply(r, a || []), i();
  }
  function i() {
    for (var t, e = 0; e < r.length; e++) {
      for (var i = r[e], n = !0, o = 1; o < i.length; o++) {
        var l = i[o];
        0 !== c[l] && (n = !1);
      }
      n && (r.splice(e--, 1), (t = s((s.s = i[0]))));
    }
    return t;
  }
  var n = {},
    c = { app: 0 },
    r = [];
  function s(e) {
    if (n[e]) return n[e].exports;
    var i = (n[e] = { i: e, l: !1, exports: {} });
    return t[e].call(i.exports, i, i.exports, s), (i.l = !0), i.exports;
  }
  (s.m = t),
    (s.c = n),
    (s.d = function (t, e, i) {
      s.o(t, e) || Object.defineProperty(t, e, { enumerable: !0, get: i });
    }),
    (s.r = function (t) {
      "undefined" !== typeof Symbol &&
        Symbol.toStringTag &&
        Object.defineProperty(t, Symbol.toStringTag, { value: "Module" }),
        Object.defineProperty(t, "__esModule", { value: !0 });
    }),
    (s.t = function (t, e) {
      if ((1 & e && (t = s(t)), 8 & e)) return t;
      if (4 & e && "object" === typeof t && t && t.__esModule) return t;
      var i = Object.create(null);
      if (
        (s.r(i),
        Object.defineProperty(i, "default", { enumerable: !0, value: t }),
        2 & e && "string" != typeof t)
      )
        for (var n in t)
          s.d(
            i,
            n,
            function (e) {
              return t[e];
            }.bind(null, n)
          );
      return i;
    }),
    (s.n = function (t) {
      var e =
        t && t.__esModule
          ? function () {
              return t["default"];
            }
          : function () {
              return t;
            };
      return s.d(e, "a", e), e;
    }),
    (s.o = function (t, e) {
      return Object.prototype.hasOwnProperty.call(t, e);
    }),
    (s.p = "/");
  var o = (window["webpackJsonp"] = window["webpackJsonp"] || []),
    l = o.push.bind(o);
  (o.push = e), (o = o.slice());
  for (var a = 0; a < o.length; a++) e(o[a]);
  var u = l;
  r.push([0, "chunk-vendors"]), i();
})({
  0: function (t, e, i) {
    t.exports = i("56d7");
  },
  "56d7": function (t, e, i) {
    "use strict";
    i.r(e);
    i("e260"), i("e6cf"), i("cca6"), i("a79d");
    var n = i("2b0e"),
      c = function () {
        var t = this,
          e = t.$createElement,
          i = t._self._c || e;
        return i(
          "div",
          [
            i("CheckinList", {
              attrs: {
                checkins: t.checkins,
                filters: t.filters,
                visibility: t.visibility,
              },
              on: { "set-visibility": t.setVisibility },
            }),
          ],
          1
        );
      },
      r = [],
      s = (i("4de4"), i("5530")),
      o = function () {
        var t = this,
          e = t.$createElement,
          i = t._self._c || e;
        return i("div", [
          i("div", [
            i(
              "button",
              {
                class: { selected: "all" == t.getVisibility },
                on: {
                  click: function (e) {
                    return t.setVisibility("all");
                  },
                },
              },
              [t._v(" All ")]
            ),
            i(
              "button",
              {
                class: { selected: "completed" == t.getVisibility },
                on: {
                  click: function (e) {
                    return t.setVisibility("completed");
                  },
                },
              },
              [t._v(" Completed ")]
            ),
            i(
              "button",
              {
                class: { selected: "not_completed" == t.getVisibility },
                on: {
                  click: function (e) {
                    return t.setVisibility("not_completed");
                  },
                },
              },
              [t._v(" Not Completed ")]
            ),
          ]),
          i(
            "table",
            { staticClass: "table" },
            [
              t._m(0),
              t._l(t.filteredCheckins, function (t) {
                return i("Checkin", {
                  key: t.id,
                  attrs: { checkin: t, test: t.scan_datetime },
                });
              }),
            ],
            2
          ),
        ]);
      },
      l = [
        function () {
          var t = this,
            e = t.$createElement,
            i = t._self._c || e;
          return i("thead", [
            i("th", [t._v("ID")]),
            i("th", [t._v("Completed")]),
            i("th", [t._v("Card ID")]),
            i("th", [t._v("Datetime")]),
          ]);
        },
      ],
      a = function () {
        var t = this,
          e = t.$createElement,
          i = t._self._c || e;
        return i("tr", [
          i("td", [t._v(t._s(t.checkin.id))]),
          i("td", [t._v(t._s(t.checkin.completed))]),
          i("td", [t._v(t._s(t.checkin.card_id))]),
          i("td", [t._v(t._s(t.checkin.scan_datetime))]),
          i("td", [
            i(
              "button",
              {
                staticClass: "btn btn-secondary",
                on: {
                  click: function (e) {
                    return t.completeCheckin(t.checkin);
                  },
                },
              },
              [t._v(" complete ")]
            ),
          ]),
        ]);
      },
      u = [],
      d = {
        props: ["test", "checkin"],
        data: function () {
          return { scan_datetime: "" };
        },
        methods: {
          completeCheckin: function (t) {
            var e = !t.complete,
              i = t.id;
            this.$store.dispatch("checkins/updateCheckin", {
              id: i,
              completed: e,
            });
          },
        },
        created: function () {},
      },
      f = d,
      h = i("2877"),
      p = Object(h["a"])(f, a, u, !1, null, null, null),
      b = p.exports,
      k = {
        name: "CheckinList",
        components: { Checkin: b },
        props: ["checkins", "filters", "visibility"],
        methods: {
          setVisibility: function (t) {
            this.$emit("set-visibility", t);
          },
        },
        computed: {
          filteredCheckins: function () {
            return this.filters[this.visibility](this.checkins);
          },
          getVisibility: function () {
            return this.visibility;
          },
          remaining: function () {
            return this.filters.active(this.checkins).length;
          },
        },
      },
      m = k,
      v = Object(h["a"])(m, o, l, !1, null, "2a455006", null),
      y = v.exports,
      _ = i("2f62"),
      g = {
        all: function (t) {
          return t;
        },
        completed: function (t) {
          return t.filter(function (t) {
            return 1 == t.completed;
          });
        },
        not_completed: function (t) {
          return t.filter(function (t) {
            return 0 == t.completed;
          });
        },
      },
      C = {
        name: "App",
        components: { CheckinList: y },
        methods: {
          setVisibility: function (t) {
            this.$store.dispatch("checkins/setVisibility", t);
          },
        },
        computed: Object(s["a"])(
          {},
          Object(_["b"])({
            visibility: function (t) {
              return t.checkins.visibility;
            },
            checkins: function (t) {
              return t.checkins.checkins;
            },
          })
        ),
        created: function () {
          this.$store.dispatch("checkins/loadCheckins");
        },
        data: function () {
          return { filters: g };
        },
      },
      w = C,
      O = Object(h["a"])(w, c, r, !1, null, null, null),
      V = O.exports,
      j = i("bfa9"),
      P = i("bc3a"),
      x = i.n(P),
      E = i("a7fe"),
      S = i.n(E),
      $ = i("b054"),
      A = i.n($),
      I =
        (i("7db0"),
        i("c975"),
        i("a434"),
        function () {
          return { visibility: "all", checkins: [] };
        }),
      L = {},
      D = {
        setVisibility: function (t, e) {
          t.visibility = e;
        },
        saveCheckins: function (t, e) {
          t.checkins = e;
        },
        updateCheckin: function (t, e) {
          var i = t.checkins.find(function (t) {
              return t.id === e.id;
            }),
            n = t.checkins.indexOf(i);
          t.checkins.splice(n, 1, e);
        },
      },
      M = {
        setVisibility: function (t, e) {
          t.commit("setVisibility", e);
        },
        loadCheckins: function (t) {
          var e = 121;
          x.a
            .get("http://127.0.0.1:5000/get-checkins/" + e)
            .then(function (e) {
              t.commit("saveCheckins", e.data.checkins);
            })
            .catch(function (t) {
              throw new Error("API ".concat(t));
            });
        },
        updateCheckin: function (t, e) {
          x.a
            .post("http://127.0.0.1:5000/update-checkin", {
              id: parseInt(e.id),
              completed: e.completed,
            })
            .then(function (e) {
              t.commit("updateCheckin", e.data);
            })
            .catch(function (t) {
              throw new Error("API ".concat(t));
            });
        },
      },
      U = { namespaced: !0, state: I, getters: L, actions: M, mutations: D },
      N = new j["a"]({ key: "checkins", storage: window.localStorage });
    n["a"].use(_["a"], S.a, x.a),
      (window.axios = x.a),
      (x.a.defaults.baseURL = Object({
        NODE_ENV: "production",
        BASE_URL: "/",
      }).VUE_APP_API_URL);
    var R = !1,
      T = R ? [A()(), N.plugin] : [N.plugin],
      J = new _["a"].Store({ plugins: T, modules: { checkins: U }, strict: R });
    (n["a"].config.productionTip = !1),
      new n["a"]({
        el: "#app",
        store: J,
        render: function (t) {
          return t(V);
        },
      });
  },
});
//# sourceMappingURL=app.845e416b.js.map
