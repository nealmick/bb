


const correct = JSON.parse(document.getElementById('correct').textContent);
const wrong = JSON.parse(document.getElementById('wrong').textContent);


const scorrect = JSON.parse(document.getElementById('scorrect').textContent);
const swrong = JSON.parse(document.getElementById('swrong').textContent);

const ev_margin1 = JSON.parse(document.getElementById('evMargin1').textContent);
const ev_margin1_count = JSON.parse(document.getElementById('evMargin1wrong').textContent);


const ev_margin2 = JSON.parse(document.getElementById('evMargin2').textContent);
const ev_margin2_count = JSON.parse(document.getElementById('evMargin2wrong').textContent);



const ev_margin3 = JSON.parse(document.getElementById('evMargin3').textContent);
const ev_margin3_count = JSON.parse(document.getElementById('evMargin3wrong').textContent);






let gameSeries1 = JSON.parse(document.getElementById('gameSeries1').textContent);
gameSeries1= gameSeries1.toString().split(',')

let gameSeries2 = JSON.parse(document.getElementById('gameSeries2').textContent);
gameSeries2= gameSeries2.toString().split(',')

let gameSeries3 = JSON.parse(document.getElementById('gameSeries3').textContent);
gameSeries3= gameSeries3.toString().split(',')

console.log(gameSeries1)

let l = []
for(i=0;i<gameSeries1.length;i+=1){
  l.push(i)
}
const data = {
  labels: l,
  datasets: [{
    label: 'Margin 1',
    data: gameSeries1,
    fill: true,
    borderColor: 'rgb(126, 176, 213)',
    tension: .1
  },{
    label: 'Margin 2',
    data: gameSeries2,
    fill: true,
    borderColor: 'rgb(178, 224, 97)',
    tension: .1
  },{
    label: 'Margin 3',
    data: gameSeries3,
    fill: true,
    borderColor: 'rgb(189, 126, 190)',
    tension: .1
}]
};



const config = {
  type: 'line',
  data: data,
  options: {
    maintainAspectRatio: false,
    plugins: {
        legend: {
          display: false
        }
      },
      layout: {
        padding: {
            // Any unspecified dimensions are assumed to be 0                     
            top: 5,
            bottom: 5,
            left: 5,
            right: 5,
        }
    }
    }
};

const historyChart = new Chart(document.getElementById('history-chart'),config);
//["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]


const margin1data = {
    labels: [
      'Win','Loss'
    ],
    datasets: [{
      label: 'Marin 1',
      data: [ev_margin1,ev_margin1_count],
      backgroundColor: [

        'rgba(126, 176, 213, 0.4)',

        'rgba(148, 150, 153, 0.3)'
      ],
      hoverOffset: 10,
      borderColor: [

      'rgb(126, 176, 213)',

      'rgb(148, 150, 153)'
    ],
      borderWidth: 1,

    
    }]
  };


const margin1config = {
    type: 'pie',
    data: margin1data,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
          },
          layout: {
            padding: {
                // Any unspecified dimensions are assumed to be 0                     
                top: 5,
                bottom: 5,
                left: 5,
                right: 5,
            }
        }
        }

  };


  const margin1 = new Chart(document.getElementById('margin1'),margin1config);



  const margin2data = {
    labels: [
        'Win','Loss'
    ],
    datasets: [{
      label: 'Marin 2',
      data: [ev_margin2,ev_margin2_count],
      backgroundColor: [

        'rgba(178, 224, 97, 0.4)',

        'rgba(148, 150, 153, 0.3)'
      ],
      hoverOffset: 10,
      borderColor: [

      'rgb(178, 224, 97)',

      'rgb(148, 150, 153)'
    ],
      borderWidth: 1,

    
    }]
  };


const margin2config = {
    type: 'pie',
    data: margin2data,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
          },
          layout: {
            padding: {
                // Any unspecified dimensions are assumed to be 0                     
                top: 5,
                bottom: 5,
                left: 5,
                right: 5,
            }
        }
        }

  };


  const margin2 = new Chart(document.getElementById('margin2'),margin2config);








  const margin3data = {
    labels: [
        'Win','Loss'
    ],
    datasets: [{
      label: 'Marin 3',
      data: [ev_margin3,ev_margin3_count],
      backgroundColor: [

        'rgba(189, 126, 190, 0.4)',

        'rgba(148, 150, 153, 0.3)'
      ],
      hoverOffset: 10,
      borderColor: [

      'rgb(189, 126, 190)',

      'rgb(148, 150, 153)'
    ],
      borderWidth: 1,

    
    }]
  };


