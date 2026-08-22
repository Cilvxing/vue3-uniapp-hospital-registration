"use strict";
const common_vendor = require("../../../common/vendor.js");
const _sfc_main = /* @__PURE__ */ common_vendor.defineComponent({
  __name: "prompt",
  emits: ["parentFunc"],
  setup(__props, { expose, emit }) {
    let show = common_vendor.ref(false);
    function onEnter() {
      console.log("\u8FDB\u5165\u4E2D\u89E6\u53D1");
    }
    function showCont() {
      show.value = true;
    }
    expose({ showCont });
    function openSetting() {
      show.value = false;
      common_vendor.index.openSetting({
        success: (res) => {
          if (res.authSetting["scope.userLocation"]) {
            console.log("00000");
            emit("parentFunc");
          }
        }
      });
    }
    return (_ctx, _cache) => {
      return {
        a: common_vendor.o(openSetting),
        b: common_vendor.o(($event) => common_vendor.isRef(show) ? show.value = false : show = false),
        c: common_vendor.unref(show),
        d: common_vendor.o(onEnter)
      };
    };
  }
});
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-004359ac"], ["__file", "D:/WeChatProject/Medical/src/pages/index/components/prompt.vue"]]);
wx.createComponent(Component);
