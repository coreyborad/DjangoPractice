var chart = new G2.Chart({
  container: 'q1',
  forceFit: true,
  height: window.innerHeight / 2
});
chart.source(q1_data, {
  ratio: {
    formatter: function formatter(val) {
      val = val * 100 + '%';
      return val;
    }
  }
});
chart.coord('theta', {
  radius: 0.75
});
chart.tooltip({
  showTitle: false,
  itemTpl: '<li><span style="background-color:{color};" class="g2-tooltip-marker"></span>{name}: {value}</li>'
});
chart.intervalStack().position('ratio').color('type').label('ratio', {
  formatter: function formatter(val, type) {
    return type.point.type + ': ' + val;
  }
}).tooltip('type*ratio', function(type, ratio) {
  ratio = ratio * 100 + '%';
  return {
    name: type,
    value: ratio
  };
}).style({
  lineWidth: 1,
  stroke: '#fff'
});
chart.render();