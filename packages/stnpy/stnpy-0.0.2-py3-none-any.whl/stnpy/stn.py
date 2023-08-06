from statistics import mean
import numpy as np
import pandas as pd
import igraph as ig
import math

def get_data(filename, delimiter, run_number=None):
    try:
        df = pd.read_csv(filename, delimiter=delimiter)
        if run_number is not None:
            return df[df["Run"] == run_number]
        return df
    except:
        raise Exception(f"Input file '{filename}' could not be read with delimiter '{delimiter}'.")

def map_positions(positions):
    position_ids = {}
    next_id = 0
    for position in positions:
        try:
            position_ids[position]
        except:
            position_ids[position] = next_id
            next_id += 1
    return  position_ids

def stn_create(filename, delimiter=",", best_fit=None, run_number=None):
    df = get_data(filename, delimiter, run_number=run_number)
    nodes_and_values = pd.DataFrame(np.concatenate([df[['Solution1', 'Fitness1']].values, df[['Solution2', 'Fitness2']].values]),
                                 columns=['position', 'fitness'])

    mapped_position_ids = map_positions(nodes_and_values['position'].to_list())
    df['Solution1'] = df['Solution1'].map(lambda x: mapped_position_ids[x])
    df['Solution2'] = df['Solution2'].map(lambda x: mapped_position_ids[x])

    if not best_fit:
        best_fit = min(nodes_and_values['fitness'])

    nodes_and_values = pd.DataFrame(
        np.concatenate([df[['Solution1', 'Fitness1']].values, df[['Solution2', 'Fitness2']].values]),
        columns=['position', 'fitness'])
    best_ids = nodes_and_values.query("fitness == @best_fit")['position']

    g = ig.Graph.DataFrame(df[['Solution1', 'Solution2']], directed=True)
    g.simplify()

    for vertex in g.vs:
        vertex["type"] = "medium"
        if vertex.degree(mode="out") == 0:
            vertex["type"] = "end"
        if vertex.degree(mode="in") == 0:
            vertex["type"] = "start"
        if vertex.index in best_ids:
            vertex["type"] = "best"

    g["best"] = best_fit
    return g

def generate_metrics(stn_graph, nruns=1.0):
    nodes = len(stn_graph.vs)
    edges = len(stn_graph.es)
    best_vertexes = [vertex for vertex in stn_graph.vs if vertex["type"] == "best"]
    nbest = len(best_vertexes)
    end_vertexes = [vertex for vertex in stn_graph.vs if vertex["type"] == "end"]
    nend = len(end_vertexes)
    components = len(stn_graph.components(mode="weak"))

    start_vertexes = [vertex for vertex in stn_graph.vs if vertex["type"] == "start"]

    if len(best_vertexes) > 0:
        best_strength = max([vertex.degree(mode="in") for vertex in best_vertexes]) / nruns
        distances = stn_graph.distances(source=start_vertexes, target=best_vertexes, mode='out')
        d = [d[0] for d in distances if math.isfinite(d[0])]
        npaths = len(d)
        plength = -1
        if npaths > 0:
            plength = mean(d)
    else:
        best_strength = 0
        plength = -1
        npaths = 0
    return nodes, edges, nbest, nend, components, best_strength, plength, npaths

def run_file(filename, delimiter=",", best_fit=None ,run_number=None):
    stn = stn_create(filename, delimiter=delimiter, best_fit=best_fit, run_number=run_number)
    return generate_metrics(stn)

