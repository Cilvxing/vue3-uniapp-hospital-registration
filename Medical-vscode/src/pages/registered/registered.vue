<template>
  <view class="regist-view">
    <view class="regist-left">
      <!-- 没有 @click="changeList(index, item._id)点击事件的时候，点击不起效果，只可以展示第一个父级科室的子科室 -->
      <!-- 其中item._id指的是父科室的id -->
      <text v-for="(item, index) in department_data" :key="index"
      :class="addColor == index ? 'addcolor' : ''"
      @click="changeList(index, item._id)"
      >
      {{item.dep_ment}}
      </text>
    </view>
    <view class="regist-right">
      <!-- 用虚拟标签block包裹，子科室数据是数组里面包含数组所以两个遍历 -->
      
      <block v-for="(item, index) in reglist_data" :key="index">
        <view v-for="(item_a, index_a) in item.dep_ment_list" :key="index_a"
        @click="jumpRoute(item_a.dep_id)"
        >
        {{item_a.dep_name}}
        </view>
      </block>
    </view>
  </view>
  <!-- 骨架屏 -->
  <skIndex v-if="skeLeton"></skIndex>
</template>

<script setup lang="ts">
import {ref,onMounted} from 'vue'
import {RequestApi} from '@/public/request'
import {Department,Reglist} from '@/public/decl-type'
// 骨架屏
import skIndex from '@/Skeleton/SK-registered.vue' 

// 父科室数据
let department_data = ref<Department[]>([])
// 请求数据
interface DeparData{
  data:{data:Department[]}
}
// 骨架屏
let skeLeton = ref(true)
onMounted(async()=>{
  const res:any = await RequestApi.DeparTment() as DeparData
   console.log("res.data[0]._id",res)
  // res.data.data[0]={_id: "af2b6af462e1780b000b7ac649eef401", dep_ment: "骨科"},
  // res.data.data[8]={_id: "af2b6af462e1780b000b7ace24bee7cd", dep_ment: "儿科"}
  department_data.value = res.data
  changeList(0,res.data[0]._id)
})

// 点击父科室加上颜色
let addColor = ref(0)
// 请求子科室数据
let reglist_data = ref<Reglist[]>([])
interface RegData{
  data:{data:Reglist[]}
}
async function changeList(index:number,id:string){
  console.log("idid",id)
  addColor.value = index
  //const res:any = await RequestApi.RegList({id}) as RegData
  const res:any=uni.request({
    url: 'http://localhost:3000/reglist', 
    data: {
      _id:id
    },
    success: res=> {
        console.log("筛选子科室",res)
        reglist_data.value=res.data
       // console.log("reglist_data",reglist_data.value)
    }
})
//reglist_data.value=res.data
  // 骨架屏
  skeLeton.value = false
}
// 跳转选择医生
function jumpRoute(id:string){
  uni.navigateTo({
    url:'/pages/doctor/index?id=' + id
  })
}
</script>

<style scoped>
  .regist-view{
    display: flex;
    justify-content: space-between;
  }
  .regist-left{
    background-color: #f5f5f5;
    width: 200rpx;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    overflow: auto;
  }
  .regist-left text{
    display: block;
    padding: 25rpx;
  }
  .addcolor{
    background-color: #ffffff;
    color: #2c76ef;
  }
  .regist-right{
    padding-left: 200rpx;
    flex: 1;
  }
  
  .regist-right view{
    padding: 25rpx;
  }
  </style>