const ctx = document.getElementById('activityChart');

const activityChart = new Chart(ctx, {

    type: 'line',

    data: {

        labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],

        datasets: [{

            label:'File Events',

            data:[5,8,12,7,15,20,10],

            borderWidth:2,

            tension:0.3

        }]

    },

    options:{

        responsive:true,

        maintainAspectRatio:false

    }

});