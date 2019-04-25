$(function() {
  let visitListEndpoint = $("a#ajaxVisitList").attr('href');

  /* Functions */

  let createTable = function(data) {
    let labels = [];
    let series = [];

    for (let i = 0; i < data.length; i++) {
      labels.push(data[i].date);
      series.push(data[i].total);
    }
    let dataTable = {
      labels: labels,
      series: [
        series,
      ]
    };

    let options = {
      low: 0,
      axisY: {
        onlyInteger: true,
        offset: 20
      }
    };

    new Chartist.Line('.ct-chart', dataTable, options);
  };


  /* Binding */

  $.ajax({
    url: visitListEndpoint,
    type: 'GET',
    success: function (data) {
      if (data.error) {
        alert('Something wrong!');
      } else {
        createTable(data.visits);
      }
    }
  });

});