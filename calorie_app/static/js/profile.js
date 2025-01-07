window.onload = function() {
  const table = document.getElementById('weightable');
  let recorded_weight = [];
  let recorded_date = [];

  for (let i = 1; i < table.rows.length; i++) {
      recorded_weight.push(parseFloat(table.rows[i].cells[0].innerHTML));
      recorded_date.push(table.rows[i].cells[1].innerHTML);
  }

  let values = recorded_weight;

  const ctxAreaChart = document.getElementById('myChart');
  const myAreaChart = new Chart(ctxAreaChart, {
      type: 'line',
      data: {
          labels: recorded_date,
          datasets: [{
              label: 'Weight',
              data: values,
              lineTension: 0.3,
              backgroundColor: 'rgba(2,117,216,0.2)',
              borderColor: 'rgba(2,117,216,1)',
              pointRadius: 5,
              pointBackgroundColor: 'rgba(2,117,216,1)',
              pointBorderColor: 'rgba(255,255,255,0.8)',
              pointHoverRadius: 5,
              pointHoverBackgroundColor: 'rgba(2,117,216,1)',
              pointHitRadius: 50,
              pointBorderWidth: 2,
          }],
      },
      options: {
          scales: {
              x: {
                  ticks: {
                      autoSkip: false,
                      maxRotation: 60,
                      minRotation: 60,
                  },
                  grid: {
                      display: true,
                  },
                  title: {
                      display: true,
                      text: 'Date',
                  },
              },
              y: {
                  ticks: {
                      min: 0,
                      max: 120,
                      callback: function (value) {
                          return value + 'kg';
                      },
                  },
                  grid: {
                      color: 'rgba(0, 0, 0, .125)',
                  },
                  title: {
                      display: true,
                      text: 'Weight in kg',
                  },
              },
          },
          legend: {
              display: false,
          },
      },
  });
};
