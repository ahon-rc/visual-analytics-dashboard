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
    let world_data = await get_data(fetch, "world_population.csv");

    // const response = await fetch(base + "/world_population.csv", { 'header': { 'Content-Type': 'text/csv' } });
    // let text_data = await response.text();
    // let parsed_data = Papa.parse(text_data, { 'header': true });

    let team_data = await get_data(fetch, "/teams_data.csv");
    let player_data = await get_data(fetch, "/players_data.csv");
    let stat_data = await get_data(fetch, "/key_stats_data.csv");
    let goal_data = await get_data(fetch, "/goals_data.csv");
    let keeper_data = await get_data(fetch, "/goalkeeping_data.csv");
    let dist_data = await get_data(fetch, "/distribution_data.csv");
    let cards_data = await get_data(fetch, "/disciplinary_data.csv");
    let defend_data = await get_data(fetch, "/defending_data.csv");
    let attempt_data = await get_data(fetch, "/attempts_data.csv");
    let attack_data = await get_data(fetch, "/attacking_data.csv");
    let responseJSON = await fetch(base + '/countries-110m.json');
    let world_topo = await responseJSON.json();

    let dataset = [];
    const response = await fetch("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson");
    dataset = await response.json();

    let data = await get_data(fetch, "/DHIT.csv");
    
    let player_map = {};
    let team_map = {};
    for (let i = 0; i < team_data.length; i++)
        team_map[team_data[i]['team_id']] = team_data[i]['team'];
    for (let i = 0; i < player_data.length; i++)
        player_map[player_data[i]['id_player']] = [player_data[i]['player_name'], team_map[player_data[i]['id_team']]];

    let top_scorer = goal_data.slice(0, 5);
    for (let idx_score = 0; idx_score < top_scorer.length; idx_score++)
    {
        top_scorer[idx_score]['name'] = player_map[top_scorer[idx_score]['id_player']][0];
        top_scorer[idx_score]['team'] = player_map[top_scorer[idx_score]['id_player']][1];
        for (let idx = 0; idx < player_data.length; idx++)
        {
            if (attempt_data[idx]['id_player'] === top_scorer[idx_score]['id_player']) {
                top_scorer[idx_score]['attempts'] = attempt_data[idx]['total_attempts'];
                top_scorer[idx_score]['on_target'] = attempt_data[idx]['attempts_on_target'];
            }
        }
    }

    return {
        team: team_data,
        player: player_data,
        stats: stat_data,
        goals: goal_data,
        keeper:keeper_data,
        dist:dist_data,
        cards:cards_data,
        defend:defend_data,
        attempt:attempt_data,
        attack: attack_data,
        team_mapping: team_map,
        player_mapping: player_map,
        top_scorers: top_scorer,
        mhd: data,
        world_topo: world_topo,
        idk: dataset,
    }
}