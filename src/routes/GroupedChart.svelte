<script>
    import Chart from 'chart.js/auto';
    import { onMount } from 'svelte';
    let {width=$bindable(), height=$bindable(), d1, d2} = $props();
    let ctx, pie;

    const sum = a => eval(a.join('+'));
    const getValues = (dic) => {
        return Object.values(dic).map((x) => (x / sum(Object.values(dic)).toFixed(4)*100));
    }
    const data = {
        labels: Object.keys(d2),
        datasets: [
            {
            label: '2016',
            data: getValues(Object.values(d1)),
            fill: false,
            borderColor: '#36A2EB',
            backgroundColor: '#9AD0F5',
            },
            {
            label: '2019',
            data: getValues(Object.values(d2)),
            fill: false,
            borderColor: '#FF6384',
            backgroundColor: '#FFB1C1',
            },
        ]
    };

    const data_pi =  {
        labels: [
            'Red',
            'Blue',
            'Yellow'
        ],
        datasets: [{
            label: 'My First Dataset',
            data: [300, 50, 100],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
            ],
            hoverOffset: 4,
            hoverBorderJoinStyle: 'round',
            hoverOffset: 15,
        }]
    }

    onMount(
        async () => {
            var chart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    indexAxis: 'y',
                    // Elements options apply to all of the options unless overridden in a dataset
                    // In this case, we are setting the border of each horizontal bar to be 2px wide
                    elements: {
                        bar: {
                            borderWidth: 2,
                        }
                    },
                    aspectRatio: 1.36,
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                font: {
                                    size: height/65
                                }
                            }
                        },
                        title: {
                            display: true,
                            text: 'Mental Health Disorder Distribution (in %)'
                        }
                    }
                },
            })
        }
    );
</script>

<div>
    <canvas bind:this={ctx}></canvas>
    <canvas bind:this={pie}></canvas>
</div>

<style>
    canvas {
        padding: 0.7vw;
    }

    div {
        height: 100%;
    }
</style>