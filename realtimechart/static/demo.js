var chartData={
                        'date':[],
                        'open':[],
                        'high':[],
                        'close':[]
                    }


//function initialupdateData(data){
//
//        $('#example').DataTable().row.add(data).draw();
//        console.log(data.Datetime,'---')
//        chart.series[0].addPoint({
//                    x: new Date(data.Datetime).getTime(),  // Convert date-time to timestamp
//                    y: data.Close
//                })
//}




$(document).ready(function() {
            // Sample data for table and graph
            // Populate DataTable
            console.log('Yes-----23')
            fetch("/api/stocks/initial/")
                .then(response => response.json())
                .then(data => {
//                    updateData(data.data)

                    $('#example').DataTable().rows.add(data.data).draw();
                   data.data.forEach(row => {
//                        chartData.date.push(new Date(row.Datetime).getTime()); // Push datetime for x-axis
//                        chartData.open.push([new Date(row.Datetime).getTime(), row.Open]); // Push open values
//                        chartData.high.push([new Date(row.Datetime).getTime(), row.High]); // Push high values
//                        chartData.close.push([new Date(row.Datetime).getTime(), row.Close]); // Push close values
                        updateData(row,false) // Uncomment if required
                    });
//                  chart.xAxis[0].setCategories(chartData.date,false);
//                  chart.series[0].setData(chartData.close,false);
//                  chart.series[1].setData(chartData.open,false);
//                  chart.series[2].setData(chartData.high,false);
                    chart.redraw()

                });


            var table = $('#example').DataTable({
                data: [],
                "order": [1,'desc'],
                columnDefs: [
                    {
                        "targets":0,
                        "data": 'Symbol'
                    },
                    {
                        "targets":1,
                        'searchable': false,
                        'data': 'Datetime',
                        "render": function (data, type, row, meta) {
                            return new Date (data)
                        },
                        "type": "date",
                    },
                    {"targets":2, data: 'Open' },
                    {"targets":3, data: 'High' },
                    {"targets":4, data: 'Low' },
                    {"targets":5,data: 'Close' },
                    {"targets":6,data: 'Volume'}
                ],
//                paging: ,  // Disable paging for simplicity
                searching: false, // Disable search
//                ordering: false // Disable sorting
            });

// Format the data for Highcharts
//            var chartData = sampleData.map(function(item) {
//                return {
//                    x: new Date(item.datetime).getTime(),  // Convert date-time to timestamp
//                    y: item.value
//                };
//            });
//            var chartData=[]
            // Initialize Highcharts to display the linear graph
            chart=Highcharts.chart('container', {
                chart: {
                    type: 'line',
                      zoomType: 'x',
                },
                title: {
                    text: 'Value over Time'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Date & Time'
                    },
//                    labels: {
//                    formatter: function () {
//
//                        var d1 = new Date(this.value);
//                        return moment(d1).format('DD, MMM YYYY HH:mm:ss');
//                    }
                },
                yAxis: {
                    title: {
                        text: 'Value'
                    }
                },
                series: [{
                    name: 'Close',
                    data: chartData.close
                    },
                {
                name: 'Oper',
                data:chartData.open
                },
             {
                name: 'High',
                data:chartData.high
            }]
            });
        });
function updateData(data,redraw_check){
        $('#example').DataTable().row.add(data).draw();
//        chart.series[0].addPoint({
//                    x: new Date(data.Datetime).getTime(),  // Convert date-time to timestamp
//                    y: data.Close
//                })
//         chart.series[1].addPoint({
//                    x: new Date(data.Datetime).getTime(),  // Convert date-time to timestamp
//                    y: data.Open
//                })
//         chart.series[2].addPoint({
//                    x: new Date(data.Datetime).getTime(),  // Convert date-time to timestamp
//                    y: data.High
//                })
//
            const timestamp = new Date(data.Datetime).getTime(); // Convert Datetime to timestamp

            chart.series[0].addPoint(
                { x: timestamp, y: data.Close },
                false // Suppress redraw
            );

            chart.series[1].addPoint(
                { x: timestamp, y: data.Open },
                false // Suppress redraw
            );

            chart.series[2].addPoint(
                { x: timestamp, y: data.High },
                false // Suppress redraw
            );

            // Redraw chart after all points are added
            if (redraw_check){
              chart.redraw();
            }


        }
 var socket = new WebSocket('ws://localhost:8000/ws/stockcharts/')
                socket.onmessage = function(e){
                    data=JSON.parse(e.data)
                    table_row=JSON.parse(data['data'])
                    console.log(JSON.parse(data['data']),'-------6')
                    existingRow =$('#example').DataTable().row(0).data()
                        updateData(table_row,true)
                     }
