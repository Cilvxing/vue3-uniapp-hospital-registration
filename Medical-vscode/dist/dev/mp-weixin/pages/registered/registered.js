"use strict";
const common_vendor = require("../../common/vendor.js");
const public_request = require("../../public/request.js");
if (!Math) {
  skIndex();
}
const skIndex = () => "../../Skeleton/SK-registered.js";
const _sfc_main = /* @__PURE__ */ common_vendor.defineComponent({
  __name: "registered",
  setup(__props) {
    let department_data = common_vendor.ref([]);
    let skeLeton = common_vendor.ref(true);
    common_vendor.onMounted(async () => {
      const res = await public_request.RequestApi.DeparTment();
      console.log("res.data[0]._id", res);
      department_data.value = res.data;
      changeList(0, res.data[0]._id);
    });
    let addColor = common_vendor.ref(0);
    let reglist_data = common_vendor.ref([]);
    async function changeList(index, id) {
      console.log("idid", id);
      addColor.value = index;
      common_vendor.index.request({
        url: "http://localhost:3000/reglist",
        data: {
          _id: id
        },
        success: (res2) => {
          console.log("\u7B5B\u9009\u5B50\u79D1\u5BA4", res2);
          reglist_data.value = res2.data;
        }
      });
      skeLeton.value = false;
    }
    function jumpRoute(id) {
      common_vendor.index.navigateTo({
        url: "/pages/doctor/index?id=" + id
      });
    }
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(common_vendor.unref(department_data), (item, index, i0) => {
          return {
            a: common_vendor.t(item.dep_ment),
            b: index,
            c: common_vendor.n(common_vendor.unref(addColor) == index ? "addcolor" : ""),
            d: common_vendor.o(($event) => changeList(index, item._id), index)
          };
        }),
        b: common_vendor.f(common_vendor.unref(reglist_data), (item, index, i0) => {
          return {
            a: common_vendor.f(item.dep_ment_list, (item_a, index_a, i1) => {
              return {
                a: common_vendor.t(item_a.dep_name),
                b: index_a,
                c: common_vendor.o(($event) => jumpRoute(item_a.dep_id), index_a)
              };
            }),
            b: index
          };
        }),
        c: common_vendor.unref(skeLeton)
      }, common_vendor.unref(skeLeton) ? {} : {});
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-3d6ffcdb"], ["__file", "D:/WeChatProject/Medical/src/pages/registered/registered.vue"]]);
wx.createPage(MiniProgramPage);
