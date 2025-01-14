<script lang="ts">
  import * as echarts from 'echarts';
  import { onMount } from 'svelte';

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
      const response = await fetch(`/${date}.json`);
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
  function formatYearData(data: [string, number][]): [string, number][] {
  return data.map(([date, value]) => [
    echarts.format.formatTime("yyyy-MM-dd", date),
    value,
  ]);
}

onMount(async () => {
  if (!yearDom || !dayDom) {
    console.error("yearDom 或 dayDom 未找到！");
    return;
  }

  await new Promise(resolve => setTimeout(resolve, 100)); // 等待 100ms，确保 DOM 加载

  if (yearChart) echarts.dispose(yearChart);
  yearChart = echarts.init(yearDom);

  try {
    const response = await fetch("/year.json");
    const rawData = await response.json();
    const formattedData = formatYearData(rawData);

    console.log("Formatted Year Data:", formattedData);

    const values = formattedData.map(([_, value]) => value);
    const minVal = Math.min(...values);
    const maxVal = Math.max(...values);

    const years = [];
    const series = [];
    let calendarIndex = 0;
    const dt = new Date();

    // 使用一个 Set 来跟踪哪些年份有数据
    const yearsWithData = new Set(formattedData.map(([date]) => date.split('-')[0]));

    for (let year = 2016; year <= dt.getFullYear(); year++) {
      if (!yearsWithData.has(year.toString())) {
        // 如果没有数据，跳过该年份
        continue;
      }

      years.push({
        range: `${year}`,
        top: 90 + calendarIndex * 220,
        left: 40,
        cellSize: ["auto", 20],
        dayLabel: { nameMap: "cn", firstDay: 1 },
        monthLabel: { nameMap: "cn" },
      });

      series.push({
        type: "heatmap",
        coordinateSystem: "calendar",
        calendarIndex: calendarIndex,
        data: formattedData.filter(([date]) => date.startsWith(`${year}`)),
      });

      calendarIndex++;
    }

    yearDom.style.height = `${240 * calendarIndex}px`;

    yearChart.setOption({
      title: { text: "年度热力图" },
      calendar: years,
      series: series,
      visualMap: {
        type: "piecewise",
        min: minVal,
        max: maxVal,
        splitNumber: 6,
        calculable: true,
        orient: "horizontal",
        left: "center",
        top: "top",
        text: ["拥挤", "空闲"],
      },
      tooltip: {
        position: "top",
        formatter: (params:any) => {
          if (params?.data) {
            const [date, value] = params.data;
            return `${date}</br>平均等待 ${value} 分钟`;
          }
          return "";
        },
      },
    });

    console.log("Heatmap Rendered Successfully.");
  } catch (error) {
    console.error("加载数据失败：", error);
  }
});


</script>

<style>
  div {
    margin: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
  }
</style>

<div bind:this={yearDom} style="width: 100%; height: 500px;"></div>
<div bind:this={dayDom} style="width: 100%; height: 500px;"></div>
