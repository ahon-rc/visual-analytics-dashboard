<script>
	import { geoPath, geoNaturalEarth1, geoAzimuthalEqualArea } from  "d3-geo";
	import { draw } from "svelte/transition";
	import { quadInOut } from "svelte/easing";

	const {data, world, width, height } = $props();

    let projection = $derived(geoNaturalEarth1().fitSize([width, height], world));
    let pathGen =  $derived(geoPath(projection));
	$inspect(width,height);
	let countries = $derived(world.features.map(feature => {
		return {
			...feature,
			path: pathGen(feature)
			}
	}));
	
	let hoveredCountryId = $state(null);
</script>

<svg {width} {height}>
	{#each countries as { id,path }}
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<path
			transition:draw={{ duration: 5000, delay: 0, easing: quadInOut }}
			d={path}
			class:active = {hoveredCountryId===id}
			onmouseenter={()=>hoveredCountryId = id}
			onmouseout={() => {hoveredCountryId = undefined}}
		/>
	{/each}
</svg>

<style>
    path {
        fill: darkgreen;
        stroke:darkgreen;
		opacity: 0.4;
		transition: opacity 0.4s ease-in-out;
		transition-delay: 0.4s;
    }

	path.active {
		fill: darkgreen;
		opacity: 0.6;
		transition-duration: 0s;
		transition-delay: 0s;
	}
</style>