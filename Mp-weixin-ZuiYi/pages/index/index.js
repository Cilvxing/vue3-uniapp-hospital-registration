"use strict";
const common_vendor = require("../../common/vendor.js");
const public_request = require("../../public/request.js");
const public_qqLocation = require("../../public/qq-Location.js");
require("../../public/qqmap-wx-jssdk.js");
if (!Math) {
  (skIndex + proMpt)();
}
const skIndex = () => "../../Skeleton/SK-index.js";
const proMpt = () => "./components/prompt.js";
const _sfc_main = /* @__PURE__ */ common_vendor.defineComponent({
  __name: "index",
  setup(__props) {
    common_vendor.useCssVars((_ctx) => ({
      "1badc801-styleOpacity": common_vendor.unref(styleOpacity),
      "1badc801-menu_top": common_vendor.unref(menu_top),
      "1badc801-menu_height": common_vendor.unref(menu_height),
      "1badc801-styleColor": common_vendor.unref(styleColor),
      "1badc801-navHeight": common_vendor.unref(navHeight)
    }));
    let menu_top = common_vendor.ref("");
    let menu_height = common_vendor.ref("");
    let navHeight = common_vendor.ref("");
    common_vendor.onMounted(() => {
      let MenuButton = common_vendor.index.getStorageSync("MenuButton");
      menu_top.value = MenuButton.top + "px";
      menu_height.value = MenuButton.height + "px";
      navHeight.value = MenuButton.top + MenuButton.height + 10 + "px";
      pageData_1();
      pageData();
    });
    let vaccine = common_vendor.ref([]);
    let pyhdata = common_vendor.ref([]);
    let registered = common_vendor.ref([]);
    let selftest = common_vendor.ref([]);
    let skeLeton = common_vendor.ref(true);
    async function pageData_1() {
      common_vendor.index.request({
        url: "http://localhost:3000/vaccine",
        data: {},
        success: (res3) => {
          console.log("HPV\u75AB\u82D7&\u56FE\u6587\u54A8\u8BE2", res3);
          vaccine.value = res3.data;
        }
      });
      common_vendor.index.request({
        url: "http://localhost:3000/reserve",
        data: {},
        success: (res22) => {
          console.log("\u8BED\u97F3\u8BC6\u522B\u6302\u53F7", res22);
          pyhdata.value = res22.data;
        }
      });
      skeLeton.value = false;
    }
    async function pageData() {
      const res = await public_request.RequestApi.FrontPage();
      await reLocate();
      registered.value = res.data.data[2].popular;
      selftest.value = res.data.data[3].self_test;
      skeLeton.value = false;
    }
    let styleOpacity = common_vendor.ref(0);
    let styleColor = common_vendor.ref("#fff");
    common_vendor.onPageScroll((event) => {
      styleOpacity.value = event.scrollTop >= 20 ? 1 : event.scrollTop / 300;
      styleColor.value = event.scrollTop >= 20 ? "#000000" : "#fff";
    });
    let cityData = common_vendor.ref("\u5317\u4EAC\u5E02 \u6D77\u6DC0\u533A");
    let addressCode = common_vendor.ref(0);
    let weather = common_vendor.ref([]);
    async function reLocate() {
      const resAddress = await public_qqLocation.getLocation();
      addressCode.value = resAddress.code;
      let lng = resAddress.lng == "none" ? "none" : JSON.stringify(resAddress.lng);
      let lat = resAddress.lat == "none" ? "none" : JSON.stringify(resAddress.lat);
      const weather_data = await public_request.RequestApi.WeaTher({ longitude: lng, latitude: lat });
      weather.value = weather_data.data.data;
      if (resAddress.code == 200) {
        cityData.value = resAddress.province + " " + resAddress.city + " " + resAddress.district;
      } else {
        cityData.value = resAddress.msg;
      }
    }
    let showcont = common_vendor.ref();
    function openTargeting() {
      showcont.value.showCont();
    }
    function vaccineApp(index) {
      switch (index) {
        case 0:
          common_vendor.index.navigateTo({ url: "/pages/hpv-vaccine/hpv-vaccine" });
          break;
        case 1:
          common_vendor.index.navigateTo({ url: "/pages/phy-exam/index" });
          break;
        case 2:
          common_vendor.index.navigateTo({ url: "/pages/graphics/index" });
      }
    }
    function regMedex(index) {
      switch (index) {
        case 0:
          common_vendor.index.navigateTo({ url: "/pages/Speech recognition/Speech recognition" });
          break;
        case 1:
          common_vendor.index.navigateTo({ url: "/pages/phy-exam/index" });
      }
    }
    function regRoute(dep_id) {
      common_vendor.index.navigateTo({
        url: "/pages/doctor/index?id=" + dep_id
      });
    }
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.s(_ctx.__cssVars()),
        b: common_vendor.unref(weather).length > 0
      }, common_vendor.unref(weather).length > 0 ? {
        c: common_vendor.unref(weather)[0].address_icon,
        d: common_vendor.t(common_vendor.unref(cityData)),
        e: common_vendor.n(common_vendor.unref(addressCode) == 202 ? "" : "prohibit"),
        f: common_vendor.o(openTargeting),
        g: common_vendor.unref(weather)[0].tigan_icon,
        h: common_vendor.t(common_vendor.unref(weather)[0].realFeel),
        i: common_vendor.unref(weather)[0].ziwxian_icon,
        j: common_vendor.t(common_vendor.unref(weather)[0].uvi),
        k: common_vendor.t(common_vendor.unref(weather)[0].temp),
        l: common_vendor.unref(weather)[0].icon,
        m: common_vendor.t(common_vendor.unref(weather)[0].condition),
        n: common_vendor.t(common_vendor.unref(weather)[0].humidity),
        o: common_vendor.t(common_vendor.unref(weather)[0].windDir),
        p: common_vendor.t(common_vendor.unref(weather)[0].windLevel),
        q: common_vendor.t(common_vendor.unref(weather)[0].tips),
        r: common_vendor.s(_ctx.__cssVars())
      } : {}, {
        s: common_vendor.f(common_vendor.unref(vaccine), (item, index, i0) => {
          return {
            a: item.image,
            b: common_vendor.t(item.title),
            c: index,
            d: common_vendor.o(($event) => vaccineApp(index), index)
          };
        }),
        t: common_vendor.s(_ctx.__cssVars()),
        v: common_vendor.f(common_vendor.unref(pyhdata), (item, index, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: common_vendor.t(item.describe),
            c: item.image,
            d: index,
            e: common_vendor.o(($event) => regMedex(index), index)
          };
        }),
        w: common_vendor.s(_ctx.__cssVars()),
        x: common_vendor.o(($event) => regMedex(0)),
        y: common_vendor.s(_ctx.__cssVars()),
        z: common_vendor.f(common_vendor.unref(registered), (item, index, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: item.image,
            c: index,
            d: common_vendor.s("background-color:" + item.background),
            e: common_vendor.o(($event) => regRoute(item.dep_id), index)
          };
        }),
        A: common_vendor.s(_ctx.__cssVars()),
        B: common_vendor.unref(skeLeton)
      }, common_vendor.unref(skeLeton) ? {
        C: common_vendor.s(_ctx.__cssVars())
      } : {}, {
        D: common_vendor.sr(showcont, "1badc801-1", {
          "k": "showcont"
        }),
        E: common_vendor.o(reLocate),
        F: common_vendor.s(_ctx.__cssVars())
      });
    };
  }
});
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-1badc801"], ["__file", "D:/WeChatProject/Medical/src/pages/index/index.vue"]]);
_sfc_main.__runtimeHooks = 1;
wx.createPage(MiniProgramPage);
