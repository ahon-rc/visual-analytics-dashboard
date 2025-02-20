<script>
	import Chart from "chart.js/auto";
	import { onMount } from "svelte";
	import * as d3 from "d3";
	import RangeSlider from "svelte-range-slider-pips";

	let { width = $bindable(), height = $bindable(), d1, d2, pi } = $props();
	let ctx, pie_1, pie_2, pie_4, chart, pi1, pi2, pi4;

	const sum = (a) => eval(a.join("+"));
	const getValues = (dic) => {
		return Object.values(dic).map(
			(x) => (x / sum(Object.values(dic)).toFixed(4)) * 100
		);
	};
	const data = {
		labels: Object.keys(d2),
		datasets: [
			{
				label: "2016",
				data: getValues(Object.values(d1)),
				fill: false,
				borderColor: "#36A2EB",
				backgroundColor: "#9AD0F5",
			},
			{
				label: "2019",
				data: getValues(Object.values(d2)),
				fill: false,
				borderColor: "#FF6384",
				backgroundColor: "#FFB1C1",
			},
		],
	};
	var year = $state(2014);
	var color = [
		d3
			.scaleOrdinal()
			.domain(Object.keys(pi["2014"][0]))
			.range(d3.schemeTableau10),
		d3
			.scaleOrdinal()
			.domain(Object.keys(pi["2014"][1]))
			.range(d3.schemeCategory10),
		d3
			.scaleOrdinal()
			.domain(Object.keys(pi["2014"][2]))
			.range(d3.schemeAccent),
		d3
			.scaleOrdinal()
			.domain(Object.keys(pi["2014"][3]))
			.range(d3.schemeSet1),
	];

	var getColor = (keys, index) => {
		keys = keys.map((x) => color[index](x));
		return keys;
	};
	const data_pi = {
		2014: [
			{
				labels: Object.keys(pi["2014"][0]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2014"][0]),
						backgroundColor: getColor(
							Object.keys(pi["2014"][0]),
							0
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2014"][1]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2014"][1]),
						backgroundColor: getColor(
							Object.keys(pi["2014"][1]),
							1
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2014"][2]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2014"][2]),
						backgroundColor: getColor(
							Object.keys(pi["2014"][2]),
							2
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2014"][3]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2014"][3]),
						backgroundColor: getColor(
							Object.keys(pi["2014"][3]),
							3
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
		],
		2016: [
			{
				labels: Object.keys(pi["2016"][0]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2016"][0]),
						backgroundColor: getColor(
							Object.keys(pi["2016"][0]),
							0
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2016"][1]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2016"][1]),
						backgroundColor: getColor(
							Object.keys(pi["2016"][1]),
							1
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2016"][2]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2016"][2]),
						backgroundColor: getColor(
							Object.keys(pi["2016"][2]),
							2
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2016"][3]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2016"][3]),
						backgroundColor: getColor(
							Object.keys(pi["2016"][3]),
							3
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
		],
		2018: [
			{
				labels: Object.keys(pi["2019"][0]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2019"][0]),
						backgroundColor: getColor(
							Object.keys(pi["2019"][0]),
							0
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2019"][1]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2019"][1]),
						backgroundColor: getColor(
							Object.keys(pi["2019"][1]),
							1
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2019"][2]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2019"][2]),
						backgroundColor: getColor(
							Object.keys(pi["2019"][2]),
							2
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
			{
				labels: Object.keys(pi["2019"][3]),
				datasets: [
					{
						label: "Mental Health Benefits",
						data: Object.values(pi["2019"][3]),
						backgroundColor: getColor(
							Object.keys(pi["2019"][3]),
							3
						),
						hoverOffset: 4,
						hoverBorderJoinStyle: "round",
						hoverOffset: 7,
					},
				],
			},
		],
	};

	function updatePies() {
		if (pi1) pi1.destroy();
		if (pi2) pi2.destroy();
		if (pi4) pi4.destroy();

		pi1 = new Chart(pie_1, {
			type: "pie",
			data: data_pi[year][0],
			options: {
				plugins: {
					aspectRatio: 1.25,
					legend: {
						position: "right",
						labels: {
							font: {
								size: height / 80,
							},
							boxWidth: width / 42,
						},
					},
					title: {
						display: true,
						text: "MH Medical Coverage Provided?",
						padding: 0,
					},
				},
			},
		});

		pi2 = new Chart(pie_2, {
			type: "pie",
			data: data_pi[year][1],
			options: {
				plugins: {
					aspectRatio: 1.25,
					legend: {
						position: "right",
						labels: {
							font: {
								size: height / 80,
							},
							boxWidth: width / 42,
						},
					},
					title: {
						display: true,
						text: "MH Resources Provided?",
						padding: 0,
					},
				},
			},
		});

		pi4 = new Chart(pie_4, {
			type: "pie",
			data: data_pi[year][3],
			options: {
				aspectRatio: 1.75,
				plugins: {
					legend: {
						position: "right",
						labels: {
							boxWidth: width / 42,
						},
					},
					title: {
						display: true,
						text: "Easy to get Medical Leave for MH Issues?",
						padding: {
							bottom: 0,
						},
					},
				},
			},
		});
	}

	function updateChart() {
		if (chart) chart.destroy();

		{
			console.log("\n\nYEAR:", year, "\n\n");
		}
		chart = new Chart(ctx, {
			type: "bar",
			data: data,
			options: {
				indexAxis: "y",
				// Elements options apply to all of the options unless overridden in a dataset
				// In this case, we are setting the border of each horizontal bar to be 2px wide
				elements: {
					bar: {
						borderWidth: 2,
					},
				},
				aspectRatio: 1.6,
				plugins: {
					legend: {
						position: "top",
						labels: {
							font: {
								size: height / 65,
							},
						},
					},
				},
			},
		});

		updatePies();
	}

	onMount(() => {
		if (typeof window !== "undefined") {
			// Ensure we are in the browser
			updateChart();
			window.addEventListener("resize", updateChart);
		}
	});

    $effect (() => updatePies())
</script>

<div class="main">
    <center
		><h2
			style="font-family:monospace; margin-top:0.5vh; margin-bottom:0vh;"
		>
			Mental Health Disorder Distribution (in %)
		</h2></center
	>
	<canvas bind:this={ctx} style="padding: 0.7vw; border-bottom-width: 3px; border-bottom-color: grey; border-bottom-style: ridge;"></canvas>
	<center
		><h2
			style="font-family:monospace; margin-top:0.5vh; margin-bottom:1.5vh;"
		>
			Company Policies on Mental Health
		</h2></center
	>
	<div
		class="bottom-container"
		style="height: {(height / 2)-30}px;"
	>
		<div style="width: fit-content; padding-left: 1vw; height: {(height / 2)-30}px;">
			<h2
				style="font-family:monospace; margin-top:0vh; margin-bottom:0vh; color: hsl(332.4, 31.6%, 77.1%);"
			>
				Year
			</h2>
			<RangeSlider
				bind:value={year}
				id="always"
				min={2014}
				max={2018}
				step={2}
				vertical
				pips
				all="label"
				on:change={(e) => {
					updatePies();
				}}
			/>
		</div>
		<div class="right" style="width: {(width * 7) / 8}px;">
			<div class="bottom" style="width: 100%; height: {height / 4 - 15}px;">
				<canvas bind:this={pie_2} class="2"></canvas>
				<canvas bind:this={pie_1} class="1"></canvas>
			</div>
			<div class="bottomer" style="width: 100%; height: {height / 4 - 15}px;;">
				<canvas bind:this={pie_4} class="pi4"></canvas>
			</div>
		</div>
	</div>
</div>

<style>
	:global(.rangeSlider) {
		padding-top: 3vh !important;
		height: 34vh !important;
		font-size: 1rem;
	}

	.main {
		height: 100%;
	}

	.bottom-container {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}

	.right {
	}
	.bottom {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-around;
	}

	.bottomer {
		display: flex;
		justify-content: center;
	}

	:root {
		--range-slider: hsl(345, 94.6%, 71%);
		--range-handle-inactive: hsl(345, 94.6%, 71%);
		--range-handle: hsl(234, 67.6%, 71%);
		--range-handle-focus: hsl(333.2, 47.5%, 84.3%);
		--range-handle-border: hsl(333.2, 47.5%, 84.3%);
		--range-range-inactive: hsl(343.8, 100%, 94.9%);
		--range-range: hsl(343.8, 100%, 94.9%);
		--range-float-inactive: hsl(162, 39.2%, 80%);
		--range-float: hsl(333.2, 47.5%, 84.3%);
		--range-float-text: hsl(0, 0%, 100%);

		--range-pip: hsl(0, 57.9%, 85.1%);
		--range-pip-text: hsl(0, 0%, 100%);
		--range-pip-active: hsl(332.4, 31.6%, 77.1%);
		--range-pip-active-text: hsl(332.5, 42.7%, 72%);
		--range-pip-hover: hsl(0, 0%, 47.1%);
		--range-pip-hover-text: hsl(180, 2.2%, 55.1%);
		--range-pip-in-range: hsl(180, 5.9%, 20%);
		--range-pip-in-range-text: hsl(300, 12.1%, 17.8%);

		font-size: 11px;
	}
</style>