const margin3config = {
    type: 'pie',
    data: margin3data,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
          },
          layout: {
            padding: {
                // Any unspecified dimensions are assumed to be 0                     
                top: 5,
                bottom: 5,
                left: 5,
                right: 5,
            }
        }
        }

  };


  const margin3 = new Chart(document.getElementById('margin3'),margin3config);




  const win_loss_data = {
    labels: [
      'Win','Loss'
    ],
    datasets: [{
      label: 'win/loss',
      data: [correct,wrong],
      backgroundColor: [

        'rgba(255, 181, 90, 0.4)',

        'rgba(148, 150, 153, 0.3)'
      ],
      hoverOffset: 10,
      borderColor: [

      'rgb(255, 181, 90)',

      'rgb(148, 150, 153)'
    ],
      borderWidth: 1,

    
    }]
  };

  const win_loss_config = {
    type: 'pie',
    data: win_loss_data,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
          },
          layout: {
            padding: {
                // Any unspecified dimensions are assumed to be 0                     
                top: 5,
                bottom: 5,
                left: 5,
                right: 5,
            }
        }
        }

  };


  const win_loss = new Chart(document.getElementById('win_loss'),win_loss_config);




  const spead_win_loss_data = {
    labels: [
      'Win','Loss'
    ],
    datasets: [{
      label: 'win/loss',
      data: [scorrect,swrong],
      backgroundColor: [

        'rgba(139, 211, 199, 0.4)',

        'rgba(148, 150, 153, 0.3)'
      ],
      hoverOffset: 10,
      borderColor: [

      'rgb(139, 211, 199)',

      'rgb(148, 150, 153)'
    ],
      borderWidth: 1,

    
    }]
  };

  const spread_win_loss_config = {
    type: 'pie',
    data: spead_win_loss_data,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
          },
          layout: {
            padding: {
                // Any unspecified dimensions are assumed to be 0                     
                top: 5,
                bottom: 5,
                left: 5,
                right: 5,
            }
        }
        }

  };


  const spread_win_loss = new Chart(document.getElementById('spred_win'),spread_win_loss_config);













  const barData = {
    labels: [
      'win',
      'loss',
      'Margin 1 win',
      'Margin 1 loss',
      'Margin 2 win',
      'Margin 2 loss',
      'Margin 3 win',
      'Margin 3 loss',

      
    ],
    datasets: [{
      label: 'Data',
      data: [correct,wrong,ev_margin1,ev_margin1_count,ev_margin2,ev_margin2_count,ev_margin3,ev_margin3_count],
      backgroundColor: [
        'rgba(255, 181, 90, 0.4)',

        'rgba(148, 150, 153, 0.3)',
        'rgba(126, 176, 213, 0.4)',
        'rgba(148, 150, 153, 0.3)',
        'rgba(178, 224, 97, 0.4)',
        'rgba(148, 150, 153, 0.3)',
        'rgba(189, 126, 190, 0.4)',
        'rgba(148, 150, 153, 0.3)',
        'rgba(139, 211, 199, 0.4)',
        'rgba(148, 150, 153, 0.3)',


      ],
      hoverOffset: 5,
      borderColor: [     
      'rgb(255, 181, 90)',
      'rgb(148, 150, 153)', 
      'rgb(126, 176, 213)',
      'rgb(148, 150, 153)',
      'rgb(178, 224, 97)',
      'rgb(148, 150, 153)',
      'rgb(189, 126, 190)',
      'rgb(148, 150, 153)',
      'rgb(139, 211, 199)',
      'rgb(148, 150, 153)'
      ],
      borderWidth: 2
    }]
  };


const barConfig = {
    type: 'bar',
    data: barData,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
          },
          layout: {
            padding: {
                // Any unspecified dimensions are assumed to be 0                     
                top: 5,
                bottom: 5,
                left: 5,
                right: 5,
            }
        }
        }

  };


  const myChart = new Chart(document.getElementById('barChart'),barConfig);