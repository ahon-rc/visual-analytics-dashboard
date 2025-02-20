import Papa from 'papaparse';
import { base } from '$app/paths';
import { json } from "d3-fetch";
import * as topojson from 'topojson-client';

async function get_data(fetch, path) {
    let response = await fetch(base + path, { 'header': { 'Content-Type': 'text/csv' } });
    let text_data = await response.text();
    let parsed_data = Papa.parse(text_data, { 'header': true });
    return parsed_data.data;
}

export async function load({ fetch }) {
    let responseJSON = await fetch(base + '/countries-110m.json');
    let world_topo = await responseJSON.json();

    responseJSON = await fetch(base + '/map_data.json');
    let world_data = await responseJSON.json();

    let dataset = [];
    const response = await fetch("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson");
    dataset = await response.json();

    let data = await get_data(fetch, "/DHIT.csv");
    let surv_14 = await get_data(fetch, "/survey_14.csv");
    let surv_19 = await get_data(fetch, "/surv_19.csv");
    
    let dic = {
        "name": "root",
        "children": [
            {
                "name": "Family History",
                "count": 0,
                "children": [
                    {
                        "name": "Male",
                        "count": 0,
                        "children": [
                            { "name": "Yes", "value": 0 },
                            { "name": "No", "value": 0 },
                            { "name": "Maybe", "value": 0 }
                        ]
                    },
                    {
                        "name": "Female",
                        "count": 0,
                        "children": [
                            { "name": "Yes", "value": 0 },
                            { "name": "No", "value": 0 },
                            { "name": "Maybe", "value": 0 }
                        ]
                    },
                    {
                        "name": "LGBTQ+",
                        "count": 0,
                        "children": [
                            { "name": "Yes", "value": 0 },
                            { "name": "No", "value": 0 },
                            { "name": "Maybe", "value": 0 }
                        ]
                    }
                ]
            },
            {
                "name": "No Family History",
                "count": 0,
                "children": [
                    {
                        "name": "Male",
                        "count": 0,
                        "children": [
                            { "name": "Yes", "value": 0 },
                            { "name": "No", "value": 0 },
                            { "name": "Maybe", "value": 0 }
                        ]
                    },
                    {
                        "name": "Female",
                        "count": 0,
                        "children": [
                            { "name": "Yes", "value": 0 },
                            { "name": "No", "value": 0 },
                            { "name": "Maybe", "value": 0 }
                        ]
                    },
                    {
                        "name": "LGBTQ+",
                        "count": 0,
                        "children": [
                            { "name": "Yes", "value": 0 },
                            { "name": "No", "value": 0 },
                            { "name": "Maybe", "value": 0 }
                        ]
                    }
                ]
            }
        ],
        "total": 0,
    };

    let dic_16 = JSON.parse(JSON.stringify(dic));
    let dic_14 = JSON.parse(JSON.stringify(dic))
    let dic_19 = JSON.parse(JSON.stringify(dic));
    let order_1 = { "Family History": 0, "No Family History": 1 };
    let order_2 = { "Male": 0, "Female": 1, "LGBTQ+": 2 };
    let value_order = { "Yes": 0, "No": 1, "Maybe": 2 };

    let add = (dictionary, hist, sex, val, check) => {
        dictionary['children'][order_1[hist]]['children'][order_2[sex]]['children'][value_order[val]]['value'] += 1;
        dictionary['children'][order_1[hist]]['children'][order_2[sex]]['count'] += 1;
        dictionary['children'][order_1[hist]]['count'] += 1;

        return dictionary;
    }
    for (let idx = 0; idx < Math.max(data.length, surv_14.length, surv_19.length); idx++)
    {
        let hist = '';
        let sex = '';
        let value = '';
        if (idx < data.length && data[idx]['mh_family_hist'] != undefined && data[idx]['mh_family_hist'] != "I don't know" && data[idx]['sex'] != undefined && data[idx]['mh_discussion_cowork'] != undefined)
        {
            hist = data[idx]['mh_family_hist'] == 'Yes' ? "Family History" : "No Family History";
            sex = data[idx]['sex'] == "Male" || data[idx]['sex'] == "Female" ? data[idx]['sex'] : "LGBTQ+";
            value = data[idx]['mh_discussion_cowork'];
            // dic_16['children'][order_1[hist]]['children'][order_2[sex]]['children'][value_order[value]]['value'] += 1;
            dic_16 = add(dic_16, hist, sex, value);
            dic_16["total"] += 1;

            dic = add(dic, hist, sex, value);
            dic['total'] += 1;
        }

        if (idx < surv_14.length && surv_14[idx]['family_history'] != undefined && surv_14[idx]['family_history'] != "I don't know" && surv_14[idx]['sex'] != undefined && surv_14[idx]['peer_discussion'] != undefined)
        {
            hist = surv_14[idx]['family_history'] == 'Yes' ? "Family History" : "No Family History";
            sex = surv_14[idx]['sex'] == "Male" || surv_14[idx]['sex'] == "Female" ? surv_14[idx]['sex'] : "LGBTQ+";
            value = (surv_14[idx]['peer_discussion'] != "Yes" && surv_14[idx]['peer_discussion'] != "No") ? "Maybe" : surv_14[idx]['peer_discussion'];

            dic_14 = add(dic_14, hist, sex, value, true);
            dic_14["total"] += 1;

            dic = add(dic, hist, sex, value);
            dic['total'] += 1;
        }

        if (idx < surv_19.length && surv_19[idx]['family_history'] != undefined && surv_19[idx]['family_history'] != "I don't know" && surv_19[idx]['sex'] != undefined && surv_19[idx]['peer_discussion'] != undefined)
        {
            hist = surv_19[idx]['family_history'] == 'Yes' ? "Family History" : "No Family History";
            sex = surv_19[idx]['sex'] == "Male" || surv_19[idx]['sex'] == "Female" ? surv_19[idx]['sex'] : "LGBTQ+";
            value = (surv_19[idx]['peer_discussion'] != "Yes" && surv_19[idx]['peer_discussion'] != "No") ? "Maybe" : surv_19[idx]['peer_discussion'];
            dic_19 = add(dic_19, hist, sex, value);
            dic_19["total"] += 1;

            dic = add(dic, hist, sex, value);
            dic['total'] += 1;
        }
    }

    const col = ["#2f5061", "#4297a0", "#9bc1c3", "#c8d6d5", "#f4eae6", "#f4c9c9", "#f4a8ac", "#e57f84"];
    let x = await fetch(base + '/disease_16.json');
    let disease_16 = await x.json();
    x = await fetch(base + '/disease_19.json');
    let disease_19 = await x.json();

    let diseases = [];
    for (let i = 0; i < Object.keys(disease_19).length; i++)
    {
        let k = Object.keys(disease_19)[i];
        diseases.push({
            title: k,
            color: col[i],
            values: [
                { year: 2019, value: disease_19[k] },
                { year: 2018, value: disease_16[k] },
            ]
        });
    }

    x = await fetch(base + '/pi_data.json');
    let pi_data = await x.json();


    return {
        mhd: data,
        world: world_data['data'],
        world_topo: world_topo,
        idk: dataset,
        tree: dic,
        tree_14: dic_14,
        tree_16: dic_16,
        tree_19: dic_19,
        diss: diseases,
        d_16: disease_16,
        d_19: disease_19,
        pi: pi_data,
    }
}