<script>
    import * as d3 from 'd3';

    let { height = $bindable(), width = $bindable(), margin, dic={}, theme = 'dark', title = 'Pie Plot' } = $props();
  // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    let radius = $derived(Math.min(width, height) / 2 - margin);
    
    const data = dic;
    
    let xScale = $derived(d3.scaleLinear().domain([0, 100]).range([-width, width]));
    let yScale = $derived(d3.scaleLinear().domain([0, 100]).range([height/2, -height/2]));
    console.log(title, ":\nxScale =",xScale(85));
    $effect(()=>console.log(title, ":\nxScale =", xScale(85),"changed"));
    // set the color scale
    let color = null;
    if(theme == 'dark')
        color = d3
        .scaleOrdinal()
        .domain(Object.keys(data))
        .range(d3.schemeDark2);
    
    else if(theme == 'tableu')
        color = d3
        .scaleOrdinal()
        .domain(Object.keys(data))
        .range(d3.schemeTableau10);

    // Compute the position of each group on the pie:
    let pie = d3
        .pie()
        .sort(null) // Do not sort group by size
        .value((d) => d[1]);
    let data_ready = pie(Object.entries(data));

    // The arc generator
    let arc = $derived(d3
        .arc()
        .innerRadius(radius * 0.5) // This is the size of the donut hole
        .outerRadius(radius * 0.8));

    console.log(title, "Arc:", data_ready);

    $effect(()=>{
        console.log(title, "Arc Changed:", data_ready);
    });
    // Another arc that won't be drawn. Just for labels positioning
    const outerArc = d3
        .arc()
        .innerRadius(radius * 0.9)
        .outerRadius(radius * 0.9);
</script>


<svg
    {width}
    {height}
    viewBox="{-width / 2}, {-height / 2}, {width}, {height}"
    style:max-width="100%"
    style:height="auto"
>
    <text x={xScale(50)} y={yScale(90)} text-anchor="middle" class="title">{title}</text>
    <line x1={xScale(0)} y1={yScale(85)} x2={xScale(100)} y2={yScale(85)} stroke="black" />

    <g class="chart-inner" transform="translate(0, {height / 12}) scale(1.15,1.15)">
        {#each data_ready as slice}
            <path d={arc(slice)} fill={color(slice.data[1])} stroke="white" />
        {/each}
    </g>
</svg>


<style>
	:global(body) {
		margin: 0;
	}
    svg {
        border: 1px solid black;
        border-radius: 6px;
    }
    .chart-inner {
        width: 100vw;
        height: 100vh;
    }
    .title {
        font: bold 15px sans-serif;
    }
</style>
