<script>
    import { onMount, onDestroy } from "svelte";
    import * as d3 from "d3";

    let container;
    let svg, arc, lineChartSvg;
    let {width, height, dic, dic14, dic16, dic19} = $props();
    let pentagonWidth = width/3.5;
    let pentagonHeight = height/30;
    let arrowLength = pentagonHeight/3;
    
    let pentagonSpacing = -5;
    let YPos;

    let lineChartHeight = height/3.5;
    let lineChartMargin = { top: 5, right: 50, bottom: 20, left: 60 };
    let linePath;
    let xScale = d3.scaleLinear().domain([0, 4]).range([0, width - lineChartMargin.left - lineChartMargin.right]);
    let yScale = d3.scaleLinear().domain([0, 100]).range([lineChartHeight, 0]);
    const years = ["", "2014", "2016", "2019"];

    const order = [{ "Family History": 0, "No Family History": 1 }, { "Male": 0, "Female": 1, "LGBTQ+": 2 }, { "Yes": 0, "No": 1, "Maybe": 2 }];

    function getcolor(color) {
        let temp = color;
        while (temp.parent != null && temp.parent.data.name != "root")
            temp = temp.parent;

        let shade = '';
        if (temp.data.name == "Family History") {
            let FHColor = d3.scaleLinear().domain([1, 3]).range(["#4CC3D9", "#68FFFF"]);
            shade = FHColor(color.depth);
        } else if (temp.data.name == "No Family History") {
            let NFHColor = d3.scaleLinear().domain([1, 3]).range(["#FFC65D", "#FCF5C6"]);
            shade = NFHColor(color.depth);
        } else return "#fff";

        const shade_dic = { 2: { "Male": 0.2, "Female": 0.1, "LGBTQ+": 0 }, 3: { "Yes": 0.2, "No": 0.1, "Maybe": 0 } };
        if (color.depth !== 1) {
            return d3.color(shade).darker(shade_dic[color.depth][color.data.name]);
        }
        return shade;
    }

    function updateChart() {
        if (!container) return;

        // Get the container siz8
        width = container.clientWidth;
        height = container.clientHeight;
        let radius = Math.min(width, height) / 3;
        pentagonWidth = width/3.5;
        pentagonHeight = height/30;
        arrowLength = pentagonHeight/3;
        
        xScale = d3.scaleLinear().domain([0, 4]).range([0, width - lineChartMargin.left - lineChartMargin.right]);
        let yScale = d3.scaleLinear().domain([0, 100]).range([lineChartHeight-lineChartMargin.bottom, 0]);
        YPos = height / 3.5 + height/10000; 


        // Remove previous chart before re-rendering
        d3.select(container).select("svg").remove();
        d3.select(container).select("svg").remove();

        svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height-lineChartHeight-pentagonHeight)
            .append("g")
            .attr("transform", `translate(${width / 2},${height / 3.7})`);

        let partition = d3.partition().size([2 * Math.PI, radius]);

        let root = d3.hierarchy(dic)
            .sum(d => d.value || 1)
            .sort((a, b) => b.value - a.value);

        partition(root);

        arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .innerRadius(d => d.y0)
            .outerRadius(d => d.y1);

        let paths = svg.selectAll("path")
            .data(root.descendants())
            .enter()
            .append("path")
            .attr("d", arc)
            .attr("fill", d => getcolor(d))
            .attr("stroke", "#fff")
            .style("cursor", "pointer")
            .on("mouseover", (event, d) => highlightPath(d, paths))
            //.on("mouseout", () => resetHighlight(paths));

        // Adding Labels with proper rotation
        svg.selectAll("text")
            .data(root.descendants())
            .enter()
            .append("text")
            .attr("transform", function (d) {
                let [x, y] = arc.centroid(d);
                let angle = ((d.x0 + d.x1) / 2) * (180 / Math.PI);
                let rotate = angle > 90 && angle < 270 ? angle + 180 : angle;
                rotate = (Math.abs(d.x1 - d.x0) < 0.3) ? rotate + 90 : rotate;
                return `translate(${x},${y}) rotate(${rotate})`;
            })
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .style("font-size", d => Math.abs(d.x1 - d.x0) < 0.3 ? "0.5vw" : "0.65vw")
            .style("fill", "black")
            .text(function(d) { 
                let text = d.depth > 0 ? d.data.name : "";
                text = Math.abs(d.x1 - d.x0) < 0.03 ? "" : text;
                return text;
            })
            .style("pointer-events", "none");

            //----------------------------------------------------------------Line Chart----------------------------------------------------------------
        let measure = Math.min(height, width);
        lineChartHeight = height/3.5;
        lineChartMargin = { top: height/156.6, right: width/8.32, bottom: height/39.15, left: width/9.93 };
        console.log("Equation:",width/60);
        lineChartSvg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", lineChartHeight + lineChartMargin.top + lineChartMargin.bottom)
            .append("g")
            .attr("transform", `translate(${lineChartMargin.left}, ${lineChartMargin.top})`);

        
        let xAxis = lineChartSvg.append("g")
            .attr("class", "x-axis")
            .attr("transform", `translate(0, ${yScale(0)})`)
            .call(d3.axisBottom(xScale).ticks(years.length).tickFormat((d, i) => years[i]));

        
        let yAxis = lineChartSvg.append("g")
            .attr("class", "y-axis")
            .call(d3.axisLeft(yScale).ticks(5));
            
        linePath = lineChartSvg.append("path")
            .attr("class", "line")
            .attr("fill", "none")
            .attr("stroke", "black")
            .attr("stroke-width", 4);

    }

    
    function updateLineChart(node) {
        if (node.depth==0 || !node) return;
        let isLeaf = (node.children) ? false : true;
        let temp = node;
        let path = [];
        while(temp.parent)
        {
            path.push(temp.data.name)
            temp = temp.parent;
        }
        path = path.reverse();
        
        let getValue = (dictionary) => {
            let x = dictionary;
            let total = dictionary['total'];
            for(let i=0; i<node.depth; i++)
            {   
                if(x.count)
                    total = x.count;
                x = x['children'][order[i][path[i]]];
            }
            x = isLeaf ? x['value'] : x['count'];
            //console.log("Path:", path, "\nx:",x, "\nTotal:", total, dictionary);
            return (x/total).toFixed(4)*100;
        };
        let data = [getValue(dic14), getValue(dic16), getValue(dic19)];

        linePath.datum(data)
            .transition()
            .duration(500)
            .attr("stroke", getcolor(node))
            .attr("d", d3.line()
                .x((d, i) => xScale(i+1)) // X-axis: 0, 1, 2
                .y(d => {console.log(d);
                    return yScale(d);}) // Y-axis: Percentage values
            );
    }
    //----------------------------------------------------------------Line Chart----------------------------------------------------------------

    function highlightPath(d, paths) {
        pentagonWidth = width/3.5;
        pentagonHeight = height/30;
        arrowLength = pentagonHeight/3;
        let pathNodes = [];
        let temp = d;
        while (temp.parent) {
            pathNodes.push(temp);
            temp = temp.parent;
        }

        paths.transition()
            .duration(100)
            .style("opacity", d => pathNodes.includes(d) ? 1 : 0.4);

        svg.selectAll(".pentagon").remove();
        svg.selectAll(".pentagon-label").remove();

        let levels = {};
        pathNodes.reverse().forEach(node => {
            if (!levels[node.depth]) 
                levels[node.depth] = [];
            levels[node.depth].push(node);
        });

        // Draw pentagons in horizontal rows
        Object.keys(levels).forEach(depth => {
            let nodes = levels[depth];
            let totalWidth = nodes.length * (pentagonWidth + pentagonSpacing);
            let startX = -(width-totalWidth)+(width/40); // Center them
            nodes.forEach((node) => {
                let xPos = startX + node.depth * (pentagonWidth + pentagonSpacing);
                let yPos = YPos; // Space out rows
                
                // Draw pentagon
                svg.append("polygon")
                    .attr("class", "pentagon")
                    .attr("points", "0,0 "+(pentagonWidth-arrowLength)+",0 "+pentagonWidth+","+pentagonHeight/2+" "+(pentagonWidth-arrowLength)+","+pentagonHeight+" 0,"+pentagonHeight+" "+arrowLength+","+pentagonHeight/2)
                    .attr("fill", getcolor(node))
                    .attr("transform", `translate(${xPos}, ${yPos})`)
                    .transition()
                    .duration(200)
                    .attr("opacity", 1);

                svg.append("text")
                .attr("class", "pentagon-label")
                .attr("x", xPos + pentagonWidth / 2)
                .attr("y", yPos + pentagonHeight / 2)
                .attr("text-anchor", "middle")
                .attr("alignment-baseline", "middle")
                .style("font-size", "0.7vw")  // Adjust as needed
                .style("fill", "black")
                .style("font-weight", "bold")
                .text(node.data.name);
            });
        });

        updateLineChart(d);
    }

    function resetHighlight(paths) {
        paths.transition()
            .duration(100)
            .style("opacity", 1);

        svg.selectAll(".pentagon")
        .transition()
        .duration(200)
        .attr("opacity", 0)
        .remove();
    }

    onMount(() => {
        if (typeof window !== "undefined") { // Ensure we are in the browser
            updateChart();
            window.addEventListener("resize", updateChart);
        }
    });

    onDestroy(() => {
        if (typeof window !== "undefined") {
            window.removeEventListener("resize", updateChart);
        }
    });
</script>

<div bind:this={container} style="width: 100%; height: 85vh;"></div>

