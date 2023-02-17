

const numpred = JSON.parse(document.getElementById('np').textContent);
const correct = JSON.parse(document.getElementById('correct').textContent);
const gain = JSON.parse(document.getElementById('gain').textContent);
const loss = JSON.parse(document.getElementById('loss').textContent);



const extraCorrect = JSON.parse(document.getElementById('extraCorrect').textContent);
const pw = JSON.parse(document.getElementById('pw').textContent);
const ev_margin1 = JSON.parse(document.getElementById('ev_margin1').textContent);
const ev_margin1_pct = JSON.parse(document.getElementById('ev_margin1_pct').textContent);


const possibleGain = numpred/2-gain
const possibleLoss = numpred/2-loss
const adata = {
    labels: [
      'Correct',
      'Predictions',
      
    ],
    datasets: [{
      label: 'Predictions',
      data: [correct, numpred],
      backgroundColor: [
        'rgba(75, 192, 192, 0.2)',  
        'rgba(87, 87, 87,.2)',
        'rgba(201, 203, 207, 0.2)',

      ],
      hoverOffset: 5,
      borderColor: [     
'rgb(75, 192, 192)',
'rgba(87, 87, 87,.5)',
      'rgb(201, 203, 207)', 
      
      ],
      borderWidth: 2
    }]
  };


const aconfig = {
    type: 'bar',
    data: adata,
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


const adata2 = {
    labels: [
      'Wrong',
      'Margin 1',
      'Correct',
    ],
    datasets: [{
      label: 'data',
      data: [pw,ev_margin1_pct,extraCorrect],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(75, 192, 192, 0.2)',  
        'rgba(87, 87, 87,.2)',

        'rgba(255, 159, 64, 0.2)',

      ],
      hoverOffset: 10,
      borderColor: [
      'rgb(255, 99, 132)',
      'rgb(75, 192, 192)',
      'rgba(87, 87, 87,.5)',
      'rgb(255, 159, 64)',

    ],
      borderWidth: 1,

    
    }]
  };


const aconfig2 = {
    type: 'doughnut',
    data: adata2,
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

  const myChart = new Chart(document.getElementById('myChart'),aconfig);

  const myChart2 = new Chart(document.getElementById('myChart2'),aconfig2);


  console.log('helloworld') 