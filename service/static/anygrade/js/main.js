if (document.querySelector('.radar')) {
    const labelsBlock = document.querySelector('.radar-labels');
    const labels = labelsBlock.textContent.split('|').map(el => el.trim());
    labelsBlock.remove();

    const dataBlock = document.querySelector('.radar-data');
    const data_ = dataBlock.textContent.split('|').map(el => el.trim().replace(',', '.'));
    dataBlock.remove();

    const label = document.querySelector('.review__subject').textContent;

    const data = {
        labels: labels,
        datasets: [{
            label: label,
            data: data_,
            fill: true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'
        }]
    };

    const config = {
        type: 'radar',
        data: data,
        options: {
            scales: {
                r: {
                    angleLines: {
                        display: false
                    },
                    suggestedMin: 0,
                    suggestedMax: 5
                }
            },
            elements: {
                line: {
                    borderWidth: 3
                }
            }
        },
    };

    const myChart = new Chart(
        document.querySelector('.radar-chart'),
        config
    );
}