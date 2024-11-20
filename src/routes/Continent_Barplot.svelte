<script>
	import { scaleLinear } from "d3-scale";
	import { bin } from "d3-array";

	let {
		data = [],
		div_width = 100,
		div_height = 100,
		continent = [],
	} = $props();

	let population = {};
	for (let i = 0; i < continent.length; i++) {
		population[continent[i]] = 0;
	}
	for (let i = 0; i < data.length; i++) {
		population[data[i]["Continent"]] += parseInt(
			data[i]["2022 Population"]
		);
	}

	let formatter = Intl.NumberFormat("en", { notation: "compact" });

	const width = div_width;
	const height = div_height;
	const axisX = scaleLinear().domain([0, 100]).range([0, width]);
	const axisY = scaleLinear().domain([0, 100]).range([height, 0]);
	const origin_x = 5;
	const origin_y = 17.5;
	var color_check = $state("antiquewhite");

	let max_pop = Math.max(...Object.values(population));
	let min_pop = Math.min(...Object.values(population));

	const min = min_pop - 20 * 10 ** 6;
	const max = max_pop;

	const scaleX = scaleLinear()
		.domain([0, continent.length + 1])
		.range([axisX(origin_x), axisX(origin_x + 88)]);
	const scaleY = scaleLinear()
		.domain([min, max])
		.range([axisY(origin_y), axisY(origin_y + 77.5)]);

	console.log("Range:", axisY(100), "->", axisY(origin_y));
	console.log(scaleY(max_pop));
	const barX = scaleLinear()
		.domain([0, continent.length + 1])
		.range([axisX(origin_x), axisX(origin_x + 88)]);
	const barY = scaleLinear()
		.domain([min, max])
		.range([axisY(origin_y + 77.5), axisY(origin_y)]);

	var histGenerator = bin().domain([min, max]).thresholds(10);

	var bins = histGenerator(Object.values(population));
	let ct = bins.length;
	bins = bins.map((d) => {
		d.index = ct;
		ct -= 1;
		return d;
	});
	console.log(min_pop, "->", barY(min_pop), max_pop, "->", barY(max_pop));
	console.log("Original", population["Asia"]);
	for (let i = 0; i < continent.length; i++) {
		console.log(
			Object.keys(population)[i],
			":",
			formatter.format(population[continent[i]])
		);
	}
	console.log("bins:", bins);
</script>

<svg width="100%" height="100%" class="graph">
	<g class="labels y-labels">
		{#each bins as y_labels}
			{console.log(y_labels)}
			<text
				x={barX(0) - 30}
				y={scaleY(y_labels["x0"]) + 4}
				style="font-size: small; font-family: monospace"
			>
				{formatter.format(y_labels["x0"])}
			</text>
			<g
				class="ticks y-ticks"
				transform="translate(0,{scaleY(max) + scaleY(min)}) scale(1,-1)"
			>
				<line
					x1={barX(0) - 2}
					x2={barX(continent.length + 1)}
					y1={barY(y_labels["x0"])}
					y2={barY(y_labels["x0"])}
				></line>
			</g>
		{/each}
	</g>

	<g class="labels x-labels">
		{#each [...continent.keys()] as label_index}
			<g
				transform="translate({axisX(origin_x) -
					145 +
					label_index * 10}, {axisY(origin_y) +
					label_index * 37 -
					165})"
			>
				<text
					x={scaleX(label_index + 1)}
					y={scaleY(0) + 20}
					text-anchor="end"
					alignment-baseline="middle"
					transform="rotate(-30)"
					style="font-size: small; font-family: monospace"
				>
					{continent[label_index]}
				</text>
			</g>

			<g class="ticks x-ticks">
				<line
					x1={scaleX(label_index + 1)}
					x2={scaleX(label_index + 1)}
					y1={axisY(origin_y - 1)}
					y2={axisY(origin_y)}
				></line>
			</g>
		{/each}
	</g>

	<g class="histogram">
		{#each [...continent.keys()] as index}
			{console.log(
				index,
				":",
				continent[index],
				"->",
				formatter.format(population[continent[index]])
			)}
			{console.log(
				index,
				":",
				formatter.format(population[continent[index]]),
				":",
				barY(population[continent[index]])
			)}
			<g
				transform="translate(0,{scaleY(max) + scaleY(min)}) scale(1,-1)"
				class="bars"
			>
				<rect
					height={barY(population[continent[index]]) - 15}
					width="40"
					x={scaleX(index + 0.75)}
					y={scaleY(max)}
				></rect>
			</g>
			<g class="text">
				<text
					x={scaleX(index + 1) - 10}
					y={barY(max - population[continent[index]])}
				>
					{formatter.format(population[continent[index]])}
				</text>
			</g>
		{/each}
	</g>

	<g class="grid y-grid">
		<line
			x1={axisX(origin_x)}
			x2={axisX(origin_x)}
			y1={axisY(origin_y)}
			y2={axisY(origin_y + 77.5)}
		></line>
	</g>
	<g class="grid x-grid">
		<line
			x1={axisX(origin_x)}
			x2={axisX(origin_x + 88)}
			y1={axisY(origin_y)}
			y2={axisY(origin_y)}
		></line>
	</g>
</svg>

<style>
	.graph {
		padding: 2%;
	}

	.graph .grid {
		stroke: #000000;
		stroke-dasharray: 0;
		stroke-width: 2;
	}

	.graph .labels .ticks {
		stroke: #464646;
		stroke-dasharray: 0;
		stroke-width: 1;
	}

	.bars {
		fill: antiquewhite;
		fill-opacity: 80%;
		border-color: black;
		border-width: 1px;
	}

	.histogram .text {
		fill: black;
		font-family: "Courier New", Courier, monospace;
		font-weight: bold;
		font-size: x-small;
	}

	.bars :hover {
		fill: rgb(253, 210, 155);
		fill-opacity: 100%;
		border-color: black;
		border-width: 1px;
	}

	.y-ticks {
		opacity: 40%;
	}
</style>
