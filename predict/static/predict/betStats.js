
let history = JSON.parse(document.getElementById('history').textContent).slice(1, -1);

let days = JSON.parse(document.getElementById('days').textContent)
history=history.split(',')
const data = {
  labels: [...Array(days).keys()].reverse(),
  datasets: [{
    label: 'Profit',
    data: history,
    fill: true,
    borderColor: 'rgb(75, 192, 192)',
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





const pv = JSON.parse(document.getElementById('pv').textContent);
const nv = JSON.parse(document.getElementById('nv').textContent);


const correct = JSON.parse(document.getElementById('correct').textContent);
const wrong = JSON.parse(document.getElementById('wrong').textContent);


const betsData = {
    labels: [
        '+Varience','-Varience'
    ],
    datasets: [{
      label: 'Predictions vs Spread',
      data: [pv,nv],
      backgroundColor: [
        'rgba(75, 192, 192, 0.2)',
        'rgba(255, 99, 132, 0.2)',

        'rgba(201, 203, 207, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(153, 102, 255, 0.2)',
      ],
      hoverOffset: 10,
      borderColor: [
      'rgb(75, 192, 192)',
      'rgb(255, 99, 132)',

      'rgb(201, 203, 207)',

      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
    ],
      borderWidth: 1,

    
    }]
  };


const betsConfig = {
    type: 'doughnut',
    data: betsData,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: true,
              position: 'bottom'
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


  const myChart2 = new Chart(document.getElementById('myChart2'),betsConfig);

  const betsDataCW = {
    labels: [
        'Correct','Wrong'
    ],
    datasets: [{
      label: 'Predictions vs Spread',
      data: [correct,wrong],
      backgroundColor: [
        'rgb(54, 162, 235,0.2)',
        'rgba(255, 99, 132, 0.2)',

        'rgba(201, 203, 207, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(153, 102, 255, 0.2)',
      ],
      hoverOffset: 10,
      borderColor: [
      'rgb(54, 162, 235)',
      'rgb(255, 99, 132)',

      'rgb(201, 203, 207)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(153, 102, 255)',

    ],
      borderWidth: 1,

    
    }]
  };


const betsConfigCW = {
    type: 'doughnut',
    data: betsDataCW,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: true,
              position: 'bottom'
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


  const myChartCW = new Chart(document.getElementById('myChartCW'),betsConfigCW);
