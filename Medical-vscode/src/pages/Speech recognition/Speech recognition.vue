<template>
<!--index.wxml-->
<!-- <view class="container">
  Weixin
</view> -->
<form bindsubmit="formSubmit">
    <view class="videoWrap">
        <textarea class='videoCon' bindinput="conInput" placeholder='等待说话...' value='{{content}}'></textarea>
    </view>
    <view class="insert-button">
    <button formType="submit" class="videoBtn sendBtn" type="default">推荐科室</button>
  </view>
</form>
<view>推荐的科室是：{{label_content}}</view>
<view class='video-konw'>
  <button type="primary" class="videoBtn {{recordState == true ? 'videoBtnBg':''}}" bindtouchstart="touchStart" bindtouchend="touchEnd">
    <text wx:if="{{recordState == false}}">按住 说话</text>
    <text wx:else>松开 结束</text>
  </button>
</view>
<view class='send-btn'>
    <!-- <button type="default" class="videoBtn sendBtn" bindtap="conInput">
     推荐科室
   </button> -->

  <button type="default" class="videoBtn sendBtn"  bindtap="gotoRegist">
     去挂号
  </button>
</view>
<!-- 开始语音 弹出语音图标表示正在录音 -->
<cover-view class="startYuyinImage" wx:if="{{recordState == true}}">
  <cover-icon></cover-icon>
  <cover-image src="https://7061-path-one-7g9wyeb1fb616373-1318944028.tcb.qcloud.la/yuyin.jpg"></cover-image>
  <cover-view>开始语音</cover-view>
</cover-view>


</template>

<script setup lang="ts">

</script>

<style scoped>
page {
  height: 100%;
  width: 100%;
  background: #FAFAFA;
  background-image: url(https://uploads-ssl.webflow.com/60e3d74…/60e3d74…_60e3a35…_Mesh%252087-p-500.jpeg);
  background-size: cover;
}

.videoWrap {
  margin-top: 150rpx;
  word-wrap: break-word;
  position: relative;
  width: 80%;
  margin-left: 10%;
  background: #FFFFFF;
  box-shadow: 0 2px 16px 2px rgba(0, 0, 0, 0.1);
  padding: 50rpx 60rpx;
  box-sizing: border-box;
  min-height: 260rpx;
}

.videoCon {
  width: 100%;
  margin: 0 auto;
  padding: 10rpx;
  background: #fff;
}

.videos {
  position: absolute;
  bottom: 0;
  left: 48rpx;
  font-size: 36rpx;
  color: #999;
  padding-bottom: 10rpx;
}

.videos icon.iconfont {
  font-size: 34rpx;
  padding: 0 17rpx 15rpx;
  border-radius: 50%;
  background: #73dbef;
  margin-right: 14rpx;
  color: #fff;
}

.consultYuyin {
  height: 100%;
  width: 90%;
}

.icon-jianpan1 {
  position: absolute;
  left: 10rpx;
  bottom: 6px;
  color: #606267;
  font-size: 60rpx;
}

.videoBtn {
  width: 50%;
  height: 80rpx;
  line-height: 80rpx;
  background-image: var(--gradualBlue);
  color: var(--white);
  border-radius: 8px;
  margin-top: 150rpx;
}
.sendBtn{
  margin-top: 80rpx;
  background-image: var(--gradualPink);
  color: var(--white);

}
.videoBtnBg {
  background: #bdb4b4;
}

.videoBtn::after {
  /* background: #fff; */
  /* color: #000; */
  border-radius: 0;
  border: none;
}

.startYuyinImage {
  position: fixed;
  top: 216rpx;
  left: 50%;
  width: 240rpx;
  height: 300rpx;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 20rpx;
  color: #fff;
  text-align: center;
  margin-left: -120rpx;
}

.startYuyinImage cover-image {
  margin: 60rpx auto;
  width: 100rpx;
  height: 100rpx;
}

.startYuyinImage cover-view {
  margin-top: 25rpx;
}
</style>