"use strict";
const common_vendor = require("../common/vendor.js");
const _sfc_main = /* @__PURE__ */ common_vendor.defineComponent({
  __name: "SK-doctor",
  setup(__props) {
    let TOP = common_vendor.ref(["", "", "", "", ""]);
    return (_ctx, _cache) => {
      return {
        a: common_vendor.f(common_vendor.unref(TOP), (item, k0, i0) => {
          return {
            a: item
          };
        }),
        b: common_vendor.f(common_vendor.unref(TOP), (item, k0, i0) => {
          return {
            a: item
          };
        })
      };
    };
  }
});
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-1b0c1dab"], ["__file", "D:/WeChatProject/Medical/src/Skeleton/SK-doctor.vue"]]);
wx.createComponent(Component);
