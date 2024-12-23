<script>
  import { onMount } from 'svelte';

  let map = null;

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
              center: [113.03041,28.187819], // 初始化地图中心点
            });
            console.log("地图加载成功");
          })
          .catch((e) => {
            console.error('地图加载失败', e);
          });
      });
    }
  });
</script>

<!-- 地图容器 -->
<div id="container"></div>

<style>
  #container {
    width: 100%;
    height: 800px;
  }
</style>
