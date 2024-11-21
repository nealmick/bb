
const correct = JSON.parse(document.getElementById('correct').textContent);
const numpred = JSON.parse(document.getElementById('np').textContent)-correct;
const gain = JSON.parse(document.getElementById('gain').textContent);
const loss = JSON.parse(document.getElementById('loss').textContent);

const extraCorrect = JSON.parse(document.getElementById('extraCorrect').textContent);
const pw = JSON.parse(document.getElementById('pw').textContent);

const ev_margin1 = JSON.parse(document.getElementById('ev_margin1').textContent);
const ev_margin1_count = JSON.parse(document.getElementById('ev_margin1_count').textContent)-ev_margin1;
const ev_margin1_pct = JSON.parse(document.getElementById('ev_margin1_pct').textContent);

const ev_margin2 = JSON.parse(document.getElementById('ev_margin2').textContent);
const ev_margin2_count = JSON.parse(document.getElementById('ev_margin2_count').textContent-ev_margin2);
const ev_margin2_pct = JSON.parse(document.getElementById('ev_margin2_pct').textContent);

const ev_margin3 = JSON.parse(document.getElementById('ev_margin3').textContent);
const ev_margin3_count = JSON.parse(document.getElementById('ev_margin3_count').textContent-ev_margin3);
const ev_margin3_pct = JSON.parse(document.getElementById('ev_margin3_pct').textContent);

const ev_margin0 = JSON.parse(document.getElementById('ev_won').textContent);
const ev_margin0_count = JSON.parse(document.getElementById('ev_won_count').textContent)-ev_margin0;
const ev_margin0_pct = JSON.parse(document.getElementById('ev_won_pct').textContent);

const possibleGain = numpred/2-gain
const possibleLoss = numpred/2-loss

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
      label: 'Marin 3',
      data: [correct,numpred],
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





  const gain_loss_data = {
    labels: [
      'Gain','Loss'
    ],
    datasets: [{
      label: 'Marin 3',
      data: [gain,loss],
      backgroundColor: [

        'rgba(190, 185, 219, 0.4)',

        'rgba(148, 150, 153, 0.3)'
      ],
      hoverOffset: 10,
      borderColor: [

      'rgb(190, 185, 219)',

      'rgb(148, 150, 153)'
    ],
      borderWidth: 1,

    
    }]
  };


const gain_loss_config = {
    type: 'pie',
    data: gain_loss_data,
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


  const gain_loss = new Chart(document.getElementById('gain_loss'),gain_loss_config);








  const margin0data = {
    labels: [
      'Win','Loss',
    ],
    datasets: [{
      label: 'Margin 0',
      data: [ev_margin0,ev_margin0_count],
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


const margin0config = {
    type: 'pie',
    data: margin0data,
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


  const margin0 = new Chart(document.getElementById('margin0'),margin0config);




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
      'Margin 0 win',
      'Margin 0 loss',
      
    ],
    datasets: [{
      label: 'Data',
      data: [correct,numpred,ev_margin1,ev_margin1_count,ev_margin2,ev_margin2_count,ev_margin3,ev_margin3_count,ev_margin0,ev_margin0_count],
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