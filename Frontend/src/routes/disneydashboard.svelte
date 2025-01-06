<script lang="ts">
    import * as echarts from "echarts";
    import { onMount } from "svelte";
  
    let yearChart: echarts.ECharts | null = null;
    let dayChart: echarts.ECharts | null = null;
    let yearDom: HTMLDivElement | null = null;
    let dayDom: HTMLDivElement | null = null;
  
    // 获取每日数据并更新柱状图
    async function get_data(date: string) {
      if (!dayDom) return;
      dayChart = echarts.init(dayDom);
      dayChart.setOption({ title: { text: `获取 ${date} 的数据中..` } });
  
      try {
        const response = await fetch(`${date}.json`);
        const data = await response.json();
  
        const option = {
          title: { text: `单日排队详情: ${data.date}` },
          toolbox: { feature: { saveAsImage: {}, dataView: {} } },
          legend: { data: ["最长等待时间", "平均等待时间"], z: 10 },
          tooltip: {
            trigger: "axis",
            axisPointer: { type: "shadow", label: { show: true } },
          },
          grid: { width: "94%", left: "60px", y2: 150 },
          yAxis: {
            type: "value",
            splitLine: { show: true },
            max: 240,
            interval: 60,
            axisLabel: { formatter: "{value} 分钟" },
          },
          xAxis: {
            type: "category",
            inverse: true,
            data: data.games,
            axisLabel: { interval: 0, rotate: 40 },
          },
          series: [
            {
              name: "最长等待时间",
              type: "bar",
              barGap: "-100%",
              data: data.max,
              itemStyle: { normal: { color: "#37a2da" } },
              label: { normal: { position: "top", formatter: "{c}m", show: true } },
            },
            {
              name: "平均等待时间",
              type: "bar",
              data: data.mean,
              itemStyle: { normal: { color: "#32c5e9" } },
              label: { normal: { position: "top", formatter: "{c}m", show: false } },
            },
          ],
        };
  
        dayChart.setOption(option);
      } catch (error) {
        console.error("获取数据失败：", error);
      }
    }
  
    // 初始化年度热力图
    onMount(async () => {
      if (!yearDom) return;
  
      // 使用 setTimeout 确保 DOM 渲染完毕
      await new Promise(resolve => setTimeout(resolve, 100));  // 等待100ms，确保 DOM 加载
  
      if (yearDom && dayDom) {
        yearChart = echarts.init(yearDom);
        dayChart = echarts.init(dayDom);
      }
      if (yearChart) {
        try {
            const response = await fetch("year.json");
            const data = await response.json();
    
            const years = [];
            const series = [];
            const dt = new Date();
            let i = 0;
    
            for (let year = 2016; year <= dt.getFullYear(); year++) {
            years.push({
                top: 90 + i * 220,
                left: 40,
                range: year,
                cellSize: ["auto", 20],
                dayLabel: {
                nameMap: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
                firstDay: 1,
                },
                monthLabel: { nameMap: "cn" },
                yearLabel: { position: "top" },
            });
    
            series.push({
                type: "heatmap",
                coordinateSystem: "calendar",
                calendarIndex: i,
                data,
            });
    
            i++;
            }
    
            // 类型断言：确保 yearDom 不为 null，并将其类型断言为 HTMLDivElement
            (yearDom as HTMLDivElement).style.height = `${240 * i}px`;
    
            const option = {
            title: { text: "年度热力图" },
            tooltip: {
                position: "top",
                formatter: (p: any) => {
                if (p && p.data && Array.isArray(p.data)) {
                    const format = echarts.format.formatTime("yyyy-MM-dd", p.data[0]);
                    return `${format}</br>平均等待 ${p.data[1]} 分钟`;
                }
                return "";
                },
            },
            toolbox: { feature: { saveAsImage: {}, dataView: {} } },
            visualMap: {
                type: "piecewise",
                itemSymbol: "triangle",
                splitNumber: 6,
                min: 0,
                max: 30,
                calculable: true,
                orient: "horizontal",
                left: "center",
                top: "top",
                z: 10,
                text: ["拥挤", "空闲"],
            },
            calendar: years,
            series,
            };
    
            yearChart.setOption(option);
    
            yearChart.on("click", (params) => {
            if (params.value && Array.isArray(params.value) && typeof params.value[0] === 'string') {
                const date = params.value[0].split("T")[0];
                get_data(date);
            } else {
                console.error("无效的参数值:", params.value);
            }
            });
    
            get_data("latest");
        } catch (error) {
            console.error("获取年度数据失败：", error);
        }
    
        // 自动调整图表尺寸
        window.onresize = () => {
            yearChart?.resize();
            dayChart?.resize();
        };
      } else {
      console.error("年图表初始化失败！");
      }
    });
  </script>
  
  <style>
    #year {
      width: 100%;
    }
  
    #day {
      width: 100%;
      height: 400px;
    }
  </style>
  
  <div>
    <div id="year" bind:this={yearDom}></div>
    <div id="day" bind:this={dayDom}></div>
  </div>
  
  