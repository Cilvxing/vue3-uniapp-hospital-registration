<template>
  <page-container :show="show" position="right" @enter="onEnter">
    <view class="pos-tips">
			<view>
				<image src="/static/other/weizhi.svg" mode="aspectFit"></image>
			</view>
			<view class="pos-tips-title">定位服务未授权，无法获取你的位置</view>
			<button plain="true" @click="openSetting" class="but-one">开启位置</button>
      <button plain="true" class="but-two" @click="show = false">关闭</button>
		</view>
  </page-container>
</template>
<!--  -->
<script setup lang="ts">
import {ref} from 'vue'
let show = ref(false)
function onEnter(){console.log('进入中触发')}
// 被父组件调用，打开弹窗
function showCont(){
  show.value = true
}
defineExpose({ showCont });
// 打开设置
const emit = defineEmits(["parentFunc"]);
function openSetting(){
  show.value = false
  uni.openSetting({
    success: (res) => {
      if(res.authSetting['scope.userLocation']){
        // 调用父组件获取位置和请求数据
        console.log('00000')
        emit('parentFunc');
      }
    }
  })
}


</script>

<style scoped>
.pos-tips{
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	width: 100%;
	height: 100%;
}
.pos-tips image{
	display: block;
	width: 200rpx;
	height: 200rpx;
}
.pos-tips-title{
	padding: 40rpx 0;
	color: #c6c6c6;
}
button{
	border: none;
	width: 400rpx;
  font-size: 33rpx;
}
.but-one{
  background-color: #2c76ef;
  color: #ffffff;
}
.but-two{
  background-color: #e8f2fe;
  color: #3a75f3;
  margin-top: 30rpx;
}
</style>