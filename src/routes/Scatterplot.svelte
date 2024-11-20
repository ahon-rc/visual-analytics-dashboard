<script>
    import { scaleLinear } from 'd3-scale';
    let { datapoints = [], long = 'from_long', lat = 'from_lat' } = $props();

    const xScale = scaleLinear().domain([-180, 180]).range([0, 800]);
    const yScale = scaleLinear().domain([-90, 90]).range([400, 0]);

    const width = 800
    const height = 400
</script>

<svg width = { width } height = { height }>
  {#each datapoints as datapoint}
    <circle cx={xScale(datapoint[long])}
            cy={yScale(datapoint[lat])}
            r=3
            class:international="{datapoint.from_country != datapoint.to_country}" />
  {/each}
</svg>

<style>
  circle {
    opacity: 0.5;
    fill: blue;
  }
  circle.international {
    fill: red;
  }
</style>