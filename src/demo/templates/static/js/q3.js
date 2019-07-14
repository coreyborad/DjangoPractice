  // 注意由于分类轴的顺序是从下往上的，所以数组的数值顺序要从小到大
//   var q3_data = [{
//     country: '巴西',
//     population: 18203
//   }, {
//     country: '印尼',
//     population: 23489
//   }, {
//     country: '美国',
//     population: 29034
//   }, {
//     country: '印度',
//     population: 104970
//   }, {
//     country: '中国',
//     population: 131744
//   }];

  var chart = new G2.Chart({
    container: 'q3',
    forceFit: true,
    height: window.innerHeight / 1.5,
    plotCfg: { margin: 40, padding:50}
  });
  chart.source(q3_data);
  chart.scale('count', {
    tickInterval: 5
  });
  chart.point().position('product_name*count').label('count', {})
  chart.interval().position('product_name*count').color('product_name', ['#7f8da9', '#fec514', '#db4c3c']);
  chart.render();