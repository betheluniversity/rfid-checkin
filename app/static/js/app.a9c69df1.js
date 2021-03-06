(function (t) {
  function e(e) {
    for (
      var n, r, o = e[0], l = e[1], a = e[2], d = 0, f = [];
      d < o.length;
      d++
    )
      (r = o[d]),
        Object.prototype.hasOwnProperty.call(c, r) && c[r] && f.push(c[r][0]),
        (c[r] = 0);
    for (n in l) Object.prototype.hasOwnProperty.call(l, n) && (t[n] = l[n]);
    u && u(e);
    while (f.length) f.shift()();
    return s.push.apply(s, a || []), i();
  }
  function i() {
    for (var t, e = 0; e < s.length; e++) {
      for (var i = s[e], n = !0, o = 1; o < i.length; o++) {
        var l = i[o];
        0 !== c[l] && (n = !1);
      }
      n && (s.splice(e--, 1), (t = r((r.s = i[0]))));
    }
    return t;
  }
  var n = {},
    c = { app: 0 },
    s = [];
  function r(e) {
    if (n[e]) return n[e].exports;
    var i = (n[e] = { i: e, l: !1, exports: {} });
    return t[e].call(i.exports, i, i.exports, r), (i.l = !0), i.exports;
  }
  (r.m = t),
    (r.c = n),
    (r.d = function (t, e, i) {
      r.o(t, e) || Object.defineProperty(t, e, { enumerable: !0, get: i });
    }),
    (r.r = function (t) {
      "undefined" !== typeof Symbol &&
        Symbol.toStringTag &&
        Object.defineProperty(t, Symbol.toStringTag, { value: "Module" }),
        Object.defineProperty(t, "__esModule", { value: !0 });
    }),
    (r.t = function (t, e) {
      if ((1 & e && (t = r(t)), 8 & e)) return t;
      if (4 & e && "object" === typeof t && t && t.__esModule) return t;
      var i = Object.create(null);
      if (
        (r.r(i),
        Object.defineProperty(i, "default", { enumerable: !0, value: t }),
        2 & e && "string" != typeof t)
      )
        for (var n in t)
          r.d(
            i,
            n,
            function (e) {
              return t[e];
            }.bind(null, n)
          );
      return i;
    }),
    (r.n = function (t) {
      var e =
        t && t.__esModule
          ? function () {
              return t["default"];
            }
          : function () {
              return t;
            };
      return r.d(e, "a", e), e;
    }),
    (r.o = function (t, e) {
      return Object.prototype.hasOwnProperty.call(t, e);
    }),
    (r.p = "/");
  var o = (window["webpackJsonp"] = window["webpackJsonp"] || []),
    l = o.push.bind(o);
  (o.push = e), (o = o.slice());
  for (var a = 0; a < o.length; a++) e(o[a]);
  var u = l;
  s.push([0, "chunk-vendors"]), i();
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
      s = [],
      r = (i("4de4"), i("5530")),
      o = function () {
        var t = this,
          e = t.$createElement,
          i = t._self._c || e;
        return i("div", [
          i("div", { staticClass: "row" }, [
            i(
              "button",
              {
                staticClass: "btn btn-link",
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
                staticClass: "btn btn-link",
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
                staticClass: "btn btn-link",
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
                return i("Checkin", { key: t.id, attrs: { checkin: t } });
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
            i("th", [t._v("Bethel ID")]),
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
          i("td", [t._v(t._s(t.checkin.bethel_id))]),
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
        props: ["checkin"],
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
        },
      },
      v = k,
      m = Object(h["a"])(v, o, l, !1, null, "1c6687d6", null),
      y = m.exports,
      _ = i("2f62"),
      C = {
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
      g = {
        name: "App",
        components: { CheckinList: y },
        methods: {
          setVisibility: function (t) {
            this.$store.dispatch("checkins/setVisibility", t);
          },
        },
        computed: Object(r["a"])(
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
          var t = this;
          this.$store.dispatch("checkins/loadCheckins"),
            (this.timer = setInterval(function () {
              t.$store.dispatch("checkins/loadCheckins");
            }, 3e3));
        },
        beforeDestroy: function () {
          clearInterval(this.timer);
        },
        data: function () {
          return { filters: C, timer: "" };
        },
      },
      w = g,
      O = Object(h["a"])(w, c, s, !1, null, null, null),
      V = O.exports,
      j = i("bfa9"),
      P = i("bc3a"),
      x = i.n(P),
      E = i("a7fe"),
      $ = i.n(E),
      I = i("b054"),
      S = i.n(I),
      A =
        (i("7db0"),
        i("c975"),
        i("fb6a"),
        i("a434"),
        i("d3b7"),
        i("ac1f"),
        i("3ca3"),
        i("1276"),
        i("ddb0"),
        i("2b3d"),
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
      U = {
        setVisibility: function (t, e) {
          t.commit("setVisibility", e);
        },
        loadCheckins: function (t) {
          var e = new URL(location.href),
            i = e.href.split("/").slice(-1)[0];
          x.a
            .get("/get-checkins/" + i)
            .then(function (e) {
              t.commit("saveCheckins", e.data.checkins);
            })
            .catch(function (t) {
              throw new Error("API ".concat(t));
            });
        },
        updateCheckin: function (t, e) {
          x.a
            .post("/update-checkin", {
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
      M = { namespaced: !0, state: A, getters: L, actions: U, mutations: D },
      R = new j["a"]({ key: "checkins", storage: window.localStorage });
    n["a"].use(_["a"], $.a, x.a),
      (window.axios = x.a),
      (x.a.defaults.baseURL = Object({
        NODE_ENV: "production",
        BASE_URL: "/",
      }).VUE_APP_API_URL);
    var N = !1,
      T = N ? [S()(), R.plugin] : [R.plugin],
      B = new _["a"].Store({ plugins: T, modules: { checkins: M }, strict: N });
    (n["a"].config.productionTip = !1),
      new n["a"]({
        el: "#app",
        store: B,
        render: function (t) {
          return t(V);
        },
      });
  },
});
//# sourceMappingURL=app.a9c69df1.js.map
