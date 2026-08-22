const app = getApp();
//引入插件：微信同声传译
const plugin = requirePlugin('WechatSI');
//获取全局唯一的语音识别管理器recordRecoManager
const manager = plugin.getRecordRecognitionManager();

let content=''
let label_content=''
let textarea_content=''//推荐的科室
let URL=''//机器学习接口
Page({

  /**
   * 页面的初始数据
   */
  data: {
    //语音
    recordState: false, //录音状态
    content:'',//内容
    textarea_content:'',//推荐的科室
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
      /**ws用的文件，这里可以删除
    this.setData({
      dataPacker:JSON.parse(options.param)
    })
    */
    //识别语音
    this.initRecord();
  },
    // bindTextAreaBlur: function(e) {
    //     this.setData({
    //     inputVal:e.detail.value
    //     })
    // },


  // 手动输入内容
  conInput: function (e) {
    this.setData({
      content:e.detail.value,
    })
  },
  formSubmit: function(e) {
    const that=this
    console.log("打印content",that.data.content)
    URL='http://127.0.0.1:3389/check/'+that.data.content
    console.log("打印URL",URL)
    wx.request({

        url: URL,

        success: res=> {

            label_content=res.data.label
            label_content="心血管内科"
            console.log("医生home自己的日期textarea_content",label_content)
            this.setData({
                label_content:label_content
               
            })

        }
    })
    },
  //识别语音 -- 初始化
  initRecord: function () {
    const that = this;
    // 有新的识别内容返回，则会调用此事件
    manager.onRecognize = function (res) {
      console.log(res)
    }
    // 正常开始录音识别时会调用此事件
    manager.onStart = function (res) {
      console.log("成功开始录音识别", res)
    }
    // 识别错误事件
    manager.onError = function (res) {
      console.error("error msg", res)
    }
    //识别结束事件
    manager.onStop = function (res) {
      console.log('..............结束录音')
      console.log('录音临时文件地址 -->' + res.tempFilePath);
      console.log('录音总时长 -->' + res.duration + 'ms');
      console.log('文件大小 --> ' + res.fileSize + 'B');
      console.log('语音内容 --> ' + res.result);
      if (res.result == '') {
        wx.showModal({
          title: '提示',
          content: '听不清楚，请重新说一遍！',
          showCancel: false,
          success: function (res) {}
        })
        return;
      }
      // var text = that.data.content + res.result;
      that.setData({
        content: res.result,

        //textarea_content:content
      })
      console.log("cdd",content)
    }
  },
  //语音  --按住说话
  touchStart: function (e) {
    this.setData({
      recordState: true  //录音状态
    })
    // 语音开始识别
    manager.start({
      lang: 'zh_CN',// 识别的语言，目前支持zh_CN en_US zh_HK sichuanhua
    })
  },
  //语音  --松开结束
  touchEnd: function (e) {
    this.setData({
      recordState: false
    })
    // 语音结束识别
    manager.stop();
  },

    /**ws用的文件，这里可以删除

  sendBarrage(){
    if(this.data.content?.length>0){
      let data = this.data.dataPacker
      data.content = this.data.content
     this.sendDataToWS(data)
    }else{
      wx.showToast({
        title: '上墙内容为空',
        icon:'error'
      })
    }

  },
  sendDataToWS(data){
    wx.sendSocketMessage({
      data: JSON.stringify(data),
    })
  },*/

  



  gotoRegist(){
      console.log("去挂号",textarea_content)
      wx.switchTab({
        url:'/pages/registered/registered'
    })
  },
  gotoONE(){
    wx.switchTab({
      url:'/pages/index/index'
  })

  }

})

