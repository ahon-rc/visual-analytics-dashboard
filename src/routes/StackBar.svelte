<script>
    import * as d3 from 'd3';
    import { bin } from "d3-array";

    let { height = $bindable(400), width = $bindable(650), margin, dic={}, theme = 'dark', title = 'Bar Plot' } = $props();

    let xScale = $derived(d3.scaleLinear().domain([0, 100]).range([0, width]));
    let yScale = $derived(d3.scaleLinear().domain([0, 100]).range([height, 0]));
    let barAreaTop = $derived(yScale(80));
    let barAreaBot = $derived(height-30);
    let barAreaLeft = $derived(xScale(10));
    let barAreaRight = $derived(width-50);
    const total = Object.keys(dic).length+2;

    let values = [];
    for(let i=0; i<total-2;i++)
        values[i] = Object.values(dic)[i][0];

    let max_val = Math.max(...Object.values(values));
	let min_val = Math.min(...Object.values(values));

    let barScaleX = $derived(d3.scaleLinear().domain([0, total-2]).range([barAreaLeft, barAreaRight]));
    let barScaleY = $derived(d3.scaleLinear().domain([0, max_val+20]).range([barAreaBot, barAreaTop]));
    
    let tempY = $derived(d3.scaleLinear().domain([0, max_val+20]).range([barAreaTop, barAreaBot]));

    var binGenerator = bin().domain([0, max_val]).thresholds(5);
	var y_axis = binGenerator(Object.values(values));

    var font_size = $derived(100/(total-2));


</script>

<svg version="1.1" style="font-family: Roboto; font-size: 12px;" 
    {width}
    {height}
    viewBox="0, 0, {width}, {height}"
    style:max-width="100%"
    style:height="auto"
    aria-hidden="false" 
    aria-label="Interactive chart">

    <text x={xScale(50)} y={yScale(90)} text-anchor="middle" class="title">{title}</text>
    <line x1={xScale(0)} y1={yScale(85)} x2={xScale(100)} y2={yScale(85)} stroke="black" />
    
    <g data-z-index="1" aria-hidden="true" class="x-tick-lines">
        {#each y_axis as val}
            {console.log(val['x1'])}
            <line x1={barScaleX(-0.1)} y1={barScaleY(val['x1'])} x2={barScaleX(total-1.25)} y2={barScaleY(val['x1'])}
            fill="none" stroke="#5e5e5e" stroke-width="1" stroke-dasharray="none" opacity="0.75"/>
        {/each}
    </g>

    <g data-z-index="1" opacity="1" class="axes">
        <line x1={barScaleX(0)} x2={barScaleX(total-1.25)} y1={barScaleY(0)} y2={barScaleY(0)} stroke-width="1.5" fill="black" stroke="#000000"/>
        <line x1={barScaleX(0)} x2={barScaleX(0)} y1={barScaleY(0)} y2={barScaleY(max_val+10)} stroke-width="1.5" fill="black" stroke="#000000"/>
    </g>
    
    <g data-z-index="1" opacity="1" aria-hidden="false" style="outline: none;" 
    class="bars">
        {#each Object.values(dic) as values, idx}
            <rect x={barScaleX(idx)+20} y={barScaleY(max_val+16)} width="30" height={tempY(values[1])-tempY(0)} fill="#94d13d" stroke="#fff" stroke-width="0.5" 
            opacity="1" transform="translate(0, {barScaleY(max_val+20) + barScaleY(0)}) scale(1,-1)"/>
            <rect x={barScaleX(idx)+20} y={barScaleY(max_val+16-values[1])} width="30" height={tempY(values[2])-tempY(0)} fill="#ff564d" stroke="#fff" stroke-width="0.5" 
            opacity="1" transform="translate(0, {barScaleY(max_val+20) + barScaleY(0)}) scale(1,-1)"/>
            <rect x={barScaleX(idx)+20} y={barScaleY(max_val+16-values[1]-values[2])} width="30" height={tempY(values[3])-tempY(0)} fill="#6f58e9" stroke="#fff" stroke-width="0.5" 
            opacity="1" transform="translate(0, {barScaleY(max_val+20) + barScaleY(0)}) scale(1,-1)"/>

            <rect x={barScaleX(idx)+20} y={barScaleY(max_val+16)} width="30" height={tempY(values[0]+0.5)-tempY(0)} fill="none" stroke="#000000" stroke-width="0.5" 
            opacity="1" transform="translate(0, {barScaleY(max_val+20) + barScaleY(0)}) scale(1,-1)"/>
        {/each}
    </g>

    <g data-z-index="1" opacity="1" aria-hidden="false" style="outline: none;" class="ticks-labels">
        {#each Object.keys(dic) as label, idx}
            <text font-family='Roboto-Regular,Roboto' x={barScaleX(idx)+35} y={barScaleY(-30)} text-anchor="middle" style="color: rgb(51, 51, 51); font-size: 0.50vw; 
                fill: rgb(51, 51, 51);" aria-hidden="true" alignment-baseline="middle">
                {label}
            </text>
        {/each}
        {#each y_axis as val}
            <text x={barScaleX(-0.4)} y={barScaleY(val['x1'])+4} font-family='Roboto-Regular,Roboto'
            text-anchor="middle" style="color: rgb(102, 102, 102); font-size: 0.6vw;" aria-hidden="true">{val['x1']}</text>
        {/each}
    </g>
</svg>

<style>
    .title {
        font: bold 15px sans-serif;
    }

    svg {
        border: 1px solid black;
        border-radius: 6px;
    }
</style>