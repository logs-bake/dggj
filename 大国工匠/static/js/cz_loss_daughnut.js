if(cz_loss){
    cz_loss.forEach(function(item) {
        let doughnut = document.getElementById(item.id);
        let myChart = echarts.init(doughnut);
        let gaugeData = [{
            value: item.loss, detail: { valueAnimation: true, offsetCenter: ['0%', '0%']}
          }];
        let option = {
          series: [{
              type: 'gauge', startAngle: 90, endAngle: -270, pointer: { show: false },
              progress: { show: true, overlap: false, roundCap: false, clip: false, color: 'red'},
              axisLine: { lineStyle: { width: 20,} },
              splitLine: { show: false },
              axisTick: { show: false },
              axisLabel: { show: false },
              data: gaugeData,
              color: item.color,
              detail: { fontSize: 22, color: 'red',
                        formatter: item.loss < 100 ? '{value}%' : (100 - item.loss).toFixed(1) +'%'
                      }
            }]
        };
        myChart.setOption(option);
    });
}





