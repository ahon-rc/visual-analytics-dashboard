<script>
    import ContinentBarplot from './Continent_Barplot.svelte';
    import Barplot from './Continent_Barplot.svelte';
    import Scatterplot from './Scatterplot.svelte';
	const { data } = $props();
    let continents = [];
    for(let i = 0; i<data.world.length; i++)
    {
        var value = data.world[i]['Continent'];
        if(continents.includes(value) || value == undefined)
        { continue; }
        else
        {
            continents.push(value)
        }
    }
    console.log(continents)
    const div_1_width = 600;
    const div_1_height = 300;
</script>

<center><h1 style="font-family:monospace"><u>World Population</u></h1></center>
<hr>
<div style="height: { div_1_height+60 }px; width:  { div_1_width }px;" class = "box">
    <h3 style="padding-left: 10px; padding-top: 1px">2022 Projections:</h3>
    <ContinentBarplot data={ data.world } div_width = { div_1_width } div_height = { div_1_height } continent = { continents }>
    </ContinentBarplot>
</div>



<style>
    .box {
        box-shadow: 0px 5px 10px 0px rgba(0, 0, 0, 0.5);
        border-radius: 20px;
        border-color: black;
        padding: 0;
    }
</style>