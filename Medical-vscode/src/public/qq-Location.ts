// 腾讯地图使用
import QQMapWX from '@/public/qqmap-wx-jssdk.js';
var qqmapsdk: any;
// 实例化API核心类
qqmapsdk = new QQMapWX({
	key: 'SJCBZ-QQ3WC-JJZ2K-ANNBR-PEDWF-LDFH7',
});

// 定位
interface Pres {
	code: number;
	city: string;
	province: string;
	district?: string;
	msg: string;
	lat: number | string;
	lng: number | string;
}
export function getLocation(): Promise<Pres> {
	return new Promise((resolve, reject) => {
		uni.startLocationUpdate({
			success: (res) => {
				uni.onLocationChange(
					async (add: { latitude: number; longitude: number }) => {
						uni.stopLocationUpdate(); //关闭监听实时位置变化，前后台都停止消息接收
						const address = await addRess(add.latitude, add.longitude);
						resolve(address);
					}
				);
			},
			fail: (err) => {
				resolve({
					code: 202,
					msg: '北京市 东城区 开启定位',
					city: 'none',
					province: 'none',
					lat: 'none',
					lng: 'none',
				});
			},
		});
	});
}

// 获取位置
interface Adddress {
	message: string;
	status: number;
	result: {
		address_component: { city: string; province: string; district: string };
		location: { lat: number; lng: number };
	};
}
function addRess(latitude: number, longitude: number): Promise<Pres> {
	return new Promise((resolve, reject) => {
		qqmapsdk.reverseGeocoder({
			location: { latitude, longitude },
			success: (res: Adddress) => {
				if (res.message == 'query ok' && res.status == 0) {
					resolve({
						code: 200,
						msg: 'success',
						city: res.result.address_component.city,
						province: res.result.address_component.province,
						district: res.result.address_component.district,
						lat: res.result.location.lat,
						lng: res.result.location.lng,
					});
				} else {
					throw {
						code: 202,
						msg: '定位失败,程序出现bug',
						city: 'none',
						province: 'none',
						lat: 'none',
						lng: 'none',
					};
				}
			},
			fail: (err: any) => {
				resolve({
					code: 202,
					msg: '定位失败,程序出现bug',
					city: 'none',
					province: 'none',
					lat: 'none',
					lng: 'none',
				});
			},
		});
	});
}
