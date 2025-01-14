<script lang="ts">
    import { onMount } from 'svelte';
    import * as echarts from 'echarts';
  
    let selectedMonth: string = '09'; // 默认选择 2016年9月
    let yearDom: HTMLDivElement | null = null; // 用来显示图表的 DOM
    let yearChart: any; // 存储 ECharts 实例
    let formattedData: [string, number][] = []; // 存储格式化后的数据
  
    const availableMonths = [
      "09", "10", "11", "12", // 2016年数据
      "01", "02", "03"  // 2017年数据
    ];
  
    // 格式化数据
    function formatYearData(data: [string, number][]): [string, number][] {
      return data.map(([date, value]) => [
        echarts.format.formatTime('yyyy-MM-dd', date),
        value,
      ]);
    }
  
    // 获取数据并初始化图表
    onMount(async () => {
      if (!yearDom) {
        console.error("yearDom 未找到！");
        return;
      }
  
      await new Promise(resolve => setTimeout(resolve, 100)); // 等待 DOM 加载
  
      if (yearChart) echarts.dispose(yearChart);
      yearChart = echarts.init(yearDom);
  
      try {
        const response = await fetch("/year.json"); // 假设你有一个 `/year.json` 文件
        const rawData = await response.json();
        formattedData = formatYearData(rawData);
  
        console.log("Formatted Year Data:", formattedData);
  
        updateChart(selectedMonth);
      } catch (error) {
        console.error("加载数据失败：", error);
      }
    });
  
    // 更新图表函数，根据用户选择的月份来筛选数据
    function updateChart(month: string) {
      // 只筛选出你有的数据月份
      if (!availableMonths.includes(month)) {
        console.error(`数据不存在 ${month} 月`);
        return;
      }
  
      const filteredData = formattedData.filter(([date]) => date.split('-')[1] === month);
      if (filteredData.length === 0) {
        console.error(`没有 ${month} 月的数据`);
        return;
      }
  
      const values = filteredData.map(([, value]) => value);
      const minVal = Math.min(...values);
      const maxVal = Math.max(...values);
  
      const years: any[] = [];
      const series: any[] = [];
      let calendarIndex = 0;
      const dt = new Date();
  
      // 只展示 2016 和 2017 的数据
      const validYears = [2016, 2017];
      
      validYears.forEach((year) => {
        years.push({
          range: `${year}`,
          top: 90 + calendarIndex * 220,
          left: 40,
          cellSize: ["auto", 20],
          dayLabel: { nameMap: "cn", firstDay: 1 },
          monthLabel: { nameMap: "cn" },
        });
  
        // 只为当前选择的月份显示数据
        series.push({
          type: "heatmap",
          coordinateSystem: "calendar",
          calendarIndex: calendarIndex,
          data: filteredData.filter(([date]) => date.startsWith(`${year}-${month}`)),
        });
  
        calendarIndex++;
      });
  
      yearDom.style.height = `${240 * calendarIndex}px`;
  
      yearChart.setOption({
        title: { text: `热力图 - ${month} 月` },
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
          formatter: (params: any) => {
            if (params?.data) {
              const [date, value] = params.data;
              return `${date}</br>平均等待 ${value} 分钟`;
            }
            return "";
          },
        },
      });
    }
  
  </script>
  
  <main>
    <div class="filters">
      <label for="month-select">选择月份：</label>
      <select id="month-select" bind:value={selectedMonth} on:change={() => updateChart(selectedMonth)}>
        <option value="09">2016年9月</option>
        <option value="10">2016年10月</option>
        <option value="11">2016年11月</option>
        <option value="12">2016年12月</option>
        <option value="01">2017年1月</option>
        <option value="02">2017年2月</option>
        <option value="03">2017年3月</option>
      </select>
    </div>
  
    <div class="chart-container">
      <div id="year-chart" bind:this={yearDom} style="height: 600px;"></div>
    </div>
  </main>
  