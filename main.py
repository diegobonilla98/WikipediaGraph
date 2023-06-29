import requests
from bs4 import BeautifulSoup
from functools import partial
import networkx as nx
import matplotlib.pyplot as plt
import concurrent.futures
from tqdm import tqdm


def filter_func(link, url):
    if 'Main_Page' in link or 'Wikipedia:' in link or 'Portal:' in link or 'Special:' in link or 'Help:' in link or url.split("/")[-1] in link or "File:" in link or "%" in link or "Category:" in link or "#" in link or "_" in link or "-" in link or len(link) < 11 or "Template:" in link or "Talk:" in link:
        return False
    return True


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def get_list_from_single(url):
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred while getting {url}: {http_err}')
        return []
    except Exception as err:
        print(f'An error occurred while getting {url}: {err}')
        return []
    print("Processing", url)
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all('a')
    wiki_links = [tag.get('href') for tag in a_tags if tag.get('href') and tag.get('href').startswith('/wiki/')]
    filter_func_custom = partial(filter_func, url=url)
    wiki_links = list(map(lambda l: "https://en.wikipedia.org" + l, filter(filter_func_custom, wiki_links)))
    wiki_links = remove_duplicates(wiki_links)[:10]

    return wiki_links


def recursive_processing(data, depth, G, parent=None, executor=None, pbar=None):
    if depth <= 0:
        return

    new_data_points = list(executor.map(get_list_from_single, [data]))

    # Flatten the list of lists
    new_data_points = [item for sublist in new_data_points for item in sublist]

    if pbar is None:
        pbar = tqdm(total=depth)

    for i, new_data in enumerate(new_data_points):
        node_id = new_data.replace("https://en.wikipedia.org/wiki/", "")

        if not G.has_node(node_id):
            # If node does not exist, add it to the graph
            G.add_node(node_id, data=new_data)

        # Regardless of whether a new node was created, add an edge from the parent
        if parent is not None:
            G.add_edge(parent, node_id)

        # Only continue processing if the node has not been visited before.
        if not G.nodes[node_id].get('visited'):
            G.nodes[node_id]['visited'] = True
            recursive_processing(new_data, depth - 1, G, parent=node_id, executor=executor, pbar=pbar)

    pbar.update(1)

    if depth == 1:
        pbar.close()


# Creating a new directed graph
G = nx.DiGraph()

# Create ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Start the recursive processing with the executor
    recursive_processing('https://en.wikipedia.org/wiki/Philosophy', 5, G, executor=executor)

# Draw the graph
nx.write_gexf(G, "graph.gexf")
nx.draw(G, with_labels=True)
plt.show()
