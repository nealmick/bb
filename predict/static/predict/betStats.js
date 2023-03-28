
const pv = JSON.parse(document.getElementById('pv').textContent);
const nv = JSON.parse(document.getElementById('nv').textContent);

const betsData = {
    labels: [
        'Positive Varience','Negative Varience'
    ],
    datasets: [{
      label: 'Predictions vs Spread',
      data: [pv,nv],
      backgroundColor: [
        'rgba(75, 192, 192, 0.2)',

        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(201, 203, 207, 0.2)'
      ],
      hoverOffset: 10,
      borderColor: [
      'rgb(75, 192, 192)',

      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(201, 203, 207)'
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


  const myChart2 = new Chart(document.getElementById('myChart2'),betsConfig);
