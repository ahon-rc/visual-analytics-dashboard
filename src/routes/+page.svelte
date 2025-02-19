<script>
    import Donut from "./Donut.svelte";
    import ChoroplethMap from "./ChloroplethMap.svelte";
    import * as d3 from 'd3';
	import StackBar from "./StackBar.svelte";
    import Sunburst from "./Sunburst.svelte";
    import GroupedChart from "./GroupedChart.svelte";
	
    const { data } = $props();
    let div_1_width = $state(400);
    let div_1_height = $state(851);
    let div_2_height = $state(0);
    let chloro_height = $state(300);
    let pie_height = $state(250);
    let donutWidth = $state(200);
    let half_height = $state(500);
    $effect(() => donutWidth = div_1_width/2 -15);
    $effect(() => pie_height = ((div_1_height-chloro_height)/2)-20);
    $effect(()=>console.log('height:',div_1_height, '\nAlso Changed:', half_height));
    const dataset = data.mhd;
    // ****************************************************
    // Donut for Age
    let ages = [];
    for(let i=0; i<dataset.length; i++){
        if(dataset[i]['age']==undefined)
            continue;
        ages.push(parseInt(dataset[i]['age']));
    }
    let top = Math.max(...ages);
    let bot = Math.min(...ages);

    var histGenerator = d3.bin().domain([bot, top]).thresholds(10);
	var bins = histGenerator(ages);
	let age_dic = {}
    for(let i=0;i<bins.length;i++){
        let start = Math.floor(bins[i]['x0']/5)*5;
        let end = Math.ceil(bins[i]['x1']/5)*5;
        
        if(i!=0)
            start += 1;
        age_dic[start+' - '+end] = bins[i]['length'];
    }
    // ****************************************************
    // Donut for Sex
	let sex_dic = {}
    for(let i=0;i<dataset.length;i++){
        let key = dataset[i]['sex'];
        if(key != undefined){
            if(Object.keys(sex_dic).includes(key))
                sex_dic[key] += 1;
            else
                sex_dic[key] = 1;
        }
    }
    // ****************************************************
    // Donut for Sex
	let role_dic = {}
    for(let i=0;i<dataset.length;i++){
        let key = dataset[i]['work_position'];
        if(key != undefined){
            if(Object.keys(role_dic).includes(key))
                role_dic[key] += 1;
            else
                role_dic[key] = 1;
        }
    }
    // ****************************************************
    // Bar Plot for Company Size
    let comp_dic = {}
    for(let i=0;i<dataset.length;i++){
        let key = dataset[i]['comp_no_empl'];
        if(key != undefined){
            if(Object.keys(comp_dic).includes(key))
                comp_dic[key][0] += 1;
            else
                comp_dic[key] = [1,0,0,0];

            if(dataset[i]['remote_flag']=="Never")
                comp_dic[key][1] += 1;
            else if(dataset[i]['remote_flag']=="Always")
                comp_dic[key][2] += 1;
            else
                comp_dic[key][3] += 1;
        }
        
    }

    const disease = data.diss;
</script>

<h1 style="font-family:monospace"><u>OSMI Mental Health in Tech Survey</u></h1>
<hr>
<div class="main-background">
    <main class="chart-container" bind:clientWidth={div_1_width} bind:clientHeight={div_1_height}>
        <center><h3 style="font-family:Courier New, Courier, monospace; margin-top:0vh; margin-bottom:0vh;">Responders' Profile</h3></center>
        <ChoroplethMap
            data={data.mhd}
            world={data.idk} 
            width={div_1_width}
            height={chloro_height}
        />
        <main class="pies-container">
            <div class="top-row" style="width:{div_1_width} height:{pie_height}">
                <Donut
                    bind:width={donutWidth}
                    bind:height={pie_height}
                    margin=20
                    dic= {age_dic}
                    title = 'Age Distribution'
                />
                <Donut
                    bind:width={donutWidth}
                    bind:height={pie_height}
                    margin=20
                    dic= {sex_dic}
                    theme = 'tableu'
                    title = 'Gender Distribution'
                />
            </div>
            <div class="bottom-row" style="width:{div_1_width} height:{pie_height}">
                <StackBar
                    bind:width={donutWidth}
                    bind:height={pie_height}
                    dic= {comp_dic}
                    margin= {chloro_height+pie_height}
                    title= 'Company Size'
                />
                <Donut
                    bind:width={donutWidth}
                    bind:height={pie_height}
                    margin=20
                    dic= {role_dic}
                    theme = 'tableu'
                    title = 'Job Roles'
                />
            </div>
        </main>
    </main>

    <main class="chart-container-2" bind:clientWidth={div_1_width} bind:clientHeight={div_2_height}>
        <center><h3 style="font-family:Courier New, Courier, monospace; margin-top:0vh; margin-bottom:0vh;">Company Policies for MHD</h3></center>
        <GroupedChart
            bind:width={div_1_width}
            bind:height={div_1_height}
            d1={data.d_16}
            d2={data.d_19}
        />
    </main>

    <main class="chart-container" bind:clientWidth={div_1_width} bind:clientHeight={div_1_height}>
        <center><h3 style="font-family:Courier New, Courier, monospace; margin-top:0vh; margin-bottom:0vh;">Family History of Mental Health vs Willingness to Discuss it with Co-Workers</h3></center>
        <Sunburst
            width={div_1_width}
            height={div_1_height}
            dic={data.tree}
            dic14={data.tree_14}
            dic16={data.tree_16}
            dic19={data.tree_19}
        />
    </main>
</div>


<style>
    .main-background {
        display: flex;
        flex-direction: row;
    }

    .chart-container {
        box-shadow: 0px 5px 10px 0px rgba(0, 0, 0, 0.5);
        border-radius: 20px;
        border-color: black;
        padding: 0;
        margin-left: 0.5vw;
        
        width: 35vw;
        height: 90vh;

        font-family: "Helvetica";
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .chart-container-2 {
        box-shadow: 0px 5px 10px 0px rgba(0, 0, 0, 0.5);
        border-radius: 20px;
        border-color: black;
        padding: 0;
        margin-left: 0.5vw;
        
        width: 35vw;
        height: 90vh;

        font-family: "Helvetica";
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .pies-container {
        border-top-width: 3px;
        border-top-color: grey;
        border-top-style: ridge;

        display: flex;
        flex-direction: column;
        padding: 0.25vw;
    }

    .top-row,.bottom-row {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        padding-top: 0.5vh;
        padding-bottom: 0.5vh;
    }
</style>