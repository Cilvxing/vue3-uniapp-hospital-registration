"use strict";
const common_vendor = require("../../common/vendor.js");
const public_request = require("../../public/request.js");
if (!Math) {
  skIndex();
}
const skIndex = () => "../../Skeleton/SK-doctor.js";
const _sfc_main = /* @__PURE__ */ common_vendor.defineComponent({
  __name: "index",
  setup(__props) {
    common_vendor.ref("\u5F53\u65E5\u6CA1\u6709\u533B\u751F\u6392\u73ED");
    let doctor_time = common_vendor.ref([]);
    let doctor_list = common_vendor.ref([]);
    let dep_id = common_vendor.ref("");
    let skeLeton = common_vendor.ref(true);
    common_vendor.onLoad(async (event) => {
      const { id } = event;
      dep_id.value = id;
      await Promise.all([
        common_vendor.index.request({
          url: "http://localhost:3000/timesele",
          data: {
            dep_id: id
          },
          success: (res) => {
            console.log("\u7B5B\u9009\u65E5\u671F", res);
            console.log(id);
            doctor_time.value = res.data;
          }
        }),
        common_vendor.index.request({
          url: "http://localhost:3000/alldlist",
          data: {
            dep_id: id
          },
          success: (res) => {
            console.log("\u7B5B\u9009\u5404\u5B50\u79D1\u5BA4\u533B\u751F", res);
            console.log(id);
            doctor_list.value = res.data;
          }
        })
      ]);
      console.log("doctor_time.value", doctor_time.value);
      console.log("doctor_list.value", doctor_list.value);
      skeLeton.value = false;
    });
    let selectIndex = common_vendor.ref(-1);
    async function allDoctor() {
      selectIndex.value = -1;
      const res = await public_request.RequestApi.AlldList({ dep_id: dep_id.value });
      console.log("\u8BF7\u6C42\u5168\u90E8\u533B\u751F\u5217\u8868", res);
      doctor_list.value = res.data.data;
    }
    async function selectDoctor(index, dep_id2, date) {
      selectIndex.value = index;
      common_vendor.index.request({
        url: "http://localhost:3000/everydlist",
        data: {
          dep_id: dep_id2,
          date
        },
        success: (res) => {
          console.log("\u6839\u636E\u65E5\u671F\u7B5B\u9009\u533B\u751F", res);
          console.log(dep_id2);
          console.log(date);
          doctor_list.value = res.data;
          console.log("doctor_list", doctor_list);
        }
      });
    }
    function jumpRoute(id) {
      console.log("id\u5177\u4F53\u662F\u4EC0\u4E48ID", id);
      common_vendor.index.navigateTo({
        url: "/pages/doctor/doctor-Homepage?id=" + id
      });
    }
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.n(common_vendor.unref(selectIndex) == -1 ? "changeColor" : ""),
        b: common_vendor.o(allDoctor),
        c: common_vendor.f(common_vendor.unref(doctor_time), (item, index, i0) => {
          return {
            a: common_vendor.t(item.date),
            b: common_vendor.t(item.week),
            c: common_vendor.n(index == common_vendor.unref(selectIndex) ? "changeColor" : ""),
            d: common_vendor.t(item.nu_source == 1 ? "\u53EF\u7EA6" : "\u65E0\u53F7"),
            e: index,
            f: common_vendor.o(($event) => selectDoctor(index, item.dep_id, item.date), index)
          };
        }),
        d: common_vendor.f(common_vendor.unref(doctor_list), (item, index, i0) => {
          return {
            a: item.avatar,
            b: common_vendor.t(item.name),
            c: common_vendor.t(item.post),
            d: common_vendor.t(item.good_at),
            e: index,
            f: common_vendor.o(($event) => jumpRoute(item._id), index)
          };
        }),
        e: common_vendor.unref(skeLeton)
      }, common_vendor.unref(skeLeton) ? {} : {});
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__file", "D:/WeChatProject/Medical/src/pages/doctor/index.vue"]]);
wx.createPage(MiniProgramPage);
