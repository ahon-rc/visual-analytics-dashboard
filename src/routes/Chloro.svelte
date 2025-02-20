<script>
	import { getContext, createEventDispatcher } from 'svelte';
	import { geoPath } from 'd3-geo';
	import { raise } from 'layercake';

	
    const { data, width, height, zGet } = getContext('LayerCake');
    
    const { projection, fixedAspectRatio = undefined, fill, stroke = '#333', strokeWidth = 0.5, features } = $props();
    const dispatch = createEventDispatcher();

	let fitSizeRange = $derived(fixedAspectRatio ? [100, 100 / fixedAspectRatio] : [$width, $height]);

	let projectionFn = $derived(projection().fitSize(fitSizeRange, $data));

	let geoPathFn = $derived(geoPath(projectionFn));

	function handleMousemove(feature) {
		return function handleMousemoveFn(e) {
			raise(this);
			// When the element gets raised, it flashes 0,0 for a second so skip that
			if (e.layerX !== 0 && e.layerY !== 0) {
				dispatch('mousemove', { e, props: feature.properties });
			}
		}
	}
</script>

    <g
        class="map-group"
        on:mouseout={(e) => dispatch('mouseout')}
        on:blur={(e) => dispatch('mouseout')}
    >
        {#each (features || $data.features) as feature}
            <path
                class="feature-path"
                fill="{fill || $zGet(feature.properties)}"
                stroke={stroke}
                stroke-width={strokeWidth}
                d="{geoPathFn(feature)}"
                on:mouseover={(e) => dispatch('mousemove', { e, props: feature.properties })}
                on:focus={(e) => dispatch('mousemove', { e, props: feature.properties })}
                on:mousemove={handleMousemove(feature)}
            ></path>
        {/each}
    </g>

<style>
	/* .feature-path {
		stroke: #333;
		stroke-width: 0.5px;
	} */
	.feature-path:hover {
		stroke: #000;
		stroke-width: 2px;
	}
	.feature-path:focus {
		outline: none;
	}
</style>
