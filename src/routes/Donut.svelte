<script>
    import * as d3 from 'd3';

    let { height = $bindable(), width = $bindable(), margin, dic={}, theme = 'dark', title = 'Pie Plot' } = $props();
  // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    let radius = $derived(Math.min(width, height) / 2 - margin);
    
    const data = dic;
    
    let xScale = $derived(d3.scaleLinear().domain([0, 100]).range([-width, width]));
    let yScale = $derived(d3.scaleLinear().domain([0, 100]).range([height/2, -height/2]));

    let xHoverScale = $derived(d3.scaleLinear().domain([0, 100]).range([0, radius*1.10]));
    let yHoverScale = $derived(d3.scaleLinear().domain([0, 100]).range([0, radius*1.10]));

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
    let data_ready = $derived(pie(Object.entries(data)));

    // The arc generator
    let arc = $derived(d3
        .arc()
        .innerRadius(radius * 0.5) // This is the size of the donut hole
        .outerRadius(radius * 0.8));

    let hoverArc = $derived(d3
        .arc()
        .innerRadius(radius * 0.55) // This is the size of the donut hole
        .outerRadius(radius * 0.85));
    
    let hoverData = $state({ "key": undefined, "value": undefined });
    $effect(()=>console.log("Scale =", xScale(42)))
</script>

<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
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
            <path d={hoverData["key"]==slice.data[0] ? hoverArc(slice) : arc(slice)} 
            transition:draw={{ duration: 5000, delay: 0, easing: quadInOut }}
            fill={hoverData["key"]==slice.data[0] ? d3.color(color(slice.data[1])).darker(0.5) : color(slice.data[1])}
            stroke="white" 
            onmouseenter={() => { hoverData = { "key": slice.data[0], "value": slice.data[1] }; }}
            onmouseleave={() => { hoverData = { "key": undefined, "value": undefined }; }}
            role="button"
            tabindex="0"/>
        {/each}
    </g>
    {#if hoverData["key"]}
        <foreignObject x={xHoverScale(-49.5)} y={yHoverScale(-32)} width= {xHoverScale(100)} height= {yHoverScale(100)} style="font-family: 'Orbitron', sans-serif;">
            <strong class="up">{hoverData["value"]}</strong>
            <div class="down">{hoverData["key"]}</div>
        </foreignObject>
    {/if}
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

    foreignObject {
        text-align: center;
        background: rgba(182, 159, 173, 0.7); 
        box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.3);
        border-radius: 100%;
        padding-top: 4vh;
    }

    .up {
        font-size: 20px;
    }

    .down {
        font-size: 12px;
    }
</style>
