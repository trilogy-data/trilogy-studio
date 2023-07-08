const Display = {
    TABLE: 'Table',
    BAR_CHART: 'Bar Chart',
    LINE_CHART: 'Line Chart'
  };
  
  const Dimensions = ['key', 'property'];
  const Metrics = ['metric'];
  const DateDimensions = ['timestamp', 'date', 'datetime']
  
  const charts = {
    Display() {
      return Display
    },
    getDimensions(columns) {
      return columns.filter(x => Dimensions.includes(x.purpose))
    },
    getMetrics(columns) {
      return columns.filter(x => Metrics.includes(x.purpose))
    },
    getDateDimensions(columns) {
      return columns.filter(x => DateDimensions.includes(x.datatype))
    },
    validChartTypes(columns) {
      const dimensions = charts.getDimensions(columns);
      const metrics = charts.getMetrics(columns);
      const dateDimensions = charts.getDateDimensions(columns);
      const validCharts = [Display.TABLE];
      if (dimensions.length === 1 && metrics.length === 1) {
        validCharts.push(Display.BAR_CHART);
      }
      if (dateDimensions.length === 1 && metrics.length === 1) {
        validCharts.push(Display.LINE_CHART);
      }
      return validCharts;
    }
  };
  
  export default charts;