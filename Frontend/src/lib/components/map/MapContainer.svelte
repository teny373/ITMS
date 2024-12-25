<script lang="ts">
  import { onMount } from 'svelte';

  let map: any = null;  // Use any type for map
  let centerCoord = '';
  let tips = '';

  onMount(() => {
    // 确保只在浏览器中加载地图
    if (typeof window !== 'undefined') {
      import('@amap/amap-jsapi-loader').then((AMapLoader) => {
        // 加载高德地图
        AMapLoader.load({
          key: "1833aea781b25698b39f474b10d71a85", // 申请好的 Web 端开发者 Key
          version: "2.0", // 指定要加载的 JSAPI 的版本
          plugins: ["AMap.Scale"], // 需要加载的插件
        })
          .then((AMap) => {
            map = new AMap.Map("container", {
              viewMode: "3D", // 是否为 3D 地图模式
              zoom: 11, // 初始化地图级别
              center: [121.33692,31.127977], // 初始化地图中心点
            });
            console.log("地图加载成功");
            map.clearMap();  // 清除地图覆盖物

        const markers = [{
          icon: '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-1.png',
          position: [116.205467, 39.907761]
        }, {
          icon: '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-2.png',
          position: [116.368904, 39.913423]
        }, {
          icon: '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-3.png',
          position: [116.305467, 39.807761]
        }];

        // 添加标记点
        markers.forEach(marker => {
          new AMap.Marker({
            map: map,
            icon: marker.icon,
            position: marker.position,
            offset: new AMap.Pixel(-13, -30)
          });
        });

        // 获取地图中心点坐标并更新
        const center = map.getCenter();
        centerCoord = `当前中心点坐标：${center.getLng()}, ${center.getLat()}`;
        tips = '成功添加三个点标记，其中有两个在当前地图视野外！';
          })
          .catch((e) => {
            console.error('地图加载失败', e);
          });
      });
    }
  });

  function handleFitViewClick() {
    if (map) {
      map.setFitView(null, false, [150, 60, 100, 60]);
      const newCenter = map.getCenter();
      centerCoord = `当前中心点坐标：${newCenter.getLng()}, ${newCenter.getLat()}`;
      tips = '通过setFitView，地图自适应显示到合适的范围内,点标记已全部显示在视野中！';
    }
  }
</script>

<!-- 地图容器 -->
<div id="container"></div>
<div class="input-card">
  <h4>地图自适应</h4>
  <input id="setFitView" type="button" class="btn" value="地图自适应显示" on:click={handleFitViewClick} />
</div>
<style>
  #container {
    width: 100%;
    height: 800px;
  }
  .input-card {
    position: fixed; 
    bottom: 20px; 
    right: 20px; 
    z-index: 1000; 
    background-color: rgba(255, 255, 255, 0.7); 
    padding: 10px;
    border-radius: 5px; 
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); 
  }

  .btn {
    cursor: pointer;
    padding: 10px 20px;
    font-size: 14px;
    background-color: #57b5e8;
    color: white;
    border: none;
    border-radius: 5px;
  }

  .input-card h4 {
    margin: 0;
    font-size: 16px;
    color: #333;
  }

</style>
