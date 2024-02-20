# Lexiconia

See the interactive map at https://jjdhunt.github.io/lexiconia

## Overview

A world built of words.

18,635 words, 41,207 definitions, for an average of 2.2 defintions per word.

## How the map of Lexiconia was built

To generate data for words (in lexiconia_generation.ipynb):
1. Use GPT to get definitions of the most common 20k words.
2. Use the text-embedding-3-small model to get sematic embeddings of (word, definition) pairs.
3. Use UMAP to project the embeddings to a 2D space.
4. Use DBSCAN to cluster the points to form 'Lands'.
5. Use k-means to cluster the remaining points into 'Seas'.
6. Use GPT to determine topics of each cluster.
7. Use GPT to come up with a creative fantasy-world name for each cluster based on its topic.
8. Use GPT to score each cluster on scales of emotional valence, physicality, and humanity.
9. Filter out NSFW words.

To create the map from the data generated above (in lexiconia_plotting.ipynb):
1. Map each (emotional valence, physicality, humanity) score to a color. This will be the color of the Land cluster. Sea cluster points will all just be white on a blue background.
2. Find the alpha-shape that encompasses the UMAP-space words points in each Land cluster.
3. Scatterplot all the UMAP word points with annotations.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/jjdhunt/lexiconia.git

2. Install the requirements
   ```sh
   pip install -r requirements.txt

3. Set up OpenAI API key

   Create a file named .env at the root level of the repo. Add the following line to it with your API key. Get your API key at https://platform.openai.com/api-keys.
   
   ```sh
   OPENAI_API_KEY=<YOUR API KEY>
